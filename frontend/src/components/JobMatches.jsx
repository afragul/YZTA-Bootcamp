import { useState } from "react";
import Card from "./ui/Card";

// Girdi: matches (JobMatchItem[]): title, job_domain, work_type,
// job_location, match_percent, description.
//
// Varsayılan görünüm: tek kart + < > ile gezinme + "X / N" sayaç.
// Alttaki "Tümünü göster" ile klasik alt alta liste görünümüne geçilir.

// snake_case teknik ad → okunabilir etiket ("remote_work" → "Remote Work")
function prettify(value) {
  if (!value) return "";
  return value
    .split("_")
    .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
    .join(" ");
}

// Eşleşme gücüne göre renk: yüksek = koyu mavi, düşük = soluk
function scoreTone(percent) {
  if (percent >= 75) return "bg-primary-800 text-primary-50";
  if (percent >= 60) return "bg-primary-500 text-white";
  return "bg-primary-200 text-primary-950";
}

function MatchBar({ percent }) {
  return (
    <div
      className="h-1.5 w-full overflow-hidden rounded-full bg-primary-50"
      role="progressbar"
      aria-valuenow={Math.round(percent)}
      aria-valuemin={0}
      aria-valuemax={100}
    >
      <div
        className="h-full rounded-full bg-primary-500 transition-all"
        style={{ width: `${Math.min(100, Math.max(0, percent))}%` }}
      />
    </div>
  );
}

function ChevronIcon({ direction }) {
  const d =
    direction === "left" ? "M12.5 15L7.5 10L12.5 5" : "M7.5 5L12.5 10L7.5 15";
  return (
    <svg width="18" height="18" viewBox="0 0 20 20" fill="none">
      <path
        d={d}
        stroke="currentColor"
        strokeWidth="1.8"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

function NavButton({ direction, onClick, disabled }) {
  return (
    <button
      type="button"
      onClick={onClick}
      disabled={disabled}
      aria-label={direction === "left" ? "Önceki ilan" : "Sonraki ilan"}
      className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full border border-primary-200 bg-white text-primary-800 transition-colors hover:bg-primary-50 disabled:cursor-not-allowed disabled:opacity-40 disabled:hover:bg-white"
    >
      <ChevronIcon direction={direction} />
    </button>
  );
}

function JobCardBody({ job }) {
  const [open, setOpen] = useState(false);
  const percent = Math.round(job.match_percent ?? 0);
  const meta = [
    prettify(job.job_domain),
    prettify(job.work_type),
    job.job_location,
  ].filter(Boolean);

  return (
    <div>
      <div className="mb-2 flex items-start justify-between gap-3">
        <div className="min-w-0">
          <h4 className="truncate font-semibold text-primary-950">
            {job.title}
          </h4>
          {meta.length > 0 && (
            <p className="mt-0.5 text-xs text-muted">{meta.join(" · ")}</p>
          )}
        </div>
        <span
          className={
            "shrink-0 rounded-full px-2.5 py-1 text-xs font-bold " +
            scoreTone(percent)
          }
        >
          %{percent}
        </span>
      </div>

      <MatchBar percent={percent} />

      {job.description && (
        <>
          <p
            className={
              "mt-3 text-sm leading-relaxed text-muted " +
              (open ? "" : "line-clamp-2")
            }
          >
            {job.description}
          </p>
          <button
            type="button"
            onClick={() => setOpen((v) => !v)}
            className="mt-1.5 text-xs font-semibold text-primary-500 hover:text-primary-800"
          >
            {open ? "Daha az göster" : "Devamını oku"}
          </button>
        </>
      )}
    </div>
  );
}

// Tek kart + gezinme oku + sayaç (varsayılan görünüm)
function Carousel({ matches }) {
  const [index, setIndex] = useState(0);
  const total = matches.length;

  function go(delta) {
    setIndex((i) => Math.min(total - 1, Math.max(0, i + delta)));
  }

  return (
    <div>
      <div className="flex items-center gap-3">
        <NavButton direction="left" onClick={() => go(-1)} disabled={index === 0} />

        <div className="min-w-0 flex-1 rounded-xl border border-primary-200 bg-white p-4">
          <JobCardBody job={matches[index]} />
        </div>

        <NavButton
          direction="right"
          onClick={() => go(1)}
          disabled={index === total - 1}
        />
      </div>

      <p className="mt-3 text-center text-xs font-medium text-muted">
        {index + 1} / {total}
      </p>
    </div>
  );
}

// Klasik alt alta liste görünümü (genişletilince)
function FullList({ matches }) {
  return (
    <ul className="space-y-3">
      {matches.map((job, i) => (
        <li key={`${job.title}-${i}`} className="rounded-xl border border-primary-200 bg-white p-4">
          <JobCardBody job={job} />
        </li>
      ))}
    </ul>
  );
}

export default function JobMatches({ matches }) {
  const [expanded, setExpanded] = useState(false);

  if (!matches || matches.length === 0) {
    return (
      <Card>
        <Card.Title>İş Eşleşmeleri</Card.Title>
        <p className="text-sm text-muted">
          CV'ne uygun ilan bulunamadı. İlan veritabanı henüz yüklenmemiş
          olabilir.
        </p>
      </Card>
    );
  }

  return (
    <Card>
      <div className="mb-3 flex items-baseline justify-between gap-2">
        <Card.Title className="mb-0">İş Eşleşmeleri</Card.Title>
        <span className="text-xs text-muted">{matches.length} ilan</span>
      </div>
      <p className="mb-4 text-sm text-muted">
        CV'ndeki becerilerle anlamsal olarak en çok örtüşen ilanlar.
      </p>

      {expanded ? <FullList matches={matches} /> : <Carousel matches={matches} />}

      {matches.length > 1 && (
        <button
          type="button"
          onClick={() => setExpanded((v) => !v)}
          className="mt-4 w-full rounded-lg border border-dashed border-primary-200 py-2 text-xs font-semibold text-primary-500 hover:border-primary-500 hover:bg-primary-50 hover:text-primary-800"
        >
          {expanded ? "Tek tek görüntüle ↑" : "Tümünü göster "}
        </button>
      )}
    </Card>
  );
}