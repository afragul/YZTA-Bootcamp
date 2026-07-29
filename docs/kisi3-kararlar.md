# Kişi 3 — Karar Günlüğü (Rol Skorlama & Öğrenme Yolu Agent)

Bu dosya, Rol Skorlama ve Öğrenme Yolu modüllerinde **neden böyle yapıldığını** kayda
alır. Kodun *ne* yaptığı `README.md`'deki teknik bölümde; burada yalnızca alternatifleri
elenen kararlar ve gerekçeleri var.

---

## 1. Neden skorlama cetveli? (0-20 / 21-40 / 41-60 / 61-80 / 81-100)

**Sorun:** İlk promptta modele sadece "0-100 arası uygunluk skoru ver" deniyordu. Model
puanı sezgiyle veriyordu; aynı CV'de aynı rol bir koşuda 60, diğerinde 85 alabiliyordu.
Skorun ne anlama geldiği tanımsızdı — "70" iyi mi, orta mı belli değildi.

**Karar:** `system_instruction`'a beş bantlı açık bir cetvel eklendi:

| Bant | Ölçüt |
|---|---|
| 0-20 | CV'de bu rolle ilgili hiçbir kanıt yok |
| 21-40 | Çok dolaylı/zayıf ilişki (sadece genel yetenekler örtüşüyor) |
| 41-60 | Temel bilgi var ama pratik proje/deneyim kanıtı yok |
| 61-80 | İlgili beceriler + en az bir somut proje veya deneyim |
| 81-100 | Rolün çekirdek becerilerinin çoğu + gerçek iş/proje deneyimi |

**Sonuç:** Puan artık sezgiyle değil ölçütle veriliyor. Bu, tutarlılık testinin (bkz. §6)
ön koşuluydu — ölçüt olmadan varyansı ölçmenin anlamı yoktu.

**Yan fayda:** Cetvel frontend'e de sızdı; rol skorları bar grafiğinde bant renkleriyle
gösteriliyor (81+ en koyu → 20 ve altı en açık), yani kullanıcı da aynı ölçütü görüyor.

---

## 2. Neden 22 rolün hepsine değil, sadece en yüksek 3 role gerekçe?

**Sorun:** "Her rol için neden bu skor" gerekçesi istendi. 22 rolün hepsine gerekçe
üretmek iki şeyi bozuyordu:
- **Şema şişmesi:** Çıktı JSON'u 22 × (rol + skor + 1-2 cümle) ile devasa büyüyor,
  token maliyeti ve üretim süresi artıyordu.
- **Değersiz içerik:** "hr_specialist: 10 — CV'de İK deneyimi yok" gibi 19 tane
  bilgisiz satır üretiliyordu. Kullanıcı zaten skoru görüyor.

**Karar:** `top_role_reasons: [{role, score, reason}]` — yalnızca **en yüksek skorlu 3
rol** için gerekçe. Prompt, gerekçenin CV'den somut kanıt (beceri/araç/proje adı)
içermesini zorunlu kılıyor; "Aday bu rol için uygundur" gibi genel geçer cümle yasak.

**Şema ortak kontrat olduğu için:** Alan eklenirken `mock_responses.py` **aynı PR
içinde** güncellendi. Aksi hâlde yeni zorunlu alan mock'ta bulunmayacağı için
`/cv/upload` `ValidationError` ile çökecek ve tüm ekibin frontend'i patlayacaktı.

---

## 3. 5 rol → 22 rol hikâyesi (`TargetRole` enum'u)

**Başlangıç:** Öğrenme planı enum'u 5 rolle sınırlıydı (ML, Backend, Frontend, Data
Scientist, DevOps). Skorlama ise 22 rol üretiyordu.

**Ortaya çıkan tutarsızlık:** ML mühendisi CV'sinde `data_analyst` 55 puanla ilk beşe
giriyor, kullanıcıya bu skor gösteriliyor, ama o role tıklayınca plan üretilemiyordu
(422). Kullanıcıya puan verip planı reddetmek savunulamaz bir davranıştı.

**Karar:** `TargetRole` enum'u, `RoleScores` ile **birebir eşleşecek** şekilde 22 role
açıldı (Kişi 1 onayıyla — endpoint'in kabul ettiği değer kümesini genişlettiği için
ortak sözleşme değişikliğiydi).

**Doğan risk ve önlemi:** Artık rol listesi **dört ayrı yerde** tanımlı:

1. `schemas/cv_analysis.py` → `RoleScores` alanları (skorun JSON şekli)
2. `cv_service.analyze_cv()` içindeki `system_instruction` (22 rolü doldurtan tek şey)
3. `schemas/learning_plan.py` → `TargetRole` enum (planın kabul ettiği roller)
4. `services/learning_service.py` → `ROLE_DISPLAY` (görünen Türkçe adlar)

