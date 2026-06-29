import os
import json
from cv_service import CVAnalysisService

def run_all_tests():
    print("=== TOPLU CV ANALİZİ TEST SÜRECİ BAŞLADI ===")
    
    # Servisi başlat
    try:
        service = CVAnalysisService()
    except Exception as e:
        print(f"Başlatma Hatası: {e}")
        return

    # Örnek CV klasör yolu
    cv_dir = "sample_cvs"
    if not os.path.exists(cv_dir):
        print(f"Hata: '{cv_dir}' klasörü bulunamadı!")
        return

    # Çıktıların kaydedileceği klasör
    output_dir = "test_results"
    os.makedirs(output_dir, exist_ok=True)

    # Klasördeki tüm .txt CV'leri oku
    cv_files = [f for f in os.listdir(cv_dir) if f.endswith(".txt")]
    if not cv_files:
        print("Klasörde test edilecek .txt uzantılı CV dosyası bulunamadı.")
        return

    print(f"Toplam {len(cv_files)} adet CV dosyası bulundu. Analiz ediliyor...\n")

    for file_name in cv_files:
        file_path = os.path.exists(os.path.join(cv_dir, file_name))
        print("-" * 50)
        print(f"Dosya Analiz Ediliyor: {file_name}")
        
        with open(os.path.join(cv_dir, file_name), "r", encoding="utf-8") as f:
            cv_text = f.read()

        try:
            result = service.analyze_cv(cv_text)
            
            # Sonucu ekrana yazdır (Özet)
            print(f"Analiz Başarılı! Toplam Deneyim: {result.get('experience_years')} yıl")
            print("Çıkarılan Roller ve Skorları:")
            for role, score in result.get('role_scores', {}).items():
                print(f" - {role}: {score}/100")
                
            # Sonucu dosyaya kaydet
            output_file_name = file_name.replace(".txt", "_result.json")
            output_file_path = os.path.join(output_dir, output_file_name)
            
            with open(output_file_path, "w", encoding="utf-8") as out_f:
                json.dump(result, out_f, indent=2, ensure_ascii=False)
            print(f"Detaylı JSON sonucu kaydedildi: {output_file_path}")
            
        except Exception as e:
            print(f"Dosya analiz edilirken hata oluştu: {file_name}. Hata: {e}")

    print("\n=== TÜM TESTLER TAMAMLANDI ===")
    print(f"Tüm analiz çıktıları '{output_dir}/' klasörüne kaydedilmiştir.")

if __name__ == "__main__":
    run_all_tests()
