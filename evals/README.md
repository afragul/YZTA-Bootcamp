# Evals — AI Kalite Ölçümleri (Kişi 3)

Bu klasör **test değil, eval** içerir: AI çıktısının *doğru* olup olmadığını değil,
**ne kadar iyi** olduğunu ölçer.

> ⚠️ Dosya adları bilerek `test_` ile başlamıyor — pytest bunları otomatik toplayıp
> CI'da çalıştırmasın diye. Çalıştırırsa Gemini kotası yanar.

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
| `guards/role_sync` | **0** | `TargetRole` ↔ `RoleScores` ↔ `ROLE_DISPLAY` senkron mu? |
| `scoring/reasons` | **0** | `top_role_reasons` rol adları/skorları tutuyor mu? |
| `scoring/accuracy` | **5** | ML CV'sine ML Engineer mi en yüksek çıkıyor? |
| `learning/plans` | **4** | Plan kalitesi: sıra, kaynak, proje, Türkçe, teknik sızıntı |

`learning/plans` **cache'li**: `results/learning/plans/` altında dosya varsa
Gemini'ye gitmez. Yeniden üretmek için o dosyaları sil.

## Çıktılar (sunum kanıtları)

- `results/scoring/accuracy.json` — skorlama doğruluğu
- `results/learning/plans/*.json` — üretilen örnek öğrenme planları

## Klasörler

- `guards/` — bedava, hızlı güvenlik kontrolleri
- `scoring/` — Rol Skorlama yeteneği
- `learning/` — Öğrenme Yolu Agent yeteneği
- `coach/` — AI Kariyer Koçu (Hafta 4)
- `results/` — üretilen kanıtlar