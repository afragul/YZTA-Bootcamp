// Backend çağrıları buradan yapılacak (şimdilik iskelet).
// API kontratı (Kişi 1) netleştikçe fonksiyonlar buraya eklenecek.

// NOT: Windows'ta "localhost" IPv6 (::1) çözülebilir; backend ise 127.0.0.1
// (IPv4) dinler → "Failed to fetch". Bu yüzden varsayılan 127.0.0.1.
const BASE_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

export async function apiGet(path) {
  const res = await fetch(`${BASE_URL}${path}`);
  if (!res.ok) throw new Error(`GET ${path} başarısız: ${res.status}`);
  return res.json();
}

export async function apiPost(path, body) {
  const res = await fetch(`${BASE_URL}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error(`POST ${path} başarısız: ${res.status}`);
  return res.json();
}

// Backend hata gövdesindeki { detail: "..." } mesajını okumaya çalışır.
async function errorDetail(res, fallback) {
  try {
    const data = await res.json();
    if (data && data.detail) return data.detail;
  } catch {
    // gövde JSON değil — sabit mesaja düş
  }
  return fallback;
}

// CV dosyasını (PDF/DOCX) yükler ve tam analiz cevabını (CVUploadResponse) döndürür.
// NOT: FormData ile Content-Type başlığı ELLE verilmez; tarayıcı multipart
// boundary'yi kendisi ekler.
export async function uploadCv(file) {
  const form = new FormData();
  form.append("file", file);
  const res = await fetch(`${BASE_URL}/cv/upload`, {
    method: "POST",
    body: form,
  });
  if (!res.ok) {
    throw new Error(await errorDetail(res, `Yükleme başarısız (${res.status}).`));
  }
  return res.json();
}

// Kayıtlı bir CV analiz sonucunu id ile geri okur (yenileme/fallback).
export async function getCvResult(cvId) {
  return apiGet(`/cv/${cvId}`);
}

// --- Öğrenme Planı (Kişi 3) ---

// Kişi 3 — Hedef role için öğrenme planı oluşturur (veya cache'den okur).
// cv_id: CV'nin veritabanı kimliği
// targetRole: Hedef rol (snake_case: "devops_engineer", "data_scientist", vb.)
// Döner: { cv_id, target_role, cached, plan }
export async function getLearningPlan(cvId, targetRole) {
  const res = await fetch(`${BASE_URL}/learning-plan`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ cv_id: cvId, target_role: targetRole }),
  });

  if (!res.ok) {
    let msg = await errorDetail(res, `Plan oluşturulamadı (${res.status}).`);
    // 502 (API kota) için özel dostu mesaj (K1 — bekleme süresi beklentisi)
    if (res.status === 502) {
      msg = "Plan şu anda üretilemedi, birkaç dakika sonra tekrar dene";
    }
    throw new Error(msg);
  }

  return res.json();
}

// --- AI Kariyer Koçu (Kişi 4) ---

// CV analizi + eşleşen ilanlarla RAG bağlamlı bir koç oturumu açar.
// Dönen session_id sonraki mesajlarda gönderilir → koç bağlamı hatırlar.
export async function initChatSession(analysis, topMatches) {
  const res = await fetch(`${BASE_URL}/chat/session`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ analysis, top_matches: topMatches ?? [] }),
  });
  if (!res.ok) {
    throw new Error(await errorDetail(res, `Oturum açılamadı (${res.status}).`));
  }
  return res.json();
}

// Koça mesaj gönderir. sessionId yoksa backend bağlamsız genel oturum açar.
export async function sendChatMessage(message, sessionId) {
  const res = await fetch(`${BASE_URL}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, session_id: sessionId ?? null }),
  });
  if (!res.ok) {
    throw new Error(await errorDetail(res, `Koç cevabı alınamadı (${res.status}).`));
  }
  return res.json();
}
