import { useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import Card from "../components/ui/Card";
import Button from "../components/ui/Button";
import { uploadCv } from "../lib/api";
import { useCv } from "../context/CvContext";

// CV Yükleme ekranı — POST /cv/upload'a bağlı.
// Dönen analiz Context'e yazılır; Dashboard oradan okur.

export default function Upload() {
  const navigate = useNavigate();
  const { setResult } = useCv();
  const inputRef = useRef(null);

  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  function pickFile(e) {
    const selected = e.target.files?.[0] ?? null;
    setFile(selected);
    setError(null);
  }

  async function handleAnalyze() {
    if (!file || loading) return;
    setLoading(true);
    setError(null);
    try {
      const result = await uploadCv(file);
      setResult(result);
      navigate("/dashboard");
    } catch (err) {
      setError(err.message || "Analiz sırasında bir hata oluştu.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="mx-auto max-w-2xl">
      <h1 className="mb-1 text-2xl font-bold text-primary-800">CV Yükle</h1>
      <p className="mb-6 text-sm text-muted">
        PDF veya DOCX yükle. Analiz birkaç saniye sürebilir.
      </p>

      <Card>
        <input
          ref={inputRef}
          type="file"
          accept=".pdf,.docx"
          onChange={pickFile}
          className="hidden"
        />

        {/* Sürükle-bırak / seçim alanı */}
        <div className="flex flex-col items-center justify-center gap-3 rounded-xl border-2 border-dashed border-primary-200 bg-primary-50 py-14 text-center">
          <p className="text-sm font-medium text-primary-800">
            {file ? file.name : "Dosyanı buraya bırak"}
          </p>
          <p className="text-xs text-muted">PDF · DOCX · en fazla 5 MB</p>
          <Button
            variant="secondary"
            onClick={() => inputRef.current?.click()}
            disabled={loading}
          >
            {file ? "Dosyayı değiştir" : "Dosya seç"}
          </Button>
        </div>

        {error && (
          <p className="mt-4 rounded-lg border border-danger bg-white px-3 py-2 text-sm text-danger">
            {error}
          </p>
        )}

        <div className="mt-6 flex justify-end">
          <Button onClick={handleAnalyze} disabled={!file || loading}>
            {loading ? "Analiz ediliyor…" : "Analiz et"}
          </Button>
        </div>
      </Card>
    </div>
  );
}
