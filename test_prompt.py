import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types
from schema import CVAnalysisOutput

# .env dosyasından API anahtarını yükle
load_dotenv()

# Gemini API anahtarı kontrolü
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("WARNING: GEMINI_API_KEY environment variable is not set. Please create a .env file and add your key.")
    print("Or set it in your system environment variables.")

def run_test():
    if not api_key:
        print("API anahtarı bulunamadığı için LLM testi atlanıyor, sadece lokal doğrulama yapılacak.")
        return
        
    print("Gemini API ile bağlantı kuruluyor...")
    client = genai.Client(api_key=api_key)
    
    sample_cv_text = """
    Ad Soyad: Caner Demir
    Eğitim: Orta Doğu Teknik Üniversitesi (ODTÜ) Bilgisayar Mühendisliği Lisans Mezunu (2024 mezuniyet)
    Beceriler: Python, FastAPI, Docker, PostgreSQL, Redis, Kubernetes, Git, Temel TensorFlow.
    Deneyim: ABC Teknoloji firmasında 1 yıl Backend Developer olarak çalıştı. Microservice mimarisi üzerinde REST API'ler yazdı.
    """
    
    print("Örnek CV analiz ediliyor...")
    try:
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=f"Aşağıdaki CV metnini analiz et ve sonucu belirtilen JSON şemasına göre doldur:\n\n{sample_cv_text}",
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=CVAnalysisOutput,
            ),
        )
        
        # Çıktıyı ekrana güzelce yazdır
        output_json = json.loads(response.text)
        print("\n=== ANALİZ BAŞARIYLA TAMAMLANDI ===")
        print(json.dumps(output_json, indent=2, ensure_ascii=False))
        
    except Exception as e:
        print(f"Hata oluştu: {e}")

if __name__ == "__main__":
    run_test()