Senkron kayması **sessiz** bir hataya yol açar: prompt'tan çıkarılan rol hata vermez,
sessizce `0` döner (çünkü `RoleScores` alanlarının `default=0` değeri var, hiçbiri
`required` değil). Bunu yakalamak için `evals/guards/role_sync.py` yazıldı — 0 Gemini
çağrısı, ~1 saniye, `RoleScores` alanları == `TargetRole` değerleri == `ROLE_DISPLAY`
anahtarları eşitliğini doğrular. **Rol düzenleyen her PR'dan önce koşulmalı.**

---

## 4. Neden lazy (tembel) plan üretimi?

**Reddedilen alternatif:** CV yüklenince 22 rolün planını önden üretip hazırda tutmak.

**Neden reddedildi:** Her plan bir Gemini çağrısı ve 10-15 saniye sürüyor.
22 rol × 15 sn ≈ **5,5 dakika** bekleme, üstelik tek bir CV yüklemesi günlük ücretsiz
kotanın (~20 istek) tamamını yakardı.

**Karar — üç katmanlı tembellik:**

1. **`rank_roles(role_scores)`** 22 rolü skora göre sıralar, `rank=1` olana
   `auto=True` verir. Dashboard açılınca **yalnızca bu rolün** planı otomatik üretilir.
2. **Kalan 21 rol** "Plan oluştur" butonu arkasında bekler; kullanıcı istemedikçe
   Gemini'ye gidilmez.
3. **DB cache:** `LearningPlan` tablosuna `(cv_id, target_role)` unique key konması
   Kişi 1'den talep edildi. Kullanıcı roller arasında gidip gelirken aynı plan ikinci
   kez istenirse Gemini'ye hiç gidilmez, DB'den döner (`cached: true`).

Frontend tarafında da aynı mantık üçüncü kez korunuyor: üretilen planlar bileşen
state'inde `{ [rol]: { plan, cached } }` olarak tutuluyor, aynı role dönüldüğünde yeni
istek atılmıyor. Otomatik yükleme `useRef` ile korunuyor — React StrictMode dev'de
effect'leri iki kez çalıştırdığı için bu koruma olmadan her açılışta çift istek giderdi.

---

## 5. Neden hedef rolü kullanıcı seçiyor? (otomatik en yüksek skor değil)

**Karar noktası:** Plan, en yüksek skorlu role otomatik mi üretilsin, yoksa kullanıcı mı
seçsin? Ayrı bir endpoint mi olsun, `/cv/upload` cevabına mı gömülsün?

**Karar:** Kullanıcı seçer + ayrı `POST /learning-plan` endpoint'i, gövde
`{cv_id, target_role}`.

**Gerekçe:**
- **Kariyer değişimi senaryosu:** "ML CV'si olan ama DevOps'a geçmek isteyen" aday, en
  yüksek skorlu role zorlanmamalı. Ürünün ayırt edici değeri tam burada.
- **`/cv/upload` hızlı kalmalı:** Plan üretimi analizden bile uzun sürüyor (10-15 sn).
  Upload cevabına gömülseydi her yükleme bu kadar uzardı.

---

## 6. Rate limit kısıtı ve retry stratejisi

**Ölçülen gerçek:** Ücretsiz kota `gemini-3.5-flash` için **günlük ~20 istek**
(proje başına, Pasifik saatiyle gece yarısı sıfırlanır). Bir kullanıcı akışı =
analiz (1) + plan (1) = **en az 2 çağrı**. Jüri 5 kez denerse kota biter.

**Yaşanan:** Geliştirme sırasında tekrar tekrar 503 ve 429 alındı; bir koşuda servis iki
kez 503 alıp üçüncü denemede planı başarıyla üretti.

**Karar — geçici hata ile kalıcı hatayı ayır:**

```
MAX_DENEME = 3
TABAN_BEKLEME_SN = 10     # 1. tekrar 10sn, 2. tekrar 20sn (üstel) + jitter
```

- `errors.APIError` yakalanır; **429 veya 5xx** ise geçici sayılıp üstel geri çekilmeyle
  tekrarlanır (jitter, eşzamanlı isteklerin aynı anda tekrar denemesini önler).
- **Kritik ayrım:** 429 gelse bile hata gövdesinde `PerDay` / `RequestsPerDay` geçiyorsa
  bu **günlük kota** demektir — beklemek işe yaramaz, saatler sonra sıfırlanacaktır.
  Bu durumda boşuna 30 saniye beklemek yerine anında hata döndürülür.
- Diğer hatalar (4xx şema hataları vb.) hiç tekrarlanmaz; tekrar denemek aynı sonucu
  verir.

**Sıcaklık farkı da bilinçli:**

