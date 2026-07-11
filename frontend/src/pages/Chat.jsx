import { useState } from "react";
import Button from "../components/ui/Button";

// AI Kariyer Koçu — İSKELET (Kişi 4).
// Şimdilik sadece arayüz + yerel state. Gerçek /chat çağrısı sonra bağlanacak.

export default function Chat() {
  const [messages, setMessages] = useState([
    {
      role: "coach",
      text: "Merhaba! CV'ni ve eşleşen ilanları gördüm. Kariyer hedeflerin hakkında konuşalım — nereden başlamak istersin?",
    },
  ]);
  const [draft, setDraft] = useState("");

  function send() {
    const text = draft.trim();
    if (!text) return;
    // TODO: POST /chat çağrısı — RAG bağlamı + oturum hafızası burada bağlanacak.
    setMessages((m) => [...m, { role: "user", text }]);
    setDraft("");
  }

  return (
    <div className="mx-auto flex h-[70vh] max-w-2xl flex-col">
      <h1 className="mb-4 text-2xl font-bold text-primary-800">AI Kariyer Koçu</h1>

      {/* Mesaj listesi */}
      <div className="flex-1 space-y-3 overflow-y-auto rounded-2xl border border-primary-200 bg-white p-5">
        {messages.map((m, i) => (
          <div
            key={i}
            className={m.role === "user" ? "flex justify-end" : "flex justify-start"}
          >
            <div
              className={
                "max-w-[80%] rounded-2xl px-4 py-2.5 text-sm " +
                (m.role === "user"
                  ? "bg-primary-800 text-primary-50"
                  : "bg-primary-50 text-primary-950")
              }
            >
              {m.text}
            </div>
          </div>
        ))}
      </div>

      {/* Yazma alanı */}
      <div className="mt-4 flex gap-2">
        <input
          value={draft}
          onChange={(e) => setDraft(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && send()}
          placeholder="Bir şeyler sor..."
          className="flex-1 rounded-lg border border-primary-200 bg-white px-3.5 py-2.5 text-sm text-primary-950 placeholder:text-muted focus-visible:border-primary-500 focus-visible:outline-none"
        />
        <Button onClick={send}>Gönder</Button>
      </div>
    </div>
  );
}
