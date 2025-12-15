import { useState, useRef, useEffect } from "react";
import "./App.css";

const API_URL = "https://rag-chat-system-2-f9yj.onrender.com/ask";

function App() {
  const [message, setMessage] = useState("");
  const [chat, setChat] = useState([]);
  const [loading, setLoading] = useState(false);
  const chatEndRef = useRef(null);

  // Auto scroll
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chat, loading]);

  const sendMessage = async () => {
    if (!message.trim() || loading) return;

    const userText = message;

    setChat((prev) => [...prev, { role: "user", text: userText }]);
    setMessage("");
    setLoading(true);

    try {
      const res = await fetch(API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          query: userText, // ✅ BACKEND MATCH
        }),
      });

      if (!res.ok) throw new Error("API error");

      const data = await res.json();
      typeBotReply(data.answer || "No response from RAG");
    } catch (err) {
      console.error(err);
      typeBotReply("Server error. Please try again.");
    }
  };

  const typeBotReply = (text) => {
    let index = 0;
    let currentText = "";

    setChat((prev) => [...prev, { role: "bot", text: "" }]);

    const interval = setInterval(() => {
      currentText += text[index] || "";
      index++;

      setChat((prev) => {
        const updated = [...prev];
        updated[updated.length - 1].text = currentText;
        return updated;
      });

      if (index >= text.length) {
        clearInterval(interval);
        setLoading(false);
      }
    }, 20);
  };

  return (
    <div className="app">
      <header className="header">
        <h1>RAG Support Assistant</h1>
        <p>AI-powered business assistant developed by Indhirakumar</p>
      </header>

      <div className="chat-box">
        {chat.map((msg, i) => (
          <div key={i} className={`message ${msg.role}`}>
            {msg.text}
          </div>
        ))}
        {loading && <div className="typing">Typing...</div>}
        <div ref={chatEndRef} />
      </div>

      <div className="input-area">
        <input
          type="text"
          placeholder="Ask something..."
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          disabled={loading}
        />
        <button onClick={sendMessage} disabled={loading}>
          Send
        </button>
      </div>
    </div>
  );
}

export default App;
