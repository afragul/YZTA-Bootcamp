"""
Ortak Gemini embedding fonksiyonu.
Hem ingest_jobs.py hem search_jobs.py BUNU kullanır.
Boylece yukleme ve sorgu HER ZAMAN ayni model + ayni boyutu kullanir.
"""
import os
import time
from google import genai
from google.genai import types
from chromadb import Documents, EmbeddingFunction, Embeddings

# gemini-embedding-001 varsayilan olarak 3072 boyut uretir ve 3072'de
# vektorler zaten L2-normalize'dir (manuel normalize gerekmez).
MODEL_NAME = "models/gemini-embedding-001"
EMBED_DIM = 3072


class GeminiEmbedding(EmbeddingFunction):
    """ChromaDB koleksiyonuna baglanan embedding fonksiyonu.

    ChromaDB depolanan dokumanlari embed'lerken __call__'u cagirir
    -> RETRIEVAL_DOCUMENT task_type kullanilir.
    Sorgu tarafi ayri: search_jobs.py embed_query()'yi cagirir
    -> RETRIEVAL_QUERY task_type (retrieval kalitesi icin dogrusu budur).
    """

    def __init__(self, key: str):
        if not key:
            raise ValueError("GEMINI_API_KEY bulunamadi. .env dosyasini kontrol et.")
        self.client = genai.Client(api_key=key)

    def _embed_one(self, text: str, task_type: str) -> list[float]:
        # Bos / string olmayan metin -> DOGRU boyutta sifir vektor (3072).
        if not text or not isinstance(text, str) or not text.strip():
            return [0.0] * EMBED_DIM

        time.sleep(1.2)  # rate limit icin nazik bekleme
        response = self.client.models.embed_content(
            model=MODEL_NAME,
            contents=text,
            config=types.EmbedContentConfig(task_type=task_type),
        )
        return response.embeddings[0].values

    def __call__(self, input: Documents) -> Embeddings:
        # Depolanan is ilanlari -> DOCUMENT
        return [self._embed_one(t, "RETRIEVAL_DOCUMENT") for t in input]

    def embed_query(self, text: str) -> list[float]:
        # Kullanicinin CV ozeti / arama metni -> QUERY
        return self._embed_one(text, "RETRIEVAL_QUERY")


def get_embedding_function() -> GeminiEmbedding:
    return GeminiEmbedding(key=os.environ.get("GEMINI_API_KEY"))