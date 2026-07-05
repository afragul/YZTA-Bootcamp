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

NextGenCV

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

## Product Backlog URL
[Miro Backlog Board](https://miro.com/app/board/uXjVH-sutSw=/)

# Sprint 1

 **Sprint Notları:** Bu sprintte projenin çekirdek altyapısı (GitHub reposu, SQLite şeması, sanal ortam) kurulmuş; CV analizi, rol skorlama ve semantik iş eşleştirme (RAG) katmanları geliştirilerek yerel testlerle (CLI + FastAPI mock endpoint) doğrulanmıştır. User Story'ler ID'lendirilmiş ve task'lere bölünmüştür.
- **Sprint içinde tamamlanması tahmin edilen puan:** 100 Puan
  <!-- Not: Toplam Product Backlog puanı 300 olarak belirlenmiş, 3 sprint'e ~100'er puan olacak şekilde dağıtılmıştır. Kendi tahminlerinizle güncelleyin. -->
- **Puan tamamlama mantığı:** Proje boyunca tamamlanması hedeflenen toplam iş yükü **300 puan** olarak tahmin edilmiştir. Bu yük 3 sprint'e eşit ağırlıkta (~100'er puan) bölünmüştür. Sprint 1'de temel altyapı ve çekirdek AI özellikleri (CV analizi, rol skorlama, RAG eşleştirme) önceliklendirilerek hedeflenen 100 puan tamamlanmıştır. Story puanları, sprint toplam puanının yarısını (50) geçmeyecek şekilde tutulmuştur.
- **Backlog düzeni ve Story seçimleri:** Backlog, ilk yapılacak story'lere göre önceliklendirilmiştir. Miro board'da **mavi kartlar User Story'leri**, **kırmızı kartlar ise bu story'lere ait yapılacak işleri (task)** temsil eder. Sprint'e, kapasiteyi aşmayacak şekilde en yüksek değerli story'ler seçilmiştir. Zaman kısıtı nedeniyle canlı web kazıma (scraping) PBI'ları kapsam dışı bırakılıp **Rejected** sütununa taşınmış; onun yerine Excel veri seti üzerinden ChromaDB'ye veri yüklemesi tercih edilmiştir.
- **Tahmini puan tamamlama tablosu (Sprint 1 – Done):**
  | User Story / İş | Puan | Durum |
  |---|---|---|
  | Proje Kurulumu, Altyapı ve Temizlik | 8 | ✅ Done |
  | GitHub Reposu ve Altyapı Kurulumu | 5 | ✅ Done |
  | SQLite ve DB Şemasının Tasarlanması | 8 | ✅ Done |
  | Proje Temizliği ve Bağımlılıkların Birleştirilmesi | 5 | ✅ Done |
  | CV Analiz Modülü | 13 | ✅ Done |
  | Gemini API Entegrasyonu ve Veri Şeması | 13 | ✅ Done |
  | CVAnalysisService ve Testlerin Koşturulması | 13 | ✅ Done |
  | RAG İş Eşleştirme Katmanı | 13 | ✅ Done |
  | Excel Veri Setinin ChromaDB'ye Ingest Edilmesi | 8 | ✅ Done |
  | Semantik İş Arama Algoritmasının Yazılması | 14 | ✅ Done |
  | **Toplam Tamamlanan** | **100** | |

- **Daily Scrum:** Daily Scrum toplantıları zamansal sebeplerden ötürü Slack/WhatsApp üzerinden yürütülmüştür. Örnek konuşma ekran görüntüleri:
  ![Daily Scrum 1](<img width="667" height="724" alt="1" src="https://github.com/user-attachments/assets/4ed8c8ac-83f2-47b8-850c-6ba3642fcd27" />
)
  ![Daily Scrum 2](<img width="672" height="292" alt="2" src="https://github.com/user-attachments/assets/a3adf0fd-2e35-4abf-8018-3854a89cca1e" />
)
  ![Daily Scrum 2](<img width="669" height="556" alt="3" src="https://github.com/user-attachments/assets/1c33e6f7-9337-47a8-b1b4-98551b017b5b" />
)

- **Sprint Board Update:** Sprint 1 board ekran görüntüsü:
 ![Sprint 1 Board](./sprint_board.jpeg)

- **Ürün Durumu:** Uygulamanın Sprint 1 sonundaki durumundan ekran görüntüleri (CLI analiz çıktısı, FastAPI Swagger `/docs`, örnek CV analiz JSON response'u):
  ![Ürün Ekran Görüntüsü 1](ProjectManagement/Sprint1Documents/product_ss1.png)
  ![Ürün Ekran Görüntüsü 2](ProjectManagement/Sprint1Documents/product_ss2.png)



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

