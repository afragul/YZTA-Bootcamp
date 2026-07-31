# Eval Özet Tablosu — AI Kalite Kanıtları (Kişi 3)

Bu dosya, `evals/` altındaki ölçümlerin **tek sayfalık özetidir** — sunumda kalite
kanıtı olarak kullanılmak üzere. Ham çıktılar aynı klasördeki JSON dosyalarında.

> **Neden eval, neden test değil?** Klasik test "kod çalışıyor mu?" sorusunu yanıtlar,
> cevabı kesindir. LLM çıktısı her koşuda değişir; sorulacak soru "çıktı yeterince
> **iyi** mi?"dir — cevabı derecelidir ve ölçülmesi gerekir.

---

## Genel tablo

| # | Yetenek | Eval | Girdi | Beklenen | Gerçek | Sonuç |
|---|---|---|---|---|---|---|
| 1 | Rol Skorlama | `scoring/accuracy` | 5 örnek CV | Her CV'de doğru rol tepede | 5/5 doğru | ✅ **%100** |
| 2 | Rol Skorlama | `scoring/consistency` | Aynı CV × 5 koşu | 1. sıradaki rol değişmesin | 5/5 koşuda aynı | ✅ **sabit** |
| 3 | Rol Skorlama | `scoring/reasons` | Üretilen gerekçeler | Rol adı + skor tutarlı | 9/9 | ✅ **tutarlı** |
| 4 | Öğrenme Yolu | `learning/plans` | 4 senaryo | Proje var, Türkçe, sızıntı yok | 4/4 | ✅ **geçti** |
| 5 | AI Koç | `coach/quality` | 6 prob | Bağlama sadık, uydurma yok | 6/6 | ✅ **%100** |
| 6 | Senkron | `guards/role_sync` | 3 rol tanımı | 22 == 22 == 22 | eşit | ✅ **senkron** |

---

## 1. Skorlama doğruluğu — `scoring/accuracy` (%100)

"ML mühendisi CV'sine gerçekten ML Engineer mi en yüksek çıkıyor?"

| CV dosyası | Beklenen rol | Gerçek (en yüksek) | Skor | Sonuç |
|---|---|---|---|---|
| `cv_backend.txt` | `backend_developer` | `backend_developer` | 90 | ✅ GEÇTİ |
| `cv_frontend.txt` | `frontend_developer` | `frontend_developer` | 95 | ✅ GEÇTİ |
| `cv_devops.txt` | `devops_engineer` | `devops_engineer` | 95 | ✅ GEÇTİ |
| `cv_ml_engineer.txt` | `machine_learning_engineer` | `machine_learning_engineer` | 90 | ✅ GEÇTİ |
| `cv_data_scientist.txt` | `data_scientist` | `data_scientist` | 85 | ✅ GEÇTİ |

**Başarı oranı: %100 (5/5)** · Ham çıktı: `scoring/accuracy.json`

Skorların hepsi 85+ bandında — yani model doğru rolü bulmakla kalmıyor, cetvelin
"güçlü aday" bandında (81-100) konumlandırıyor.

---

## 2. Skor kararlılığı — `scoring/consistency` (sabit)

**Neden kritik?** `rank_roles()` skorlara dayanıyor. Skorlar oynarsa "otomatik plan
üretilen rol" (rank 1) her sayfa yüklemesinde değişir — kullanıcı her açılışta farklı
bir plan görür.

Aynı CV (`cv_ml_engineer.txt`) **5 kez** analiz edildi:

| Ölçüm | Sonuç |
|---|---|
| 1. sıradaki rol sabit mi? | ✅ **Evet** — 5/5 koşuda `machine_learning_engineer` |
| Ortalama oynama | **4.09 puan** |
| En yüksek oynama | **10 puan** |

Rol bazında (ilk 5):

| Rol | 5 koşudaki skorlar | Aralık | Ortalama | Std. sapma |
|---|---|---|---|---|
| `machine_learning_engineer` | 90, 85, 85, 85, 95 | 10 | 88 | 4.0 |
| `data_scientist` | 80, 75, 75, 75, 85 | 10 | 78 | 4.0 |
| `data_analyst` | 55, 55, 50, 55, 55 | 5 | 54 | 2.0 |
| `data_engineer` | 50, 50, 45, 50, 50 | 5 | 49 | 2.0 |
| `backend_developer` | 45, 45, 40, 45, 45 | 5 | 44 | 2.0 |

**Yorum:** Oynama tek bir bandın içinde kalıyor (ör. ML 85-95 → hepsi "güçlü aday"
bandında). Sıralama korunuyor, dolayısıyla `auto=True` rolü kararlı. `temperature=0.2`
tercihi burada karşılığını veriyor.

Ham çıktı: `scoring/consistency.json`

---

## 3. Gerekçe tutarlılığı — `scoring/reasons` (0 Gemini çağrısı 💚)

`top_role_reasons` alanındaki her kayıt için:

| Kontrol | Sonuç |
|---|---|
| `role` adı `role_scores`'taki snake_case adla birebir mi? | ✅ |
| `score` değeri `role_scores`'taki puanla aynı mı? | ✅ |
| `reason` boş değil mi? | ✅ |

**9/9 geçti (3 dosya × 3 gerekçe).** AI'ın gerekçe uydurmadığını (ör. olmayan bir rol adı
yazmak, farklı bir puan söylemek) doğrular. Kayıtlı analiz çıktıları üzerinden çalışır —
**kota harcamaz.**

