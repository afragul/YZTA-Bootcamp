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
<img width="1349" height="1158" alt="SPRİNT 1 BOARD" src="https://github.com/user-attachments/assets/b713e150-6a7b-40f1-9a99-2f58f2e0a75f" />


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

 **Sprint Notları:** Bu sprintte ürün **çalışan bir backend'den kullanılabilir bir uygulamaya** dönüştürüldü. Sprint 2 sonunda backend'in tamamı canlıydı ancak panelde yalnızca CV analiz kartları bağlıydı; bu sprintte kalan üç yetenek — **rol skorları**, **öğrenme yolu** ve **iş eşleşmeleri** — arayüze bağlanarak yükle → analiz → panel → plan → koç akışı uçtan uca tamamlandı. Rol skorlama tarafında en yüksek 8 rol, skor bandına göre renklendirilmiş yatay bar grafiğiyle ve en yüksek 3 rol için CV'den somut kanıt gösteren gerekçelerle sunuldu. Öğrenme Yolu Agent'ının çıktısı hafta hafta düğümlerden oluşan bir zaman çizelgesine dönüştürüldü; `rank_roles()` çıktısını kullanan rol seçici bağlandı ve kota gerçeğine uygun **üç katmanlı tembel yükleme** hayata geçirildi: yalnızca birinci sıradaki rolün planı otomatik üretiliyor, kalan 21 rol buton arkasında bekliyor, üretilen planlar hem veritabanında (`cached: true`) hem bileşen state'inde saklanarak aynı rol ikinci kez istendiğinde Gemini'ye hiç gidilmiyor. Kullanıcı deneyiminde sprintin ayırt edici çıktısı **aşamalı yükleme göstergesi** oldu: Gemini çağrıları 10-25 saniye sürdüğü için pasif bir "Analiz ediliyor…" yazısı uygulamanın donduğu izlenimi veriyordu; bunun yerine backend'in gerçekten yürüttüğü pipeline adımları (dosya doğrulama → metin çıkarma → yapay zeka analizi → RAG eşleştirme → kayıt) kullanıcıya sırayla gösterildi. Backend tek bir HTTP cevabı döndürdüğü için gerçek ilerleme bilinemez; bu nedenle **bilerek yüzde gösterilmedi**, yalnızca gerçek geçen süre sayacı ve o an çalıştığı tahmin edilen adım sunuldu, son adım asla "tamamlandı" işaretlenmedi. AI Kariyer Koçu güvenlik ve kalite açısından sertleştirildi: promptuna **rol kilidi** kuralı eklenerek prompt injection denemelerine direnç kazandırıldı, `chat()` çağrısına 429/5xx için üstel geri çekilmeli yeniden deneme konuldu ve koçun bağlama sadakati altı problu bir eval bataryasıyla ölçüldü. Bu bataryanın en değerli kontrolü **sayı temellendirmesi (number grounding)** oldu: koç "%88 eşleşen ilan" derken bu sayıyı gerçekten bağlamdan alıp almadığı denetlendi ve uydurma yüzde bulunmadı (6/6, %100). Semantik eşleştirme tarafında iş ilanı veri seti 200'den **247 ilana** çıkarılarak 22 hedef rolün tamamında örnek bulunması sağlandı; daha önce hiç ilanı olmayan kategoriler (ör. `digital_marketing_specialist` 0 → 7) dolduruldu, eksik `job_domain` alanları düzeltildi ve tekrar eden kayıt/boş açıklama kontrolü yapıldı — zenginleştirme sonrası örnek CV'lerde en iyi eşleşmeler %94-98 aralığına çıktı. Analiz çekirdeğinde **token/maliyet optimizasyonu** yapıldı: her çağrıda yeniden üretilen yanıt şeması ve sistem talimatı servis başlatılırken bir kez hesaplanacak şekilde önbelleğe alındı, sistem promptu çıktı kalitesini belirleyen kırmızı çizgiler (22 rol listesi, skorlama cetveli, `gaps` biçimi) korunarak yoğunlaştırıldı ve `usage_metadata` üzerinden token kullanımı ölçülebilir hâle getirildi. Son olarak sprintin kalite kanıtları tek bir yerde toplandı: skorlama + agent katmanının teknik dokümantasyonu, tasarım kararlarının gerekçelerini kayda alan bir karar günlüğü ve altı eval'in "girdi → beklenen → gerçek" biçiminde birleştirildiği özet tablo yazıldı.
