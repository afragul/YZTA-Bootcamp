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
        
        # Projede skorlama yapacağımız 15 hedef rol
        self.target_roles = [
            "Backend Developer",
            "Frontend Developer",
            "Mobile Developer",
            "DevOps Engineer",
            "Machine Learning Engineer",
            "Data Scientist",
            "Data Analyst",
            "UI/UX Designer",
            "Product Manager",
            "Project Manager",
            "Digital Marketing Specialist",
            "Business Analyst",
            "Sales / Account Specialist",
            "HR Specialist / Recruiter",
            "Customer Success Specialist"
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
        belirlenen 15 hedef rol için skorlama yapar ve JSON/Sözlük olarak döner.
        """
        response_schema = self._get_clean_schema()
        
        # Yapay zekaya 15 rolün tamamını analiz etmesini söyleyen sistem talimatı
        system_instruction = (
            "Sen profesyonel bir Kariyer ve İK Asistanı yapay zekasısın. Görevin, sana verilen "
            "CV metnini titizlikle incelemek ve belirtilen JSON şemasına uygun şekilde analiz etmektir.\n\n"
            "ÖNEMLİ KURALLAR:\n"
            "1. Deneyim yılını sayısal (float) olarak çıkar.\n"
            "2. Eğitim geçmişini listele.\n"
            "3. Adayın sahip olduğu hem teknik hem de sosyal/iletişim (soft skills) becerilerini listele.\n"
            "4. Adayın güçlü yönlerini (strengths) ve gelişim alanlarını (gaps) net maddeler halinde belirt.\n"
            "5. 'role_scores' altındaki tüm alanlar için adayın CV'sine göre 0-100 arasında uygunluk skoru ata:\n"
            "   - backend_developer, frontend_developer, mobile_developer, devops_engineer\n"
            "   - machine_learning_engineer, data_scientist, data_analyst\n"
            "   - ui_ux_designer, product_manager, project_manager\n"
            "   - digital_marketing_specialist, business_analyst, sales_specialist\n"
            "   - hr_specialist, customer_success_specialist\n"
            "Her bir alan için kesinlikle sayısal bir puan hesaplamalı ve boş bırakmamalısın."
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