> ⚠️ **Kapsam notu:** `test_results/` altındaki 5 çıktıdan **2'si** (`cv_devops_result.json`,
> `cv_frontend_result.json`) `top_role_reasons` alanını hiç içermiyor — bunlar alan şemaya
> eklenmeden önce üretilmiş ve yeniden üretilmemiş eski çıktılar. Eval bu iki dosyayı
> sessizce atlamıyor, ayrıca raporluyor. Kapsamı 15 kontrole çıkarmak için
> `python run_cv_tests.py` ile yeniden üretilmeleri gerekir (canlı Gemini, 2 çağrı).

Ham çıktı: `scoring/reasons.json`

---

## 4. Plan kalitesi — `learning/plans` (4/4 senaryo)

Dört senaryo bilinçli seçildi: aynı alanda derinleşme, kariyer değişimi, yan geçiş ve
teknik olmayan role geçiş.

| # | Senaryo | CV → Hedef rol | Süre | Adım | Proje var? | Türkçe? | Teknik sızıntı |
|---|---|---|---|---|---|---|---|
| 1 | Aynı alanda derinleşme | ML → `machine_learning_engineer` | 5 hafta | 14 | ✅ | ✅ | yok |
| 2 | **Kariyer değişimi (demo)** | Backend → `devops_engineer` | 6 hafta | 18 | ✅ | ✅ | yok |
| 3 | Yan geçiş | ML → `data_analyst` | 5 hafta | 10 | ✅ | ✅ | yok |
| 4 | Teknik olmayan role geçiş | Backend → `ui_ux_designer` | 6 hafta | 12 | ✅ | ✅ | yok |

**Otomatik kontroller:**
- **Proje adımı var mı?** (Kural 7) — planda portfolyoda gösterilebilir somut çıktı
  üreten en az bir `proje` adımı olmalı.
- **Türkçe karakter var mı?** (Kural 11) — çıktı `ç, ğ, ı, İ, ö, ş, ü` içeriyor mu;
  yoksa model bozuk Türkçeye kaymış demektir.
- **Teknik sızıntı** — teknik olmayan hedef rollerde (UI/UX) yazılım terimlerinin
  `topic` / `resource_suggestion` alanlarına sızıp sızmadığı.

Ham çıktılar: `learning/plans/*.json` (4 dosya)

**Not:** Senaryo 2 (Backend → DevOps) aynı zamanda **demo planıdır** — canlı üretim
riski (503 + `temperature=0.4` kararsızlığı) almamak için önceden üretilip donduruldu.

---

## 5. AI Koç kalitesi — `coach/quality` (6/6, %100)

Koçun CV analizi + eşleşen ilanlar bağlamına sadık kalıp kalmadığı 6 probla ölçüldü.

| Ölçüm | Sonuç |
|---|---|
| Prob sayısı | 6 |
| Geçen | **6** |
| Başarı oranı | **%100** |
| Mod | canlı (`temperature=0.6`, tek koşu) |

**Kritik kontroller (hepsi geçti):**

| Kontrol | Ne doğrular |
|---|---|
| `turkce` | Cevap Türkçe mi |
| `dolu` | Cevap boş dönmemiş mi |
| `baglam_gercek_kw` | Cevap gerçekten CV bağlamından besleniyor mu |
| `sayi_grounding` | **Uydurma yüzde var mı** — cevaptaki her sayı bağlamda geçmeli |

`sayi_grounding` en değerlisi: koçun "%88 eşleşen ilan" derken bu sayıyı gerçekten
bağlamdan alıp almadığını denetler. Sonuç: **uydurma yüzde `[]` (hiç yok).**

**Yumuşak uyarı (kritik değil):** Bir cevap 225 kelime — sistem promptundaki
"kısa ve net" kuralının sınırında. Bilgi doğru, yalnızca uzun.

Ham çıktı: `coach/quality.json`

---

## 6. Rol senkronu — `guards/role_sync` (0 Gemini çağrısı 💚)

Rol listesi dört ayrı yerde tanımlı. Guard, üç Python nesnesinin eşitliğini doğrular:

```
RoleScores alanları  ==  TargetRole değerleri  ==  ROLE_DISPLAY anahtarları
        22                      22                        22
```

**Neden gerekli?** Skorlamaya rol eklenip enum'a eklenmezse hata **sessizdir** —
`RoleScores` alanlarının `default=0` değeri olduğu için o rol hata vermeden `0` döner,
butonu da sessizce çalışmaz. Guard bunu 1 saniyede, kota harcamadan yakalar.

**Rol düzenleyen her PR'dan önce koşulmalı:**

```bash
python -m evals.guards.role_sync
```

---

## Kota maliyeti (tabloyu yeniden üretmek isteyen için)

| Eval | Çağrı | Komut |
|---|---|---|
| `guards/role_sync` | **0** 💚 | `python -m evals.guards.role_sync` |
| `scoring/reasons` | **0** 💚 | `python -m evals.scoring.reasons` |
| `scoring/accuracy` | 5 💸 | `python -m evals.scoring.accuracy` |
| `scoring/consistency` | 3-5 💸 | `python -m evals.scoring.consistency` |
| `learning/plans` | 4 💸 | `python -m evals.learning.plans` (cache varsa 0) |
| `coach/quality` | 6 💸 | `python -m evals.coach.quality` |
| **Tümü** | **~20** | Günlük ücretsiz kotanın tamamı |

> ⚠️ Ücretsiz kota `gemini-3.5-flash` için günlük ~20 istek. Tabloyu tek oturumda
> baştan üretmek kotanın **tamamını** yakar. `learning/plans` cache'lidir —
> `results/learning/plans/` altındaki JSON'lar silinmedikçe Gemini'ye gitmez.
