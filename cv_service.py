import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types
from schema import CVAnalysisOutput

# .env dosyasından çevresel değişkenleri yükle
load_dotenv(override=True)

class CVAnalysisService:
    def __init__(self):
        # Gemini API anahtarını yükler ve istemciyi başlatır
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY ortam değişkeni set edilmemiş! Lütfen .env dosyasını kontrol edin.")
        self.client = genai.Client(api_key=api_key)
        self.model_name = "gemini-2.5-flash"
        
        # Projede skorlama yapacağımız hedef roller
        self.target_roles = [
            "Backend Developer",
            "Frontend Developer",
            "Machine Learning Engineer",
            "Data Scientist",
            "DevOps Engineer"
        ]

    def _get_clean_schema(self) -> dict:
        # Pydantic modelinden additionalProperties alanını temizler (Gemini Developer API uyumluluğu için)
        raw_schema = CVAnalysisOutput.model_json_schema()
        
        def remove_additional_properties(schema):
            if isinstance(schema, dict):
                schema.pop("additionalProperties", None)
                for key, value in schema.items():
                    remove_additional_properties(value)
            elif isinstance(schema, list):
                for item in schema:
                    remove_additional_properties(item)
            return schema
            
        return remove_additional_properties(raw_schema)

    def analyze_cv(self, cv_text: str) -> dict:
        """
        Ham CV metnini alır, yapılandırılmış şemaya göre analiz eder,
        belirlenen hedef roller için skorlama yapar ve JSON/Sözlük olarak döner.
        """
        response_schema = self._get_clean_schema()
        
        # Rollerimizi yapay zekaya dikte eden sistem talimatı
        system_instruction = (
            "Sen profesyonel bir İK ve Kariyer Asistanı yapay zekasısın. Görevin, sana verilen "
            "CV metnini titizlikle incelemek ve belirtilen JSON şemasına uygun şekilde analiz etmektir.\n\n"
            "ÖNEMLİ KURALLAR:\n"
            "1. Deneyim yılını sayısal (float) olarak çıkar.\n"
            "2. Eğitim geçmişini listele.\n"
            "3. Adayın güçlü yönlerini (strengths) ve gelişim alanlarını (gaps) net maddeler halinde belirt.\n"
            "4. 'role_scores' altındaki her rol (backend_developer, frontend_developer, machine_learning_engineer, data_scientist, devops_engineer) için 0-100 arasında uygunluk skoru ata."
        )

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=f"Lütfen aşağıdaki CV metnini analiz et ve sonucu dön:\n\n{cv_text}",
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    response_mime_type="application/json",
                    response_schema=response_schema,
                    temperature=0.2 # Puanlamanın tutarlı olması için düşük sıcaklık
                ),
            )
            return json.loads(response.text)
        except Exception as e:
            print(f"[CVAnalysisService] Analiz hatası: {e}")
            raise e
