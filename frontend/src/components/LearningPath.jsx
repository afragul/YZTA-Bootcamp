import { useState, useRef, useEffect } from "react";
import Card from "./ui/Card";
import Button from "./ui/Button";
import { getLearningPlan } from "../lib/api";

// Kişi 3 — Rol seçici + öğrenme yolu zaman çizelgesi.
// 3a: role_rankings'ten butonlar, ilk 8 + "Tüm roller (22)" toggle
// 3b: auto: true olan rol otomatik yüklensin (useRef ile tek sefer),
//     diğer roller "Plan oluştur" butonu ile, cache'de tutulanlar tekrar yüklenmesin
// 3c: Zaman çizelgesi — summary, haftalar, adımlar (proje tipi vurgulu)
//
// Props:
//   cvId: CV veritabanı kimliği (API çağrısında)
//   analysis: CVAnalysisOutput (şu an kullanılmıyor; gelecekte boşluk filtrelemesi için ayrılmış)
//   rankings: role_rankings (rol seçici listesi)

// ============================================================================
// K5 — Skor bandı → renk token (RoleScores.jsx'teki barRenkSinifi ile aynı)
// ============================================================================
// Zemin ve metin rengi birlikte döner; aksi hâlde koyu zeminde koyu yazı
// okunmaz hâle gelir (Kişi 4'ün JobMatches'teki scoreTone kalıbı).
function rolRengi(score) {
  if (score >= 81) return "bg-primary-950 text-primary-50";
  if (score >= 61) return "bg-primary-800 text-primary-50";
  if (score >= 41) return "bg-primary-500 text-white";
  return "bg-primary-200 text-primary-950";
}

// resource_type → görünen etiket (ayrı bölümde "resource_type değerleri" listesi var)
function resourceTypeEtiket(type) {
  const etiketi = {
    kurs: "Kurs",
    dokumantasyon: "Dokümantasyon",
    video: "Video",
    kitap: "Kitap",
    proje: "Proje",
  };
  return etiketi[type] || type;
}

