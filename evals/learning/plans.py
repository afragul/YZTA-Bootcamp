import json
import os
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from evals._paths import TEST_RESULTS, LEARNING_PLANS

from services.learning_service import LearningPathService, rank_roles

# (analiz sonucu dosyasi, hedef rol) - hedef rol TargetRole'un 22 degerinden biri
SENARYOLAR = [
    ("cv_ml_engineer_result.json", "machine_learning_engineer"),
    ("cv_backend_result.json", "devops_engineer"),
    ("cv_ml_engineer_result.json", "data_analyst"),
    ("cv_backend_result.json", "ui_ux_designer"),
]

# Cagrilar arasi bekleme (RPM limitine takilmamak icin)
BEKLEME_SN = 6

# Teknik olmayan rollerde GORULMEMESI gereken kelimeler
YAZILIM_KELIMELERI = [
    "docker", "kubernetes", "terraform", "fastapi", "django",
    "pytest", "devops", "pyspark", "ci/cd", "kafka",
]

# Bu roller teknik degil -> yazilim konusu onerilmemeli
TEKNIK_OLMAYAN_ROLLER = {
    "ui_ux_designer", "graphic_designer", "hr_specialist",
    "digital_marketing_specialist", "customer_success_specialist",
    "product_manager", "project_manager",
}

TURKCE_KARAKTERLER = set("çğıöşüÇĞİÖŞÜ")


def siralamayi_yazdir(role_scores: dict) -> None:
    """Frontend'in rol secicisinde ne gorecegini simule et (ilk 8)."""
    print("\n  FRONTEND ROL SECICI (22 rol, skora gore - ilk 8):")
    for r in rank_roles(role_scores)[:8]:
        isaret = "[OTOMATIK]" if r["auto"] else "[buton]   "
        print(f"    {isaret} #{r['rank']:<2} {r['score']:>3}  {r['display']}")
    print("    ... (kalan 14 rol de buton)")


def plani_yazdir(plan: dict, hedef_rol: str) -> dict:
    """Plani ekrana basar ve otomatik kalite kontrolu yapar. Kontrol sonucunu dondurur."""
    print(f"\n  HEDEF ROL : {plan['target_role']}")
    print(f"  SURE      : {plan['total_weeks']} hafta")
    print(f"  OZET      : {plan['summary']}\n")

    toplam_saat = 0
    proje_var = False

    for hafta in plan["weeks"]:
        hafta_saat = sum(a["estimated_hours"] for a in hafta["steps"])
        toplam_saat += hafta_saat
        print(f"  == HAFTA {hafta['week']}: {hafta['focus']}  ({hafta_saat} saat)")
        for adim in hafta["steps"]:
            if adim["resource_type"].lower() == "proje":
                proje_var = True
            print(f"     {adim['order']}. {adim['topic']}  ({adim['estimated_hours']} sa)")
            print(f"        Neden : {adim['reason']}")
            print(f"        Kaynak: [{adim['resource_type']}] {adim['resource_suggestion']}")
        print()

    # 1) Teknik olmayan role yazilim konusu onerilmis mi?
    sizinti = []
    if hedef_rol in TEKNIK_OLMAYAN_ROLLER:
        sizinti =  teknik_sizinti_bul(plan)

    # 2) Cikti duzgun Turkce mi? (hic Turkce karakter yoksa suphelidir)
    turkce_ok = bool(TURKCE_KARAKTERLER & set(json.dumps(plan, ensure_ascii=False)))

    print("  --- OTOMATIK KONTROL ---")
    print(f"  Toplam sure        : {toplam_saat} saat")
    print(f"  Proje adimi var mi : {'EVET' if proje_var else 'HAYIR -> Kural 7 calismiyor!'}")
    print(f"  Turkce karakterler : {'OK' if turkce_ok else 'YOK -> Kural 10 calismiyor! (guclu/güçlü)'}")
    if hedef_rol in TEKNIK_OLMAYAN_ROLLER:
        if sizinti:
            print(f"  TEKNIK SIZINTI     : VAR -> {sizinti}")
            print(f"                       Kural 1 calismiyor! Teknik olmayan role yazilim onerilmis.")
        else:
            print(f"  TEKNIK SIZINTI     : YOK (teknik olmayan rol icin dogru plan)")

    return {
        "proje_var": proje_var,
        "turkce_ok": turkce_ok,
        "teknik_sizinti": sizinti,
        "toplam_saat": toplam_saat,
    }

