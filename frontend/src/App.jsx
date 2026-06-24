import { useState } from "react";
import PDFUploader from "./components/PDFUploader";
import AgentLogs from "./components/AgentLogs";
import ChatPanel from "./components/ChatPanel";
import "./index.css";

function App() {
  const [uploadedFile, setUploadedFile] = useState(null);
  const [agentLogs, setAgentLogs] = useState([]);
  const [messages, setMessages] = useState([]);
  const [isProcessing, setIsProcessing] = useState(false);

  return (
    <div className="app-container">
      {/* Header */}
      <header className="header">
        <div className="logo">
          <span className="logo-icon">🛡️</span>
          <span className="logo-text">DocuTrust</span>
        </div>
        <span className="header-tag">Enterprise RAG Platform</span>
      </header>

      {/* Main Layout */}
      <main className="main-layout">

        {/* Top Half - PDF Uploader */}
        <section className="top-pane">
          <h2 className="pane-title">📄 Documents</h2>
          <PDFUploader
            uploadedFile={uploadedFile}
            setUploadedFile={setUploadedFile}
          />
        </section>

        {/* Bottom Half - Agent + Chat side by side */}
        <div className="bottom-panes">
          <section className="pane">
            <h2 className="pane-title">🤖 Agent Activity</h2>
            <AgentLogs logs={agentLogs} isProcessing={isProcessing} />
          </section>

          <section className="pane">
            <h2 className="pane-title">💬 Ask Questions</h2>
            <ChatPanel
              messages={messages}
              setMessages={setMessages}
              setAgentLogs={setAgentLogs}
              setIsProcessing={setIsProcessing}
              uploadedFile={uploadedFile}
            />
          </section>
        </div>

      </main>
    </div>
  );
}

export default App;