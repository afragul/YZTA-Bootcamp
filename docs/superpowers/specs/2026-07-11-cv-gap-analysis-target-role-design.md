# Tasarım: Hedef role göre eksik analizi (gaps)

**Tarih:** 2026-07-11
**Sahip:** Kişi 2 (CV İşleme & AI Analiz)
**Kapsam:** Yalnızca `backend/services/cv_service.py` içindeki prompt. Şemaya dokunmaz; Kişi 1/3/4'e bağlı değildir.

## Amaç

Rehber Kişi 2 – Hafta 4 maddesi "Eksik analizi: hedef role göre eksik beceriler"
şu an yarım: `gaps` alanı üretiliyor ama **genel** — belirli bir role bağlı değil.
Bu tasarım, `gaps`'i adayın en uygun rollerine göre keskinleştirir. Örn. genel
"Docker deneyimi az" yerine `[DevOps Engineer] Kubernetes/Terraform deneyimi CV'de yok`.

## Mevcut durum

`_attempt_analysis` içindeki `system_instruction`, madde 4:
> "4. Adayın güçlü yönlerini (strengths) ve gelişim alanlarını (gaps) net maddeler halinde belirt."

`gaps` şeması: `CVAnalysisOutput.gaps: list[str]` (düz string listesi). Prompt ayrıca
madde 5–6'da 22 rolü 0–100 skorluyor ve madde 7'de en yüksek 3 rolü `top_role_reasons`
olarak gerekçelendiriyor (Kişi 3'ün eklediği bölüm).

## Kararlar

| Karar | Seçim |
|---|---|
| Hedef rol tanımı | Adayın en yüksek 3 `role_scores` rolü (otomatik türetilir) |
| Temsil | `gaps: list[str]` DÜZ kalır; her madde başına rol etiketi (`[Rol Adı] ...`) |
| Değişiklik yüzeyi | Yalnızca prompt (system_instruction madde 4); şema/imza/dönüş değişmez |
| strengths | Dokunulmaz (bu iş sadece eksikler hakkında) |
| Bağımsızlık | Şema değişmediği için Kişi 1/3/4 etkilenmez, haber gerekmez |

## Davranış

`system_instruction` madde 4, şu davranışı isteyecek şekilde güncellenir:

- `strengths`: eskisi gibi genel güçlü yönler.
- `gaps`: adayın **en yüksek skorlu 3 rolü** için (madde 5–6'daki `role_scores` ile aynı
  roller) eksik/zayıf noktalar. Her madde:
  - `[Rol Görünen Adı] eksik veya zayıf nokta` formatında başlar
    (örn. `[Machine Learning Engineer] Üretim ortamında model dağıtımı (MLOps) deneyimi yok`).
  - CV'den **somut kanıta** dayanır (beceri/araç/proje eksikliği); tahmin veya varsayım yok.
  - Rol etiketi `role_scores`/`top_role_reasons`'taki rollerle **tutarlı** olmalı.
- Odak: her rol için en önemli birkaç eksik (rol başına ~1–3 madde); liste kısa ve
  eyleme dönük kalsın, top-3 çıktıyı kalabalıklaştırmasın.

Madde 4 dışındaki prompt bölümleri (skorlama cetveli, top_role_reasons) değişmez.

## Yapı

- Tek dosya: `backend/services/cv_service.py`, `_attempt_analysis` içindeki
  `system_instruction` string'inin 4. maddesi.
- `CVAnalysisOutput` şeması, `analyze_cv`/`_attempt_analysis` imzaları, retry mantığı,
  dönüş tipi (`dict`) — hiçbiri değişmez.

## Bağımsızlık / ekip kontratı

`gaps` tipi `list[str]` olarak korunduğu için `CVAnalysisOutput` (dondurulmuş ekip
kontratı) değişmez. Kişi 1 (orkestrasyon), Kişi 3 (rol skorlama), Kişi 4 (RAG) hiçbir
şekilde etkilenmez. Rol etiketleri Kişi 3'ün `role_scores`'una **dayanır** ama runtime'da
ondan bir şey beklemez (hepsi aynı tek Gemini çağrısında üretilir).

## Doğrulama

Bu bir **prompt kalite** değişikliğidir; içerik LLM'e bağlı ve deterministik değildir.

- **Offline pytest içeriği doğrulayamaz** (testler sahte client kullanıyor). Ancak
  `gaps` tipi değişmediği için mevcut **20 offline test bozulmamalı** — regresyon
  güvencesi olarak yeşil kalmalılar (`_VALID_OUTPUT` ve `test_cv_service.py`
  etkilenmez).
- **Asıl doğrulama canlı `run_cv_tests.py` ile** (kök dizin, canlı Gemini + kota):
  `sample_cvs/*.txt` analiz edilir, `test_results/*.json` içindeki `gaps` maddelerinin
  artık `[Rol Adı] ...` etiketli ve role özgü geldiği göz kontrolüyle teyit edilir.
  Beklenen: her CV için gaps, o CV'nin en yüksek 3 rolüne atıfta bulunur; etiketler
  `role_scores`'taki en yüksek rollerle tutarlıdır.

## Kapsam dışı (YAGNI)

- Edge case'ler (kısa/alakasız/boş belge → güvenli cevap) — ayrı Hafta 4 görevi, ayrı spec.
- `strengths`'i role göre yapılandırmak.
- Yapılandırılmış `role_gaps` alanı / herhangi bir şema değişikliği (bilinçli olarak
  bağımsız kalmak için dışarıda bırakıldı).
- `analyze_cv`'ye `target_role` parametresi eklemek.