export default function LearningPath({ cvId, analysis, rankings }) {
  // ========================================================================
  // STATE
  // ========================================================================
  const [showAllRoles, setShowAllRoles] = useState(false); // ilk 8 mi 22 mi
  const [selectedRole, setSelectedRole] = useState(null); // hangisini seçli
  const [loadedPlans, setLoadedPlans] = useState({}); // { [role]: { plan, cached } }
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // K2 — auto: true olan rolü yalnızca bir kez tetikle
  const hasAutoLoaded = useRef(false);

  // ========================================================================
  // GÜVENLIK CHECK
  // ========================================================================
  if (!cvId) {
    return (
      <Card>
        <Card.Title>Öğrenme Yolu</Card.Title>
        <p className="text-sm text-muted">CV kimliği eksik.</p>
      </Card>
    );
  }

  if (!Array.isArray(rankings) || rankings.length === 0) {
    return (
      <Card>
        <Card.Title>Öğrenme Yolu</Card.Title>
        <p className="text-sm text-muted">Rol sıralaması yüklenmedi.</p>
      </Card>
    );
  }

  // ========================================================================
  // 3B — PLAN YÜKLEME FONKSIYONU (useEffect'ten ÖNCE tanımla)
  // ========================================================================
  async function handleLoadPlan(role) {
    // Zaten cache'de varsa, tekrar yükleme yok (K3)
    if (loadedPlans[role]) {
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await getLearningPlan(cvId, role);
      // response: { cv_id, target_role, cached, plan }
      setLoadedPlans((prev) => ({
        ...prev,
        [role]: {
          plan: response.plan,
          cached: response.cached || false,
        },
      }));
    } catch (err) {
      setError(err.message || "Plan yükleme başarısız.");
    } finally {
      setLoading(false);
    }
  }

  function handleRetry() {
    if (selectedRole) {
      handleLoadPlan(selectedRole);
    }
  }

  // ========================================================================
  // 3B — AUTO YÜKLEME (rank 1, useRef ile tek sefer, K2 uyum)
  // ========================================================================
  useEffect(() => {
    // Mount'ta auto: true olan rolü bul ve otomatik yükle
    const autoRole = rankings.find((r) => r.auto === true);

    if (autoRole && !hasAutoLoaded.current && !loadedPlans[autoRole.role]) {
      // Henüz yüklenmemişse → tetikle
      hasAutoLoaded.current = true;
      setSelectedRole(autoRole.role);
      handleLoadPlan(autoRole.role);
    }
  }, []); // mount'ta bir kez

  // ========================================================================
  // 3A — ROL SEÇİCİ LOGIC
  // ========================================================================
  const rollerListesi = showAllRoles ? rankings : rankings.slice(0, 8);
  const kalanRolSayisi = rankings.length - 8;

  // ========================================================================
  // RENDER
  // ========================================================================
  return (
    <Card className="mt-5">
      <Card.Title>Öğrenme Yolu</Card.Title>

      {/* ====================================================================
          3A — ROL SEÇİCİ (çip butonları)
          ==================================================================== */}
      <div className="mb-4">
        <p className="mb-3 text-sm font-medium text-primary-800">Hedef Rol</p>

        {/* Rol butonları — çip görünümü, seçili olan border'lu */}
        <div className="flex flex-wrap gap-2">
          {rollerListesi.map((r) => {
            const isSelected = selectedRole === r.role;
            return (
              <button
                key={r.role}
                type="button"
                onClick={() => {
                  setSelectedRole(r.role);
                  setError(null); // Hata temizle (yeni rol)
                }}
                disabled={loading}
                className={
                  "flex items-center gap-2 rounded-lg px-3 py-1.5 text-sm font-medium transition-colors disabled:opacity-50 " +
                  (isSelected
                    ? "border-2 border-primary-500 bg-primary-50 text-primary-800"
                    : "border border-primary-200 bg-white text-primary-800 hover:border-primary-500")
                }
                aria-pressed={isSelected}
              >
                <span>{r.display}</span>
                <span
                  className={
                    "rounded-full px-1.5 py-0.5 text-xs font-bold " +
                    rolRengi(r.score)
                  }
                >
                  {r.score}
                </span>
              </button>
            );
          })}
        </div>

        {/* "Tüm roller" toggle (K2 — 22 butonu birden göstermek boğar) */}
        {kalanRolSayisi > 0 && (
          <button
            type="button"
            onClick={() => setShowAllRoles(!showAllRoles)}
            className="mt-2 text-sm font-semibold text-primary-500 hover:text-primary-800"
          >
            {showAllRoles ? "◀ Kapat" : `▶ Tüm roller (${rankings.length})`}
          </button>
        )}
      </div>

      {/* ====================================================================
          3B — PLAN YÜKLEME (auto yok ise "Plan oluştur" butonu)
          ==================================================================== */}
      {selectedRole && !rankings.find((r) => r.role === selectedRole && r.auto)?.auto && (
        <div className="mb-4 w-full">
          <Button
            onClick={() => handleLoadPlan(selectedRole)}
            disabled={loading || !!loadedPlans[selectedRole]}
            className="w-full"
          >
            {loadedPlans[selectedRole] ? "Plan Yüklü" : "Plan Oluştur"}
          </Button>
        </div>
      )}

      {/* K1 — Bekleme durumu: 10-15 saniye uyarısı */}
      {loading && (
        <div className="mb-4 rounded-lg bg-primary-50 p-4">
          <p className="mb-1 text-sm font-medium text-primary-800">
            …planı hazırlanıyor
          </p>
          <p className="text-xs text-muted">10-15 saniye sürebilir.</p>
        </div>
      )}

      {/* Hata durumu + "Tekrar dene" butonu */}
      {error && (
        <div className="mb-4 rounded-lg bg-danger bg-opacity-10 p-4">
          <p className="mb-2 text-sm font-medium text-danger">{error}</p>
          <Button
            variant="ghost"
            onClick={handleRetry}
            className="text-xs"
          >
            Tekrar Dene
          </Button>
        </div>
      )}

      {/* ====================================================================
          3C — ZAMAN ÇİZELGESİ (plan var ise render et)
          ==================================================================== */}
      {selectedRole && loadedPlans[selectedRole] && !loading && !error && (
        <PlanTimeline
          plan={loadedPlans[selectedRole].plan}
          cached={loadedPlans[selectedRole].cached}
        />
      )}

      {/* Boş durum (plan yüklenmedi veya yok) */}
      {selectedRole && !loadedPlans[selectedRole] && !loading && !error && (
        <p className="text-sm text-muted">Plan henüz yüklenmedi.</p>
      )}
    </Card>
  );
}