- **Sprint içinde tamamlanması tahmin edilen puan:** 100 Puan
  <!-- Not: Toplam Product Backlog puanı 300 olarak belirlenmiş, 3 sprint'e ~100'er puan olacak şekilde dağıtılmıştır. -->
- **Puan tamamlama mantığı:** Proje boyunca hedeflenen toplam iş yükü **300 puan** olarak tahmin edilmiş ve 3 sprint'e eşit ağırlıkta (~100'er puan) bölünmüştür. Sprint 3'te öncelik, Sprint 2 review'ında gelecek sprinte bırakılan işlerdi: arayüzün kalan modüllerinin canlı backend'e bağlanması, responsive düzen ve loading/hata/empty state'ler, iş ilanı veri setinin zenginleştirilmesi, token/maliyet optimizasyonu, her modülün dokümantasyonu ve uygulamanın canlıya alınması. Bu işlerin **deploy dışındaki tamamı** teslim edilmiştir.
- **Backlog düzeni ve Story seçimleri:** Miro board'da **mavi kartlar User Story'leri**, **kırmızı kartlar ise bu story'lere ait yapılacak işleri (task)** temsil eder. Sprint 3'e, ürünü demo edilebilir bütünlüğe taşıyan story'ler öncelikle alınmıştır: kullanıcının gördüğü üç eksik modülün bağlanması, uzun AI beklemelerinin yönetilmesi ve kalite kanıtlarının belgelenmesi. Deploy (backend için Docker + Render/Railway, frontend için Vercel) story'si sprint içinde kapatılamamıştır; gerekçesi ve planı aşağıda "Sprint Review" ve "Alınan Aksiyonlar" bölümlerinde açıklanmıştır.
- **Tahmini puan tamamlama tablosu (Sprint 3):**
  | User Story / İş | Puan | Durum |
  |---|---|---|
  | **Rol Skorlama & Öğrenme Yolu Arayüzü** | **21** | ✅ Done |
  | Rol skorları görselleştirmesi: en yüksek 8 rol, skor bandına göre renklendirme + skor gerekçeleri | 5 | ✅ Done |
  | Öğrenme yolu zaman çizelgesi: hafta düğümleri, adım kartları, proje adımı vurgusu | 8 | ✅ Done |
  | Rol seçici (`rank_roles()`) + üç katmanlı tembel yükleme (auto / buton / cache) | 5 | ✅ Done |
  | `POST /learning-plan` arayüz bağlantısı (`getLearningPlan`) + 502 dostu hata mesajı | 3 | ✅ Done |
  | **Kullanıcı Deneyimi: Uzun AI Beklemelerinin Yönetimi** | **8** | ✅ Done |
  | Aşamalı yükleme göstergesi (`AiLoader`): gerçek pipeline adımları + geçen süre sayacı | 5 | ✅ Done |
  | Tarama animasyonu (SVG + CSS, bağımlılıksız) + `prefers-reduced-motion` desteği | 3 | ✅ Done |
  | **AI Kariyer Koçu: Güvenlik & Kalite** | **13** | ✅ Done |
  | Koç promptuna rol kilidi kuralı (prompt injection direnci) | 5 | ✅ Done |
  | `chat()` için 429/5xx üstel geri çekilmeli yeniden deneme | 3 | ✅ Done |
  | Koç kalite eval'i: 6 prob (bağlam sadakati, sayı temellendirmesi, hafıza, injection) → 6/6 | 5 | ✅ Done |
  | **Semantik Eşleştirme: Veri Seti Zenginleştirme** | **13** | ✅ Done |
  | İş ilanı veri seti 200 → 247; 22 rolün tamamında örnek sağlanması, boş kategorilerin doldurulması | 8 | ✅ Done |
  | Veri temizliği (eksik `job_domain`, tekrar eden id / boş açıklama kontrolü) + eşleşme doğrulaması (%94-98) | 5 | ✅ Done |
  | **İş Eşleşmeleri & Chat Arayüzü** | **13** | ✅ Done |
  | İş eşleşmeleri carousel'ı: tek kart + ok navigasyonu + "Tümünü göster" liste görünümü | 5 | ✅ Done |
  | AI Koç chat arayüzü: `/chat/session` ile RAG bağlamlı oturum, `sessionStorage` ile kalıcı hafıza | 8 | ✅ Done |
  | **Analiz Çekirdeği: Token / Maliyet Optimizasyonu** | **11** | ✅ Done |
  | Yanıt şeması ve sistem talimatının servis başlangıcında bir kez hesaplanması (çağrı başına tekrarlı iş kaldırıldı) | 8 | ✅ Done |
  | `usage_metadata` üzerinden token kullanım ölçümü (`last_usage`) | 3 | ✅ Done |
  | **Dokümantasyon & Kalite Kanıtları** | **13** | ✅ Done |
  | Skorlama + agent katmanının teknik dokümantasyonu (README bölümü) | 5 | ✅ Done |
  | Karar günlüğü (`docs/kisi3-kararlar.md`): 10 başlıkta tasarım kararı ve gerekçesi | 5 | ✅ Done |
  | Birleşik eval özet tablosu (`evals/results/OZET.md`): 6 eval, girdi → beklenen → gerçek | 3 | ✅ Done |
  | **Canlıya Alma (Deploy)** | **8** | ⏳ Devam ediyor |
  | Backend Docker + Render/Railway, frontend Vercel, CORS ve prod ortam değişkenleri | 8 | ⏳ Devam ediyor |
  | **Toplam Tamamlanan** | **92** | |
  | **Toplam Planlanan** | **100** | |

