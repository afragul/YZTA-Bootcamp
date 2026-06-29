# AI Çekirdek (Kişi 2) Geliştirme Yol Haritası & Proje Durumu

Bu doküman, **AI Destekli Kariyer Asistanı** projesinde **Kişi 2 (AI Çekirdek)** rolünün yaptığı çalışmaları ve önümüzdeki haftalarda yapacağı görevleri takip etmek amacıyla hazırlanmıştır.

---

## 📊 Genel Durum Özeti

| Hafta | Tema | Durum | Açıklama |
| :--- | :--- | :---: | :--- |
| **Hafta 1** | Kurulum, Tasarım & Mock Veri | 🟢 Tamamlandı | Şema ve mock veriler donduruldu, test ortamı hazırlandı. |
| **Hafta 2** | CV Analizi (Prompt v1) | 🟡 Sıradaki | Ham metinden yapılandırılmış veri çıkarma ve doğrulama. |
| **Hafta 3** | Skorlama & Eksik Analizi | ⚪ Beklemede | Rol uygunluk skorları ve gelişim alanlarının analizi. |
| **Hafta 4** | Chat Beyin & İyileştirme | ⚪ Beklemede | Kariyer Koçu sistem promptu ve edge case kontrolleri. |
| **Hafta 5** | Kalite, Dokümantasyon & Sunum | ⚪ Beklemede | Prompt test tabloları ve demo senaryosu hazırlığı. |

---

## 🟢 Hafta 1: Kurulum & API Kontratı (Tamamlandı)
- [x] Masaüstünde `ai_core_module` çalışma klasörünün oluşturulması.
- [x] Pydantic ile veri şemasının tasarlanması ([schema.py](file:///C:/Users/TUF/Desktop/ai_core_module/schema.py)).
- [x] Ekip entegrasyonu için mock veri setinin üretilmesi ([mock_data.json](file:///C:/Users/TUF/Desktop/ai_core_module/mock_data.json)).
- [x] Gemini API bağlantısı için test scriptinin yazılması ([test_prompt.py](file:///C:/Users/TUF/Desktop/ai_core_module/test_prompt.py)).
- [x] Ortam değişkenleri dosyasının yapılandırılması ([.env](file:///C:/Users/TUF/Desktop/ai_core_module/.env)).
- [x] Sanal ortam (`venv`) oluşturulması.
- [x] `.gitignore` dosyasının eklenmesi (güvenli paylaşım için).


---

## 🟡 Hafta 2: CV Analizi & Yapısal Veri (Sıradaki)
- [ ] Kişi 1 (Backend) ile entegre çalışacak LLM servis wrapper'ının yazılması.
- [ ] **Prompt v1 Tasarımı:** CV metninden kişisel bilgiler, eğitim, deneyim ve yetenekleri hatasız ayıklayan promptun hazırlanması.
- [ ] Gemini API **Structured JSON Output** özelliğinin aktifleştirilerek Pydantic şemasıyla eşleştirilmesi.
- [ ] Farklı formatlardaki 5-10 örnek CV üzerinde promptun kararlılığının test edilmesi.

---

## ⚪ Hafta 3: Rol Skorlama & Eksik Analizi
- [ ] **Prompt v2 Tasarımı:** Adayın hedef rollere (ML, Backend, Frontend vb.) 0-100 arası uygunluk skorunun hesaplanması.
- [ ] Belirlenen skorların gerekçelerinin (reasoning) açıklanması.
- [ ] **Eksik Analizi (Gap Analysis):** Adayın seçtiği hedef role göre hangi becerilerde eksik kaldığının ("Docker tecrübesi zayıf" vb.) tespiti.
- [ ] Çıktıların Kişi 1'in ana orkestrasyon API'sine bağlanması.

---

## ⚪ Hafta 4: Chat Beyin & Prompt İyileştirme
- [ ] AI Kariyer Koçu (Chatbot) için sistem promptunun (System Instruction) yazılması.
- [ ] Chatbot'un sadece CV analizi ve RAG'den gelen iş ilanları bağlamında konuşmasının sınırlandırılması.
- [ ] **Edge Case Kontrolleri:** Çok kısa CV, boş/anlamsız yüklemeler veya zararlı girdiler (prompt injection) için koruma katmanları eklenmesi.
- [ ] Token optimizasyonu yapılarak API maliyetlerinin düşürülmesi.

---

## ⚪ Hafta 5: Kalite, Dokümantasyon & Sunum
- [ ] Promptlar için girdi -> beklenen çıktı -> gerçek çıktı tablolarının oluşturulması (Mini Evaluation Table).
- [ ] Geliştirilen promptların ve AI mimarisinin detaylı dokümante edilmesi.
- [ ] Jüri sunumu ve demo senaryosu için "wow" etkisi yaratacak örnek bir CV analiz çıktısının hazırlanması.

---

## 🛠️ Nasıl Çalıştırılır?
1. `.env` dosyasına `GEMINI_API_KEY` değerinizi ekleyin.
2. Bağımlılıkları kurun:
   ```bash
   pip install -r requirements.txt
   ```
3. Test scriptini çalıştırın:
   ```bash
   python test_prompt.py
   ```
