import math
import os
import sys
import chromadb
from dotenv import load_dotenv

# Bu dosyanin dizinini path'e ekle -> 'embedding' hem standalone hem paket
# (services.search_jobs) olarak import edildiginde bulunur.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from embedding import get_embedding_function  # ingest ile AYNI embedding

load_dotenv()

_current_dir = os.path.dirname(os.path.abspath(__file__))
_db_path = os.path.join(_current_dir, "..", "data", "chromadb")

_ef = get_embedding_function()
_client = chromadb.PersistentClient(path=_db_path)
_collection = None


def _get_collection():
    global _collection
    if _collection is None:
        _collection = _client.get_collection(
            name="tech_job_postings", embedding_function=_ef
        )
    return _collection


def _distance_to_percent(distance: float) -> float:
    """cosine distance -> KALIBRE gosterim yuzdesi (siralama-koruyan).

    Sorun: alakali eslesmelerin cosine benzerligi dar/yuksek bir bantta
    (~0.60-0.68) toplaniyor; ham (1-distance)*100 bunu 60-68'e sikistirinca
    kullanici mukemmel eslesmeyi "%67" gorup dusuk saniyor, liste ayrismiyor.

    Cozum: benzerligi sigmoid ile sezgisel bir 0-100'e yay. Fonksiyon MONOTON,
    yani siralama HIC degismez; sadece gosterim olcegi degisir.
    """
    similarity = max(0.0, min(1.0, 1.0 - distance))
    return _calibrate(similarity)


# --- Skor kalibrasyonu (gosterim) ---
# Parametreler test_relevance floor probe'u ile OLCULEN dagilimdan secildi:
#   - gemini-embedding tabani yuksek: ALAKASIZ sorgular bile ~0.58-0.59 benzerlik alir
#     (hepsi ayni "is/beceri" uzayinda oldugu icin).
#   - ALAKALI eslesmeler ~0.62-0.68.
# Bu yuzden midpoint tabanin ustune, gercek eslesmelerin altina (~0.60) konur;
# steepness dar bandi (0.60-0.68) genis bir 0-100'e yayar.
# Sonuc (olculen): alakasiz ~%38-44 (<%50), iyi eslesme ~%86-90.
# Dataset ciddi degisirse floor probe'u tekrar kosup bu iki degeri ayarla.
_CALIB_MIDPOINT = 0.60    # ~%50 gosterilecek "sinirda" benzerlik (alakasiz tavaninin ustu)
_CALIB_STEEPNESS = 28.0   # egri dikligi; buyudukce iyi/kotu ayrisimi keskinlesir


def _calibrate(similarity: float) -> float:
    """cosine benzerligi (~0.4-0.7) -> sezgisel gosterim yuzdesi (0-100)."""
    pct = 100.0 / (1.0 + math.exp(-_CALIB_STEEPNESS * (similarity - _CALIB_MIDPOINT)))
    return round(pct, 1)


def _as_dict(obj) -> dict:
    if obj is None:
        return {}
    if hasattr(obj, "model_dump"):
        return obj.model_dump()
    return dict(obj) if not isinstance(obj, dict) else obj


def build_search_text(analysis) -> str:
    """Kisi 2'nin analiz ciktisindan damitilmis, skill-yogun ARAMA METNI uretir.

    Ham CV yerine bunu search_jobs'a vermek retrieval kalitesini artirir:
    isim/okul/yil gibi gurultuyu atar, embedding'i becerilere odaklar.

    Uretilen metin: beceriler + deneyim + hedef rol (role_scores'ta en yuksek).
    strengths bilincli olarak DAHIL EDILMEZ (uzun prose -> gurultu).
    """
    a = _as_dict(analysis)
    parts: list[str] = []

    skills = a.get("skills") or []
    if skills:
        parts.append("Beceriler: " + ", ".join(str(s) for s in skills))

    exp = a.get("experience_years")
    if exp is not None:
        parts.append(f"Deneyim: {exp} yil")

    role_scores = _as_dict(a.get("role_scores"))
    if role_scores:
        top_role = max(role_scores.items(), key=lambda kv: kv[1])[0]
        parts.append("Hedef rol: " + top_role.replace("_", " "))

    return ". ".join(parts)


def search_jobs(cv_text: str, n: int = 5, include_raw: bool = False) -> list[dict]:
    """CV ozeti / arama metni -> en uygun n ilan.

    Donen her oge JobMatchItem kontratina BIREBIR uyar (frontend'e hazir):
      title, job_domain, work_type, job_location, match_percent, description
    Kisi 1'in top_matches[] alanina dogrudan girebilir.

    include_raw=True -> ek 'raw_score' (kalibrasyon oncesi ham benzerlik) eklenir.
      Bu SADECE tani/test icindir; production/frontend cagrisinda kullanma.
    """
    if not cv_text or not cv_text.strip():
        return []

    # Sorguyu RETRIEVAL_QUERY task_type ile embed'le, sonra vektorle sorgula.
    query_vec = _ef.embed_query(cv_text)
    res = _get_collection().query(
        query_embeddings=[query_vec],
        n_results=n,
    )

    matches = []
    for doc, meta, dist in zip(
        res["documents"][0], res["metadatas"][0], res["distances"][0]
    ):
        item = {
            "title": meta.get("title", "Belirtilmemis"),
            "job_domain": meta.get("job_domain", "Belirtilmemis"),
            "work_type": meta.get("work_type", "Belirtilmemis"),
            "job_location": meta.get("job_location", "Belirtilmemis"),
            "match_percent": _distance_to_percent(dist),
            "description": doc,
        }
        if include_raw:
            # kalibrasyon oncesi ham cosine benzerligi (0-1) - sadece tani icin
            item["raw_score"] = round(max(0.0, min(1.0, 1.0 - dist)), 4)
        matches.append(item)
    return matches


def search_jobs_from_analysis(analysis, n: int = 5) -> list[dict]:
    """Kolaylik: Kisi 2 analizi -> skills-metni -> en uygun n ilan.

    Orkestrasyon (Kisi 1) icin tek cagri:
        top_matches = search_jobs_from_analysis(analysis, n=5)
    build_search_text + search_jobs'u birlestirir. Ham CV yerine damitilmis
    skills-metniyle sorgular (test: daha yuksek + isabetli skor).
    """
    return search_jobs(build_search_text(analysis), n=n)


if __name__ == "__main__":
    # Terminalden test: python search_jobs.py "aradigin sey"
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        query = "Python ve FastAPI ile backend sistemleri gelistiren, SQL bilen biriyim."

    print(f"Aranan: {query}\n")
    results = search_jobs(query, n=5)

    if not results:
        print("Sonuc yok. Once ingest_jobs.py'yi calistirdin mi?")
    else:
        print("En uygun ilanlar:")
        for r in results:
            print(f"  %{r['match_percent']:<5} | {r['title']}  "
                  f"({r['job_domain']} / {r['work_type']} / {r['job_location']})")
            print(f"          {r['description'][:90]}...\n")