- **Daily Scrum:** Daily Scrum toplantıları zamansal sebeplerden ötürü WhatsApp üzerinden yürütülmüştür. Örnek konuşma ekran görüntüleri:
  <img width="581" height="477" alt="image" src="https://github.com/user-attachments/assets/dd8c4f1d-fa56-4f65-9470-38cc1e885e20" />
  <img width="680" height="102" alt="image" src="https://github.com/user-attachments/assets/a0998a7c-b85e-40b4-924c-eda49f56b695" />
  <img width="1136" height="232" alt="image" src="https://github.com/user-attachments/assets/f58b435c-d3bc-4358-860e-cbd20c4b8843" />

- **Sprint Board Update:** Sprint 3 board ekran görüntüsü:
  <img width="1310" height="1192" alt="image" src="https://github.com/user-attachments/assets/e5b78c8e-8348-42f4-a981-306b67e82fb6" />

- **Ürün Durumu:** Uygulamanın Sprint 3 sonundaki durumundan ekran görüntüleri:
<img width="1912" height="908" alt="Ekran görüntüsü 2026-07-31 011411" src="https://github.com/user-attachments/assets/826f3c7b-a809-41a3-81c1-f3e52bd4ca8e" />
<img width="860" height="525" alt="Ekran görüntüsü 2026-07-31 011443" src="https://github.com/user-attachments/assets/caeef999-b9b3-45b5-b324-aaf44b9b9e40" />
<img width="876" height="565" alt="Ekran görüntüsü 2026-07-31 011451" src="https://github.com/user-attachments/assets/32533588-fab7-438d-8126-a9dcac4c2bab" />
<img width="1253" height="791" alt="Ekran görüntüsü 2026-07-31 011522" src="https://github.com/user-attachments/assets/98aa0583-79e7-4bdd-af0b-88cd8312ef4b" />
<img width="1088" height="892" alt="Ekran görüntüsü 2026-07-31 011539" src="https://github.com/user-attachments/assets/307ce398-fb2c-4c30-a077-f9a7b6275a97" />
<img width="1000" height="902" alt="Ekran görüntüsü 2026-07-31 011554" src="https://github.com/user-attachments/assets/9bc291e5-9f80-4da7-b391-3354bf6cab0b" />
<img width="1058" height="857" alt="Ekran görüntüsü 2026-07-31 011606" src="https://github.com/user-attachments/assets/58118008-9682-4ba5-bc38-1c4a357a5bfa" />
<img width="802" height="710" alt="Ekran görüntüsü 2026-07-31 011617" src="https://github.com/user-attachments/assets/78240d58-f3fe-4e55-8c45-9fe800c0b415" />
<img width="717" height="716" alt="Ekran görüntüsü 2026-07-31 011753" src="https://github.com/user-attachments/assets/df3fbb2c-210b-4e86-9c15-70b79d32a924" />
<img width="701" height="672" alt="Ekran görüntüsü 2026-07-31 011809" src="https://github.com/user-attachments/assets/b4a37c79-c857-4cd4-ad36-112a874cb767" />
<img width="712" height="682" alt="Ekran görüntüsü 2026-07-31 011818" src="https://github.com/user-attachments/assets/1be8df05-780d-49fc-b60f-3e363686943b" />

