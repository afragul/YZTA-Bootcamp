"""
Relevans testi v2 (Kisi 4 - Sprint 3).

Iki arama yontemini YAN YANA kiyaslar:
  A) Ham CV metni      -> search_jobs
  B) Damitilmis skills -> build_search_text(Kisi 2 analizi) -> search_jobs

Amac: skills-metni gercekten daha iyi/ayrik eslesme veriyor mu gormek.

On kosul:
  1) backend/.env icinde GEMINI_API_KEY
  2) ingest yapilmis olmali:  cd backend/services && python ingest_jobs.py

Calistirma (repo kokune YA DA backend/ icine koyabilirsin):
  python test_relevance.py           # N=5
  python test_relevance.py 3         # N=3

Not: B yontemi her CV icin Kisi 2'nin analyze_cv'sini cagirir (LLM). 5 CV -> 5 analiz cagrisi.
"""
import glob
import os
import sys

from dotenv import load_dotenv


def _find_root(start: str) -> str:
    d = start
    for _ in range(5):
        if os.path.isdir(os.path.join(d, "sample_cvs")) and \
           os.path.isdir(os.path.join(d, "backend", "services")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    raise RuntimeError("Repo koku bulunamadi (sample_cvs + backend/services).")


_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = _find_root(_HERE)

load_dotenv(os.path.join(_ROOT, "backend", ".env"))
load_dotenv()

# backend/ path'e -> 'services' ve 'schemas' paket olarak import edilebilir
sys.path.insert(0, os.path.join(_ROOT, "backend"))
from services.search_jobs import search_jobs, build_search_text  # noqa: E402

# Kisi 2'nin analizi (skills icin). Yoksa/patlyorsa B yontemi atlanir.
try:
    from services.cv_service import CVAnalysisService  # noqa: E402
    _analyzer = CVAnalysisService()
except Exception as e:  # noqa: BLE001
    _analyzer = None
    print(f"[uyari] Kisi 2 analiz servisi yuklenemedi ({e}). Sadece ham CV testi kosacak.\n")


EXPECTED = {
    "backend": ["backend", "python", "api", "server", "django", "fastapi", "java",
                "node", "software engineer", "software developer", "dotnet", ".net",
                "golang", "microservice", "sql"],
    "frontend": ["frontend", "front end", "front-end", "react", "javascript", "ui",
                 "web developer", "full stack", "typescript", "angular", "vue"],
    "devops": ["devops", "kubernetes", "aws", "cloud", "ci/cd", "infrastructure",
               "sre", "site reliability", "platform", "terraform", "docker"],
    "data_scientist": ["data scientist", "data analyst", "analytics", "machine learning",
                       "data engineer", "business intelligence", "power bi", "statistic",
                       "insights", "revenue cycle"],
    "ml_engineer": ["machine learning", "ml engineer", "ai", "deep learning", "nlp",
                    "data scientist", "computer vision", "pytorch", "tensorflow", "graphics"],
}


def _is_relevant(role: str, m: dict) -> bool:
    kws = EXPECTED.get(role, [])
    hay = f"{m.get('title','')} {m.get('job_domain','')} {m.get('description','')[:200]}".lower()
    return any(k in hay for k in kws)


def _run(role: str, query: str, n: int, label: str):
    matches = search_jobs(query, n=n, include_raw=True)
    print(f"  [{label}]  sorgu: {query[:70]}{'...' if len(query) > 70 else ''}")
    if not matches:
        print("    Sonuc yok! ingest yapildi mi?")
        return None
    rel = 0
    for m in matches:
        ok = _is_relevant(role, m)
        rel += ok
        print(f"      {'OK ' if ok else '?? '}kal%{m['match_percent']:<5} "
              f"ham{m.get('raw_score','?'):<7} | "
              f"[{m['job_domain'][:16]:16}] {m['title'][:40]}")
    scores = [m["match_percent"] for m in matches]
    top, low = max(scores), min(scores)
    print(f"      -> top=%{top}  low=%{low}  aralik={top-low:.1f}  rol-uygun={rel}/{len(matches)}")
    return {"top": top, "low": low, "spread": round(top - low, 1), "rel": rel, "n": len(matches)}


def main() -> None:
    n = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 5
    cv_files = sorted(glob.glob(os.path.join(_ROOT, "sample_cvs", "*.txt")))
    if not cv_files:
        print("sample_cvs/*.txt bulunamadi.")
        return

    rows = []
    for path in cv_files:
        role = os.path.basename(path).replace("cv_", "").replace(".txt", "")
        cv_text = open(path, encoding="utf-8").read()
        print(f"\n{'='*72}\n### CV: {role}")

        a = _run(role, cv_text, n, "A ham CV")

        b = None
        if _analyzer is not None:
            try:
                analysis = _analyzer.analyze_cv(cv_text)
                query = build_search_text(analysis)
                b = _run(role, query, n, "B skills ")
            except Exception as e:  # noqa: BLE001
                print(f"  [B atlandi] analiz hatasi: {e}")

        rows.append((role, a, b))

    # Kiyas ozeti
    print(f"\n{'='*72}\nKIYAS OZETI  (A=ham CV, B=skills-metni)")
    hdr = f"{'CV':15} | {'A top%':>6} {'A spr':>6} {'A uyg':>6} | {'B top%':>6} {'B spr':>6} {'B uyg':>6}"
    print(hdr); print("-" * len(hdr))
    for role, a, b in rows:
        astr = f"{a['top']:>6} {a['spread']:>6} {str(a['rel'])+'/'+str(a['n']):>6}" if a else f"{'-':>6} {'-':>6} {'-':>6}"
        bstr = f"{b['top']:>6} {b['spread']:>6} {str(b['rel'])+'/'+str(b['n']):>6}" if b else f"{'-':>6} {'-':>6} {'-':>6}"
        print(f"{role:15} | {astr} | {bstr}")
    # Floor probe: alakasiz sorgular -> kalibrasyon esiginin dogru yerde
    # oldugunu dogrula (bu isler ideal olarak <%50 kalmali).
    print(f"\n{'='*72}\nFLOOR PROBE (alakasiz sorgular, kalibrasyon esigi kontrolu)")
    for label, q in [
        ("garson/servis", "Beceriler: yemek pisirme, garsonluk, servis, kasa, mutfak"),
        ("hemsirelik", "Beceriler: hasta bakimi, hemsirelik, ilac takibi, klinik gozlem"),
    ]:
        ms = search_jobs(q, n=3, include_raw=True)
        print(f"  [{label}] {q[:52]}")
        for m in ms:
            print(f"      kal%{m['match_percent']:<5} ham{m.get('raw_score','?'):<7} | {m['title'][:44]}")
    print("  -> Kalibre skorlar dusukse (ideali <%50) esik dogru yerde demektir.")

    print("\nBakilacak: B'nin top% ve spread'i A'dan yuksekse skills-metni daha iyi ayiriyor demektir.")


if __name__ == "__main__":
    main()