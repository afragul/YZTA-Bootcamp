import json
import os
import random
import time

from dotenv import load_dotenv
from google import genai
from google.genai import errors, types

from schemas.learning_plan import LearningPlanOutput, TargetRole

load_dotenv(override=True)

# Rate limit (429) icin yeniden deneme ayarlari
MAX_DENEME = 3          # toplam deneme sayisi
TABAN_BEKLEME_SN = 10   # 1. tekrar 10sn, 2. tekrar 20sn (ustel geri cekilme)

# Prompt ve arayuz icin okunabilir rol adlari.
# 22 rol - TargetRole enum'u ile birebir ayni anahtarlar.
# NOT: Buradaki metinler prompt'a da giriyor. Gemini girdinin dil stilini taklit
# ettigi icin BURASI DUZGUN TURKCE OLMAK ZORUNDA (bkz. sistem promptu kural 10).
ROLE_DISPLAY = {
    # Yazilim gelistirme
    "backend_developer": "Backend Geliştirici",
    "frontend_developer": "Frontend Geliştirici",
    "fullstack_developer": "Full Stack Geliştirici",
    "mobile_developer": "Mobil Geliştirici",
    "devops_engineer": "DevOps Mühendisi",
    "cloud_engineer": "Bulut Mühendisi",
    # Yapay zeka ve veri
    "machine_learning_engineer": "Makine Öğrenmesi Mühendisi",
    "data_scientist": "Veri Bilimci",
    "data_engineer": "Veri Mühendisi",
    "data_analyst": "Veri Analisti",
    "bi_analyst": "İş Zekası Analisti",
    "database_administrator": "Veritabanı Yöneticisi",
    # Guvenlik ve sistem
    "cybersecurity_specialist": "Siber Güvenlik Uzmanı",
    "systems_administrator": "Sistem Yöneticisi",
    # Tasarim
    "ui_ux_designer": "UI/UX Tasarımcı",
    "graphic_designer": "Grafik Tasarımcı",
    # Urun ve yonetim
    "product_manager": "Ürün Yöneticisi",
    "project_manager": "Proje Yöneticisi",
    "business_analyst": "İş Analisti",
    # Pazarlama, IK, musteri
    "digital_marketing_specialist": "Dijital Pazarlama Uzmanı",
    "hr_specialist": "İnsan Kaynakları Uzmanı",
    "customer_success_specialist": "Müşteri Başarı Uzmanı",
}


def rank_roles(role_scores: dict) -> list[dict]:
    """
    Adayin 22 rollük skorlarini siralar ve frontend'in rol secicisini besler.

      - rank=1 (auto=True)      -> dashboard acilinca plani OTOMATIK uretilir
      - rank=2..22 (auto=False) -> "Plan olustur" butonuna basilinca uretilir

    Args:
        role_scores: CV analizinden gelen 22 rollük skor sozlugu

    Returns:
        [{rank, role, display, score, auto}, ...]  skora gore azalan sirada (22 kayit)
    """
    siralanmis = sorted(
        (
            {
                "role": rol.value,
                "display": ROLE_DISPLAY[rol.value],
                "score": role_scores.get(rol.value, 0),
            }
            for rol in TargetRole
        ),
        key=lambda x: x["score"],
        reverse=True,
    )

    for i, item in enumerate(siralanmis, start=1):
        item["rank"] = i
        item["auto"] = i == 1  # SADECE en uygun rolun plani otomatik uretilir

    return siralanmis


