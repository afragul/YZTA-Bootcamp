import Card from "./ui/Card";

// Kişi 3 — Rol skorları grafiği.
// role_rankings dizisinden en yüksek 8 rolü yatay bar olarak gösterir,
// altında top_role_reasons'tan (en yüksek 3 rol) "bu skor neden verildi"
// gerekçelerini listeler.
// Props:
//   analysis  → top_role_reasons içindir (CVAnalysisOutput)
//   rankings  → role_rankings (rol skora göre sıralı, display alanı Türkçe)

const KAC_BAR = 8; // Görev 1: en yüksek 8 rolü göster

// Kişi 3 — skor bandına göre bar dolgu rengi (K5 skorlama cetveli).
// Koyu mavi = güçlü uyum, açık mavi = zayıf uyum. Yalnızca palet token'ları.
// Palette 4 kullanışlı mavi ton verdiği için en zayıf iki bant (0-40) tek
// açık tonda birleşir; zaten bar genişliği de zayıflığı gösterir.
function barRenkSinifi(score) {
  if (score >= 81) return "bg-primary-950"; // 81-100 · Güçlü aday
  if (score >= 61) return "bg-primary-800"; // 61-80  · Uygun
  if (score >= 41) return "bg-primary-500"; // 41-60  · Geliştirilebilir
  return "bg-primary-200"; // 0-40 · Zayıf / Alakasız
}

// snake_case teknik ad → okunabilir etiket ("data_scientist" → "Data Scientist").
// top_role_reasons'ta display gelmediği için yedek olarak kullanılır.
function rolAdiGuzellestir(role) {
  return role
    .split("_")
    .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
    .join(" ");
}

export default function RoleScores({ analysis, rankings }) {
  // role_rankings boş/eksik gelirse çökme yok, bilgilendirici mesaj.
  if (!Array.isArray(rankings) || rankings.length === 0) {
    return (
      <Card>
        <Card.Title>Rol Uygunluğu</Card.Title>
        <p className="text-sm text-muted">
          Rol skorları hesaplanamadı.
        </p>
      </Card>
    );
  }

  const enYuksekRoller = rankings.slice(0, KAC_BAR);

  // Teknik ad → Türkçe display sözlüğü; gerekçelerde rolü etiketlemek için.
  const displaySozlugu = {};
  for (const r of rankings) {
    if (r && r.role) displaySozlugu[r.role] = r.display;
  }

  const reasons = Array.isArray(analysis?.top_role_reasons)
    ? analysis.top_role_reasons
    : [];

  return (
    <Card>
      <Card.Title>Rol Uygunluğu</Card.Title>

      {/* En yüksek 8 rol — yatay bar */}
      <ul className="mt-1 space-y-3">
        {enYuksekRoller.map((r) => {
          const score = Number(r.score) || 0;
          return (
            <li key={r.role} className="flex items-center gap-3">
              {/* Rol adı — dar ekranda taşmasın diye sabit genişlik + truncate */}
              <span
                className="w-28 shrink-0 truncate text-sm font-medium text-primary-800"
                title={r.display}
              >
                {r.display}
              </span>

              {/* Bar rayı + dolgu (dolgu genişliği dinamik → style ile) */}
              <div className="h-2.5 flex-1 overflow-hidden rounded-full bg-primary-50">
                <div
                  role="progressbar"
                  aria-valuenow={score}
                  aria-valuemin={0}
                  aria-valuemax={100}
                  aria-label={`${r.display} uygunluk skoru`}
                  className={"h-full rounded-full " + barRenkSinifi(score)}
                  style={{ width: `${score}%` }}
                />
              </div>

              {/* Skor sayısı */}
              <span className="w-9 shrink-0 text-right text-sm font-semibold text-primary-950">
                {score}
              </span>
            </li>
          );
        })}
      </ul>

      {/* En yüksek 3 rol için skor gerekçeleri (K6 — bu veri artık kullanılıyor) */}
      {reasons.length > 0 && (
        <div className="mt-6 border-t border-primary-200 pt-4">
          <h4 className="mb-3 text-sm font-semibold text-primary-800">
            Skor Gerekçeleri
          </h4>
          <ul className="space-y-3">
            {reasons.map((rr, i) => {
              const display =
                displaySozlugu[rr.role] || rolAdiGuzellestir(rr.role);
              return (
                <li key={i} className="text-sm">
                  <div className="mb-0.5 flex flex-wrap items-baseline gap-x-2">
                    <span className="font-semibold text-primary-800">
                      {display}
                    </span>
                    <span className="text-xs font-semibold text-primary-500">
                      {rr.score}/100
                    </span>
                  </div>
                  <p className="text-muted">{rr.reason}</p>
                </li>
              );
            })}
          </ul>
        </div>
      )}
    </Card>
  );
}
