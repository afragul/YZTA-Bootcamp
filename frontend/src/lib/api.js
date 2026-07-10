// Backend çağrıları buradan yapılacak (şimdilik iskelet).
// API kontratı (Kişi 1) netleştikçe fonksiyonlar buraya eklenecek.

const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

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
