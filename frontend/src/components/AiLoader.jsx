import { useEffect, useState } from "react";

// AI beklemeleri için aşamalı yükleme göstergesi.
//
// Neden aşamalı? Gemini çağrıları 10-25 saniye sürüyor. Tek bir "Yükleniyor…"
// yazısı bu sürede uygulamanın donduğu izlenimi veriyor. Aşamalar, backend'in
// GERÇEKTEN yaptığı adımlar (bkz. upload_service.process_cv_upload) olduğu için
// kullanıcı beklerken ne olduğunu görüyor.
//
// DİKKAT — dürüstlük notu: Backend tek bir HTTP cevabı döndürdüğü için gerçek
// ilerleme bilinmiyor. Aşama SIRASI gerçek, aşama SÜRELERİ ise ölçülmüş
// tahminlerdir. Bu yüzden bilerek yüzde gösterilmiyor; yalnızca geçen süre
// (gerçek) ve o an çalıştığı tahmin edilen adım gösteriliyor. Son aşamada
// beklenir, cevap gelince bileşen zaten kaldırılır.

// Süreler saniye cinsinden — sample_cvs ile yapılan koşulardan ölçüldü.
export const CV_ASAMALARI = [
  { etiket: "Dosya doğrulanıyor", saniye: 1 },
  { etiket: "CV metni çıkarılıyor", saniye: 2 },
  { etiket: "Yapay zeka CV'ni analiz ediyor", saniye: 12 },
  { etiket: "İş ilanları eşleştiriliyor", saniye: 5 },
  { etiket: "Sonuçlar hazırlanıyor", saniye: 3 },
];

export const PLAN_ASAMALARI = [
  { etiket: "Eksiklerin inceleniyor", saniye: 2 },
  { etiket: "Uygun kaynaklar seçiliyor", saniye: 5 },
  { etiket: "Haftalık plan kuruluyor", saniye: 8 },
];

// Bu süreden sonra "beklenenden uzun sürüyor" notu gösterilir.
const UZUN_SURUYOR_ESIGI = 30;

export default function AiLoader({ baslik, asamalar = CV_ASAMALARI }) {
  const [aktifIndex, setAktifIndex] = useState(0);
  const [gecenSaniye, setGecenSaniye] = useState(0);

  // Geçen süre sayacı — bu değer GERÇEK, tahmin değil.
  useEffect(() => {
    const sayac = setInterval(() => setGecenSaniye((s) => s + 1), 1000);
    return () => clearInterval(sayac);
  }, []);

  // Aşama ilerletme. Son aşamaya gelince durur: cevabın ne zaman geleceğini
  // bilmediğimiz için "bitti" göstermek yanıltıcı olurdu.
  useEffect(() => {
    if (aktifIndex >= asamalar.length - 1) return;
    const zamanlayici = setTimeout(
      () => setAktifIndex((i) => i + 1),
      asamalar[aktifIndex].saniye * 1000
    );
    return () => clearTimeout(zamanlayici);
  }, [aktifIndex, asamalar]);

  const uzunSuruyor = gecenSaniye >= UZUN_SURUYOR_ESIGI;

  return (
    <div
      role="status"
      aria-live="polite"
      className="flex flex-col items-center gap-5 rounded-xl bg-primary-50 px-4 py-8 sm:flex-row sm:items-start sm:gap-8 sm:px-8"
    >
      <TaramaGorseli />

      <div className="w-full min-w-0">
        <p className="mb-1 text-center text-sm font-semibold text-primary-800 sm:text-left">
          {baslik}
        </p>
        <p className="mb-5 text-center text-xs text-muted sm:text-left">
          {gecenSaniye} saniye geçti
          {uzunSuruyor && " · beklenenden uzun sürüyor, hâlâ çalışıyor"}
        </p>

        {/* Aşama listesi — Öğrenme Yolu zaman çizelgesiyle aynı görsel dil */}
        <ol className="relative space-y-3 pl-8">
          {/* Dikey çizgi: merkezi 12px, dairelerle hizalı */}
          <div className="absolute bottom-2 left-[11px] top-2 w-0.5 bg-primary-200" />

          {asamalar.map((asama, i) => {
            const tamamlandi = i < aktifIndex;
            const aktif = i === aktifIndex;

            return (
              <li key={asama.etiket} className="relative">
                {/* Daire düğüm — left-[-32px] üst kapsayıcının pl-8'ini geri alır,
                    böylece 24px'lik dairenin merkezi çizgiyle çakışır. */}
                <span
                  aria-hidden
                  className={
                    "absolute left-[-32px] top-0 flex h-6 w-6 items-center justify-center rounded-full border-2 " +
                    (tamamlandi
                      ? "border-primary-800 bg-primary-800"
                      : aktif
                        ? "animate-nabiz-yumusak border-primary-500 bg-white"
                        : "border-primary-200 bg-white")
                  }
                >
                  {tamamlandi && (
                    <svg viewBox="0 0 20 20" className="h-3 w-3 fill-white">
                      <path d="M7.6 13.4 4.2 10l-1.2 1.2 4.6 4.6 9-9-1.2-1.2z" />
                    </svg>
                  )}
                </span>

                <span
                  className={
                    "block text-sm leading-6 " +
                    (aktif
                      ? "font-semibold text-primary-800"
                      : tamamlandi
                        ? "text-muted"
                        : "text-primary-200")
                  }
                >
                  {asama.etiket}
                </span>
              </li>
            );
          })}
        </ol>
      </div>
    </div>
  );
}

