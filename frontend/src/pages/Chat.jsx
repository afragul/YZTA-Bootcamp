import { useEffect, useRef, useState } from "react";
import { Link } from "react-router-dom";
import Button from "../components/ui/Button";
import { initChatSession, sendChatMessage } from "../lib/api";
import { useCv } from "../context/CvContext";

// AI Kariyer Koçu (Kişi 4).
// CV analizi + eşleşen ilanlar varsa önce /chat/session ile RAG bağlamlı bir
// oturum açılır; sonraki mesajlar /chat'e session_id ile gider (oturum hafızası).
// Analiz yoksa bağlamsız genel sohbet olarak çalışır.

const SESSION_KEY = "coach_session_id";

function greeting(hasContext) {
  return hasContext
    ? "Merhaba! CV'ni ve sana en uygun ilanları inceledim. Kariyer hedeflerin hakkında konuşalım — nereden başlamak istersin?"
    : "Merhaba! Kariyer sorularını yanıtlamaya hazırım. Daha kişisel öneriler için önce CV'ni yükleyebilirsin.";
}

function Bubble({ role, children }) {
  const isUser = role === "user";
  return (
    <div className={isUser ? "flex justify-end" : "flex justify-start"}>
      <div
        className={
          "max-w-[80%] whitespace-pre-wrap rounded-2xl px-4 py-2.5 text-sm leading-relaxed " +
          (isUser
            ? "bg-primary-800 text-primary-50"
            : role === "error"
              ? "border border-danger/30 bg-white text-danger"
              : "bg-primary-50 text-primary-950")
        }
      >
        {children}
      </div>
    </div>
  );
}

function TypingDots() {
  return (
    <div className="flex justify-start">
      <div className="flex gap-1 rounded-2xl bg-primary-50 px-4 py-3">
        {[0, 150, 300].map((delay) => (
          <span
            key={delay}
            className="h-1.5 w-1.5 animate-bounce rounded-full bg-primary-500"
            style={{ animationDelay: `${delay}ms` }}
          />
        ))}
      </div>
    </div>
  );
}

export default function Chat() {
  const { result } = useCv();
  const hasContext = Boolean(result?.analysis);

  const [messages, setMessages] = useState([
    { role: "coach", text: greeting(hasContext) },
  ]);
  const [draft, setDraft] = useState("");
  const [sending, setSending] = useState(false);
  const sessionIdRef = useRef(sessionStorage.getItem(SESSION_KEY) || null);
  const bottomRef = useRef(null);

  // Yeni mesaj geldikçe en alta kaydır
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, sending]);

  // Analiz varsa ve henüz oturum yoksa RAG bağlamlı oturumu aç.
  // Hata olursa sessiz geçiyoruz: /chat bağlamsız oturumla yine de çalışır.
  useEffect(() => {
    if (!hasContext || sessionIdRef.current) return;
    let cancelled = false;
    (async () => {
      try {
        const data = await initChatSession(result.analysis, result.top_matches);
        if (cancelled) return;
        sessionIdRef.current = data.session_id;
        sessionStorage.setItem(SESSION_KEY, data.session_id);
      } catch {
        // bağlamsız devam
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [hasContext, result]);

  async function send() {
    const text = draft.trim();
    if (!text || sending) return;

    setMessages((m) => [...m, { role: "user", text }]);
    setDraft("");
    setSending(true);

    try {
      const data = await sendChatMessage(text, sessionIdRef.current);
      if (data.session_id) {
        sessionIdRef.current = data.session_id;
        sessionStorage.setItem(SESSION_KEY, data.session_id);
      }
      setMessages((m) => [...m, { role: "coach", text: data.reply }]);
    } catch (err) {
      setMessages((m) => [
        ...m,
        { role: "error", text: err.message || "Bir şeyler ters gitti." },
      ]);
    } finally {
      setSending(false);
    }
  }

  return (
    <div className="mx-auto flex h-[70vh] max-w-2xl flex-col">
      <div className="mb-4 flex flex-wrap items-baseline justify-between gap-2">
        <h1 className="text-2xl font-bold text-primary-800">AI Kariyer Koçu</h1>
        {!hasContext && (
          <Link
            to="/upload"
            className="text-sm font-semibold text-primary-500 hover:text-primary-800"
          >
            CV yükle → kişisel öneriler
          </Link>
        )}
      </div>

      <div className="flex-1 space-y-3 overflow-y-auto rounded-2xl border border-primary-200 bg-white p-5">
        {messages.map((m, i) => (
          <Bubble key={i} role={m.role}>
            {m.text}
          </Bubble>
        ))}
        {sending && <TypingDots />}
        <div ref={bottomRef} />
      </div>

      <div className="mt-4 flex gap-2">
        <input
          value={draft}
          onChange={(e) => setDraft(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && send()}
          disabled={sending}
          placeholder={sending ? "Koç yazıyor..." : "Bir şeyler sor..."}
          className="flex-1 rounded-lg border border-primary-200 bg-white px-3.5 py-2.5 text-sm text-primary-950 placeholder:text-muted focus-visible:border-primary-500 focus-visible:outline-none disabled:opacity-60"
        />
        <Button onClick={send} disabled={sending || !draft.trim()}>
          Gönder
        </Button>
      </div>
    </div>
  );
}