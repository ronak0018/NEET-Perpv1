import React, { useState, useEffect, useRef } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { getDetailedStudySubjects, getDetailedStudyContent } from "../api";

const SUBJECT_ICONS = {
  Anatomy: "🦴", Surgery: "🔪", Radiology: "📡", Psychiatry: "🧠",
  Anaesthesia: "💉", Physiology: "🫀", Pharmacology: "💊", Pathology: "🔬",
  Microbiology: "🦠", Biochemistry: "🧬", "Forensic Medicine": "⚖️",
  PSM: "🏥", Medicine: "🩺", Ophthalmology: "👁️", ENT: "👂",
  Dermatology: "🧴", Orthopaedics: "🦿", Paediatrics: "👶",
  "Obstetrics & Gynaecology": "🤰",
};

export default function DetailedStudy() {
  const [subjects, setSubjects] = useState([]);
  const [active, setActive] = useState(null);
  const [content, setContent] = useState("");
  const [loading, setLoading] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [searchTerm, setSearchTerm] = useState("");
  const contentRef = useRef(null);

  useEffect(() => {
    getDetailedStudySubjects().then((res) => setSubjects(res.data));
  }, []);

  const loadSubject = async (subject) => {
    setActive(subject);
    setSidebarOpen(false);
    setLoading(true);
    try {
      const res = await getDetailedStudyContent(subject);
      setContent(res.data.content);
    } catch {
      setContent("Failed to load content.");
    } finally {
      setLoading(false);
      if (contentRef.current) contentRef.current.scrollTop = 0;
    }
  };

  const filteredSubjects = subjects.filter((s) =>
    s.toLowerCase().includes(searchTerm.toLowerCase())
  );

  // Build table-of-contents from markdown headings
  const toc = [];
  if (content) {
    const lines = content.split("\n");
    for (const line of lines) {
      const m = line.match(/^(#{1,3})\s+(.+)/);
      if (m) {
        const level = m[1].length;
        const text = m[2].replace(/\*\*/g, "").trim();
        const id = text.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/-+$/, "");
        toc.push({ level, text, id });
      }
    }
  }

  const scrollToHeading = (id) => {
    const el = document.getElementById(id);
    if (el) el.scrollIntoView({ behavior: "smooth", block: "start" });
  };

  return (
    <div className="ds-page">
      {/* Mobile hamburger */}
      <button className="ds-hamburger" onClick={() => setSidebarOpen(!sidebarOpen)}>
        {sidebarOpen ? "✕" : "☰"} Subjects
      </button>

      {/* Sidebar */}
      <aside className={`ds-sidebar ${sidebarOpen ? "open" : ""}`}>
        <h3 className="ds-sidebar-title">📚 Subjects</h3>
        <input
          className="ds-search"
          type="text"
          placeholder="Filter subjects..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
        <ul className="ds-subject-list">
          {filteredSubjects.map((s) => (
            <li key={s}>
              <button
                className={`ds-subject-btn ${active === s ? "active" : ""}`}
                onClick={() => loadSubject(s)}
              >
                <span className="ds-icon">{SUBJECT_ICONS[s] || "📖"}</span>
                {s}
              </button>
            </li>
          ))}
        </ul>
      </aside>

      {/* Main content area */}
      <main className="ds-main" ref={contentRef}>
        {!active && !loading && (
          <div className="ds-welcome">
            <div className="ds-welcome-icon">📖</div>
            <h2>Detailed Study</h2>
            <p>Select a subject from the sidebar to start reading comprehensive NEET PG notes.</p>
            <div className="ds-subject-grid">
              {subjects.map((s) => (
                <button key={s} className="ds-subject-card" onClick={() => loadSubject(s)}>
                  <span className="ds-card-icon">{SUBJECT_ICONS[s] || "📖"}</span>
                  <span className="ds-card-label">{s}</span>
                </button>
              ))}
            </div>
          </div>
        )}

        {loading && <div className="ds-loading"><div className="ds-spinner" />Loading...</div>}

        {active && !loading && (
          <>
            {/* Floating TOC (desktop) */}
            {toc.length > 0 && (
              <details className="ds-toc">
                <summary>Table of Contents</summary>
                <ul>
                  {toc.slice(0, 60).map((t, i) => (
                    <li key={i} className={`ds-toc-l${t.level}`}>
                      <button onClick={() => scrollToHeading(t.id)}>{t.text}</button>
                    </li>
                  ))}
                </ul>
              </details>
            )}
            <div className="ds-content-body">
              <ReactMarkdown
                remarkPlugins={[remarkGfm]}
                components={{
                  h1: ({ children, ...props }) => {
                    const id = String(children).toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/-+$/, "");
                    return <h1 id={id} {...props}>{children}</h1>;
                  },
                  h2: ({ children, ...props }) => {
                    const id = String(children).toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/-+$/, "");
                    return <h2 id={id} {...props}>{children}</h2>;
                  },
                  h3: ({ children, ...props }) => {
                    const id = String(children).toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/-+$/, "");
                    return <h3 id={id} {...props}>{children}</h3>;
                  },
                }}
              />
            </div>
            <button className="ds-back-top" onClick={() => contentRef.current?.scrollTo({ top: 0, behavior: "smooth" })}>
              ↑ Top
            </button>
          </>
        )}
      </main>
    </div>
  );
}
