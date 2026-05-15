import React, { useState, useEffect, useRef } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { getMasterNotesSubjects, getMasterNoteContent } from "../api";

const SUBJECT_ICONS = {
  Anatomy: "🦴", Surgery: "🔪", Radiology: "📡", Psychiatry: "🧠",
  Anaesthesia: "💉", Physiology: "🫀", Pharmacology: "💊", Pathology: "🔬",
  Microbiology: "🦠", Biochemistry: "🧬", "Forensic Medicine": "⚖️",
  PSM: "🏥", Medicine: "🩺", Ophthalmology: "👁️", ENT: "👂",
  Dermatology: "🧴", Orthopaedics: "🦿", Paediatrics: "👶",
  "Obstetrics & Gynaecology": "🤰",
};

export default function MasterNotes() {
  const [subjects, setSubjects] = useState([]);
  const [active, setActive] = useState(null);
  const [content, setContent] = useState("");
  const [loading, setLoading] = useState(false);
  const [searchTerm, setSearchTerm] = useState("");
  const [fontSize, setFontSize] = useState(16);
  const contentRef = useRef(null);

  useEffect(() => {
    getMasterNotesSubjects().then((res) => setSubjects(res.data));
  }, []);

  const loadSubject = async (subject) => {
    setActive(subject);
    setLoading(true);
    try {
      const res = await getMasterNoteContent(subject);
      setContent(res.data.content);
    } catch {
      setContent("Failed to load notes.");
    } finally {
      setLoading(false);
      if (contentRef.current) contentRef.current.scrollTop = 0;
    }
  };

  const filteredSubjects = subjects.filter((s) =>
    s.toLowerCase().includes(searchTerm.toLowerCase())
  );

  // Build table-of-contents from headings
  const toc = [];
  if (content) {
    for (const line of content.split("\n")) {
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
    <div className="mn-page">
      {/* Subject selector panel */}
      {!active && (
        <div className="mn-home">
          <div className="mn-hero">
            <h1>📚 Master Notes</h1>
            <p>Comprehensive, high-yield study notes for NEET PG preparation. Select a subject to start reading.</p>
          </div>
          <input
            className="mn-filter"
            type="text"
            placeholder="🔍 Search subjects..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
          <div className="mn-grid">
            {filteredSubjects.map((s) => (
              <button key={s} className="mn-card" onClick={() => loadSubject(s)}>
                <span className="mn-card-icon">{SUBJECT_ICONS[s] || "📖"}</span>
                <span className="mn-card-label">{s}</span>
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Reading view */}
      {active && (
        <div className="mn-reader">
          {/* Top bar */}
          <div className="mn-topbar">
            <button className="mn-back-btn" onClick={() => { setActive(null); setContent(""); }}>
              ← Back
            </button>
            <h2 className="mn-title">
              {SUBJECT_ICONS[active] || "📖"} {active}
            </h2>
            <div className="mn-controls">
              <button onClick={() => setFontSize((f) => Math.max(12, f - 2))} title="Decrease font">A-</button>
              <span className="mn-font-size">{fontSize}px</span>
              <button onClick={() => setFontSize((f) => Math.min(24, f + 2))} title="Increase font">A+</button>
            </div>
          </div>

          {loading && <div className="mn-loading"><div className="mn-spinner" />Loading notes...</div>}

          {!loading && (
            <div className="mn-content-wrapper">
              {/* Table of Contents sidebar */}
              {toc.length > 0 && (
                <aside className="mn-toc">
                  <h4>Contents</h4>
                  <ul>
                    {toc.slice(0, 80).map((t, i) => (
                      <li key={i} className={`mn-toc-l${t.level}`}>
                        <button onClick={() => scrollToHeading(t.id)}>{t.text}</button>
                      </li>
                    ))}
                  </ul>
                </aside>
              )}

              {/* Main reading pane */}
              <div className="mn-reading-pane" ref={contentRef} style={{ fontSize: `${fontSize}px` }}>
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
                    table: ({ children, ...props }) => (
                      <div className="mn-table-wrap"><table {...props}>{children}</table></div>
                    ),
                  }}
                />
              </div>
            </div>
          )}

          {/* Back to top */}
          <button
            className="mn-top-btn"
            onClick={() => contentRef.current?.scrollTo({ top: 0, behavior: "smooth" })}
          >
            ↑ Top
          </button>
        </div>
      )}
    </div>
  );
}