| Servis | Sıcaklık | Gerekçe |
|---|---|---|
| `cv_service` (skorlama) | `0.2` | Puanlama tutarlı olmalı; aynı CV benzer skor almalı |
| `learning_service` (plan) | `0.4` | Aynı hedefe birden fazla geçerli yol var; plan yaratıcı olabilir ama savrulmamalı |

**Demo riski ve önlemi:** `0.4` sıcaklık, üç koşuda üç farklı (ama geçerli) stack
üretebiliyor. Bu, canlı demoda "kararsız" izlenimi yaratır; üstelik 503 riski de var.
Bu yüzden demo planının **önceden üretilip dosyaya dondurulmasına** karar verildi —
`evals/results/learning/plans/cv_backend__devops_engineer.json` (Backend → DevOps,
kariyer değişimi senaryosu).

---

## 7. Neden `evals/`, neden `test_` öneki yok?

**Ayrım:** Klasik test "kod **çalışıyor** mu?" sorusunu yanıtlar — cevabı kesindir
(geçti/kaldı), bedavadır. LLM çıktısı ise her koşuda değişir; sorulacak soru "çıktı
yeterince **iyi** mi?"dir — cevabı derecelidir ve **Gemini kotası yakar**.

Bu iki şey aynı klasörde durursa biri diğerini bozar: CI'da `pytest` koşulduğunda
eval'ler de toplanır ve günlük kota yanar.

**Karar:**
- Eval'ler `evals/` altında, `guards/` · `scoring/` · `learning/` · `coach/` · `results/`
  şeklinde yeteneğe göre ayrıldı.
- Dosya adları **bilerek** `test_` ile başlamıyor → pytest onları otomatik toplamıyor.
- `python -m evals.x.y` ile çalıştırılıyor (`_paths.py` yolu ayarlıyor).
- Her eval'in **kaç çağrı yaktığı** `evals/README.md`'de tabloyla yazılı; `guards/`
  ve `scoring/reasons` **0 çağrı** (bedava, her PR'da koşulabilir).

---

## 8. Sahte alarm düzeltmeleri (eval'in kendisi de hata yapabilir)

Plan kalite eval'i, teknik olmayan rollerde (UI/UX, İK, pazarlama) "teknik sızıntı"
arıyordu. İki sahte alarm çıktı:

- **`"sql"` → `"PostgreSQL"` içinde eşleşiyordu.** Alt dize araması yerine kelime sınırı
  (`\b`) kullanıldı.
- **`"backend"`** kelimesi, kariyer geçişi köprüsü kuran meşru cümlelerde geçiyordu
  ("mevcut backend deneyimin şu açıdan işine yarar"). Arama yalnızca `topic` ve
  `resource_suggestion` alanlarıyla sınırlandı; `reason` alanı hariç tutuldu.

**Ders:** Eval bir ölçüm aracıdır ve kendisi de kalibre edilmelidir. Kalibre edilmemiş
bir eval, gerçek hataları gizlerken olmayan hataları raporlar.

---

## 9. Prompt kalibrasyonu — tur 2 (gözlenen hatalar → kurallar)

İlk plan çıktıları okunduğunda beş somut sorun görüldü; her biri promptta bir kurala
dönüştü:

| Gözlenen hata | Eklenen kural |
|---|---|
| Var olmayan bir YouTube kanalı uydurdu | **Kural 12:** yalnızca birinci-el/resmî kaynak; şahıs adı taşıyan kanal önerme |
| Aynı kaynağa bir `[video]`, bir `[kurs]` dedi | **Kural 5:** `resource_type` kesin eşleme tablosu |
| Ücretli kaynağı ücretsiz gibi sundu (IxDF) | **Kural 5:** `(ücretsiz)` / `(ücretli)` / `(ücretli olabilir)` etiketi zorunlu |
| "production-ready", "uzman" vaadi verdi | **Kural 10:** aşırı vaat yasağı — 60-80 saatlik plan kimseyi uzman yapmaz |
| CV'de olmayan beceriyi adaya atfetti | **Kural 3:** yalnızca verilen `skills` listesindeki beceriler sayılabilir |

**Ders:** Prompt kuralları baştan tahminle değil, **çıktı okunarak** yazıldı. Her kural
gerçek bir hatanın karşılığı; spekülatif kural eklenmedi.

---

## 10. Türkçe karakter kararı

Model, girdinin dil stilini taklit ediyor. `ROLE_DISPLAY` sözlüğü bozuk Türkçeyle
yazılırsa (`Makine Ogrenmesi Muhendisi`) model çıktının tamamını bozuk Türkçeyle
üretiyordu.

**Karar:** `ROLE_DISPLAY` düzgün Türkçeyle yazıldı (`Makine Öğrenmesi Mühendisi`) ve
promptta **Kural 11** ile Türkçe karakter zorunluluğu açıkça belirtildi; teknoloji ve
ürün adları (Docker, PyTorch, Figma) orijinal hâlinde bırakılıyor.
