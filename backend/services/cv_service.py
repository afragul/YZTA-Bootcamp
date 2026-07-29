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


class InvalidCVError(Exception):
    """Girdi metninin gecerli bir CV olmadigini belirtir (cok kisa/bos veya alakasiz belge)."""


MIN_CV_TEXT_LENGTH = 40

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

        # Statik girdiler bir kez hesaplanir (her cagride yeniden uretme -> tekrarli is azalir).
        self._response_schema = self._get_clean_schema()
        self._system_instruction = self._build_system_instruction()

        # Son basarili cagrinin token kullanimi (usage_metadata). Cagri yapilmadan once None.
        self.last_usage: dict | None = None

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

    def _build_system_instruction(self) -> str:
        """22 rolun tamamini doldurtan sistem talimatini uretir (bir kez, __init__'te).

        Token maliyetini dusurmek icin yogunlastirilmistir; ancak cikti kalitesini
        belirleyen KIRMIZI CIZGILER korunur: 22 snake_case rol listesi, 0-100 skorlama
        cetveli, gaps '[rol_adi]' zorunlu bicimi ve top_role_reasons kurallari.
        """
        return (
            "Sen profesyonel bir Kariyer ve İK Asistanı yapay zekasısın. Verilen CV metnini "
            "incele ve belirtilen JSON şemasına uygun analiz üret. Tüm puan ve gerekçeleri "
            "CV'deki SOMUT kanıta dayandır; tahmin veya varsayım yapma.\n\n"
            "KURALLAR:\n"
            "0. Metin bir CV değilse (tarif, haber, makale, rastgele metin) TÜM alanları boş/0 "
            "döndür: skills=[], experience_years=0, education=[], strengths=[], gaps=[], tüm "
            "role_scores=0, top_role_reasons=[].\n"
            "1. experience_years: deneyim yılı (float). education: eğitim geçmişi. skills: teknik, "
            "sektörel ve sosyal (soft) becerilerin listesi.\n"
            "2. strengths: adayın genel güçlü yönleri, net maddeler halinde.\n"
            "3. gaps: SADECE en yüksek skorlu 3 role özgü eksikler. Her madde İSTİSNASIZ "
            "'[rol_teknik_adı] ...' ile başlamalı; etiketsiz veya genel zayıflık (örn. 'iletişim "
            "eksik') YAZMA. Köşeli parantezdeki ad role_scores'taki snake_case adın AYNISI ve en "
            "yüksek 3 rolden biri olmalı. Aday o rolde güçlü olsa bile onu DAHA İYİ yapacak eksik "
            "beceri/araç/deneyimi yaz; rol başına en önemli 1-3 eksik, liste kısa ve eyleme dönük. "
            "Örnek: '[machine_learning_engineer] Üretim ortamında model dağıtımı (MLOps) deneyimi yok'.\n"
            "4. role_scores: aşağıdaki 22 alanın HEPSİNE 0-100 uygunluk skoru ver, hiçbirini boş "
            "bırakma:\n"
            "   backend_developer, frontend_developer, fullstack_developer, mobile_developer, "
            "devops_engineer, cloud_engineer, machine_learning_engineer, data_scientist, "
            "data_engineer, data_analyst, bi_analyst, database_administrator, "
            "cybersecurity_specialist, systems_administrator, ui_ux_designer, graphic_designer, "
            "product_manager, project_manager, business_analyst, digital_marketing_specialist, "
            "hr_specialist, customer_success_specialist.\n"
            "5. Skorlama cetveli (her role aynı uygula): 0-20 ilgili kanıt yok; 21-40 çok "
            "dolaylı/zayıf ilişki; 41-60 temel bilgi var, proje/deneyim yok; 61-80 ilgili "
            "beceriler + en az bir somut proje/deneyim; 81-100 çekirdek becerilerin çoğu + gerçek "
            "iş/proje deneyimi.\n"
            "6. top_role_reasons: en yüksek skorlu 3 rolü azalan sırada yaz. Her biri için 'role' = "
            "role_scores'taki snake_case adın AYNISI, 'score' = verdiğin puanın AYNISI, 'reason' = "
            "CV'den somut kanıt (beceri/araç/proje/deneyim) içeren 1-2 cümle. Genel geçer gerekçe "
            "(örn. 'Aday bu rol için uygundur') yazma."
        )

    def _attempt_analysis(self, cv_text: str) -> dict:
        """Tek bir Gemini cagrisi yapar, ciktiyi semaya gore dogrular, dict dondurur.

        Cagri / JSON parse / dogrulama hatalarini YAKALAMAZ; retry mantigi
        analyze_cv'ye aittir. Basarili donus her zaman CVAnalysisOutput semasina
        uygun bir dict'tir. Yan etki: basarili cagrida self.last_usage guncellenir
        ve token kullanimi konsola basilir.
        """
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=f"Lütfen aşağıdaki CV metnini analiz et ve sonucu dön:\n\n{cv_text}",
            config=types.GenerateContentConfig(
                system_instruction=self._system_instruction,
                response_mime_type="application/json",
                response_schema=self._response_schema,
                temperature=0.2,  # Puanlamanın tutarlı olması için düşük sıcaklık
            ),
        )

        self._record_usage(response)

        data = json.loads(response.text)
        validated = CVAnalysisOutput(**data)
        return validated.model_dump()

    def _record_usage(self, response) -> None:
        """Yanittaki usage_metadata'yi self.last_usage'a yazar ve konsola basar.

        Savunmaci: usage_metadata yoksa (orn. testteki sahte yanit) sessizce gecer,
        cagriyi bozmaz.
        """
        usage = getattr(response, "usage_metadata", None)
        if usage is None:
            return
        prompt_tokens = getattr(usage, "prompt_token_count", None)
        output_tokens = getattr(usage, "candidates_token_count", None)
        total_tokens = getattr(usage, "total_token_count", None)
        self.last_usage = {
            "prompt_token_count": prompt_tokens,
            "candidates_token_count": output_tokens,
            "total_token_count": total_tokens,
        }
        print(
            f"[token] girdi(prompt)={prompt_tokens} "
            f"çıktı={output_tokens} toplam={total_tokens}"
        )

    def _is_effectively_empty(self, result: dict) -> bool:
        """Model, metnin CV olmadigini bos/0 ciktiyla sinyalledi mi?

        skills bos VE tum role_scores 0 ise etkin bos sayilir (muhafazakar AND).
        """
        if result.get("skills"):
            return False
        role_scores = result.get("role_scores") or {}
        return all(score == 0 for score in role_scores.values())

    def analyze_cv(self, cv_text: str) -> dict:
        """Ham CV metnini analiz eder; gecersiz girdide InvalidCVError firlatir.

        Katman 1 (API'siz): cok kisa/bos girdi -> InvalidCVError.
        Retry + sema dogrulama: gecici hatada tekrar dener (bkz. CVAnalysisError).
        Katman 2: model CV olmadigini bos ciktiyla sinyallerse -> InvalidCVError.
        """
        # Katman 1: Python uzunluk kontrolu (Gemini cagrilmaz)
        if not cv_text or len(cv_text.strip()) < MIN_CV_TEXT_LENGTH:
            raise InvalidCVError(
                "Girdi cok kisa veya bos; gecerli bir CV olarak analiz edilemez."
            )

        last_error: Exception | None = None
        for attempt in range(1, MAX_ATTEMPTS + 1):
            try:
                result = self._attempt_analysis(cv_text)
            except (json.JSONDecodeError, ValidationError) as output_err:
                # Model bir sonraki denemede duzgun JSON/sema uretebilir; beklemeden dene
                last_error = output_err
                continue
            except Exception as api_err:
                # Gecici API hatasi: artan bekleme sonra tekrar dene
                last_error = api_err
                if attempt < MAX_ATTEMPTS:
                    time.sleep(BACKOFF_BASE_SECONDS * attempt)
                continue

            # Katman 2: model metnin CV olmadigini bos ciktiyla sinyalledi mi?
            if self._is_effectively_empty(result):
                raise InvalidCVError(
                    "Metin bir CV gibi analiz edilemedi (alakasiz belge olabilir)."
                )
            return result

        raise CVAnalysisError(
            f"CV analizi {MAX_ATTEMPTS} denemede başarısız: {last_error}"
        ) from last_error