*   **Sprint Review:**
    *   **Alınan Kararlar:** Öğrenme planı üretiminin kota maliyeti nedeniyle **tembel (lazy) yükleme** kalıcı mimari karar olarak benimsenmiştir; 22 rolün planını önden üretmek tek CV yüklemesinde günlük ücretsiz kotanın tamamını yakacağı için reddedilmiştir. Uzun AI beklemelerinde kullanıcıya **yüzdeli ilerleme çubuğu gösterilmemesi** kararlaştırılmıştır: backend tek bir HTTP cevabı döndürdüğü için gerçek ilerleme bilinemez ve uydurma bir yüzde kullanıcıyı yanıltır; bunun yerine gerçek pipeline adımları ve gerçek geçen süre gösterilmektedir. Demo'da öğrenme planının **canlı üretilmemesi**, önceden üretilip dondurulmuş planın kullanılması kararlaştırılmıştır (plan servisi `temperature=0.4` ile çalıştığı için aynı hedefe farklı geçerli yollar üretebiliyor ve 503 riski bulunuyor). Deploy story'si, backend tarafında CORS'un ortam değişkenine taşınmasını ve kalıcı depolama (SQLite veritabanı + yüklenen dosyalar) çözümünü gerektirdiği için sprint içinde kapatılamamış, Sprint 3 sonrası ilk iş olarak planlanmıştır.
    *   **Ürün Bütünlüğü:** Sprint 3 sonunda kullanıcı akışının tamamı çalışır durumdadır: CV yükleme → analiz → panel (analiz kartları + rol skorları + iş eşleşmeleri) → hedef rol seçimi → öğrenme planı → AI koç sohbeti. Offline birim testleri 23/23 geçmekte, rol senkron guard'ı 22/22/22 doğrulamaktadır.
    *   **Sprint Review Katılımcıları:** Muhammed Behlül Alar, Tolga Duy, Afragül Tığ, Ekin Karıncalı.

*   **Sprint Retrospective**

    *   Sprint 3 çalışmalarımızın ardından ekibimizin gerçekleştirdiği değerlendirme toplantısı sonucunda ortaya çıkan kazanımlar, karşılaşılan zorluklar ve aksiyon planımız şu şekildedir:

