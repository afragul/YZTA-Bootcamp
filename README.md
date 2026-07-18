# Takım İsmi

CodeCrafters

# Ürün İle İlgili Bilgiler

*   Yazılım ve yapay zeka alanında kariyer hedefleyen öğrencilerin ve teknoloji sektörüne yeni adım atan adayların CV'lerini analiz ederek; yazılım, tasarım, yönetim, pazarlama ve insan kaynakları gibi 22 farklı meslek rolüne göre uygunluk puanlaması yapan, gelişim alanlarını (eksikleri) çıkaran, semantik iş ilanlarıyla eşleştirme sunan ve kişiselleştirilmiş öğrenme yolları üreten akıllı kariyer danışmanlığı uygulaması.


## Takım Elemanları

| <div align="center">Name</div>   | <div align="center">Title</div>  | <div align="center">Socials</div>     |
| :---------- | :---------- | :----------: |
| Afragül Tığ     | Product Owner     | [![linkedin](https://github.com/user-attachments/assets/3baa645a-33bc-4786-8327-cb0f92356f0a)](https://www.linkedin.com/in/afragul-tig/)   | 
| Tolga Duy     | Scrum Master     | [![linkedin](https://github.com/user-attachments/assets/3baa645a-33bc-4786-8327-cb0f92356f0a)](https://www.linkedin.com/in/tolga-duy/) |
| Ekin Karıncalı      | Developer      | [![linkedin](https://github.com/user-attachments/assets/3baa645a-33bc-4786-8327-cb0f92356f0a)](https://www.linkedin.com/in/ekin-karıncalı-698844295/)   |
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
  <img width="1114" height="1112" alt="Image" src="https://github.com/user-attachments/assets/83c15df1-bebf-423f-a702-fdc8c460c90d" />
<img width="1217" height="1439" alt="Image" src="https://github.com/user-attachments/assets/429405a0-ab3b-45e7-8fe2-14798c11d93b" />

- **Sprint Board Update:** Sprint 1 board ekran görüntüsü:
<img width="1600" height="1192" alt="Image" src="https://github.com/user-attachments/assets/10f2c705-8283-4df9-bc54-63669a775491" />

- **Ürün Durumu:** Uygulamanın Sprint 1 sonundaki durumundan ekran görüntüleri (CLI analiz çıktısı, FastAPI Swagger `/docs`, örnek CV analiz JSON response'u):
  <img width="942" height="722" alt="Image" src="https://github.com/user-attachments/assets/6d8453a1-9c81-4421-a195-0a5cd0a97eee" />
<img width="394" height="918" alt="Image" src="https://github.com/user-attachments/assets/85208d88-9b21-4127-a730-f9ed1cd456ec" />



*   **Sprint Review:** 
    *   **Alınan Kararlar:** Veritabanı (SQLite) oluşturulması, kullanıcı kaydı ve giriş işlemlerinde e-posta ile toplanacak veriler için gerekli görülmüştür. Fakat bir yandan da CV analiz çıktılarının veritabanında tek tek ayrı sütunlar halinde saklanması yerine `role_scores_json` ve `skills_json` şeklinde JSON formatında saklanması mimariyi sadeleştirmek amacıyla uygun bulunmuştur. Canlı web kazıma (scraping) işlemi zaman kısıtından dolayı elenmiş, onun yerine Excel veri seti üzerinden ChromaDB veri yüklemesi yapılması kesinleştirilmiştir. Bu sebeple canlı scraping PBI'ları kapsam dışı bırakılmıştır. Çıkan ürünün yerel analiz testlerinde (CLI) ve FastAPI mock endpoint testlerinde hiçbir problem görülmemiştir.
    *   **Ekstra Koyulması Gereken Özellikler:** Adayın hedeflerine uygun kaynaklar sunan bir *Akıllı Öğrenme Yolu Agent'ı* ve adayın kendi analizi bağlamında konuşabileceği hafızalı bir *AI Kariyer Koçu Chatbot'u* ek özellikler olarak belirlenmiş ve gelecek sprint iş listesine eklenmiştir.
    *   **Sprint Review Katılımcıları:** Muhammed Behlül Alar, Tolga Duy, Afragül Tığ, Ekin Karıncalı.

*   **Sprint Retrospective**

    *   Sprint 1 çalışmalarımızın ardından ekibimizin gerçekleştirdiği değerlendirme toplantısı sonucunda ortaya çıkan kazanımlar, karşılaşılan zorluklar ve aksiyon planımız şu şekildedir:

###  Neler İyi Gitti? (Başarılar)
*   **Paralel Geliştirme:** API sözleşmesinin (API Contract) ilk günlerde dondurulması ve mock API yanıtlarının hazırlanması sayesinde Frontend (React) ve Backend (FastAPI) ekipleri birbirini beklemeden tamamen bağımsız ve paralel çalışabildi.
*   **Hata Yönetimi ve Çözüm Hızı:** Gemini Developer API'nin `additionalProperties` (dinamik sözlük) kısıtlaması nedeniyle aldığımız hata, `RoleScores` yapısını statik bir Pydantic modeline dönüştürerek hızlıca çözüldü. Bu sayede hem API kısıtlaması aşıldı hem de 22 rolün tamamı için isabetli puanlama garantilendi.
*   **Rol Kapsamının Genişletilmesi:** Başlangıçtaki 5 temel yazılım rolü, veritabanı analizimiz doğrultusunda İK, yönetim, pazarlama ve tasarımı da kapsayan 22 farklı sektörel role çıkartılarak uygulamanın pazar değeri artırıldı.

###  Nelerde Zorlandık / Neler Geliştirilebilir? (Zorluklar)
*   **Klasör ve Mimaride Mükerrerlik:** Dosya yollarının (kök dizin ile `backend` klasörü) çakışması ve aynı şemaların iki farklı dosyada (`schema.py` ve `cv_analysis.py`) tanımlanması kod entegrasyonu aşamasında kafa karışıklığına yol açtı.
*   **Paket Bağımlılıkları Yönetimi:** Proje başlangıcında iki adet `requirements.txt` dosyasının bulunması sanal ortamda sürüm çakışmalarına neden oldu.
*   **Statik Analiz Uyarıları:** Dinamik import yolları (`sys.path.append`) nedeniyle VS Code (Pylance) üzerinde kod editörünün kütüphaneleri tanıyamaması ve sarı hata çizgileri oluşturması geliştirici deneyimini olumsuz etkiledi.

###  Alınan Aksiyonlar ve Çözümler (Action Items)
*   **Mimari Sadeleştirme:** Kök dizindeki mükerrer şema ve servis dosyaları silindi. Tüm servisler ve veri modelleri backend içerisindeki standart klasör yapılarına taşındı.
*   **Bağımlılıkların Birleştirilmesi:** Projeden mükerrer requirements.txt dosyası kaldırılarak kök dizinde tek bir dosya altında birleştirildi ve sanal ortam (`venv`) güncellendi.
*   **VS Code Yapılandırması:** Proje köküne `.vscode/settings.json` dosyası eklenerek editörün importları otomatik çözmesi sağlandı ve tüm statik analiz uyarıları giderildi.
*   **Gelecek Sprint Hedefi:** Dosya yükleme anında tetiklenecek PDF/DOCX metin ayrıştırıcı (parser) servisini yazıp FastAPI ve AI entegrasyonunu tamamlayarak mock akışı canlı akışa dönüştürmek.


# Sprint 2

 **Sprint Notları:** Bu sprintte Sprint 1'de kurulan çekirdek altyapı **mock akıştan canlı akışa** geçirildi. PDF/DOCX ayrıştırıcı (parser) servisi yazıldı, gerçek dosya yükleme (`POST /cv/upload`) ve uçtan uca orkestrasyon (upload → parse → analiz → RAG eşleştirme → DB → tek JSON) tamamlandı. Sprint 1 review'ında gelecek sprint iş listesine eklenen iki ek özellik geliştirildi: **hafızalı AI Kariyer Koçu chatbot'u** (RAG bağlamı + oturum hafızası) ve **Akıllı Öğrenme Yolu Agent'ı** (eksik → adım adım plan). Ayrıca semantik eşleştirme skorları kalibre edilerek demo'da anlamlı yüzdeler elde edildi ve frontend scaffold'u (React + Vite + Tailwind) kuruldu. User Story'ler ID'lendirilip task'lere bölünmüştür.Analiz çekirdeği güvenilir bir servise dönüştürüldü — Gemini'den yapılandırılmış çıktı garantisi (JSON mode + Pydantic şema doğrulama) sağlandı ve geçici API hatalarını şema hatalarından ayıran yeniden deneme/geri çekilme (retry/backoff) mekanizması eklendi; böylece anlık Gemini dalgalanmaları kullanıcıya hata olarak yansımıyor. Eksik analizi hedef role göre keskinleştirildi: gaps artık genel değil, adayın en uygun rollerine etiketli ve somut kanıta dayalı üretiliyor (ör. [devops_engineer] Kubernetes/Terraform deneyimi yok). Edge-case güvenliği getirildi; çok kısa, boş veya alakasız belgeler (tarif/haber vb.) iki katmanlı savunmayla yakalanıp uydurma analiz yerine net "geçersiz CV" sinyali (InvalidCVError) dönüyor. Bu davranışların tamamı Gemini çağırmayan, kota harcamayan offline birim testleriyle güvence altına alındı ve analiz çıktısı şeması (CVAnalysisOutput / RoleScores) dört modül arasındaki dondurulmuş entegrasyon kontratı olarak sabitlendi. Son olarak frontend'de CV analiz sonuç kartları (beceriler, güçlü yönler, rol-etiketli gelişim alanları) canlı backend'e bağlanarak yükle → analiz → panel akışı uçtan uca çalışır hâle getirildi. Rol skorlama katmanı v2'ye taşındı: prompt'a 0–100 aralığını beş banda bölen açık bir skorlama cetveli (0–20 alakasız … 81–100 güçlü aday) eklenerek puanlamanın sezgiyle değil ölçütle verilmesi sağlandı; ayrıca en yüksek 3 rol için CV'den somut kanıt gösteren gerekçe alanı (`top_role_reasons`) şemaya eklendi ve şema ortak kontrat olduğu için `mock_responses.py` aynı PR içinde güncellenerek mock akışın kırılması engellendi. Öğrenme Yolu Agent'ı bu skorlama üzerine kuruldu: hedef rolü kullanıcının seçtiği, ayrı bir `POST /learning-plan` sözleşmesiyle çalışan ve `/cv/upload` cevabına hiç dokunmayan saf bir servis olarak tasarlandı (`build_plan(target_role, gaps, skills) → dict`; servis DB, `cv_id` ve HTTP bilmiyor). `TargetRole` enum'u `RoleScores` ile birebir eşleşecek şekilde 22 role açıldı — böylece kullanıcıya skoru gösterilen her rolün planı üretilebilir hâle geldi ve "55 puan verilip plan üretilememesi" tutarsızlığı ortadan kalktı. Plan üretimi kota gerçeğine göre tembel (lazy) kurgulandı: `rank_roles()` 22 rolü adayın skoruna göre sıralıyor, dashboard yalnızca birinci sıradaki rolün planını otomatik üretiyor, kalan 21 rol "Plan oluştur" butonu arkasında bekliyor — aksi hâlde tek CV yüklemesi 22 Gemini çağrısı anlamına gelirdi. Sprint'in ayırt edici mühendislik çıktısı ise `evals/` kalite ölçüm altyapısı oldu: klasik testler "kod çalışıyor mu" sorusunu yanıtlar, LLM çıktısı her koşuda değiştiği için "çıktı yeterince iyi mi" sorusu ayrı bir ölçüm katmanı gerektirdi. Bu altyapıyla skorlama doğruluğu 5/5 (%100), gerekçe tutarlılığı 15/15 ve plan kalitesi 4/4 senaryoda ölçülerek raporlandı.
- **Sprint içinde tamamlanması tahmin edilen puan:** 100 Puan
  <!-- Not: Toplam Product Backlog puanı 300 olarak belirlenmiş, 3 sprint'e ~100'er puan olacak şekilde dağıtılmıştır. Kendi tahminlerinizle güncelleyin. -->
- **Puan tamamlama mantığı:** Proje boyunca hedeflenen toplam iş yükü **300 puan** olarak tahmin edilmiş ve 3 sprint'e eşit ağırlıkta (~100'er puan) bölünmüştür. Sprint 2'de öncelik, Sprint 1'deki mock akışı canlıya çevirmek (dosya yükleme + parser + orkestrasyon) ve Sprint 1 review'ında karara bağlanan iki ek özelliği (AI Kariyer Koçu + Öğrenme Yolu Agent) hayata geçirmekti; hedeflenen 100 puan tamamlanmıştır. Story puanları, sprint toplam puanının yarısını (50) geçmeyecek şekilde tutulmuştur.
- **Backlog düzeni ve Story seçimleri:** Miro board'da **mavi kartlar User Story'leri**, **kırmızı kartlar ise bu story'lere ait yapılacak işleri (task)** temsil eder. Sprint 2'ye, kapasiteyi aşmayacak şekilde canlı akışı ve ürünün ayırt edici özelliklerini (RAG koç + öğrenme yolu) tamamlayan en yüksek değerli story'ler alınmıştır. Deploy (Docker, Render/Vercel), dataset temizliği/büyütme ve responsive cila işleri **Sprint 3'e** planlanmıştır.
- **Tahmini puan tamamlama tablosu (Sprint 2 – Done):**
  | User Story / İş | Puan | Durum |
  |---|---|---|
  | Dosya Yükleme & Ayrıştırma (Mock → Canlı) | 16 | ✅ Done |
  | `POST /cv/upload` endpoint'i + boyut/tip doğrulama (PDF/DOCX) | 8 | ✅ Done |
  | PDF/DOCX metin ayrıştırıcı servisi (pdfplumber + python-docx) | 8 | ✅ Done |
  | Orkestrasyon & Auth | 21 | ✅ Done |
  | Ana orkestrasyon endpoint'i (upload→parse→analiz→RAG→DB→tek JSON) | 13 | ✅ Done |
  | Auth (JWT kayıt/giriş) + hata yönetimi & loglama | 8 | ✅ Done |
  | AI Kariyer Koçu (Chatbot) | 18 | ✅ Done |
  | `coach_service`: RAG bağlamı + oturum hafızası (bellek-içi) | 13 | ✅ Done |
  | `/chat` + `/chat/session` endpoint'leri | 5 | ✅ Done |
  | Semantik Eşleştirme İyileştirme | 13 | ✅ Done |
  | Skills-damıtılmış sorgu (`build_search_text`) + `match_percent` kalibrasyonu (sigmoid) + relevans testi | 13 | ✅ Done |
  | Akıllı Öğrenme Yolu Agent & Skorlama Kalitesi | 21 | ✅ Done |
  | Skorlama v2: 0–100 skorlama cetveli + `top_role_reasons` gerekçe alanı (+ mock senkronu) | 4 | ✅ Done |
  | `learning_plan.py` şeması: 22 rollük `TargetRole` enum + `LearningPlanOutput` + `RankedRole` | 3 | ✅ Done |
  | Öğrenme yolu agent v1: eksik + hedef rol → haftalık plan (12 kurallı sistem promptu) | 8 | ✅ Done |
  | Kaynak önerisi (tür + somut kaynak + ücret etiketi) + `rank_roles()` lazy plan sıralaması | 3 | ✅ Done |
  | `evals/` kalite ölçüm altyapısı + 503/429 üstel geri çekilmeli retry | 3 | ✅ Done |
  | Frontend Scaffold & Modül İskeletleri | 11 | ✅ Done |
  | React + Vite + Tailwind scaffold + tasarım sistemi + routing | 8 | ✅ Done |
  | 4 sayfa iskeleti (Giriş · CV Yükle · Dashboard · Chat) | 3 | ✅ Done |
  | **Toplam Tamamlanan** | **100** | |

- **Daily Scrum:** Daily Scrum toplantıları zamansal sebeplerden ötürü Slack/WhatsApp üzerinden yürütülmüştür. Örnek konuşma ekran görüntüleri:
<img width="1556" height="375" alt="Image" src="https://github.com/user-attachments/assets/bd8b747c-100a-4c96-947e-f765d109a32d" />
<img width="1527" height="409" alt="Image" src="https://github.com/user-attachments/assets/05742dbe-105e-4a45-bdef-35e7dd9dc366" />
<img width="1125" height="207" alt="Image" src="https://github.com/user-attachments/assets/a08982c2-e122-4dfa-b5de-a56702d56af9" />

- **Sprint Board Update:** Sprint 2 board ekran görüntüsü:


- **Ürün Durumu:** Uygulamanın Sprint 2 sonundaki durumundan ekran görüntüleri:
<img width="600" height="550" alt="Image" src="https://github.com/user-attachments/assets/e1bd6551-733b-4f9b-adcc-ac8bf04ebf35" />
<img width="1192" height="639" alt="Image" src="https://github.com/user-attachments/assets/b7ba6579-4fae-47d6-bb1a-18424a360967" />


*   **Sprint Review:** 
    *   **Alınan Kararlar:** AI Kariyer Koçu'nun oturum hafızası, demo için yeterli görülerek **bellek-içi (in-memory)** tutulmasına karar verildi (sunucu restart'ında sıfırlanır; kalıcı hafıza kapsam dışı bırakıldı). Semantik eşleştirmede ham cosine benzerliği skorları 60–65 bandına sıkıştırdığı için (gemini-embedding'in alakasız baseline'ı ~0.59), sıralama ham skorla korunurken kullanıcıya gösterilen `match_percent`'in **monoton bir sigmoid dönüşümle** (midpoint 0.60) kalibre edilmesine karar verildi; böylece iyi eşleşmeler ~%85–90 okunur hale geldi. Frontend'i tek kişiye yıkmamak için "her modül sahibi kendi arayüzünü yapar" modeli benimsendi. Ortak/dondurulmuş API kontratına (`api_contract.py`) veya çekirdek dosyalara (`main.py`) dokunan her PR'ın merge öncesi **Kişi 1 review'ından** geçmesi kurala bağlandı. Canlı akış (upload → analiz → eşleşme → koç) uçtan uca test edilmiş, blocker bir sorunla karşılaşılmamıştır.
CV analiz çıktısının her koşulda güvenilir olması için, ham json.loads yerine Pydantic şema doğrulaması yapılmasına ve temperature=0.2'nin determinist olmaması ile anlık 429/503 dalgalanmalarına karşı yeniden deneme/geri çekilme (retry/backoff) eklenmesine karar verildi; geçici API hataları artan beklemeyle, şema/JSON hataları ise beklemeden tekrarlanıyor, böylece başarı dönüşünün daima şemaya uygun olması garanti altına alındı. Eksik analizinin (gaps) hedef role göre etiketlenmesi kararlaştırılırken, CVAnalysisOutput dondurulmuş ekip kontratı olduğundan şema tipi değiştirilmedi; rol etiketi ([devops_engineer] ...) prompt düzeyinde tutularak Kişi 1/3/4'ün branch'lerinin bozulmaması sağlandı. Geçersiz/alakasız belge tespiti için şemaya is_cv/confidence alanı eklemek veya ayrı bir "bu bir CV mi?" ön-çağrısı yapmak, ek kota ve gecikme getireceği için bilinçli olarak kapsam dışı bırakıldı; bunun yerine iki katmanlı savunma benimsendi — Python uzunluk kontrolü (MIN_CV_TEXT_LENGTH=40, hiç API çağırmadan kısa girdiyi eler, kota tasarrufu) ve modelin boş çıktı sinyali (InvalidCVError → HTTP 422). "Bu geçerli bir CV mi?" nihai kararı ise bilinçli olarak LLM analizine bırakıldı (parser eşiği 30, analiz eşiği 40 olacak şekilde ayrıştırıldı). Frontend'de "her modül sahibi kendi arayüzünü yapar" modeline uygun olarak CV analiz sonuç kartları (beceriler, güçlü yönler, rol-etiketli gelişim alanları) canlı backend'e bağlandı ve akış uçtan uca doğrulandı.
Öğrenme planında hedef rolün nasıl belirleneceği bir karar noktasıydı: planın en yüksek skorlu role otomatik üretilmesi yerine **hedef rolü kullanıcının seçmesi** ve planın ayrı bir `POST /learning-plan` endpoint'inden dönmesi kararlaştırıldı — böylece "ML CV'si olan ama DevOps'a geçmek isteyen" aday da desteklenmiş oldu ve `/cv/upload` hızlı kalmaya devam etti. `TargetRole` enum'unun başlangıçtaki 5 rolle sınırlı tutulması, skorlamanın 22 rol üretmesiyle çeliştiği için (ör. ML CV'sinde `data_analyst` 55 puanla ilk beşe giriyor ama planı üretilemiyordu) enum `RoleScores` ile birebir eşleşecek şekilde **22 role açıldı**; senkron kayması sessiz bir hataya (422 / skor 0) yol açacağı için `evals/guards/role_sync.py` koruma testi eklendi. Kota gerçeği nedeniyle 22 planın önden üretilmesi bilinçli olarak reddedildi ve **lazy üretim** benimsendi (yalnızca `rank=1` otomatik, kalan 21 rol butonla); tekrar eden isteklerin Gemini'ye gitmemesi için `LearningPlan` tablosuna `(cv_id, target_role)` unique key ile DB cache konulması Kişi 1'den talep edildi. Plan servisinin `temperature=0.4` ile çalışması, aynı hedefe birden fazla geçerli yol bulunduğu için kabul edildi; ancak bunun demo'da tutarsızlık izlenimi yaratmaması adına **demo planının önceden üretilip dondurulmasına** karar verildi. Son olarak, LLM çıktısının kalitesinin göz kararıyla değil ölçümle takip edilmesi için `evals/` altyapısı kuruldu ve dosya adlarının bilerek `test_` öneki almaması kararlaştırıldı (pytest CI'da bunları otomatik toplarsa günlük Gemini kotası yanardı).
    *  **Ekstra Koyulması Gereken Özellikler:** Demo'da zengin sonuç çıkması için iş ilanı dataset'inin temizlenip büyütülmesi, uygulamanın canlıya alınması (backend için Docker + Render/Railway, frontend için Vercel) ve responsive düzen + loading/hata/empty state'ler gelecek (Sprint 3) iş listesine eklendi.
    *  **Sprint Review Katılımcıları:** Muhammed Behlül Alar, Tolga Duy, Afragül Tığ, Ekin Karıncalı.

*   **Sprint Retrospective**
Sprint 2 çalışmalarımızın ardından ekibimizin gerçekleştirdiği değerlendirme toplantısı sonucunda ortaya çıkan kazanımlar, karşılaşılan zorluklar ve aksiyon planımız şu şekildedir:
    
###  Neler İyi Gitti? (Başarılar)
*   **Mock'tan Canlıya Sorunsuz Geçiş:** Sprint 1'de dondurulan API kontratı sayesinde parser, orkestrasyon, koç ve öğrenme yolu servisleri birbirini beklemeden paralel geliştirildi; mock akış uçtan uca canlı akışa problemsiz dönüştürüldü.
*   **Ürünün Ayırt Edici Özellikleri Tamamlandı:** Sprint 1 review'ında karara bağlanan iki ek özellik — hafızalı AI Kariyer Koçu ve Öğrenme Yolu Agent'ı — bu sprintte teslim edildi; ürün artık analizden öteye "danışmanlık" sunuyor.
*   **Anlamlı Eşleşme Skorları:** Skor kalibrasyonu sayesinde demo'da "neden her şey %62?" sorununa düşülmedi; iyi eşleşmeler ~%85–90, alakasızlar %50 altında okunuyor.
*   **Dayanıklı Analiz, Sıfır Hata Sızması:** Pydantic doğrulama + retry/backoff sayesinde Gemini'nin anlık 429/503 dalgalanmaları kullanıcıya hata olarak yansımadı; başarılı dönüşün her zaman şemaya uygun olması garanti altına alındı.
*   **Role Özgü Eksik Analizi:** gaps genel zayıflıklardan çıkarılıp adayın en uygun 3 rolüne etiketli ve somut kanıta dayalı hâle getirildi; bu sayede frontend'deki "Gelişim Alanları" kartı rol rozetleriyle anlamlı okunuyor.
*   **Geçersiz CV'de Uydurma Analizin Önlenmesi:** İki katmanlı savunma (API'siz uzunluk kontrolü + modelin boş-çıktı sinyali) sayesinde alakasız/boş belgeler net "geçersiz CV" (422) dönüyor; demo'da "saçma bir belgeye ciddi analiz üretme" riski ortadan kalktı. Kısa girdiler hiç API'ye gitmeden elenerek kota da korundu.
*   **Ölçülebilir AI Kalitesi (`evals/`):** LLM çıktısı "çalışıyor/çalışmıyor" ile değerlendirilemediği için yetenek bazlı bir ölçüm katmanı kuruldu (`guards/` · `scoring/` · `learning/` · `coach/` · `results/`). Sonuçlar: rol senkronu 22/22/22, skorlama doğruluğu 5/5 (%100), gerekçe tutarlılığı 15/15, plan kalitesi 4/4 senaryo. Bu çıktılar sunumda somut kalite kanıtı olarak kullanılabilir durumda.
*   **Prompt Kalibrasyonunun Ölçümle Doğrulanması:** Eval'ler sayesinde göz kararıyla fark edilemeyecek dört kalite sorunu yakalanıp kapatıldı: uydurma kaynak önerisi (var olmayan bir YouTube kanalı), teknik olmayan rollere (UI/UX, İK) yazılım konusu sızması, 77 saatlik bir plana "uzman/production-ready" gibi aşırı vaat ve aynı kaynağa farklı `resource_type` atanması. Prompt 12 kurala çıkarılarak dördü de düzeltildi ve düzeltmeler yeniden koşularak kanıtlandı.
*   **Kariyer Geçişi Senaryosunun Çalışması:** Backend CV'sinden DevOps planı üretilen senaryoda model, ilgisiz görünen bir eksiği ("frontend deneyimi yok") hedef role köprüleyerek yeniden çerçeveledi (React build çıktılarının S3/CloudFront ile dağıtımı). Ürünün asıl değer önerisi olan "kariyer değiştirici" senaryosu böylece demo'ya hazır hâle geldi.
*   **Sessiz Kırılmalara Karşı Koruma:** `TargetRole` ↔ `RoleScores` ↔ `ROLE_DISPLAY` senkronunu doğrulayan guard testi, Gemini çağrısı yapmadan 1 saniyede çalışıyor; ileride skorlamaya rol eklenip enum'a eklenmezse hata sessizce üretime sızmak yerine testte yakalanacak.


###  Nelerde Zorlandık / Neler Geliştirilebilir? (Zorluklar)
*   **Embedding Skor Dağılımı:** gemini-embedding'in alakasız metinlerdeki baseline'ı ~0.59 olduğu için, ham `(1 - distance) × 100` skorları dar bir 60–65 bandına sıkışıyordu; bu, kalibrasyon yapılmadan demo'da tüm eşleşmeleri birbirine benzer ve "düşük" gösteriyordu.
*   **Import Yolları:** Dinamik embedding import yolları `ModuleNotFoundError`'a yol açtı; `search_jobs.py` ve `ingest_jobs.py` içinde `sys.path` müdahalesi gerekti.
*   **Dataset Dengesizliği:** 22 hedef rol tanımlıyken dataset'te bazı rollere (tasarım, İK, pazarlama vb.) karşılık gelen ilan sayısı çok az; bu rollerde eşleşme kalitesi arz eksikliğinden zayıf kalıyor.
*   **Dosya Sahipliği Sınırları:** Ortak dosyalara (`main.py`, `api_contract.py`) dokunan geliştirmelerde sahiplik sınırlarının netleştirilmesi ve koordinasyon gerekti.
*   **Deterministik Olmayan Çıktının Test Edilebilirliği:** temperature=0.2 olsa da analiz metni (strengths/skills ifadeleri) her koşuda farklı üretiliyor; offline testler içeriği doğrulayamadığı için sahte-client + regresyon güvencesi + canlı göz kontrolü kombinasyonu gerekti. Bu değişkenlik git diff'inde regresyon gibi görünebiliyor.
*   **Structured Output Şema Uyumsuzluğu:** Gemini Developer API, Pydantic'in ürettiği additionalProperties alanını reddediyor; şema response_schema olarak verilmeden önce bu alanın özyinelemeli temizlenmesi gerekti (aynı temizlik öğrenme yolu servisinde de tekrarlandı).
*   **Gemini Kota/Yoğunluk Kısıtı:** Ücretsiz katmandaki günlük kota (429) ve model yoğunluğu (503), canlı uçtan uca analizi zaman zaman engelledi; retry bunu yumuşatsa da demo günü için ayrı kota/anahtar planı gerekiyor.
*   **Enum → String Dönüşüm Tuzağı:** Python 3.12'de `str(TargetRole.DEVOPS_ENGINEER)` ifadesi `"TargetRole.DEVOPS_ENGINEER"` döndürdüğü için, enum doğrudan prompt'a yazıldığında hata alınmıyor ama prompt sessizce bozuluyor ve plan kalitesi düşüyordu; servis girişinde normalizasyon gerekti.
*   **Kotanın Ürün Tasarımını Belirlemesi:** Ücretsiz katmanın günlük ~20 istek sınırı, "22 rolün planını önden üret" gibi kullanıcı deneyimi açısından cazip bir tasarımı teknik olarak imkânsız kıldı; mimari, kalite değil kota kısıtına göre şekillendirilmek zorunda kalındı.
*   **Model Çıktısının Prompt Yazımını Taklit Etmesi:** Sistem promptunda ASCII olarak yazılan `'(ucretsiz)'` etiketi, "düzgün Türkçe yaz" kuralı mevcut olmasına rağmen model tarafından birebir kopyalandı; tırnak içinde verilen literal metnin genel dil kuralını ezdiği görüldü ve prompt'taki tüm örnek metinlerin Türkçe karakterlerle yazılması gerekti.
*   **Otomatik Kalite Kontrolünde Yanlış Pozitif:** Teknik olmayan rollerde yazılım konusu arayan kontrol, `"sql"` ifadesini `"PostgreSQL"` içinde yakalayıp alarm üretti; ayrıca `"backend"` kelimesi, adayın geçmişini anlatan meşru köprü cümlelerinde geçtiği için hatalı işaretlendi. Kontrol, kelime sınırı (`\b`) kullanacak ve yalnızca öğretilen içeriğe (`topic` + `resource_suggestion`) bakacak şekilde yeniden yazıldı.
*   **Plan Çıktısının Deterministik Olmaması:** Aynı CV ve aynı hedef rolle yapılan üç koşuda üç farklı teknoloji yığını üretildi (ECS+CloudFront / Kubernetes+ArgoCD / ECS+Fargate). Üçü de geçerli yollar olsa da bu değişkenlik demo'da tutarsızlık izlenimi yaratma riski taşıyor.
*   **Geliştirme Ortamı Yapılandırması:** `.vscode/settings.json` yalnızca workspace kökünden okunduğu için, repo bir üst klasör üzerinden açıldığında `extraPaths` ayarı devre dışı kalıyor ve Sprint 1'de çözüldüğü varsayılan Pylance uyarıları geliştiricinin makinesinde geri geliyordu.


###  Alınan Aksiyonlar ve Çözümler (Action Items)
*   **Skor Kalibrasyonu:** Sıralama için ham benzerlik korunurken, gösterilen `match_percent` monoton sigmoid (midpoint 0.60, steepness 28) ile kalibre edildi; ayrıca ham CV yerine skills-damıtılmış metinle sorgulanarak skorlar hem yükseldi hem daha iyi ayrıştı.
*   **Geçersiz Girdi Savunması:** Kısa/boş/alakasız belgelere karşı iki katmanlı kontrol eklendi — API'siz uzunluk eşiği (MIN_CV_TEXT_LENGTH=40, kota tasarrufu) ve modelin boş-çıktı sinyali → InvalidCVError (HTTP 422); her iki kontrol de retry döngüsünün dışına konumlandırılarak boşa deneme engellendi.
*   **Frontend Bağlantı Düzeltmesi (IPv6/IPv4):** Analiz sonuç kartları canlı backend'e bağlanırken Windows'ta localhost'un IPv6 (::1) çözülüp uvicorn'un yalnızca IPv4 (127.0.0.1) dinlemesinden kaynaklanan "Failed to fetch" hatası tespit edildi; api.js varsayılan adresi 127.0.0.1'e çekilerek giderildi.
*   **Structured Output Şema Uyumu:** Gemini Developer API'nin reddettiği additionalProperties alanı, şema response_schema olarak verilmeden önce model_json_schema() çıktısından özyinelemeli temizlendi (aynı çözüm öğrenme yolu servisine de uygulandı).
*   **Analiz Dayanıklılığı (Retry + Doğrulama):** analyze_cv'ye 3 denemeli retry döngüsü ve Pydantic şema doğrulaması eklendi; geçici API hataları (429/5xx) artan beklemeyle, JSON/şema hataları beklemeden tekrarlanacak şekilde ayrıştırıldı, nihai başarısızlık tek bir CVAnalysisError'a (→ HTTP 502) dönüştürüldü.
*   **Import Düzeltmesi:** İlgili servis dosyalarına `sys.path` eklenerek embedding import sorunu giderildi.
*   **Demo Odağı:** Demo senaryosu, dataset'te güçlü arz bulunan rollere (Backend / Full Stack / Data / DevOps) odaklandı; dataset temizliği/büyütme işi Sprint 3'e alındı.
*   **Branch & Review Disiplini:** Her iş feature branch + Pull Request akışıyla ilerledi; ortak/dondurulmuş dosyalara dokunan PR'lar için Kişi 1 review'ı zorunlu kılındı (main'e direkt push yok).
*   **Eval Altyapısının Kurulması:** Kök dizinde dağınık duran ölçüm scriptleri `evals/` altında yeteneğe göre gruplandı (`guards/` bedava kontroller · `scoring/` · `learning/` · `coach/` · `results/` üretilen kanıtlar). Tüm yol çözümlemesi tek bir `_paths.py` dosyasına toplandı; böylece klasör yapısı değişirse scriptlere dokunulmayacak. Dosyalar `python -m evals.<klasör>.<script>` ile çalıştırılıyor ve hangi eval'in kaç Gemini çağrısı harcadığı `evals/README.md` içinde belgelendi.
*   **Prompt Kalibrasyonu (12 Kural):** Halüsinasyonu engellemek için yalnızca birinci el/kurumsal kaynak önerme zorunluluğu, teknik olmayan rollerde alan uyumu, verilen `skills` listesi dışında adaya beceri atfetme yasağı, `resource_type` için kesin eşleme kuralı, her kaynağa ücretli/ücretsiz etiketi zorunluluğu ve "uzman/production-ready" gibi aşırı vaat ifadelerinin yasaklanması eklendi; her kural yeniden koşularak doğrulandı.
*   **Öğrenme Yolu Servisine Retry/Backoff:** `errors.APIError` yakalanarak 429 ve 5xx geçici hatalar üstel geri çekilmeyle (10sn → 20sn, jitter'lı) tekrarlanıyor; günlük kota (RPD) aşımı ise beklemenin işe yaramayacağı bir durum olduğu için ayırt edilip anında hata olarak dönülüyor. Gerçek bir koşuda servis iki kez 503 alıp üçüncü denemede planı başarıyla üretti.
*   **Rol Senkron Koruması:** `evals/guards/role_sync.py`, `TargetRole` · `RoleScores` · `ROLE_DISPLAY` listelerini karşılaştırıp uyuşmazlıkta hata veriyor. Gemini çağrısı yapmadığı için PR öncesi rutin kontrol olarak kullanılabiliyor.
*   **Kota Koruması ve Cache:** Plan eval'i üretilmiş çıktıları diskten okuyarak tekrar Gemini'ye gitmiyor; eval dosyaları bilerek `test_` öneki almayarak pytest'in CI'da bunları toplayıp kotayı yakması engellendi. Kotanın demo günü tükenme riskine karşı ödemeli katmana (pay-as-you-go) geçiş yapıldı.
*   **VS Code Yapılandırması (Sprint 1 aksiyonunun tamamlanması):** Repo klasörünün doğrudan workspace olarak açılması ve `extraPaths` listesine `evals/` için `"."` eklenmesiyle kalan Pylance uyarıları giderildi; ayrıca repo içinde kalan kullanılmayan boş bir sanal ortam klasörü silindi.
*   **Gelecek Sprint Hedefi (Sprint 3):** Backend'i Docker + Render/Railway'e, frontend'i Vercel'e deploy edip CORS + prod ayarlarını tamamlamak; iş ilanı dataset'ini temizleyip büyütmek; responsive düzen + loading/hata/empty state'leri eklemek; her modülün dokümantasyonunu yazıp sunumu birlikte hazırlamak. Analiz tarafında token/maliyet optimizasyonu (system prompt'un kısaltılması ve retry'ın günlük kota (RPD) ile dakikalık limiti (RPM) ayırt ederek gereksiz çağrıları azaltması), analiz katmanının dokümantasyonu ve sample_cvs/ PDF'leriyle uçtan uca demo doğrulaması hedefleniyor. Rol skorlama ve öğrenme yolu tarafında Sprint 3 hedefleri: rol skorlarının bar/radar grafiğiyle görselleştirilmesi, öğrenme planının hafta hafta zaman çizelgesi olarak sunulması ve `rank_roles()` çıktısını kullanan rol seçicinin bağlanması (birinci sıradaki rol otomatik yüklü, kalan 21 rol butonla); AI Kariyer Koçu'nun sistem promptunun kalibre edilip `evals/coach/` altında ölçülmesi; demo için kullanılacak öğrenme planının önceden üretilip dondurularak canlı üretim riskinin ortadan kaldırılması; ve skorlama + agent bölümünün teknik dokümantasyonunun yazılması.



# Sprint 3