// CV belgesi + üzerinde süzülen tarama ışını.
// Metafor: "yapay zeka CV'ni okuyor". Salt dekoratif → aria-hidden.
function TaramaGorseli() {
  return (
    <svg
      viewBox="0 0 120 120"
      aria-hidden
      className="h-28 w-28 shrink-0"
    >
      <defs>
        {/* Işın yalnızca belgenin içinde görünsün */}
        <clipPath id="ai-loader-belge">
          <rect x="34" y="22" width="52" height="76" rx="6" />
        </clipPath>
        {/* Işının yumuşak parlaması */}
        <linearGradient id="ai-loader-isin" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="var(--color-primary-500)" stopOpacity="0" />
          <stop offset="50%" stopColor="var(--color-primary-500)" stopOpacity="0.55" />
          <stop offset="100%" stopColor="var(--color-primary-500)" stopOpacity="0" />
        </linearGradient>
      </defs>

      {/* Arka plandaki nefes alan halkalar */}
      <circle
        cx="60"
        cy="60"
        r="52"
        className="animate-nabiz-yumusak fill-none stroke-primary-200"
        strokeWidth="1.5"
      />
      <circle
        cx="60"
        cy="60"
        r="44"
        className="animate-nabiz-yumusak fill-none stroke-primary-200"
        strokeWidth="1.5"
        style={{ animationDelay: "0.6s" }}
      />

      {/* Belge gövdesi */}
      <rect
        x="34"
        y="22"
        width="52"
        height="76"
        rx="6"
        className="fill-white stroke-primary-500"
        strokeWidth="2"
      />

      {/* Metin satırları */}
      <g className="fill-primary-200">
        <rect x="43" y="34" width="26" height="4" rx="2" />
        <rect x="43" y="45" width="34" height="3" rx="1.5" />
        <rect x="43" y="53" width="30" height="3" rx="1.5" />
        <rect x="43" y="66" width="34" height="3" rx="1.5" />
        <rect x="43" y="74" width="22" height="3" rx="1.5" />
        <rect x="43" y="85" width="30" height="3" rx="1.5" />
      </g>

      {/* Tarama ışını */}
      <g clipPath="url(#ai-loader-belge)">
        <rect
          x="34"
          y="22"
          width="52"
          height="16"
          fill="url(#ai-loader-isin)"
          className="animate-tarama"
        />
        <rect
          x="34"
          y="36"
          width="52"
          height="1.5"
          className="animate-tarama fill-primary-500"
        />
      </g>
    </svg>
  );
}