###  Neler İyi Gitti? (Başarılar)
*   **Ürün Uçtan Uca Tamamlandı:** Sprint 2'de backend'in tamamı canlı olmasına rağmen panelde yalnızca analiz kartları bağlıydı. Bu sprintte kalan üç modül (rol skorları, öğrenme yolu, iş eşleşmeleri) bağlanarak ürün ilk kez baştan sona kullanılabilir hâle geldi.
*   **Beklemenin Anlamlı Hâle Getirilmesi:** 10-25 saniyelik Gemini beklemeleri, backend'in gerçek pipeline adımlarını gösteren aşamalı bir göstergeyle yönetildi. Kullanıcı artık "uygulama dondu mu?" diye düşünmüyor, sistemin ne yaptığını görüyor.
*   **Dürüst Arayüz Kararı:** Gerçek ilerleme bilinemediği için sahte yüzde göstermek yerine yalnızca doğrulanabilir bilgi (gerçek geçen süre + gerçek pipeline adımları) sunuldu. Son adım hiçbir zaman "tamamlandı" işaretlenmedi.
*   **Ölçülmüş Koç Güvenliği:** Prompt injection direnci ve bağlam sadakati göz kararıyla değil eval'le doğrulandı. Sayı temellendirmesi kontrolü, koçun bağlamda olmayan bir yüzde uydurmadığını kanıtladı (6/6).
*   **Veri Seti Kapsamının Tamamlanması:** İş ilanı veri seti 22 hedef rolün **tamamını** kapsayacak şekilde genişletildi; daha önce hiç ilanı olmayan roller için "skor veriliyor ama eşleşme gelmiyor" tutarsızlığı ortadan kalktı.
*   **Maliyet Bilinci:** Analiz çekirdeğinde çağrı başına tekrarlanan şema/prompt üretimi kaldırılıp token kullanımı ölçülebilir hâle getirilerek kota tüketimi kontrol altına alındı.

###  Nelerde Zorlandık / Neler Geliştirilebilir? (Zorluklar)
*   **Günlük Kota Sınırı:** `gemini-3.5-flash` ücretsiz kotasının günlük ~20 istekle sınırlı olması, canlı eval koşularını ve arayüz testlerini ciddi biçimde yavaşlattı. Bir kullanıcı akışı bile en az iki çağrı (analiz + plan) tükettiği için geliştirme sırasında sık sık kota beklendi.
*   **Deploy Bağımlılık Zinciri:** Canlıya alma tek bir işten ibaret değil: CORS'un ortam değişkenine taşınması, kalıcı depolama (ücretsiz host'lar diski her yeniden başlatmada siliyor) ve ChromaDB indeksinin sunucuda yeniden kurulması gerekiyor. Bu zincir sprint sonuna sığmadı.
*   **Paylaşılan Frontend Dosyalarında Çakışma:** `Dashboard.jsx` ve `api.js` üç kişinin birden dokunduğu dosyalar olduğu için merge çakışmaları yaşandı; her iki tarafın katkısını koruyacak şekilde elle birleştirme gerekti.
*   **Tarayıcı Testinde Kota Tüketimi:** Arayüz durumlarını (yükleniyor / hata / boş) gerçek isteklerle denemek kotayı hızla tükettiği için testlerin sahte cevaplarla yapılması gerekti.

###  Alınan Aksiyonlar ve Çözümler (Action Items)
*   **Üç Katmanlı Cache:** Aynı planın tekrar tekrar üretilmesini önlemek için veritabanında `(cv_id, target_role)` cache'i, bileşen state'inde plan saklama ve `useRef` ile tek seferlik otomatik yükleme birlikte uygulandı; böylece rol seçiciyle gezinirken Gemini'ye hiç ek istek gitmiyor.
*   **Sahte Cevapla Arayüz Testi:** Yükleme/hata/boş durumları kota harcamadan doğrulamak için tarayıcıda geçici sahte cevaplar kullanıldı; aşama ilerlemesi, hizalama ve 375px davranışı bu yolla ölçülerek doğrulandı.
*   **Paylaşılan Dosyalarda Minimum Müdahale:** `Dashboard.jsx` gibi ortak dosyalarda değişiklik yalnızca bileşen bağlama satırlarıyla sınırlı tutuldu; her modülün mantığı kendi bileşen dosyasında toplandı.
*   **Kalite Kanıtlarının Tek Yerde Toplanması:** Dağınık eval çıktıları `evals/results/OZET.md` altında tek tabloya indirildi; her ölçümün kaç Gemini çağrısı yaktığı da belgelenerek kota koruması sağlandı.
*   **Sprint Sonrası İlk İş — Canlıya Alma:** Deploy zincirinin sırası netleştirildi: (1) CORS'un `ALLOWED_ORIGINS` ortam değişkenine taşınması, (2) backend için Dockerfile + Render/Railway servisi, (3) kalıcı depolama (Postgres veya persistent disk), (4) sunucuda ChromaDB indeksinin kurulması, (5) frontend için `vercel.json` (SPA yönlendirmesi) ve `VITE_API_URL` ile Vercel dağıtımı.
*   **Kota Riskine Karşı Önlem:** Demo ve jüri sunumu sırasında kotanın tükenmemesi için ücretli katmana geçiş veya demo verisinin önceden üretilip dondurulması kararlaştırıldı.

