# Demo Senaryosu — Rol Skorlama & Öğrenme Yolu (Kişi 3)

Jüri önünde ürünün canlı gösterimi için adım adım senaryo.
Anlatı: **"Backend geliştirici DevOps'a geçmek istiyor."**

> **Neden bu senaryo?** Rakip projeler CV analiz eder. Bizim ürünümüzün ayırt edici
> yanı analizden sonrasını da söylemesi: hangi role geçebilirsin, eksiğin ne, hangi
> sırayla kapatacaksın. Kariyer değişimi senaryosu bunu tek ekranda gösteriyor.

---

## ⚠️ Demo öncesi hazırlık (bunu atlarsan demo çöker)

### 1. Kota kontrolü

Ücretsiz Gemini kotası günlük **~20 istek**. Aşağıdaki hazırlık 2-3 çağrı yakar.
**Demo gününde başka hiçbir eval koşma** — kota biterse ekran hata verir.

### 2. Planı önden üretip cache'e düşür — EN KRİTİK ADIM

Öğrenme planı servisi `temperature=0.4` ile çalışıyor: **aynı CV + aynı rol için her
koşuda farklı (ama geçerli) bir plan üretiyor.** Birinde AWS, diğerinde Azure önerebilir.
Üstüne Gemini'nin 503 hataları biniyor. Yani **jüri önünde canlı plan üretmek kumar.**

Çözüm, sistemde zaten var: `learning_plan_service`, aynı `(analysis_id, target_role)`
için plan varsa Gemini'ye **hiç gitmez**, veritabanından `cached: true` ile döner.

Demodan **en az bir saat önce**, demo makinesinde:

1. `cv_backend.pdf` dosyasını yükle (aşağıdaki akışın 1-3. adımları)
2. Panelde **DevOps Mühendisi** rolüne tıkla → "Plan Oluştur" → plan üretilsin
3. Sayfayı yenile, tekrar DevOps'a tıkla → plan **anında** gelmeli ve
   **"Kayıtlı plan"** notu görünmeli

Üçüncü adımı gördüysen hazırsın: demo sırasında o role tıklamak Gemini'ye gitmeyecek,
prova ettiğinle **birebir aynı** planı gösterecek.

> 🚫 **`backend/data/app.db` dosyasını demo öncesi SİLME.** Cache orada duruyor.
> Silersen hazırlık boşa gider ve demoda canlı üretime düşersin.

### 3. Servisleri ayağa kaldır

```bash
cd backend
uvicorn main:app --reload
```

```bash
cd frontend
npm run dev
```

Tarayıcıyı **geniş pencerede** aç. Panelde 375px'te yatay taşma var (iş eşleşmeleri
kartından kaynaklanıyor); dar pencerede gösterme.

### 4. Yedekleri hazırla

| Yedek | Nerede | Ne zaman kullanılır |
|---|---|---|
| Dondurulmuş plan JSON | `evals/results/learning/plans/cv_backend__devops_engineer.json` | Uygulama hiç açılmazsa "plan böyle görünüyor" diye göster |
| Eval özet tablosu | `evals/results/OZET.md` | Kalite sorusu gelirse |
| Ekran görüntüleri | README Sprint 3 bölümü | Her şey çökerse |

---

## 🎬 Demo akışı (~5 dakika)

### Adım 1 — CV Yükle ekranı  ·  ~15 sn

`/upload` ekranında `sample_cvs/cv_backend.pdf` dosyasını seç.

> *"Elimizde 1,5 yıl deneyimli bir backend geliştiricinin CV'si var. Python, FastAPI,
> Django, Docker, PostgreSQL biliyor."*

**"Analiz et"e bas.**

### Adım 2 — Aşamalı yükleme göstergesi  ·  ~20 sn

Analiz sürerken ekranda CV belgesi üzerinde süzülen tarama ışını ve aşamalar görünür:
dosya doğrulanıyor → CV metni çıkarılıyor → yapay zeka analiz ediyor → iş ilanları
eşleştiriliyor → sonuçlar hazırlanıyor.

**Bu 20 saniyeyi boş geçirme, anlat:**

