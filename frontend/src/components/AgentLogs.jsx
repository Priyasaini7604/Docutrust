import { useEffect, useRef } from "react";

const stepIcons = {
  retrieve: "🔍",
  grade: "⚖️",
  rewrite: "✏️",
  websearch: "🌐",
  generate: "✅",
  error: "❌",
};

function AgentLogs({ logs, isProcessing }) {
  const bottomRef = useRef(null);

  // Auto scroll to bottom jab naya log aaye
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [logs]);

  return (
    <div className="logs-container">
      {/* Empty state */}
      {logs.length === 0 && !isProcessing && (
        <div className="logs-empty">
          <span className="logs-empty-icon">🤖</span>
          <p>Agent activity will appear here</p>
          <p className="logs-empty-hint">Upload a PDF and ask a question</p>
        </div>
      )}

      {/* Processing indicator */}
      {isProcessing && logs.length === 0 && (
        <div className="logs-thinking">
          <span className="thinking-dot" />
          <span className="thinking-dot" />
          <span className="thinking-dot" />
          <p>Agent is thinking...</p>
        </div>
      )}

      {/* Logs list */}
      {logs.map((log, index) => (
        <div key={index} className={`log-item log-${log.type}`}>
          <div className="log-header">
            <span className="log-icon">{stepIcons[log.type] || "📌"}</span>
            <span className="log-step">{log.step}</span>
            <span className="log-time">{log.time}</span>
          </div>
          {log.message && (
            <p className="log-message">{log.message}</p>
          )}
        </div>
      ))}

      {/* Processing spinner at bottom */}
      {isProcessing && logs.length > 0 && (
        <div className="logs-thinking">
          <span className="thinking-dot" />
          <span className="thinking-dot" />
          <span className="thinking-dot" />
        </div>
      )}

      <div ref={bottomRef} />
    </div>
  );
}

export default AgentLogs;