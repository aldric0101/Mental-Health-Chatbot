import { useEffect, useRef, useState } from "react";
import { sendMessage, detectEmotion } from "./api";
import "./App.css";
import SpeechInput from "./components/SpeechInput";

function App() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const scrollRef = useRef(null);

  const handleSend = async (msgOverride) => {
    const outgoing = (msgOverride ?? input).trim();
    if (!outgoing || loading) return;

    setLoading(true);
    const userMsg = { text: outgoing, sender: "user", ts: Date.now() };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");

    try {
      const [{ reply }, { emotion }] = await Promise.all([
        sendMessage(outgoing),
        detectEmotion(outgoing),
      ]);
      const botMsg = { text: `${reply} (Emotion: ${emotion})`, sender: "bot", ts: Date.now(), emotion };
      setMessages((prev) => [...prev, botMsg]);
    } catch (e) {
      setMessages((prev) => [...prev, { text: "Sorry, something went wrong. Please try again.", sender: "bot", ts: Date.now() }]);
    } finally {
      setLoading(false);
      // Auto-scroll
      setTimeout(() => { if (scrollRef.current) scrollRef.current.scrollTop = scrollRef.current.scrollHeight; }, 0);
    }
  };

  // Optional TTS
  useEffect(() => {
    const last = messages[messages.length - 1];
    if (last?.sender === "bot" && "speechSynthesis" in window) {
      const utter = new SpeechSynthesisUtterance(last.text.replace(/\(Emotion: .*?\)$/, ""));
      window.speechSynthesis.cancel();
      window.speechSynthesis.speak(utter);
    }
  }, [messages]);

  const renderMessage = (msg, i) => {
    const isBot = msg.sender === "bot";
    // Extract sentiment for pill
    const match = /\(Emotion:\s*(.+?)\)$/.exec(msg.text);
    const sentiment = msg.emotion || (match ? match[1] : null);
    const cleanText = msg.text.replace(/\s*\(Emotion: .+?\)\s*$/, "");

    return (
      <div key={i} className={`row ${isBot ? "bot" : "user"}`}>
        <div className="bubble">
          {cleanText}
          {sentiment && (
            <div className="meta">
              <span className="sentiment">{sentiment}</span>
            </div>
          )}
        </div>
      </div>
    );
  };

  return (
    <div className="app">
      <div className="chat-card">
        <div className="header">
          <h2> Mental Health Chatbot</h2>
          <div className="pill">Supportive • Private • Local</div>
        </div>

        <div className="scroll" ref={scrollRef}>
          {messages.map(renderMessage)}
          {loading && <div className="typing">Bot is typing…</div>}
        </div>

        <div className="footer">
          <div className="input" style={{flex:1}}>
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleSend()}
              placeholder="Type how you're feeling…"
              disabled={loading}
            />
          </div>
          <button className="btn primary" onClick={() => handleSend()} disabled={loading}>
            {loading ? "Sending…" : "Send"}
          </button>
        </div>

        <div style={{ padding: "0 14px 14px" }}>
          <SpeechInput onResult={(t) => handleSend(t)} />
        </div>
      </div>
    </div>
  );
}

export default App;