class LearningPathService:
    """
    Girdi : hedef rol + adayin eksikleri (gaps) + mevcut becerileri (skills)
    Cikti : haftalara bolunmus, gerekceli, somut kaynakli ogrenme plani (dict)

    Bu servis DB bilmez, cv_id bilmez, HTTP bilmez.
    Kisi 1'in POST /learning-plan endpoint'i tarafindan cagrilir:

        service = LearningPathService()
        plan = service.build_plan(req.target_role, gaps, skills)
    """

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY bulunamadi! Proje kokundeki .env dosyasini kontrol et."
            )
        self.client = genai.Client(api_key=api_key)
        self.model_name = "gemini-3.5-flash"

    @staticmethod
    def _normalize_role(target_role) -> str:
        """
        TUZAK KORUMASI:
        Kisi 1 enum gonderirse (TargetRole.DEVOPS_ENGINEER), f-string bunu
        'TargetRole.DEVOPS_ENGINEER' diye yazar ve prompt bozulur.
        Enum de gelse string de gelse her zaman 'devops_engineer' dondurur.
        """
        if isinstance(target_role, TargetRole):
            return target_role.value
        return str(target_role)

    @staticmethod
    def _gunluk_kota_mi(hata: Exception) -> bool:
        """
        429 iki farkli sey olabilir ve COZUMLERI FARKLI:
          - RPM (dakikalik) asimi -> birkac saniye bekleyince duzelir  -> RETRY ANLAMLI
          - RPD (gunluk) asimi    -> ertesi gune kadar acilmaz         -> RETRY ANLAMSIZ

        Gunluk kota dolduysa bosuna 30 saniye bekletmeyelim, hemen hata verelim.
        Google hata govdesinde 'PerDay' / 'RequestsPerDay' gecirir.
        """
        mesaj = str(hata)
        return "PerDay" in mesaj or "RequestsPerDay" in mesaj

    def _get_clean_schema(self) -> dict:
        """
        Gemini Developer API 'additionalProperties' alanini kabul etmiyor.
        Pydantic semasindan bu alani temizler. (cv_service.py ile ayni yaklasim.)
        """
        schema = LearningPlanOutput.model_json_schema()

        def strip(node):
            if isinstance(node, dict):
                node.pop("additionalProperties", None)
                for value in node.values():
                    strip(value)
            elif isinstance(node, list):
                for item in node:
                    strip(item)
            return node

        return strip(schema)

    def _build_system_instruction(self) -> str:
        # DIKKAT: "teknik mentor" DEGIL. Enum'da IK, tasarim, pazarlama rolleri de var.
        return (
            "Sen deneyimli bir kariyer mentorusun. Adayin HEDEF ROLU, mevcut "
            "BECERILERI ve EKSIKLERI sana verilecek. Gorevin: eksikleri kapatacak, "
            "haftalara bolunmus, adim adim bir ogrenme plani uretmek.\n\n"
            "KURALLAR:\n"
            "1. ALANA UYUM SAGLA: Hedef rol teknik degilse (Insan Kaynaklari, "
            "tasarim, pazarlama, urun/proje yonetimi), O ALANIN kendi araclarina ve "
            "pratiklerine gore plan yap. Yazilim rolu olmayan bir role Docker/SQL "
            "gibi konular ONERME. Orn: IK icin ise alim surecleri ve IK yazilimlari; "
            "tasarim icin Figma ve tasarim sistemleri; pazarlama icin SEO, analitik "
            "ve kampanya araclari.\n"
            "2. MANTIKLI SIRA: Once temel/on kosul olan konudan basla. Bir konu "
            "digerinin on kosuluysa once onu koy (Docker'i ogrenmeden Kubernetes'e "
            "gecme; tasarim ilkelerini ogrenmeden tasarim sistemine gecme).\n"
            "3. TEKRAR ETTIRME: Adayin ZATEN sahip oldugu becerileri plana koyma. "
            "Sadece eksikleri ve hedef rol icin kritik olan konulari isle.\n"
            "4. HER ADIMDA GEREKCE: 'reason' alaninda bu konunun hedef rolde NE ISE "
            "YARADIGINI ve hangi eksigi kapattigini yaz. 'Bu onemlidir' gibi bos "
            "cumle kurma.\n"
            "5. SOMUT KAYNAK: 'resource_suggestion' alaninda gercek bir kaynak veya "
            "proje fikri ver. Orn: 'Docker resmi dokumantasyonu - Get Started', "
            "'Figma Community'den bir dashboard klonlayip yeniden tasarla', "
            "'Google Analytics sertifikasi'. 'Bir kurs al', 'Online kaynaklardan "
            "calis' gibi bos oneri YASAK.\n"
            "6. GERCEKCI YUK: Her hafta 2-4 adim olsun, haftalik toplam sure 10-15 "
            "saati asmasin. Plan toplam 4-8 hafta arasi olsun.\n"
            "7. PRATIK ZORUNLU: Sadece izlemek/okumak yetmez. Planda en az bir tane "
            "'proje' turunde adim OLMALI - is basvurusunda gosterilebilecek somut "
            "cikti (portfolyo parcasi, vaka calismasi, uygulama, kampanya taslagi).\n"
            "8. KARIYER GECISI FARKINDALIGI: Aday hedef rolden uzaksa (mevcut "
            "becerileri baska bir alandaysa), gecisi kopru kurarak planla: once "
            "mevcut becerilerinden hangileri hedef rolde ise yariyor onu belirt, "
            "sonra eksikleri kapat.\n"
            "9. ALAKASIZ EKSIKLERI ELE: Verilen eksiklerden hedef rolle ilgisi "
            "OLMAYANLARI plana koyma. Ancak dolayli olarak ise yariyorsa "
            "(orn: DevOps icin frontend build ciktisinin dagitimi) o acidan "
            "degerlendirebilirsin.\n"
            "10. 'summary' alaninda adayin mevcut durumunu ve bu planin onu nereye "
            "goturecegini 2-3 cumleyle ozetle.\n"
            "11. DIL: Ciktinin TAMAMINI duzgun Turkce yaz. Turkce karakterleri "
            "(ç, ğ, ı, İ, ö, ş, ü) DOGRU kullan: 'guclu' degil 'güçlü', 'ogrenme' "
            "degil 'öğrenme', 'muhendis' degil 'mühendis'. Teknoloji ve urun "
            "adlarini (Docker, PyTorch, AWS, Figma) orijinal haliyle birak."
        )

    def build_plan(self, target_role, gaps: list[str], skills: list[str]) -> dict:
        """
        Hedef role gore kisisellestirilmis ogrenme plani uretir.
        TEK rol icin TEK Gemini cagrisi yapar (429 durumunda yeniden dener).

        Args:
            target_role: TargetRole enum'u VEYA string ("devops_engineer")
            gaps:        CV analizinden gelen eksikler
            skills:      CV analizinden gelen mevcut beceriler

        Returns:
            LearningPlanOutput semasina uygun dict

        Raises:
            ValueError:  target_role 22 rolden biri degilse
            ClientError: 429 (gunluk kota) veya diger API hatalari
        """
        rol_kodu = self._normalize_role(target_role)

        # Savunma: gecersiz rol Gemini'ye hic gitmesin (bosuna token yakma)
        if rol_kodu not in ROLE_DISPLAY:
            raise ValueError(
                f"Gecersiz target_role: '{rol_kodu}'. "
                f"Gecerli roller: {list(ROLE_DISPLAY.keys())}"
            )

        rol_adi = ROLE_DISPLAY[rol_kodu]

        eksikler = "\n".join(f"- {g}" for g in gaps) if gaps else "(belirtilmemis)"
        beceriler = ", ".join(skills) if skills else "(belirtilmemis)"

        contents = (
            f"HEDEF ROL: {rol_adi}\n\n"
            f"ADAYIN MEVCUT BECERILERI:\n{beceriler}\n\n"
            f"ADAYIN EKSIKLERI:\n{eksikler}\n\n"
            f"Bu adayin '{rol_adi}' rolune hazirlanmasi icin haftalara bolunmus, "
            "gerekceli ve somut kaynakli bir ogrenme plani uret."
        )

        # --- Ustel geri cekilme (exponential backoff) ile yeniden deneme ---
        for deneme in range(MAX_DENEME):
            try:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=contents,
                    config=types.GenerateContentConfig(
                        system_instruction=self._build_system_instruction(),
                        response_mime_type="application/json",
                        response_schema=self._get_clean_schema(),
                        temperature=0.4,  # plan yaratici olabilir ama savrulmasin
                    ),
                )
                return json.loads(response.text)

            except errors.ClientError as e:
                kod = getattr(e, "code", None)

                # 429 disindaki hatalar (400 sema hatasi, 404 model yok...) -> hemen firlat
                if kod != 429:
                    print(f"[LearningPathService] API hatasi ({rol_kodu}): {e}")
                    raise

                # 429 ama GUNLUK kota dolmus -> beklemek anlamsiz, hemen firlat
                if self._gunluk_kota_mi(e):
                    print(
                        f"[LearningPathService] GUNLUK KOTA DOLDU ({rol_kodu}). "
                        "Yeniden denemek anlamsiz - kota Pasifik saatiyle gece "
                        "yarisi sifirlanir."
                    )
                    raise

                # 429 dakikalik (RPM) asim -> son deneme degilse bekle ve tekrar dene
                if deneme < MAX_DENEME - 1:
                    bekle = TABAN_BEKLEME_SN * (2 ** deneme)  # 10sn, 20sn
                    bekle += random.uniform(0, 2)  # jitter: es zamanli istekler carpismasin
                    print(
                        f"[LearningPathService] Rate limit (RPM), {bekle:.1f} sn "
                        f"bekleniyor... (deneme {deneme + 1}/{MAX_DENEME})"
                    )
                    time.sleep(bekle)
                    continue

                # Denemeler bitti
                print(
                    f"[LearningPathService] {MAX_DENEME} deneme sonrasi hala rate "
                    f"limit ({rol_kodu})."
                )
                raise

            except Exception as e:
                # Ag hatasi, JSON parse hatasi vb.
                print(f"[LearningPathService] Beklenmeyen hata ({rol_kodu}): {e}")
                raise