// ============================================================================
// 3C — ZAMAN ÇİZELGESİ BİLEŞENİ (plan render etme)
// ============================================================================
function PlanTimeline({ plan, cached }) {
  if (!plan || !plan.weeks) {
    return <p className="text-sm text-muted">Plan yok.</p>;
  }

  // Toplam saat (tüm adımlar + estimated_hours)
  const totalHours = plan.weeks.reduce((sum, week) => {
    return (
      sum +
      week.steps.reduce((weekSum, step) => weekSum + (step.estimated_hours || 0), 0)
    );
  }, 0);

  return (
    <div className="mt-6 space-y-6 border-t border-primary-200 pt-6">
      {/* Özet */}
      <div className="space-y-2">
        <p className="text-sm text-primary-950">{plan.summary}</p>
        <div className="flex flex-wrap gap-x-4 gap-y-1 text-xs text-muted">
          <span>
            <span className="font-semibold text-primary-800">{plan.total_weeks}</span> hafta
          </span>
          <span>
            <span className="font-semibold text-primary-800">{totalHours}</span> saat
          </span>
          {cached && (
            <span className="rounded-md bg-primary-50 px-2 py-0.5 text-primary-500">
              Kayıtlı plan
            </span>
          )}
        </div>
      </div>

      {/* Haftalar — dikey çizgi + hafta düğümleri */}
      <div className="relative space-y-6 pl-12">
        {/* Dikey çizgi (absolute) */}
        <div className="absolute left-4 top-0 bottom-0 w-0.5 bg-primary-200" />

        {plan.weeks.map((week, weekIndex) => {
          const weekHours = week.steps.reduce(
            (sum, step) => sum + (step.estimated_hours || 0),
            0
          );

          return (
            <div key={weekIndex} className="space-y-3">
              {/* Hafta başlığı + düğüm */}
              <div className="relative">
                {/* Daire düğüm (absolute, çizginin üstüne) */}
                <div className="absolute left-[-42px] top-1 h-6 w-6 rounded-full border-2 border-primary-500 bg-white" />

                <div className="flex items-baseline justify-between">
                  <h4 className="font-semibold text-primary-800">
                    Hafta {week.week} · {week.focus}
                  </h4>
                  <span className="text-xs text-muted">{weekHours}s</span>
                </div>
              </div>

              {/* Adımlar */}
              <ul className="space-y-2">
                {week.steps.map((step, stepIndex) => {
                  const isProje = step.resource_type === "proje";
                  return (
                    <li
                      key={stepIndex}
                      className={
                        "rounded-lg border px-3 py-2 text-sm " +
                        (isProje
                          ? "border-primary-500 bg-primary-50"
                          : "border-primary-200 bg-white")
                      }
                    >
                      {/* Başlık: order · topic · resource_type chip */}
                      <div className="mb-1 flex flex-wrap items-center gap-2">
                        <span className="font-semibold text-primary-800">
                          {step.order}. {step.topic}
                        </span>
                        <span
                          className={
                            "rounded-md px-2 py-0.5 text-xs font-medium " +
                            (isProje
                              ? "bg-primary-500 text-white"
                              : "bg-primary-200 text-primary-800")
                          }
                        >
                          {resourceTypeEtiket(step.resource_type)}
                        </span>
                        <span className="ml-auto text-xs font-semibold text-primary-500">
                          {step.estimated_hours}s
                        </span>
                      </div>

                      {/* Gerekçe (soluk) */}
                      {step.reason && (
                        <p className="mb-2 text-xs text-muted">{step.reason}</p>
                      )}

                      {/* Kaynak önerisi */}
                      {step.resource_suggestion && (
                        <p className="break-words text-xs text-primary-800">
                          <span className="font-medium">Kaynak:</span>{" "}
                          {step.resource_suggestion}
                        </p>
                      )}
                    </li>
                  );
                })}
              </ul>
            </div>
          );
        })}
      </div>
    </div>
  );
}