def teknik_sizinti_bul(plan: dict) -> list:
    """
    SADECE OGRETILEN icerige bakar (topic + resource_suggestion).
    'reason' ve 'summary'ye BAKMAZ - orada adayin gecmisi mesru sekilde anilir.
    Kelime siniri (\b) kullanir -> 'sql' artik 'PostgreSQL' icinde eslesmez.
    """
    parcalar = []
    for hafta in plan["weeks"]:
        for adim in hafta["steps"]:
            parcalar.append(adim["topic"])
            parcalar.append(adim["resource_suggestion"])
    metin = " ".join(parcalar).lower()
    return [k for k in YAZILIM_KELIMELERI if re.search(rf"\b{re.escape(k)}\b", metin)]


def main():
    service = LearningPathService()
    ozet = []

    for i, (dosya, hedef_rol) in enumerate(SENARYOLAR, start=1):
        dosya_yolu = os.path.join(TEST_RESULTS, dosya)
        with open(dosya_yolu, "r", encoding="utf-8") as f:
            analiz = json.load(f)

        gaps = analiz.get("gaps", [])
        skills = analiz.get("skills", [])
        role_scores = analiz.get("role_scores", {})

        ad = dosya.replace("_result.json", "")
        cikti = os.path.join(LEARNING_PLANS, f"{ad}__{hedef_rol}.json")

        print("=" * 92)
        print(f"SENARYO {i}  |  CV: {os.path.basename(dosya)}  ->  HEDEF: {hedef_rol}")
        print(f"EKSIKLER: {gaps}")
        print("=" * 92)

        if i == 1:  # rol siralamasini bir kez goster yeter
            siralamayi_yazdir(role_scores)

        # --- KOTA KORUMASI: zaten uretilmis plani tekrar uretme ---
        if os.path.exists(cikti):
            print(f"\n  [CACHE] Plan zaten var, Gemini'ye GIDILMIYOR: {cikti}")
            print(f"          Yeniden uretmek istersen bu dosyayi sil.\n")
            with open(cikti, "r", encoding="utf-8") as f:
                plan = json.load(f)
            kontrol = plani_yazdir(plan, hedef_rol)
            ozet.append((i, hedef_rol, "CACHE", kontrol))
            continue

        # --- Gemini cagrisi (hata olsa bile digerleri devam etsin) ---
        try:
            plan = service.build_plan(target_role=hedef_rol, gaps=gaps, skills=skills)
        except Exception as e:
            hata = str(e)
            kisa = "KOTA DOLDU (429)" if "429" in hata or "RESOURCE_EXHAUSTED" in hata else hata[:80]
            print(f"\n  [ATLANDI] {hedef_rol} -> {kisa}\n")
            ozet.append((i, hedef_rol, "HATA", None))
            time.sleep(BEKLEME_SN)
            continue

        kontrol = plani_yazdir(plan, hedef_rol)

        with open(cikti, "w", encoding="utf-8") as f:
            json.dump(plan, f, indent=2, ensure_ascii=False)
        print(f"\n  -> Kaydedildi: {cikti}\n")

        ozet.append((i, hedef_rol, "URETILDI", kontrol))

        # RPM limitine takilmamak icin araya nefes koy (son senaryodan sonra gerek yok)
        if i < len(SENARYOLAR):
            print(f"  ({BEKLEME_SN} sn bekleniyor - rate limit korumasi)\n")
            time.sleep(BEKLEME_SN)

    # ------------------ GENEL OZET ------------------
    print("\n" + "=" * 92)
    print("GENEL OZET")
    print("=" * 92)
    print(f"{'#':<4}{'HEDEF ROL':<30}{'DURUM':<12}{'PROJE':<8}{'TURKCE':<9}{'SIZINTI'}")
    print("-" * 92)
    for i, rol, durum, k in ozet:
        if k is None:
            print(f"{i:<4}{rol:<30}{durum:<12}{'-':<8}{'-':<9}-")
        else:
            proje = "OK" if k["proje_var"] else "YOK"
            turkce = "OK" if k["turkce_ok"] else "YOK"
            sizinti = "VAR!" if k["teknik_sizinti"] else "yok"
            print(f"{i:<4}{rol:<30}{durum:<12}{proje:<8}{turkce:<9}{sizinti}")
    print("=" * 92)

    hatali = [r for _, r, d, _ in ozet if d == "HATA"]
    if hatali:
        print(f"UYARI: Su senaryolar calismadi -> {hatali}")
        print("       Kota dolduysa yarin (Pasifik saati gece yarisi sifirlaniyor) tekrar dene.")


if __name__ == "__main__":
    main()