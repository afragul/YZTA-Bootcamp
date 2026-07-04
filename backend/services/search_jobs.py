import os
import sys
import chromadb
from dotenv import load_dotenv

from embedding import get_embedding_function  # ingest ile AYNI embedding

load_dotenv()

_current_dir = os.path.dirname(os.path.abspath(__file__))
_db_path = os.path.join(_current_dir, "..", "data", "chromadb")

# Modul yuklenirken bir kez baglan (her aramada yeniden acmamak icin)
_ef = get_embedding_function()
_client = chromadb.PersistentClient(path=_db_path)
_collection = _client.get_collection(name="tech_job_postings", embedding_function=_ef)


def _distance_to_percent(distance: float) -> float:
    """cosine distance (0..2) -> benzerlik yuzdesi (0..100)."""
    similarity = 1.0 - distance
    similarity = max(0.0, min(1.0, similarity))
    return round(similarity * 100, 1)


def search_jobs(cv_text: str, n: int = 5) -> list[dict]:
    """CV ozeti / arama metni -> en uygun n ilan (yuzde skorla).

    Donen yapi Kisi 1'in top_matches[] alanina dogrudan girebilir.
    """
    if not cv_text or not cv_text.strip():
        return []

    # Sorguyu RETRIEVAL_QUERY task_type ile embed'le, sonra vektorle sorgula.
    query_vec = _ef.embed_query(cv_text)
    res = _collection.query(
        query_embeddings=[query_vec],
        n_results=n,
    )

    matches = []
    for doc, meta, dist in zip(
        res["documents"][0], res["metadatas"][0], res["distances"][0]
    ):
        matches.append(
            {
                "title": meta.get("title", "Belirtilmemis"),
                "job_domain": meta.get("job_domain", "Belirtilmemis"),
                "work_type": meta.get("work_type", "Belirtilmemis"),
                "job_location": meta.get("job_location", "Belirtilmemis"),
                "match_percent": _distance_to_percent(dist),
                "description": doc,
            }
        )
    return matches


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