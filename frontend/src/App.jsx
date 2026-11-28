
import { useState } from "react";
import "./App.css";

function getCsrfToken() {
  const cookie = document.cookie
    .split("; ")
    .find((item) => item.startsWith("csrftoken="));

  return cookie ? cookie.split("=")[1] : "";
}

async function readApiResponse(response) {
  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    throw new Error(
      data.detail ||
      data.error ||
      data.file?.[0] ||
      `Request failed (${response.status})`
    );
  }

  return data;
}


function App() {
  const [file, setFile] = useState(null);
  const [question, setQuestion] = useState("");
  const [message, setMessage] = useState("");
  const [dragging, setDragging] = useState(false);
  const [documentId, setDocumentId] = useState(null);
    const [answer, setAnswer] = useState("");
const [sources, setSources] = useState([]);
const [uploading, setUploading] = useState(false);
const [asking, setAsking] = useState(false);

  const suggestions = [
    "Summarize this document",
    "What are the key points?",
    "Explain the main topics"
  ];

  
const handleFile = async (selectedFile) => {
  if (!selectedFile) return;

  setFile(null);
  setDocumentId(null);
  setAnswer("");
  setSources([]);

  if (!selectedFile.name.toLowerCase().endsWith(".pdf")) {
    setMessage("Please select a PDF file.");
    return;
  }

  if (selectedFile.size > 10 * 1024 * 1024) {
    setMessage("File must be smaller than 10 MB.");
    return;
  }

  setFile(selectedFile);
  setUploading(true);
  setMessage("Uploading and processing PDF...");

  try {
    const formData = new FormData();
    formData.append("title", selectedFile.name);
    formData.append("file", selectedFile);

    const response = await fetch("/api/documents/", {
      method: "POST",
      credentials: "same-origin",
      headers: {
        "X-CSRFToken": getCsrfToken(),
      },
      body: formData,
    });

    const data = await readApiResponse(response);

    setDocumentId(data.id);
    setMessage("PDF uploaded and processed successfully!");
  } catch (error) {
    setMessage("Upload failed: " + error.message);
  } finally {
    setUploading(false);
  }
};


   
const handleAsk = async (event) => {
  event.preventDefault();

  if (!documentId) {
    setMessage("Please upload and process a PDF first.");
    return;
  }

  if (!question.trim()) {
    setMessage("Please enter a question.");
    return;
  }

  setAsking(true);
  setAnswer("");
  setSources([]);
  setMessage("Generating your AI answer...");

  try {
    const response = await fetch("/api/ask/", {
      method: "POST",
      credentials: "same-origin",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCsrfToken(),
      },
      body: JSON.stringify({
        document_id: documentId,
        question: question,
      }),
    });

    const data = await readApiResponse(response);

    setAnswer(data.answer || "No answer generated.");
    setSources([...new Set(data.sources || [])]);
    setMessage("");
  } catch (error) {
    setMessage("Error: " + error.message);
  } finally {
    setAsking(false);
  }
};


  return (
    <div className="app-layout">

      {/* Sidebar */}
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon">✦</div>
          <div>
            <h2>DocuMind</h2>
            <span>AI DOCUMENT ASSISTANT</span>
          </div>
        </div>

        <div className="sidebar-section">
          <p className="sidebar-label">YOUR WORKSPACE</p>
          <div className="nav-active">▦ &nbsp; Dashboard</div>
        </div>

        <div className="sidebar-bottom">
          <div className="status-dot"></div>
          <span>Personal Workspace</span>
          <p>Built with Django + React + RAG</p>
        </div>
      </aside>

      {/* Main Content */}
      <main className="main-content">

        <div className="topbar">
          <div>
            <span className="eyebrow">YOUR AI WORKSPACE</span>
            <h1>Document Dashboard</h1>
          </div>
          <span className="top-badge">✦ Powered by AI</span>
        </div>

        {/* Welcome Banner */}
        <div className="hero">
          <div className="hero-content">
            <span className="hero-tag">✦ SMART DOCUMENT ANALYSIS</span>
            <h2>Your documents, understood.</h2>
            <p>
              Upload a PDF, ask questions, and discover
              insights using the power of AI.
            </p>
          </div>
          <div className="hero-art">✧</div>
        </div>

        <div className="content-grid">

          <div className="left-column">

            {/* Upload */}
            <section className="card">
              <div className="section-heading">
                <div className="section-icon">📄</div>
                <div>
                  <h3>Upload Document</h3>
                  <p>Choose a PDF to get started</p>
                </div>
              </div>

              <label
                className={`upload-zone ${dragging ? "dragging" : ""}`}
                onDragOver={(e) => {
                  e.preventDefault();
                  setDragging(true);
                }}
                onDragLeave={() => setDragging(false)}
                onDrop={(e) => {
                  e.preventDefault();
                  setDragging(false);
                  handleFile(e.dataTransfer.files[0]);
                }}
              >
                <input
                  type="file"
                  accept=".pdf,application/pdf"
                  onChange={(e) => handleFile(e.target.files[0])}
                  hidden
                />
                <div className="upload-icon">☁</div>
                <strong>Click or drag your PDF here</strong>
                <p>PDF files only · Maximum 10 MB</p>
                <span className="upload-button">Browse Files</span>
              </label>

              {file && (
                <div className="selected-file">
                  <span>📄 {file.name}</span>
                  <span className="ready"> {uploading ? "Processing..." : documentId ? "Ready ✓" : "Not ready"}</span>
                </div>
              )}
            </section>

            {/* Ask Question */}
            <section className="card">
              <div className="section-heading">
                <div className="section-icon">✦</div>
                <div>
                  <h3>Ask Your Document</h3>
                  <p>Get answers from your PDF</p>
                </div>
              </div>

              <form onSubmit={handleAsk}>
                <textarea
                  placeholder="What would you like to know about this document?"
                  value={question}
                  onChange={(e) => setQuestion(e.target.value)}
                  rows="4"
                />

                <p className="suggestion-title">TRY ASKING</p>

                <div className="suggestions">
                  {suggestions.map((item) => (
                    <button
                      key={item}
                      type="button"
                      className="suggestion"
                      onClick={() => setQuestion(item)}
                    >
                      {item}
                    </button>
                  ))}
                </div>

                <button type="submit" className="ask-button" disabled={uploading || asking}>
                  {asking ? "Generating Answer..." : "✦ Ask DocuMind AI"}
                </button>
              </form>

              {message && (
                <p className="notification" role="status">{message}</p>
              )}
            </section>
          </div>

          <div className="right-column">

            {/* AI Answer */}
            <section className="card answer-card">
                {answer ? (
                <div className="answer-result">
                <p>{answer}</p>

                {sources.length > 0 && (
                <small>Source pages: {sources.join(", ")}</small>
                 )}
                 </div>
                ) : (
                <div className="empty-answer">
                     <div className="empty-icon">✦</div>
                    <h3>Ready when you are</h3>
                    <p>
                    Upload a document and ask a question
                    to get an AI-powered answer.
                    </p>
                </div>
                )}

            </section>

            {/* Guide */}
            <section className="card guide-card">
              <h3>How it works</h3>

              <div className="guide-step">
                <span>01</span>
                <div>
                  <strong>Upload</strong>
                  <p>Select your PDF document.</p>
                </div>
              </div>

              <div className="guide-step">
                <span>02</span>
                <div>
                  <strong>Ask</strong>
                  <p>Enter a question about the PDF.</p>
                </div>
              </div>

              <div className="guide-step">
                <span>03</span>
                <div>
                  <strong>Discover</strong>
                  <p>Receive an AI-generated answer.</p>
                </div>
              </div>
            </section>

          </div>
        </div>

        <footer>
          DocuMind AI · Built with React, Django & Gemini
        </footer>
      </main>
    </div>
  );
}

export default App;
