import { useState, useRef, useEffect } from "react";
import { Send, AlertCircle } from "lucide-react";
import { askQuestion, uploadPDF } from "../services/api";

function ChatPanel({ messages, setMessages, setAgentLogs, setIsProcessing, uploadedFile }) {
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [uploaded, setUploaded] = useState(false);
  const bottomRef = useRef(null);

  // Auto scroll to bottom
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // Upload PDF when file changes
  useEffect(() => {
    if (uploadedFile) {
      handleUpload();
    }
  }, [uploadedFile]);

  const handleUpload = async () => {
    try {
      await uploadPDF(uploadedFile);
      setUploaded(true);
    } catch (error) {
      console.error("Upload failed:", error);
      setUploaded(false);
    }
  };

  const handleSend = async () => {
    if (!question.trim() || !uploaded) return;

    const userMessage = { role: "user", content: question };
    setMessages((prev) => [...prev, userMessage]);
    setQuestion("");
    setLoading(true);
    setIsProcessing(true);
    setAgentLogs([]);

    try {
      const result = await askQuestion(question);

      // Set agent logs from backend
      setAgentLogs(result.steps.map((step) => ({
        ...step,
        time: new Date().toLocaleTimeString(),
      })));

      // Set AI response
      const aiMessage = {
        role: "assistant",
        content: result.answer,
        citations: result.citations,
      };
      setMessages((prev) => [...prev, aiMessage]);

    } catch (error) {
      const errorMessage = {
        role: "assistant",
        content: "Something went wrong. Please try again!",
        citations: [],
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
      setIsProcessing(false);
    }
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
            <p className="chat-empty-hint">
              {uploaded ? "PDF ready! Ask your question." : "Upload a PDF first"}
            </p>
          </div>
        )}

        {messages.map((msg, index) => (
          <div key={index} className={`message message-${msg.role}`}>
            <span className="message-label">
              {msg.role === "user" ? "🧑 You" : "🤖 DocuTrust"}
            </span>
            <p className="message-content">{msg.content}</p>

            
          </div>
        ))}

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
        {!uploaded && uploadedFile && (
          <p className="chat-warning">⏳ Uploading PDF to backend...</p>
        )}
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
            disabled={loading}
          />
          <button
            className="chat-send-btn"
            onClick={handleSend}
            disabled={loading ||!question.trim()}
          >
            <Send size={18} />
          </button>
        </div>
      </div>
    </div>
  );
}

export default ChatPanel;