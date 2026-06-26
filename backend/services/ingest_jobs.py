import os
import pandas as pd
import chromadb
from chromadb import Documents, EmbeddingFunction, Embeddings
from google import genai
from dotenv import load_dotenv
import time

# 1. Çevresel Değişkenleri Yükle
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

# 2. Kendi Özel Gemini Embedding Fonksiyonumuz (Stabil Model)
class ModernGeminiEmbedding(EmbeddingFunction):
    def __init__(self, key: str):
        self.client = genai.Client(api_key=key)
        # Terminal çıktına göre en doğru isim:
        self.model_name = "models/gemini-embedding-001"

    def __call__(self, input: Documents) -> Embeddings:
        embeddings = []
        for text in input:
            if not text or not isinstance(text, str):
                embeddings.append([0.0] * 768)
                continue

            # HER İSTEKTEN SONRA 1 SANİYE BEKLE
            time.sleep(1.2)

            response = self.client.models.embed_content(
                model=self.model_name,
                contents=text
            )
            embeddings.append(response.embeddings[0].values)
        return embeddings

gemini_ef = ModernGeminiEmbedding(key=api_key)

# 3. Kalıcı Veritabanı Yolu Ayarla
current_dir = os.path.dirname(__file__)
db_path = os.path.join(current_dir, "..", "data", "chromadb")
client = chromadb.PersistentClient(path=db_path)

# 4. Koleksiyonu Oluştur
collection = client.get_or_create_collection(
    name="tech_job_postings",
    embedding_function=gemini_ef
)

# 5. Excel Dosyasını Oku
excel_path = os.path.join(current_dir, "..", "data", "jobs_dataset.xlsx")
print("Excel dosyası okunuyor...")
df = pd.read_excel(excel_path)

df.columns = df.columns.str.strip()
df = df.dropna(subset=['job_id', 'title', 'description'])

print(f"Toplam {len(df)} ilan bulundu. Gemini ile vektörlenip ChromaDB'ye yükleniyor...")
print("Bu işlem Google API hızına bağlı olarak birkaç dakika sürebilir. Lütfen bekleyin...\n")

# 6. Verileri Hazırla
documents = df['description'].tolist()
metadatas = df[['title', 'job_domain', 'work_type', 'job_location']].fillna("Belirtilmemiş").to_dict('records')
ids = [str(job_id) for job_id in df['job_id'].tolist()]

# 7. Verileri ChromaDB'ye Ekle
batch_size = 20
for i in range(0, len(documents), batch_size):
    end_idx = min(i + batch_size, len(documents))

    collection.upsert(
        documents=documents[i:end_idx],
        metadatas=metadatas[i:end_idx],
        ids=ids[i:end_idx]
    )
    print(f"--- {end_idx}/{len(documents)} ilan başarıyla işlendi ---")

print("\nTüm ilanlar vektörlendi ve veritabanı diske kalıcı olarak kaydedildi.")