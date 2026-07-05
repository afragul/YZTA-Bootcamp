# Takım İsmi

CodeCrafters

# Ürün İle İlgili Bilgiler

*   Yazılım ve yapay zeka alanında kariyer hedefleyen öğrencilerin ve teknoloji sektörüne yeni adım atan adayların CV'lerini analiz ederek; yazılım, tasarım, yönetim, pazarlama ve insan kaynakları gibi 22 farklı meslek rolüne göre uygunluk puanlaması yapan, gelişim alanlarını (eksikleri) çıkaran, semantik iş ilanlarıyla eşleştirme sunan ve kişiselleştirilmiş öğrenme yolları üreten akıllı kariyer danışmanlığı uygulaması.


## Takım Elemanları

| <div align="center">Name</div>   | <div align="center">Title</div>  | <div align="center">Socials</div>     |
| :---------- | :---------- | :----------: |
| Afragül Tığ     | Product Owner     | [![linkedin](https://github.com/user-attachments/assets/3baa645a-33bc-4786-8327-cb0f92356f0a)](https://www.linkedin.com/in/afragul-tig/)   | 
| Tolga Duy     | Scrum Master     | [![linkedin](https://github.com/user-attachments/assets/3baa645a-33bc-4786-8327-cb0f92356f0a)](https://www.linkedin.com/in/tolga-duy/) |
| Ekin Karıncalı      | Developer      | [![linkedin](https://github.com/user-attachments/assets/3baa645a-33bc-4786-8327-cb0f92356f0a)](https://www.linkedin.com/in//)   |
| Muhammed Behlül Alar      | Developer     | [![linkedin](https://github.com/user-attachments/assets/3baa645a-33bc-4786-8327-cb0f92356f0a)](https://www.linkedin.com/in/muhammed-behlül-alar/)    |

## Ürün İsmi

--AI Destekli Kariyer Asistanı--

## Ürün Açıklaması

*   Yazılım ve yapay zeka alanında kariyer hedefleyen öğrencilerin ve yeni adayların CV'lerini analiz ederek en uygun yazılım rollerine göre puanlama yapan, gelişim alanlarını (eksikleri) çıkaran, semantik iş ilanlarıyla eşleştirme sunan ve kişiselleştirilmiş öğrenme yolları üreten akıllı kariyer danışmanlığı uygulaması.

## Ürün Özellikleri

*   **CV Yükleme ve Ayrıştırma:** PDF/DOCX formatındaki öz geçmişlerin taranarak yapısal verilere dönüştürülmesi.
*   **CV Analizi ve Rol Skorlama:** LLM (Gemini/OpenAI) ile adayın yazılım geliştirme, yapay zeka/veri, tasarım, ürün yönetimi, pazarlama ve insan kaynakları gibi 22 farklı sektörel rol için 0-100 arası uygunluk skorunun hesaplanması ve eksik analizi yapılması.
*   **Semantik İş Eşleştirme:** ChromaDB vektör veri tabanı kullanılarak adayın profiline en uygun iş ilanlarının listelenmesi.
*   **Akıllı Öğrenme Yolu (Agent):** Tespit edilen eksiklere göre haftalık/günlük kişiselleştirilmiş kaynak ve ders çalışma planı oluşturulması.
*   **AI Kariyer Koçu (Chatbot):** Adayın kendi CV'si ve analiz raporu bağlamında kariyer tavsiyeleri alabileceği interaktif sohbet robotu.

## Hedef Kitle

*   YZTA (Yapay Zeka Teknoloji Akademisi) mezunları
*   Üniversite öğrencileri (Bilgisayar Mühendisliği, Yazılım vb.)
*   Yazılım sektörüne geçiş yapmak isteyen kariyer değiştiriciler
*   CV'sini güçlendirmek ve eksiklerini kapatmak isteyen junior geliştiriciler


# Sprint 1








*   **Sprint Review:** 
    *   **Alınan Kararlar:** Veritabanı (SQLite) oluşturulması, kullanıcı kaydı ve giriş işlemlerinde e-posta ile toplanacak veriler için gerekli görülmüştür. Fakat bir yandan da CV analiz çıktılarının veritabanında tek tek ayrı sütunlar halinde saklanması yerine `role_scores_json` ve `skills_json` şeklinde JSON formatında saklanması mimariyi sadeleştirmek amacıyla uygun bulunmuştur. Canlı web kazıma (scraping) işlemi zaman kısıtından dolayı elenmiş, onun yerine Excel veri seti üzerinden ChromaDB veri yüklemesi yapılması kesinleştirilmiştir. Bu sebeple canlı scraping PBI'ları kapsam dışı bırakılmıştır. Çıkan ürünün yerel analiz testlerinde (CLI) ve FastAPI mock endpoint testlerinde hiçbir problem görülmemiştir.
    *   **Ekstra Koyulması Gereken Özellikler:** Adayın hedeflerine uygun kaynaklar sunan bir *Akıllı Öğrenme Yolu Agent'ı* ve adayın kendi analizi bağlamında konuşabileceği hafızalı bir *AI Kariyer Koçu Chatbot'u* ek özellikler olarak belirlenmiş ve gelecek sprint iş listesine eklenmiştir.
    *   **Sprint Review Katılımcıları:** Muhammed Behlül Alar, Tolga Duy, Afragül Tığ, Ekin Karıncalı.

*   **Sprint Retrospective**

    *   Sprint 1 çalışmalarımızın ardından ekibimizin gerçekleştirdiği değerlendirme toplantısı sonucunda ortaya çıkan kazanımlar, karşılaşılan zorluklar ve aksiyon planımız şu şekildedir:

### 🟢 Neler İyi Gitti? (Başarılar)
*   **Paralel Geliştirme:** API sözleşmesinin (API Contract) ilk günlerde dondurulması ve mock API yanıtlarının hazırlanması sayesinde Frontend (React) ve Backend (FastAPI) ekipleri birbirini beklemeden tamamen bağımsız ve paralel çalışabildi.
*   **Hata Yönetimi ve Çözüm Hızı:** Gemini Developer API'nin `additionalProperties` (dinamik sözlük) kısıtlaması nedeniyle aldığımız hata, `RoleScores` yapısını statik bir Pydantic modeline dönüştürerek hızlıca çözüldü. Bu sayede hem API kısıtlaması aşıldı hem de 22 rolün tamamı için isabetli puanlama garantilendi.
*   **Rol Kapsamının Genişletilmesi:** Başlangıçtaki 5 temel yazılım rolü, veritabanı analizimiz doğrultusunda İK, yönetim, pazarlama ve tasarımı da kapsayan 22 farklı sektörel role çıkartılarak uygulamanın pazar değeri artırıldı.

### 🔴 Nelerde Zorlandık / Neler Geliştirilebilir? (Zorluklar)
*   **Klasör ve Mimaride Mükerrerlik:** Dosya yollarının (kök dizin ile `backend` klasörü) çakışması ve aynı şemaların iki farklı dosyada (`schema.py` ve `cv_analysis.py`) tanımlanması kod entegrasyonu aşamasında kafa karışıklığına yol açtı.
*   **Paket Bağımlılıkları Yönetimi:** Proje başlangıcında iki adet `requirements.txt` dosyasının bulunması sanal ortamda sürüm çakışmalarına neden oldu.
*   **Statik Analiz Uyarıları:** Dinamik import yolları (`sys.path.append`) nedeniyle VS Code (Pylance) üzerinde kod editörünün kütüphaneleri tanıyamaması ve sarı hata çizgileri oluşturması geliştirici deneyimini olumsuz etkiledi.

### 🚀 Alınan Aksiyonlar ve Çözümler (Action Items)
*   **Mimari Sadeleştirme:** Kök dizindeki mükerrer şema ve servis dosyaları silindi. Tüm servisler ve veri modelleri backend içerisindeki standart klasör yapılarına taşındı.
*   **Bağımlılıkların Birleştirilmesi:** Projeden mükerrer requirements.txt dosyası kaldırılarak kök dizinde tek bir dosya altında birleştirildi ve sanal ortam (`venv`) güncellendi.
*   **VS Code Yapılandırması:** Proje köküne `.vscode/settings.json` dosyası eklenerek editörün importları otomatik çözmesi sağlandı ve tüm statik analiz uyarıları giderildi.
*   **Gelecek Sprint Hedefi:** Dosya yükleme anında tetiklenecek PDF/DOCX metin ayrıştırıcı (parser) servisini yazıp FastAPI ve AI entegrasyonunu tamamlayarak mock akışı canlı akışa dönüştürmek.


# Sprint 2
# Sprint 3