---

# Teknik Dokümantasyon — Rol Skorlama & Öğrenme Yolu Agent

> Bu bölüm modülün **nasıl çalıştığını** anlatır. *Neden böyle tasarlandığı*
> (elenen alternatifler, gerekçeler) ayrı bir karar günlüğünde:
> [`docs/kisi3-kararlar.md`](docs/kisi3-kararlar.md).
> Kalite ölçümlerinin özeti: [`evals/results/OZET.md`](evals/results/OZET.md).

Modül üç yetenekten oluşur: **(1) Rol Skorlama**, **(2) Öğrenme Yolu Agent'ı**,
**(3) AI Kariyer Koçu sistem promptu**. Üçü de `gemini-3.5-flash` kullanır.

## 1. Rol Skorlama

CV metnini 22 meslek rolüne göre 0-100 arası puanlar ve en yüksek 3 rol için
gerekçe üretir.

**Kod:** `backend/services/cv_service.py` · **Şema:** `backend/schemas/cv_analysis.py`

**Çıktı sözleşmesi (`CVAnalysisOutput`):**

| Alan | Tip | Açıklama |
|---|---|---|
| `role_scores` | `RoleScores` | 22 rolün her biri için 0-100 tam sayı |
| `top_role_reasons` | `RoleReason[]` | En yüksek 3 rol: `{role, score, reason}` |
| `gaps` | `string[]` | Rol etiketli eksikler: `"[devops_engineer] Kubernetes deneyimi yok"` |
| `skills`, `strengths`, `experience_years`, `education` | — | Kişi 2'nin analiz alanları |

**Skorlama cetveli** — puan sezgiyle değil, prompt'taki bu ölçütle verilir:

| Bant | Anlam | Ölçüt |
|---|---|---|
| 81-100 | Güçlü aday | Çekirdek becerilerin çoğu + gerçek iş/proje deneyimi |
| 61-80 | Uygun | İlgili beceriler + en az bir somut proje/deneyim |
| 41-60 | Geliştirilebilir | Temel bilgi var, pratik kanıt yok |
| 21-40 | Zayıf | Çok dolaylı ilişki, sadece genel yetenekler örtüşüyor |
| 0-20 | Alakasız | CV'de bu rolle ilgili kanıt yok |

Bu bantlar frontend'e de yansır: rol skorları bar grafiğinde bant renkleriyle gösterilir
(81+ en koyu → 20 ve altı en açık).

**Teknik notlar:**
- `temperature=0.2` — puanlamanın tutarlı olması için düşük tutuldu.
  Ölçülen kararlılık: aynı CV 5 koşuda ortalama **4.09 puan** oynuyor, 1. sıradaki rol
  **5/5 koşuda sabit** kaldı.
- `MAX_ATTEMPTS = 3` — çağrı/JSON parse/şema doğrulama hataları için yeniden deneme.
- Structured output: `CVAnalysisOutput` şeması Gemini'ye `response_schema` olarak
  verilir. Gemini Developer API `additionalProperties` alanını reddettiği için şema
  `_get_clean_schema()` ile özyinelemeli temizlenir.

> ⚠️ **Sessiz kırılma tuzağı:** `RoleScores` alanlarının `default=0` değeri var,
> dolayısıyla şemada **hiçbiri `required` değil**. 22 rolü gerçekten doldurtan tek şey
> prompt'un kapanış cümlesidir. Bir rolü prompt metninden çıkarırsanız hata **vermez**,
> sessizce `0` döner.

