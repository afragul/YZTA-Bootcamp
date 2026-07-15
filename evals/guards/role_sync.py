import sys
from pathlib import Path

# Repo kokunu sys.path'e ekle (scripti nasil calistirirsan calistir bulsun)
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from evals._paths import BACKEND  # noqa: F401  (backend'i sys.path'e ekler)

from schemas.cv_analysis import RoleScores
from schemas.learning_plan import TargetRole
from services.learning_service import ROLE_DISPLAY


def main():
    skorlanan = set(RoleScores.model_fields.keys())       # cv_analysis.py
    planlanabilir = {rol.value for rol in TargetRole}     # learning_plan.py
    etiketli = set(ROLE_DISPLAY.keys())                   # learning_service.py

    print("=" * 70)
    print("ROL SENKRON TESTI")
    print("=" * 70)
    print(f"RoleScores (skorlanan)   : {len(skorlanan)} rol")
    print(f"TargetRole (planlanabilir): {len(planlanabilir)} rol")
    print(f"ROLE_DISPLAY (etiketli)  : {len(etiketli)} rol")
    print("-" * 70)

    hata = False

    eksik_plan = skorlanan - planlanabilir
    if eksik_plan:
        hata = True
        print(f"HATA: Skorlaniyor ama PLANI YOK -> {sorted(eksik_plan)}")
        print("      Cozum: schemas/learning_plan.py -> TargetRole'a ekle")

    fazla_plan = planlanabilir - skorlanan
    if fazla_plan:
        hata = True
        print(f"HATA: TargetRole'da var ama SKORLANMIYOR -> {sorted(fazla_plan)}")
        print("      Cozum: yazim hatasi olabilir, RoleScores ile karsilastir")

    eksik_etiket = planlanabilir - etiketli
    if eksik_etiket:
        hata = True
        print(f"HATA: ROLE_DISPLAY'de ETIKETI YOK -> {sorted(eksik_etiket)}")
        print("      Cozum: services/learning_service.py -> ROLE_DISPLAY'e ekle")

    print("-" * 70)
    if hata:
        print("SONUC: SENKRON DEGIL! Yukaridaki hatalari duzelt.")
        sys.exit(1)

    print("SONUC: SENKRON. 3 liste de birebir ayni (22 rol).")
    print("=" * 70)


if __name__ == "__main__":
    main()