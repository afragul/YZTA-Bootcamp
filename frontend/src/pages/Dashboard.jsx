import { Link } from "react-router-dom";
import Card from "../components/ui/Card";
import AnalysisResult from "../components/AnalysisResult";
import { useCv } from "../context/CvContext";

// Panel — herkesin kendi UI'ını taktığı yer:
//   Kişi 2 → analiz sonuç kartları (güçlü yönler / eksikler)  ← BAĞLANDI
//   Kişi 3 → rol skorları (bar/radar) + öğrenme yolu          (iskelet)
//   Kişi 4 → iş eşleşmeleri listesi (yüzdeyle)                (iskelet)

export default function Dashboard() {
  const { result } = useCv();

  // Henüz CV yüklenmemiş → boş durum
  if (!result) {
    return (
      <div>
        <h1 className="mb-6 text-2xl font-bold text-primary-800">Panel</h1>
        <Card>
          <Card.Title>Henüz analiz yok</Card.Title>
          <p className="mb-4 text-sm text-muted">
            Analiz sonuçlarını görmek için önce bir CV yükle.
          </p>
          <Link
            to="/upload"
            className="text-sm font-semibold text-primary-500 hover:text-primary-800"
          >
            CV Yükle →
          </Link>
        </Card>
      </div>
    );
  }

  return (
    <div>
      <div className="mb-6 flex flex-wrap items-baseline justify-between gap-2">
        <h1 className="text-2xl font-bold text-primary-800">Panel</h1>
        {result.filename && (
          <span className="text-sm text-muted">{result.filename}</span>
        )}
      </div>

      {/* Kişi 2 — CV analiz sonuç kartları */}
      <AnalysisResult analysis={result.analysis} />

      {/* Kişi 3 / Kişi 4 — henüz iskelet (bu planın kapsamı dışında) */}
      <div className="mt-5 grid gap-5 md:grid-cols-2">
        <Card>
          <Card.Title>Rol Uygunluğu</Card.Title>
          <p className="text-sm text-muted">
            Rol skorları ve öğrenme yolu burada. (Kişi 3)
          </p>
        </Card>

        <Card>
          <Card.Title>İş Eşleşmeleri</Card.Title>
          <p className="text-sm text-muted">
            CV'ne en uygun ilanlar, eşleşme yüzdesiyle burada listelenecek. (Kişi 4)
          </p>
        </Card>
      </div>

      <div className="mt-8">
        <Link
          to="/chat"
          className="text-sm font-semibold text-primary-500 hover:text-primary-800"
        >
          AI Koç ile konuş →
        </Link>
      </div>
    </div>
  );
}
