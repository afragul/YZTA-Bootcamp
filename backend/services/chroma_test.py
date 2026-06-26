import os
import chromadb
import chromadb.utils.embedding_functions as embedding_functions
from dotenv import load_dotenv

load_dotenv()

gemini_ef = embedding_functions.GoogleGenerativeAiEmbeddingFunction(
    api_key=os.environ.get("GEMINI_API_KEY")
)

client = chromadb.Client()

collection = client.create_collection(
    name="job_postings_openai",
    embedding_function=gemini_ef
)

# 4. Sisteme örnek ilanlar ekle
collection.add(
    documents=[
        "Backend Developer. Python, FastAPI, SQL ve sistem mimarisi konularında deneyimli.",
        "Frontend Developer. React, Vite ve Tailwind CSS ile arayüz geliştirecek.",
        "Data Scientist. Veri analizi, Makine Öğrenmesi, Pandas, NumPy ve XGBoost bilen takım arkadaşı aranıyor."
    ],
    metadatas=[{"role": "backend"}, {"role": "frontend"}, {"role": "data_science"}],
    ids=["job_1", "job_2", "job_3"]
)

print("Örnek ilanlar OpenAI ile vektörlenip veritabanına eklendi!\n")

kullanici_sorgusu = "Python ve veritabanı teknolojileri kullanarak arka uç sistemleri geliştirmek istiyorum."
print(f" Aranan Özellikler: '{kullanici_sorgusu}'\n")

results = collection.query(
    query_texts=[kullanici_sorgusu],
    n_results=1
)

print("🎯 En Uygun Eşleşme:")
print(results["documents"][0][0])