## 2. Öğrenme Yolu Agent'ı

Hedef rol + eksikler → hafta hafta, kaynaklı, gerekçeli çalışma planı.

**Kod:** `backend/services/learning_service.py` (saf Gemini) +
`backend/services/learning_plan_service.py` (orkestrasyon)
**Şema:** `backend/schemas/learning_plan.py` · **Endpoint:** `POST /learning-plan`

**Katman ayrımı:** `LearningPathService` DB, HTTP veya `cv_id` bilmez —
`build_plan(target_role, gaps, skills) → dict` imzasıyla saf bir servistir.
DB'den okuma, cache kontrolü ve `cv_id` çözümleme `learning_plan_service.py`'nin işidir.

**İstek / cevap:**

```jsonc
// POST /learning-plan
{ "cv_id": "uuid", "target_role": "devops_engineer" }

// Cevap
{
  "cv_id": "uuid", "target_role": "devops_engineer",
  "cached": false,                    // true → DB'den geldi, Gemini'ye gidilmedi
  "plan": {
    "summary": "...", "total_weeks": 6,
    "weeks": [{
      "week": 1, "focus": "Haftanın ana odağı",
      "steps": [{
        "order": 1, "topic": "Docker temelleri",
        "reason": "Bu adım neden gerekli...",
        "resource_type": "dokumantasyon",     // kurs · dokumantasyon · video · kitap · proje
        "resource_suggestion": "Docker resmî dokümantasyonu (ücretsiz)",
        "estimated_hours": 6
      }]
    }]
  }
}
```

**12 kurallı sistem promptu** — her kural gözlenen bir hatanın karşılığıdır:

| # | Kural | Ne sağlar |
|---|---|---|
| 1 | Alana uyum | Teknik olmayan rolde (İK, tasarım) yazılım terimi geçmez |
| 2 | Mantıklı sıra | Ön koşul konu önce gelir |
| 3 | Tekrar/uydurma yasağı | Adayın sahip olduğu beceri plana konmaz; **verilen `skills` dışında beceri atfedilemez** |
| 4 | Gerekçe zorunlu | Her adımda "bu ne işe yarar" |
| 5 | Somut kaynak + doğru tip | Tek kaynak, `resource_type` kesin eşleme, **`(ücretsiz)`/`(ücretli)` etiketi zorunlu** |
| 6 | Gerçekçi yük | Haftada 2-4 adım, 10-15 saat; plan 4-8 hafta |
| 7 | Proje zorunlu | En az bir **portfolyoda gösterilebilir** çıktı |
| 8 | Kariyer geçişi köprüsü | Mevcut becerilerden hangisi işe yarıyor, önce o |
| 9 | Eksikleri öneme göre sırala | Çekirdek eksik önce, alakasız olan hiç |
| 10 | Gerçekçi özet | "production-ready", "uzman" **yasak** |
| 11 | Düzgün Türkçe | `ç ğ ı İ ö ş ü` doğru; ürün adları orijinal |
| 12 | Yalnızca birinci-el kaynak | Resmî dokümantasyon/kurumsal platform; **şahıs adı taşıyan kanal önerilemez** |

**Rol sıralama — `rank_roles(role_scores)`:**

22 rolü skora göre sıralar, frontend'in rol seçicisini besler:

```python
[{"rank": 1, "role": "machine_learning_engineer",
  "display": "Makine Öğrenmesi Mühendisi", "score": 85, "auto": True}, ...]
```

`rank=1` → `auto=True` (panel açılınca planı otomatik üretilir) ·
`rank=2..22` → `auto=False` ("Plan oluştur" butonu arkasında bekler).

**Neden tembel (lazy)?** 22 rol × ~15 sn = 5,5 dakika bekleme **ve** günlük ücretsiz
kotanın (~20 istek) tamamı. Üç katmanlı koruma: (1) yalnızca rank 1 otomatik,
(2) `(cv_id, target_role)` DB cache → `cached: true`, (3) frontend bileşen state'inde
saklama.

**Retry stratejisi (`MAX_DENEME=3`, `TABAN_BEKLEME_SN=10`):**

