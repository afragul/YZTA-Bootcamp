import os, sys, json
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend"))

from services.cv_service import CVAnalysisService

# Hangi CV'yi test edeceksen burayı değiştir
CV_FILE = "sample_cvs/cv_data_scientist.txt" 

with open(CV_FILE, "r", encoding="utf-8") as f:
    cv_text = f.read()

service = CVAnalysisService()
result = service.analyze_cv(cv_text)

print(f"\n=== {CV_FILE} ===\n")

# 1) Skorlar cetvele uyuyor mu? (en yüksek 5)
top5 = sorted(result["role_scores"].items(), key=lambda x: x[1], reverse=True)[:5]
print("EN YUKSEK 5 ROL:")
for rol, skor in top5:
    print(f"  {skor:>3} | {rol}")

# 2) Gerekçeler geldi mi, mantıklı mı?
print("\nTOP_ROLE_REASONS:")
for r in result.get("top_role_reasons", []):
    print(f"\n  [{r['score']}] {r['role']}")
    print(f"      {r['reason']}")

print("\nEN DUSUK 5 ROL (0-20 arasi olmali):")
bottom5 = sorted(result["role_scores"].items(), key=lambda x: x[1])[:5]
for rol, skor in bottom5:
    print(f"  {skor:>3} | {rol}")