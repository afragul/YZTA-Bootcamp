# Evals — AI Kalite Ölçümleri (Kişi 3)

Bu klasör **test değil, eval** içerir: AI çıktısının *doğru* olup olmadığını değil,
**ne kadar iyi** olduğunu ölçer.

> ⚠️ Dosya adları bilerek `test_` ile başlamıyor — pytest bunları otomatik toplayıp
> CI'da çalıştırmasın diye. Çalıştırırsa Gemini kotası yanar.

| | Test (klasik) | Eval (AI) |
|---|---|---|
| Sorusu | "Kod **çalışıyor** mu?" | "Çıktı **iyi** mi?" |
| Cevap | Kesin: geçti/kaldı | Dereceli: %100 doğru, ±5 tutarlı |
| Maliyet | Bedava, milisaniye | **Gemini çağrısı yakar** |

## Çalıştırma

**Her zaman repo kökünden, `-m` ile:**

```bash
python -m evals.guards.role_sync      # 0 çağrı  💚
python -m evals.scoring.reasons       # 0 çağrı  💚
python -m evals.scoring.accuracy      # 5 çağrı  💸
python -m evals.learning.plans        # 4 çağrı  💸 (cache varsa 0)
```

## Kota uyarısı

Gemini ücretsiz kotası **günlük ~20 istek** (`gemini-3.5-flash`, proje başına).
Kota Pasifik saatiyle gece yarısı sıfırlanır.

| Eval | Çağrı | Ne ölçer |
|---|---|---|
| `guards/role_sync` | **0** 💚 | `TargetRole` ↔ `RoleScores` ↔ `ROLE_DISPLAY` senkron mu? |
| `scoring/reasons` | **0** 💚 | `top_role_reasons`'taki rol adları/skorlar tutuyor mu? |
| `scoring/accuracy` | **5** 💸 | ML CV'sine ML Engineer mi en yüksek çıkıyor? (doğruluk %) |
| `scoring/consistency` | **3** 💸 | Aynı CV N kez → skorlar ne kadar oynuyor? |
| `learning/plans` | **4** 💸 | Plan kalitesi: sıra, kaynak, proje, Türkçe, teknik sızıntı |

`learning/plans` **cache'li**: `results/learning/plans/` altında dosya varsa
Gemini'ye gitmez, diskten okur. **Yeniden üretmek için o JSON'ları sil.**

## Çıktılar (sunum kanıtları)

- `results/scoring/accuracy.json` — skorlama doğruluğu (beklenen vs gerçek)
- `results/scoring/consistency.json` — skor kararlılığı (aynı CV N kez)
- `results/learning/plans/*.json` — 4 senaryolu örnek öğrenme planları

## Klasörler

| Klasör | İçeriği |
|---|---|
| `guards/` | 💚 Bedava, hızlı güvenlik kontrolleri (0 çağrı) |
| `scoring/` | 🔵 Rol Skorlama yeteneğinin eval'leri |
| `learning/` | 🟣 Öğrenme Yolu Agent eval'leri |
| `coach/` | 🟠 AI Kariyer Koçu (Hafta 4'te dolacak) |
| `results/` | 📊 Üretilen kanıtlar — **sunum malzemesi** |
| `_paths.py` | 🔧 Tüm yol ayarları tek yerde |

---

## Bilinen kısıtlar

- **503 UNAVAILABLE** — Google sunucusu yoğun. Servislerde üstel geri çekilmeli
  retry var (10sn → 20sn, 3 deneme). Yine de gelirse birkaç dakika sonra dene.
- **`cv_service.py`'de retry YOK** — 503/429 gelince direkt patlıyor.
  Eval script'lerinde kendi retry'ımız var, ama **canlı üründe risk** (@Kişi2).