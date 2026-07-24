import { Link } from "react-router-dom";
import Card from "../components/ui/Card";
import AnalysisResult from "../components/AnalysisResult";
import RoleScores from "../components/RoleScores";
import LearningPath from "../components/LearningPath";
import { useCv } from "../context/CvContext";

// Panel — herkesin kendi UI'ını taktığı yer:
//   Kişi 2 → analiz sonuç kartları (güçlü yönler / eksikler)  ← BAĞLANDI
//   Kişi 3 → rol skorları (bar/radar) + öğrenme yolu          ← BAĞLANDI
//   Kişi 4 → iş eşleşmeleri listesi (yüzdeyle)                (iskelet)

// Kişi 3 — Test için mock data (dev ortamında)
const mockResult = {
  cv_id: "test-123",
  filename: "cv_ml_engineer.pdf",
  analysis: {
    skills: ["Python", "PyTorch", "TensorFlow", "MLflow", "PostgreSQL", "Docker"],
    experience_years: 3,
    education: [
      {
        degree: "Lisans",
        department: "Bilgisayar Mühendisliği",
        school: "Orta Doğu Teknik Üniversitesi",
        graduation_year: 2021,
      },
    ],
    strengths: ["Derin öğrenme modeller geliştirme deneyimi", "Veri işleme ve ön işleme"],
    gaps: [
      "[machine_learning_engineer] Büyük veri teknolojileri (Spark) deneyimi yok",
      "[data_scientist] Veritabanı yönetimi deneyimi sınırlı",
    ],
    role_scores: {
      machine_learning_engineer: 85,
      data_scientist: 75,
      data_analyst: 50,
      devops_engineer: 45,
      data_engineer: 45,
      backend_developer: 40,
      cloud_engineer: 35,
      business_analyst: 35,
      bi_analyst: 30,
      product_manager: 25,
      database_administrator: 25,
      fullstack_developer: 20,
      project_manager: 20,
      systems_administrator: 15,
      customer_success_specialist: 10,
      frontend_developer: 10,
      mobile_developer: 10,
      cybersecurity_specialist: 10,
      ui_ux_designer: 10,
      graphic_designer: 10,
      digital_marketing_specialist: 10,
      hr_specialist: 10,
    },
    top_role_reasons: [
      {
        role: "machine_learning_engineer",
        score: 85,
        reason: "CV'de PyTorch ve TensorFlow deneyimi var, derin öğrenme projeleri yapılmış",
      },
      {
        role: "data_scientist",
        score: 75,
        reason: "İstatistiksel modelleme ve Python analiz kabiliyeti mevcut",
      },
      {
        role: "data_analyst",
        score: 50,
        reason: "SQL bilgisi mevcut fakat görselleştirme ve BI aracı deneyimi yok",
      },
    ],
  },
  top_matches: [],
  role_rankings: [
    {
      rank: 1,
      role: "machine_learning_engineer",
      display: "Makine Öğrenmesi Mühendisi",
      score: 85,
      auto: true,
    },
    { rank: 2, role: "data_scientist", display: "Veri Bilimci", score: 75, auto: false },
    { rank: 3, role: "data_analyst", display: "Veri Analisti", score: 50, auto: false },
    { rank: 4, role: "devops_engineer", display: "DevOps Mühendisi", score: 45, auto: false },
    { rank: 5, role: "data_engineer", display: "Veri Mühendisi", score: 45, auto: false },
    { rank: 6, role: "backend_developer", display: "Backend Geliştirici", score: 40, auto: false },
    { rank: 7, role: "cloud_engineer", display: "Bulut Mühendisi", score: 35, auto: false },
    {
      rank: 8,
      role: "business_analyst",
      display: "İş Analisti",
      score: 35,
      auto: false,
    },
    { rank: 9, role: "bi_analyst", display: "İş Zekası Analisti", score: 30, auto: false },
    {
      rank: 10,
      role: "product_manager",
      display: "Ürün Yöneticisi",
      score: 25,
      auto: false,
    },
    {
      rank: 11,
      role: "database_administrator",
      display: "Veritabanı Yöneticisi",
      score: 25,
      auto: false,
    },
    {
      rank: 12,
      role: "fullstack_developer",
      display: "Full Stack Geliştirici",
      score: 20,
      auto: false,
    },
    {
      rank: 13,
      role: "project_manager",
      display: "Proje Yöneticisi",
      score: 20,
      auto: false,
    },
    {
      rank: 14,
      role: "systems_administrator",
      display: "Sistem Yöneticisi",
      score: 15,
      auto: false,
    },
    {
      rank: 15,
      role: "customer_success_specialist",
      display: "Müşteri Başarı Uzmanı",
      score: 10,
      auto: false,
    },
    {
      rank: 16,
      role: "frontend_developer",
      display: "Frontend Geliştirici",
      score: 10,
      auto: false,
    },
    {
      rank: 17,
      role: "mobile_developer",
      display: "Mobil Geliştirici",
      score: 10,
      auto: false,
    },
    {
      rank: 18,
      role: "cybersecurity_specialist",
      display: "Siber Güvenlik Uzmanı",
      score: 10,
      auto: false,
    },
    { rank: 19, role: "ui_ux_designer", display: "UI/UX Tasarımcı", score: 10, auto: false },
    {
      rank: 20,
      role: "graphic_designer",
      display: "Grafik Tasarımcı",
      score: 10,
      auto: false,
    },
    {
      rank: 21,
      role: "digital_marketing_specialist",
      display: "Dijital Pazarlama Uzmanı",
      score: 10,
      auto: false,
    },
    {
      rank: 22,
      role: "hr_specialist",
      display: "İnsan Kaynakları Uzmanı",
      score: 10,
      auto: false,
    },
  ],
};

export default function Dashboard() {
  const { result: contextResult } = useCv();
  // Dev ortamında mock data kullan (frontend test için)
  const result = contextResult || (import.meta.env.DEV ? mockResult : null);

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

      {/* Kişi 3 / Kişi 4 — bileşenler bağlı */}
      <div className="mt-5 grid gap-5 md:grid-cols-2">
        <RoleScores
          analysis={result.analysis}
          rankings={result.role_rankings}
        />

        <Card>
          <Card.Title>İş Eşleşmeleri</Card.Title>
          <p className="text-sm text-muted">
            CV'ne en uygun ilanlar, eşleşme yüzdesiyle burada listelenecek. (Kişi 4)
          </p>
        </Card>
      </div>

      {/* Kişi 3 — Öğrenme yolu zaman çizelgesi (tam genişlik) */}
      <LearningPath
        cvId={result.cv_id}
        analysis={result.analysis}
        rankings={result.role_rankings}
      />

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
