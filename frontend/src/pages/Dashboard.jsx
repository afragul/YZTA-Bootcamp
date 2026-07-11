import { Link } from "react-router-dom";
import Card from "../components/ui/Card";

// Panel — İSKELET.
// Bu sayfa herkesin kendi UI'ını taktığı yer:
//   Kişi 2 → analiz sonuç kartları (güçlü yönler / eksikler)
//   Kişi 3 → rol skorları (bar/radar) + öğrenme yolu
//   Kişi 4 → iş eşleşmeleri listesi (yüzdeyle)  ← senin alanın

export default function Dashboard() {
  return (
    <div>
      <h1 className="mb-6 text-2xl font-bold text-primary-800">Panel</h1>

      <div className="grid gap-5 md:grid-cols-2">
        <Card>
          <Card.Title>CV Analizi</Card.Title>
          <p className="text-sm text-muted">
            Güçlü yönler ve eksikler burada listelenecek. (Kişi 2)
          </p>
        </Card>

        <Card>
          <Card.Title>Rol Uygunluğu</Card.Title>
          <p className="text-sm text-muted">
            Rol skorları ve öğrenme yolu burada. (Kişi 3)
          </p>
        </Card>

        {/* Kişi 4 — İş Eşleşmeleri (senin modülün) */}
        <Card className="md:col-span-2">
          <Card.Title>İş Eşleşmeleri</Card.Title>
          <p className="mb-4 text-sm text-muted">
            CV'ne en uygun ilanlar, eşleşme yüzdesiyle burada listelenecek.
          </p>
          <div className="flex items-center gap-4 rounded-xl bg-primary-50 p-4">
            <span className="rounded-lg bg-primary-800 px-2.5 py-1 text-sm font-semibold text-primary-50">
              %88
            </span>
            <span className="text-sm text-primary-950">
              Örnek: Junior ML Engineer — eşleşme gücü mavi tonuyla gösterilir.
            </span>
          </div>
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
