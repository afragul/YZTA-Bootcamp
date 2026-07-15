import os
import json
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import ValidationError
from schemas.cv_analysis import CVAnalysisOutput


class CVAnalysisError(Exception):
    """CV analizinin (Gemini cagrisi + JSON parse + sema dogrulama) basarisiz oldugunu belirtir."""


MAX_ATTEMPTS = 3
BACKOFF_BASE_SECONDS = 1.0


# .env dosyasından çevresel değişkenleri yükle
load_dotenv(override=True)

class CVAnalysisService:
    def __init__(self):
        # Gemini API anahtarını yükler ve istemciyi başlatır
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY ortam değişkeni set edilmemiş! Lütfen .env dosyasını kontrol edin.")
        self.client = genai.Client(api_key=api_key)
        self.model_name = "gemini-3.5-flash"
        
        # Projede skorlama yapacağımız 22 hedef rol (jobs_dataset.xlsx analizinden türetilmiştir)
        self.target_roles = [
            "Backend Developer",
            "Frontend Developer",
            "Full Stack Developer",
            "Mobile Developer",
            "DevOps Engineer",
            "Cloud Engineer / Architect",
            "Machine Learning Engineer",
            "Data Scientist",
            "Data Engineer",
            "Data Analyst",
            "Business Intelligence (BI) Analyst",
            "Database Administrator (DBA)",
            "Cybersecurity Specialist",
            "Systems / Network Administrator",
            "UI/UX Designer",
            "Graphic Designer",
            "Product Manager",
            "Project Manager",
            "Business Analyst",
            "Digital Marketing Specialist",
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

    def _attempt_analysis(self, cv_text: str) -> dict:
        """Tek bir Gemini cagrisi yapar, ciktiyi semaya gore dogrular, dict dondurur.

        Cagri / JSON parse / dogrulama hatalarini YAKALAMAZ; retry mantigi
        analyze_cv'ye aittir. Basarili donus her zaman CVAnalysisOutput semasina
        uygun bir dict'tir.
        """
        response_schema = self._get_clean_schema()

        # Yapay zekaya 22 rolun tamamini analiz etmesini soyleyen sistem talimati
        system_instruction = (
            "Sen profesyonel bir Kariyer ve İK Asistanı yapay zekasısın. Görevin, sana verilen "
            "CV metnini titizlikle incelemek ve belirtilen JSON şemasına uygun şekilde analiz etmektir.\n\n"
            "ÖNEMLİ KURALLAR:\n"
            "1. Deneyim yılını sayısal (float) olarak çıkar.\n"
            "2. Eğitim geçmişini listele.\n"
            "3. Adayın sahip olduğu teknik, sektörel ve sosyal (soft skills) becerilerini listele.\n"
            "4. Adayın güçlü yönlerini (strengths) ve gelişim alanlarını (gaps) net maddeler halinde belirt.\n"
            "5. 'role_scores' altındaki tüm 22 alan için adayın CV'sine göre 0-100 arasında uygunluk skoru ata:\n"
            "   - Yazılım Geliştirme: backend_developer, frontend_developer, fullstack_developer, mobile_developer, devops_engineer, cloud_engineer\n"
            "   - Veri & AI Sistemleri: machine_learning_engineer, data_scientist, data_engineer, data_analyst, bi_analyst, database_administrator\n"
            "   - Altyapı & Güvenlik: cybersecurity_specialist, systems_administrator\n"
            "   - Tasarım: ui_ux_designer, graphic_designer\n"
            "   - Yönetim & Analiz: product_manager, project_manager, business_analyst\n"
            "   - İş Operasyonları: digital_marketing_specialist, hr_specialist, customer_success_specialist\n"
            "Her bir alan için kesinlikle sayısal bir puan hesaplamalı ve boş bırakmamalısın.\n"
            "6. SKORLAMA CETVELİ - her rol için bu ölçütü aynı şekilde uygula:\n"
            "   - 0-20  : CV'de bu rolle ilgili hiçbir kanıt yok.\n"
            "   - 21-40 : Çok dolaylı/zayıf ilişki (sadece genel yetenekler örtüşüyor).\n"
            "   - 41-60 : Temel bilgi var ama pratik proje/deneyim kanıtı yok.\n"
            "   - 61-80 : İlgili beceriler + en az bir somut proje veya deneyim var.\n"
            "   - 81-100: Rolün çekirdek becerilerinin çoğu + gerçek iş/proje deneyimi var.\n"
            "   Puanı DAİMA CV'deki somut kanıta dayandır, tahmin yürütme veya varsayımda bulunma.\n"
            "7. 'top_role_reasons' alanını doldur: role_scores içindeki EN YÜKSEK skorlu 3 rolü "
            "skora göre azalan sırada yaz. Her biri için:\n"
            "   - 'role': role_scores'taki teknik alan adının AYNISI olmalı (orn: machine_learning_engineer)\n"
            "   - 'score': role_scores'ta verdiğin puanın AYNISI olmalı\n"
            "   - 'reason': 1-2 cümlelik gerekçe. Gerekçede CV'den SOMUT kanıt göster "
            "(beceri adı, araç adı, proje veya deneyim). Genel geçer cümle kurma.\n"
            "   Örnek iyi gerekçe: 'PyTorch ve MLflow ile model geliştirme ve deney takibi deneyimi "
            "bu rolün çekirdek gereksinimlerini karşılıyor.'\n"
            "   Örnek kötü gerekçe: 'Aday bu rol için uygundur.' (somut kanıt yok)"
        )

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=f"Lütfen aşağıdaki CV metnini analiz et ve sonucu dön:\n\n{cv_text}",
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json",
                response_schema=response_schema,
                temperature=0.2,  # Puanlamanın tutarlı olması için düşük sıcaklık
            ),
        )

        data = json.loads(response.text)
        validated = CVAnalysisOutput(**data)
        return validated.model_dump()

    def analyze_cv(self, cv_text: str) -> dict:
        """Ham CV metnini analiz eder; retry + sema dogrulama ile saglam dict dondurur.

        En fazla MAX_ATTEMPTS deneme yapar:
          - Cikti hatasi (bozuk JSON / semaya uymayan) -> beklemeden tekrar dener.
          - API hatasi (timeout / 429 / 5xx vb.) -> artan bekleme sonra tekrar dener.
        Tum denemeler tukenirse CVAnalysisError firlatir (orijinal sebep zincirlenir).
        """
        last_error: Exception | None = None
        for attempt in range(1, MAX_ATTEMPTS + 1):
            try:
                return self._attempt_analysis(cv_text)
            except (json.JSONDecodeError, ValidationError) as output_err:
                # Model bir sonraki denemede duzgun JSON/sema uretebilir; beklemeden dene
                last_error = output_err
            except Exception as api_err:
                # Gecici API hatasi: artan bekleme sonra tekrar dene
                last_error = api_err
                if attempt < MAX_ATTEMPTS:
                    time.sleep(BACKOFF_BASE_SECONDS * attempt)

        raise CVAnalysisError(
            f"CV analizi {MAX_ATTEMPTS} denemede başarısız: {last_error}"
        ) from last_error
