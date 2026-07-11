import os
import sys
import pandas as pd
import chromadb
from dotenv import load_dotenv

# 'embedding' modulu her koşulda bulunsun (standalone + paket import)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from embedding import get_embedding_function  # <-- ORTAK embedding (tek kaynak)


load_dotenv()

gemini_ef = get_embedding_function()

current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, "..", "data", "chromadb")
client = chromadb.PersistentClient(path=db_path)

#  Koleksiyon (cosine mesafesi -> yuzde skora cevirmesi kolay)
collection = client.get_or_create_collection(
    name="tech_job_postings",
    embedding_function=gemini_ef,
    metadata={"hnsw:space": "cosine"},
)

excel_path = os.path.join(current_dir, "..", "data", "jobs_dataset.xlsx")
print("Excel dosyasi okunuyor...")
df = pd.read_excel(excel_path)

df.columns = df.columns.str.strip()
df = df.dropna(subset=["job_id", "title", "description"])
# guvenlik: bos/whitespace aciklamalari da at (embedding'i anlamsiz olur)
df = df[df["description"].astype(str).str.strip() != ""]

print(f"Toplam {len(df)} ilan bulundu. Gemini ile vektorlenip ChromaDB'ye yukleniyor...")
print("Bu islem Google API hizina bagli olarak birkac dakika surebilir. Lutfen bekleyin...\n")

documents = df["description"].astype(str).tolist()
metadatas = (
    df[["title", "job_domain", "work_type", "job_location"]]
    .fillna("Belirtilmemis")
    .to_dict("records")
)
ids = [str(job_id) for job_id in df["job_id"].tolist()]

batch_size = 20
for i in range(0, len(documents), batch_size):
    end_idx = min(i + batch_size, len(documents))
    collection.upsert(
        documents=documents[i:end_idx],
        metadatas=metadatas[i:end_idx],
        ids=ids[i:end_idx],
    )
    print(f"--- {end_idx}/{len(documents)} ilan basariyla islendi ---")

print(f"\nTum ilanlar vektorlendi. Koleksiyondaki toplam kayit: {collection.count()}")
print("Veritabani diske kalici olarak kaydedildi.")