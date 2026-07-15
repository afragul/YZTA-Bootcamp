import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from evals._paths import TEST_RESULTS

for fname in os.listdir(TEST_RESULTS):
    if not fname.endswith(".json"):
        continue

    with open(os.path.join(TEST_RESULTS, fname), "r", encoding="utf-8") as f:
        data = json.load(f)

    print("=" * 70)
    print(f"DOSYA: {fname}")

    scores = data.get("role_scores", {})
    reasons = data.get("top_role_reasons", [])

    if not reasons:
        print("  HATA: top_role_reasons alani BOS veya YOK!")
        continue

    # Gercekten en yuksek 3 rol mu?
    gercek_top3 = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:3]
    print(f"  Skorlara gore gercek top 3: {[r for r, s in gercek_top3]}")

    for r in reasons:
        rol = r.get("role")
        skor = r.get("score")

        isim_ok = rol in scores                      # rol adi gercek mi?
        skor_ok = isim_ok and scores[rol] == skor    # skor tutuyor mu?
        gerekce_ok = len(r.get("reason", "")) > 30   # gerekce dolu mu?

        durum = "OK" if (isim_ok and skor_ok and gerekce_ok) else "SORUN"
        print(f"\n  [{durum}] {rol} = {skor}")
        if not isim_ok:
            print("      -> ROL ADI role_scores'ta YOK (AI uydurmus!)")
        if isim_ok and not skor_ok:
            print(f"      -> SKOR UYUSMUYOR (role_scores'ta: {scores[rol]})")
        if not gerekce_ok:
            print("      -> GEREKCE COK KISA / BOS")
        print(f"      Gerekce: {r.get('reason')}")

print("\n" + "=" * 70)
print("Kontrol bitti.")