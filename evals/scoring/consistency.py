"""
Skor tutarlilik olcumu (Kisi 3).

Ayni CV'yi N kez analiz eder, skorlarin ne kadar oynadigini olcer.

NEDEN KRITIK: rank_roles() en yuksek skorlu role gore "otomatik plan"
uretiyor. Skorlar oynarsa kullanicinin otomatik plani her yuklemede
degisebilir -> urun tutarsiz gorunur.

MALIYET: 5 Gemini cagrisi (gunluk kotanin ~1/4'u!)
CALISTIRMA: python -m evals.scoring.consistency
"""

import json
import os
import statistics
import sys
from pathlib import Path
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from evals._paths import SAMPLE_CVS, SCORING_RESULTS

from services.cv_service import CVAnalysisService

CV_DOSYA = "cv_ml_engineer.txt"
TEKRAR = 5


def main():
    cv_yolu = os.path.join(SAMPLE_CVS, CV_DOSYA)
    with open(cv_yolu, "r", encoding="utf-8") as f:
        cv_text = f.read()

    service = CVAnalysisService()
    kosular = []

    for i in range(1, TEKRAR + 1):
        print(f"Analiz {i}/{TEKRAR} ...")

        # 503/429 gecici hatalarina karsi kendi retry'imiz
        # (cv_service.py'de retry YOK - Kisi 2'nin dosyasi, ona haber verildi)
        for deneme in range(3):
            try:
                kosular.append(service.analyze_cv(cv_text)["role_scores"])
                break
            except Exception as e:
                if deneme == 2:
                    print(f"  3 deneme sonrasi basarisiz: {e}")
                    raise
                bekle = 10 * (2 ** deneme)  # 10sn, 20sn
                print(f"  Hata ({type(e).__name__}), {bekle} sn bekleniyor... "
                      f"(deneme {deneme + 1}/3)")
                time.sleep(bekle)

        time.sleep(3)  # kosular arasi nefes (RPM korumasi)

    roller = list(kosular[0].keys())

    # EN ONEMLI METRIK: en yuksek rol her kosuda ayni mi?
    # (Bu rol dashboard'da OTOMATIK plan uretilecek olan rol!)
    top_roller = [max(k, key=k.get) for k in kosular]
    top_sabit = len(set(top_roller)) == 1

    satirlar = []
    for rol in roller:
        skorlar = [k[rol] for k in kosular]
        satirlar.append(
            {
                "rol": rol,
                "skorlar": skorlar,
                "aralik": max(skorlar) - min(skorlar),
                "ortalama": round(statistics.mean(skorlar), 1),
                "std_sapma": round(statistics.pstdev(skorlar), 2),
            }
        )
    satirlar.sort(key=lambda s: s["aralik"], reverse=True)

    print("\n" + "=" * 86)
    print(f"TUTARLILIK RAPORU  |  {CV_DOSYA}  |  {TEKRAR} kosu")
    print("=" * 86)
    print(f"{'ROL':<32}{'SKORLAR':<24}{'ARALIK':<9}{'ORT':<8}{'STD'}")
    print("-" * 86)
    for s in satirlar[:10]:
        print(
            f"{s['rol']:<32}{str(s['skorlar']):<24}"
            f"{s['aralik']:<9}{s['ortalama']:<8}{s['std_sapma']}"
        )
    print("-" * 86)

    ort_aralik = statistics.mean(s["aralik"] for s in satirlar)
    max_aralik = max(s["aralik"] for s in satirlar)

    print(
        "En yuksek rol her kosuda ayni mi? : "
        + (f"EVET ({top_roller[0]})" if top_sabit else f"HAYIR! -> {top_roller}")
    )
    print(f"Ortalama oynama (22 rol)         : +/- {ort_aralik:.1f} puan")
    print(f"En kotu oynama                   : {max_aralik} puan ({satirlar[0]['rol']})")
    print("=" * 86)

    if top_sabit and ort_aralik <= 5:
        print("SONUC: TUTARLI. Otomatik plan rolu her zaman ayni cikiyor.")
    elif top_sabit:
        print("SONUC: KISMEN TUTARLI. AKSIYON: cv_service.py temperature 0.2 -> 0.1")
    else:
        print("SONUC: TUTARSIZ! En yuksek rol degisiyor -> otomatik plan rolu de degisir.")
        print("AKSIYON: temperature 0.1 + prompt'a 'puanlari tekrarlanabilir ver' kurali")

    cikti_yolu = os.path.join(SCORING_RESULTS, "consistency.json")
    with open(cikti_yolu, "w", encoding="utf-8") as f:
        json.dump(
            {
                "cv": CV_DOSYA,
                "kosu_sayisi": TEKRAR,
                "en_yuksek_rol_sabit": top_sabit,
                "en_yuksek_roller": top_roller,
                "ortalama_oynama": round(ort_aralik, 2),
                "max_oynama": max_aralik,
                "detay": satirlar,
            },
            f,
            indent=2,
            ensure_ascii=False,
        )
    print(f"\nDetayli rapor: {cikti_yolu}")


if __name__ == "__main__":
    main()