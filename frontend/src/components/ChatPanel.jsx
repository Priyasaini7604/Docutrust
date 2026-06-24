import { useState, useRef, useEffect } from "react";
import { Send, AlertCircle } from "lucide-react";

function ChatPanel({ messages, setMessages, setAgentLogs, setIsProcessing, uploadedFile }) {
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef(null);

  // Auto scroll to bottom
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = async () => {
    if (!question.trim()) return;
    if (!uploadedFile) {
      alert("Pehle PDF upload karo!");
      return;
    }

    const userMessage = { role: "user", content: question };
    setMessages((prev) => [...prev, userMessage]);
    setQuestion("");
    setLoading(true);
    setIsProcessing(true);
    setAgentLogs([]);

    // Dummy agent logs for now (backend se aayenge baad mein)
    const dummyLogs = [
      { type: "retrieve", step: "Retrieving chunks", message: "Searching relevant document sections...", time: now() },
      { type: "grade", step: "Grading relevance", message: "Checking if chunks are relevant to query...", time: now() },
      { type: "generate", step: "Generating answer", message: "Producing final answer with citations...", time: now() },
    ];

    // Simulate step by step logs
    for (let i = 0; i < dummyLogs.length; i++) {
      await delay(1000);
      setAgentLogs((prev) => [...prev, dummyLogs[i]]);
    }

    // Dummy answer
    await delay(1000);
    const aiMessage = {
      role: "assistant",
      content: "This is a dummy answer. Backend connect hone ke baad real answer aayega!",
      citations: [
        { page: 2, text: "Relevant section from your document will appear here." },
      ],
    };

    setMessages((prev) => [...prev, aiMessage]);
    setLoading(false);
    setIsProcessing(false);
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="chat-container">
      {/* Messages Area */}
      <div className="chat-messages">
        {messages.length === 0 && (
          <div className="chat-empty">
            <span className="chat-empty-icon">💬</span>
            <p>Ask anything about your document</p>
            <p className="chat-empty-hint">Upload a PDF first, then type your question</p>
          </div>
        )}

        {messages.map((msg, index) => (
          <div key={index} className={`message message-${msg.role}`}>
            {/* Label */}
            <span className="message-label">
              {msg.role === "user" ? "🧑 You" : "🤖 DocuTrust"}
            </span>

            {/* Content */}
            <p className="message-content">{msg.content}</p>

            {/* Citations */}
            {msg.citations && msg.citations.length > 0 && (
              <div className="citations">
                {msg.citations.map((cite, i) => (
                  <div key={i} className="citation-item">
                    <AlertCircle size={12} color="#4f8ef7" />
                    <span className="citation-page">Page {cite.page}:</span>
                    <span className="citation-text">{cite.text}</span>
                  </div>
                ))}
              </div>
            )}
          </div>
        ))}

        {/* Loading bubble */}
        {loading && (
          <div className="message message-assistant">
            <span className="message-label">🤖 DocuTrust</span>
            <div className="message-loading">
              <span className="thinking-dot" />
              <span className="thinking-dot" />
              <span className="thinking-dot" />
            </div>
          </div>
        )}

        <div ref={bottomRef} />
      </div>

      {/* Input Area */}
      <div className="chat-input-area">
        {!uploadedFile && (
          <p className="chat-warning">⚠️ Upload a PDF to start asking questions</p>
        )}
        <div className="chat-input-row">
          <textarea
            className="chat-input"
            placeholder="Ask a question about your document..."
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={handleKeyDown}
            rows={2}
            disabled={loading || !uploadedFile}
          />
          <button
            className="chat-send-btn"
            onClick={handleSend}
            disabled={loading || !uploadedFile || !question.trim()}
          >
            <Send size={18} />
          </button>
        </div>
      </div>
    </div>
  );
}

// Helper functions
const delay = (ms) => new Promise((res) => setTimeout(res, ms));
const now = () => new Date().toLocaleTimeString();

export default ChatPanel;