> *"Burada gösterdiğimiz adımlar süsleme değil — arka planda gerçekten çalışan pipeline'ın
> kendisi. Bilerek yüzde göstermiyoruz: backend tek bir cevap döndürüyor, gerçek ilerlemeyi
> bilemeyiz. Uydurma bir yüzde göstermektense kullanıcıya sadece doğrulayabildiğimizi
> gösteriyoruz — geçen süre ve o an çalışan adım."*

Bu cümle jüriye **mühendislik dürüstlüğü** sinyali verir; not getiren detaylardan biri.

### Adım 3 — Panel: analiz kartları  ·  ~20 sn

Panel açılır. Üstte CV özeti, beceriler, güçlü yönler ve **rol etiketli gelişim alanları**
görünür.

> *"Eksikler genel değil, role etiketli. `[devops_engineer] Kubernetes ve AWS/GCP deneyimi
> yok` diyor — yani hangi eksiğin hangi hedefe engel olduğunu biliyoruz. Birazdan bunu
> kullanacağız."*

### Adım 4 — Rol skorları  ·  ~30 sn

Sol kartta en yüksek 8 rol, skor bandına göre renklendirilmiş barlarla:

| Rol | Skor |
|---|---|
| Backend Geliştirici | **85** |
| DevOps Mühendisi | **50** |
| Veritabanı Yöneticisi | 50 |
| Veri Mühendisi | 45 |
| Bulut Mühendisi | 40 |

> *"22 rol için puanlama yapıyoruz. Puanlar sezgiyle değil, prompt'a koyduğumuz beş bantlı
> bir cetvelle veriliyor: 81-100 güçlü aday, 41-60 temel bilgi var ama pratik kanıt yok.
> Aynı CV'yi beş kez analiz ettik, birinci sıradaki rol beş seferinde de aynı çıktı."*

Aşağıdaki **skor gerekçelerini** göster: en yüksek 3 rol için CV'den somut kanıt
gösteriliyor (FastAPI, Docker, PostgreSQL gibi).

### Adım 5 — İş eşleşmeleri  ·  ~20 sn

Sağ kartta semantik eşleşen ilanlar, yüzdeleriyle.

> *"İlanları anahtar kelimeyle değil, anlamsal olarak eşleştiriyoruz — CV'yi vektöre
> çevirip 247 ilanlık veri tabanında en yakınlarını buluyoruz."*

### Adım 6 — Kariyer değişimi: DevOps planı  ·  ~90 sn — **DEMONUN ZİRVESİ**

Sayfayı aşağı kaydır. Öğrenme Yolu bölümünde birinci sıradaki rolün (Backend Geliştirici)
planı otomatik yüklenmiş durumda.

> *"Birinci sıradaki rolün planını otomatik üretiyoruz. Ama asıl ilginç senaryo şu:
> ya bu kişi backend'de kalmak istemiyorsa?"*

**DevOps Mühendisi butonuna tıkla.** Plan cache'ten anında gelir (`Kayıtlı plan` notu
görünür).

> *"DevOps skoru 50 — yani temeli var ama eksikleri de var. Sistem ona 6 haftalık,
> 18 adımlık bir geçiş planı çıkardı."*

Zaman çizelgesini göstererek anlat:

| Hafta | Odak | Süre |
|---|---|---|
| 1 | CI/CD Temelleri ve GitHub Actions | 11 sa |
| 2 | AWS Bulut Platformu Temelleri | 12 sa |
| 3 | Terraform ile Altyapı Kodlama (IaC) | 12 sa |
| 4 | Konteyner Dağıtımı ve Gelişmiş CI/CD | 13 sa |
| 5 | **Bitirme Projesi** — Altyapı ve Hazırlık | 13 sa |
| 6 | **Bitirme Projesi** — Pipeline ve Canlıya Alım | 14 sa |

Vurgulanacak üç şey:

1. **Köprü kuruyor:** *"Adayın zaten bildiği Docker'ı sıfırdan öğretmiyor, onun üstüne
   Kubernetes ve Terraform koyuyor."*
2. **Proje zorunlu:** Son iki hafta portfolyoda gösterilebilir bir bitirme projesi.
   *"Kurs izlemekle bitmiyor, elle bir şey üretiyor."*
3. **Kaynaklar somut ve etiketli:** Her adımda gerçek kaynak adı ve **(ücretsiz)** /
   **(ücretli)** etiketi var. *"Modelin kaynak uydurmasını engellemek için prompt'a
   yalnızca resmî/birinci el kaynak kuralı koyduk — kişi adı taşıyan YouTube kanalı
   önermesi yasak, çünkü ilk sürümde var olmayan bir kanal uydurmuştu."*

### Adım 7 — AI Kariyer Koçu  ·  ~45 sn

`/chat` ekranına geç. Şu soruyu sor:

> **"Eşleşen ilanlardan hangisi bana en uygun, yüzde kaç?"**

Koç, CV analizi ve eşleşen ilanlar bağlamından cevap verir.

> *"Koç sadece bu adayın kendi verisine dayanarak konuşuyor. Cevaptaki her yüzdenin
> gerçekten bağlamda geçip geçmediğini otomatik olarak denetliyoruz — koçun sayı
> uydurmadığını ölçtük."*

**Vakit varsa** hafızayı da göster:

> **"Peki bu rollerden ikincisi için ilk ne öğrenmeliyim?"**

Koç önceki mesajı hatırlayıp devam eder.

---

## 🛡️ Bir şey ters giderse

| Sorun | Ne yap |
|---|---|
| Plan gelmiyor / hata veriyor | Cache hazırlanmamış demektir. Panic yok: `evals/results/learning/plans/cv_backend__devops_engineer.json` dosyasını aç, *"planın çıktısı bu"* diye göster. |
| İş eşleşmeleri boş | ChromaDB indeksi yok. `cd backend/services && python ingest_jobs.py` — **ama dakikalar sürer**, demo sırasında yapma. Bu bölümü atla, diğerlerine geç. |
| Koç cevap vermiyor | Kota bitmiş olabilir. Chat bölümünü atla; öğrenme yolu zaten demonun zirvesi. |
| Analiz 30 sn'den uzun sürüyor | Yükleme göstergesi zaten *"beklenenden uzun sürüyor"* diyor. Panikleme, o sırada eval sonuçlarından bahset. |
| Uygulama hiç açılmıyor | README Sprint 3 bölümündeki ekran görüntülerine geç. |

---

## 🚫 Demoda YAPMA

- **Yeni bir CV yükleme.** Kota yakar, 20 saniye sürer ve analiz sonucunun ne çıkacağını
  bilmiyorsun.
- **Prova edilmemiş bir role tıklama.** Cache'te yoksa canlı üretime düşer: 10-15 saniye
  bekleme + 503 riski + prova ettiğinden farklı içerik.
- **Dar pencere / mobil görünüm.** Panelde 375px'te yatay taşma var.
- **`app.db` dosyasını silme.** Hazırlıkta ürettiğin cache orada.

---

## Kalite sorusu gelirse

*"AI çıktısının doğru olduğunu nereden biliyorsunuz?"* diye sorulursa —
`evals/results/OZET.md` dosyasını aç:

| Ölçüm | Sonuç |
|---|---|
| Skorlama doğruluğu | 5/5 (%100) |
| Skor kararlılığı | 1. rol 5/5 koşuda sabit, ortalama oynama 4.09 puan |
| Gerekçe tutarlılığı | 9/9 |
| Plan kalitesi | 4/4 senaryo |
| Koç bağlam sadakati | 6/6 |
| Rol senkronu | 22 == 22 == 22 |

> *"Klasik test 'kod çalışıyor mu' der. LLM çıktısı her koşuda değiştiği için ayrı bir
> ölçüm katmanı kurduk: 'çıktı yeterince iyi mi' sorusunu yanıtlayan eval'ler."*

---

## Prova notu

**Bu senaryoyu en az bir kez baştan sona prova et.** Yazılı metin kâğıt üstünde kalırsa
işe yaramaz — provada "burada 20 saniye bekliyoruz, o sırada ne konuşacağım?" gibi
boşluklar ortaya çıkar. Süreleri kendi konuşma hızına göre güncelle.
