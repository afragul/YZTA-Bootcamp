import { useNavigate } from "react-router-dom";
import Card from "../components/ui/Card";
import Button from "../components/ui/Button";

// CV Yükleme ekranı — İSKELET.
// Yükleme backend'i (POST /cv/upload) Kişi 1'e ait.

export default function Upload() {
  const navigate = useNavigate();

  return (
    <div className="mx-auto max-w-2xl">
      <h1 className="mb-1 text-2xl font-bold text-primary-800">CV Yükle</h1>
      <p className="mb-6 text-sm text-muted">
        PDF veya DOCX yükle. Analiz birkaç saniye sürebilir.
      </p>

      <Card>
        {/* Sürükle-bırak alanı (şimdilik görsel iskelet) */}
        <div className="flex flex-col items-center justify-center gap-3 rounded-xl border-2 border-dashed border-primary-200 bg-primary-50 py-14 text-center">
          <p className="text-sm font-medium text-primary-800">
            Dosyanı buraya bırak
          </p>
          <p className="text-xs text-muted">PDF · DOCX · en fazla 5 MB</p>
          <Button variant="secondary">Dosya seç</Button>
        </div>

        <div className="mt-6 flex justify-end">
          <Button onClick={() => navigate("/dashboard")}>Analiz et</Button>
        </div>
      </Card>
    </div>
  );
}