| Durum | Davranış |
|---|---|
| 429 (dakikalık limit) veya 5xx | Üstel geri çekilme: 10sn → 20sn (+ jitter), 3 deneme |
| 429 **ama** gövdede `PerDay`/`RequestsPerDay` | **Günlük kota** — beklemek anlamsız, anında hata |
| Diğer hatalar (şema vb.) | Hiç tekrarlanmaz |

`temperature=0.4` — aynı hedefe birden fazla geçerli yol olduğu için plan yaratıcı
olabilir, ama savrulmasın diye düşük tutuldu.

## 3. AI Kariyer Koçu sistem promptu

**Kod:** `backend/services/coach_service.py` (`_SYSTEM_PERSONA`) ·
**Endpoint'ler:** `POST /chat/session`, `POST /chat`

Koç, CV analizi + eşleşen ilanları metinsel bağlama çevirip (`_build_context()`)
**yalnızca bu bağlama dayanarak** cevap verir. Oturum hafızası bellek-içidir
(`_sessions` dict); sunucu yeniden başlayınca sıfırlanır.

Ölçüm: **6/6 prob geçti (%100)**. En kritik kontrol `sayi_grounding` — koçun
"%88 eşleşen ilan" derken bu sayıyı gerçekten bağlamdan alıp almadığını denetler.
Sonuç: **uydurma yüzde yok.**

## 4. Rol listesi DÖRT yerde tanımlı — senkron zorunlu

Bir hedef rol eklemek/yeniden adlandırmak **dördünü birden** gerektirir:

| # | Yer | Ne tanımlar |
|---|---|---|
| 1 | `schemas/cv_analysis.py` → `RoleScores` | Skorların JSON şekli |
| 2 | `cv_service.py` → `system_instruction` | Gemini'ye 22 rolü doldurtan tek şey |
| 3 | `schemas/learning_plan.py` → `TargetRole` | Planın kabul ettiği roller |
| 4 | `services/learning_service.py` → `ROLE_DISPLAY` | Görünen Türkçe adlar |

Senkron kayması **sessizdir** (hata vermez, skor `0` döner / buton çalışmaz).
Bu yüzden rol düzenleyen her PR'dan önce:

```bash
python -m evals.guards.role_sync
```

0 Gemini çağrısı, ~1 saniye. `RoleScores` alanları == `TargetRole` değerleri ==
`ROLE_DISPLAY` anahtarları eşitliğini doğrular.

## 5. Frontend bağlantısı

| Bileşen | Dosya | Besleyen alan |
|---|---|---|
| Rol skorları grafiği + gerekçeler | `frontend/src/components/RoleScores.jsx` | `role_rankings`, `analysis.top_role_reasons` |
| Rol seçici + öğrenme yolu çizelgesi | `frontend/src/components/LearningPath.jsx` | `role_rankings`, `cv_id` |
| API çağrısı | `frontend/src/lib/api.js` → `getLearningPlan(cvId, targetRole)` | `POST /learning-plan` |

Frontend, plan üretiminin 10-15 saniye sürdüğünü kullanıcıya açıkça bildirir
("10-15 saniye sürebilir"), `cached: true` gelen planlarda "Kayıtlı plan" notu gösterir.

## 6. Kalite ölçümleri (özet)

| Yetenek | Eval | Sonuç |
|---|---|---|
| Skorlama doğruluğu | `scoring/accuracy` | **5/5 (%100)** |
| Skor kararlılığı | `scoring/consistency` | 1. rol **5/5 sabit**, ort. oynama 4.09 |
| Gerekçe tutarlılığı | `scoring/reasons` | **9/9** (0 çağrı 💚) |
| Plan kalitesi | `learning/plans` | **4/4 senaryo** |
| Koç kalitesi | `coach/quality` | **6/6 (%100)** |
| Rol senkronu | `guards/role_sync` | **22 == 22 == 22** (0 çağrı 💚) |

Ayrıntılı tablolar ve ham çıktılar: [`evals/results/OZET.md`](evals/results/OZET.md)
