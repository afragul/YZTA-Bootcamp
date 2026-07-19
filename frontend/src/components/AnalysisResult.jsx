import Card from "./ui/Card";

// Kişi 2 — CV analiz sonuç kartları.
// Girdi: analysis (CVAnalysisOutput): skills, experience_years, education,
// strengths, gaps (rol-etiketli: "[rol] metin").

// "[machine_learning_engineer] MLOps deneyimi yok" → { role, text }
function parseGap(gap) {
  const match = /^\s*\[([^\]]+)\]\s*(.*)$/.exec(gap);
  if (match) return { role: prettifyRole(match[1]), text: match[2] };
  return { role: null, text: gap };
}

// snake_case teknik ad → okunabilir etiket ("machine_learning_engineer" → "Machine Learning Engineer")
function prettifyRole(role) {
  return role
    .split("_")
    .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
    .join(" ");
}

function educationLine(item) {
  const parts = [item.degree, item.department, item.school].filter(Boolean);
  const head = parts.join(" · ");
  return item.graduation_year ? `${head} (${item.graduation_year})` : head;
}

function Empty({ children }) {
  return <p className="text-sm text-muted">{children}</p>;
}

export default function AnalysisResult({ analysis }) {
  if (!analysis) return null;

  const {
    skills = [],
    experience_years = 0,
    education = [],
    strengths = [],
    gaps = [],
  } = analysis;

  return (
    <div className="flex flex-col gap-5">
      {/* Özet satırı: deneyim + eğitim */}
      <Card>
        <Card.Title>CV Özeti</Card.Title>
        <div className="flex flex-wrap items-center gap-x-6 gap-y-1 text-sm">
          <span className="text-primary-950">
            <span className="font-semibold text-primary-800">
              {experience_years}
            </span>{" "}
            yıl deneyim
          </span>
        </div>
        {education.length > 0 ? (
          <ul className="mt-3 space-y-1">
            {education.map((e, i) => (
              <li key={i} className="text-sm text-muted">
                {educationLine(e)}
              </li>
            ))}
          </ul>
        ) : (
          <p className="mt-3 text-sm text-muted">Eğitim bilgisi belirtilmemiş.</p>
        )}
      </Card>

      {/* Beceriler */}
      <Card>
        <Card.Title>Beceriler</Card.Title>
        {skills.length > 0 ? (
          <div className="flex flex-wrap gap-2">
            {skills.map((s, i) => (
              <span
                key={i}
                className="rounded-lg bg-primary-50 px-2.5 py-1 text-sm font-medium text-primary-800"
              >
                {s}
              </span>
            ))}
          </div>
        ) : (
          <Empty>Beceri belirtilmemiş.</Empty>
        )}
      </Card>

      {/* Güçlü yönler */}
      <Card>
        <Card.Title>Güçlü Yönler</Card.Title>
        {strengths.length > 0 ? (
          <ul className="space-y-2">
            {strengths.map((s, i) => (
              <li key={i} className="flex gap-2 text-sm text-primary-950">
                <span aria-hidden className="mt-0.5 font-bold text-success">
                  ✓
                </span>
                <span>{s}</span>
              </li>
            ))}
          </ul>
        ) : (
          <Empty>Güçlü yön belirtilmemiş.</Empty>
        )}
      </Card>

      {/* Eksikler (hedef role göre) */}
      <Card>
        <Card.Title>Gelişim Alanları</Card.Title>
        {gaps.length > 0 ? (
          <ul className="space-y-2.5">
            {gaps.map((g, i) => {
              const { role, text } = parseGap(g);
              return (
                <li key={i} className="flex flex-wrap items-start gap-2 text-sm">
                  {role && (
                    <span className="rounded-md border border-primary-200 bg-primary-50 px-2 py-0.5 text-xs font-semibold text-primary-500">
                      {role}
                    </span>
                  )}
                  <span className="text-primary-950">{text}</span>
                </li>
              );
            })}
          </ul>
        ) : (
          <Empty>Gelişim alanı belirtilmemiş.</Empty>
        )}
      </Card>
    </div>
  );
}
