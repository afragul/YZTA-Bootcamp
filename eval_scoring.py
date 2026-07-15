import os
import sys
import json

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend"))

from services.cv_service import CVAnalysisService

# Her ornek CV'nin dosya adindan beklenen en yuksek rolu biliyoruz.
BEKLENEN = {
    "cv_backend.txt": "backend_developer",
    "cv_frontend.txt": "frontend_developer",
    "cv_devops.txt": "devops_engineer",
    "cv_ml_engineer.txt": "machine_learning_engineer",
    "cv_data_scientist.txt": "data_scientist",
}


def main():
    service = CVAnalysisService()
    satirlar = []

    for dosya, beklenen_rol in BEKLENEN.items():
        yol = os.path.join("sample_cvs", dosya)
        with open(yol, "r", encoding="utf-8") as f:
            cv_text = f.read()

        print(f"Analiz ediliyor: {dosya} ...")
        sonuc = service.analyze_cv(cv_text)
        skorlar = sonuc["role_scores"]

        # En yuksek skorlu rol hangisi?
        gercek_rol = max(skorlar, key=skorlar.get)
        gecti = gercek_rol == beklenen_rol

        satirlar.append(
            {
                "dosya": dosya,
                "beklenen": beklenen_rol,
                "gercek": gercek_rol,
                "skor": skorlar[gercek_rol],
                "beklenenin_skoru": skorlar[beklenen_rol],
                "sonuc": "GECTI" if gecti else "KALDI",
            }
        )

    # Tabloyu bas
    print("\n" + "=" * 100)
    print(f"{'DOSYA':<24}{'BEKLENEN':<28}{'GERCEK (en yuksek)':<28}{'SKOR':<8}{'SONUC'}")
    print("-" * 100)
    for s in satirlar:
        print(
            f"{s['dosya']:<24}{s['beklenen']:<28}{s['gercek']:<28}"
            f"{s['skor']:<8}{s['sonuc']}"
        )
    print("-" * 100)

    basari = sum(1 for s in satirlar if s["sonuc"] == "GECTI")
    oran = basari / len(satirlar) * 100
    print(f"BASARI ORANI: {basari}/{len(satirlar)}  (%{oran:.0f})")
    print("=" * 100)

    # Sunumda kullanmak icin diske yaz
    with open("eval_results.json", "w", encoding="utf-8") as f:
        json.dump(
            {"basari_orani": oran, "detay": satirlar}, f, indent=2, ensure_ascii=False
        )
    print("\nDetayli sonuc: eval_results.json")


if __name__ == "__main__":
    main()