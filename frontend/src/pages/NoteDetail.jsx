import React, { useState, useEffect } from "react";
import { useParams, Link, useNavigate } from "react-router-dom";
import { getNote, deleteNote } from "../api";

const TABS = [
  { key: "full_notes", label: "📝 Full Notes" },
  { key: "mnemonics", label: "🧠 Mnemonics" },
  { key: "clinical_concepts", label: "🏥 Clinical Concepts" },
  { key: "mcqs", label: "❓ MCQs" },
  { key: "rapid_revision", label: "⚡ Rapid Revision" },
];

export default function NoteDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [note, setNote] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState("full_notes");

  useEffect(() => {
    const load = async () => {
      try {
        const res = await getNote(id);
        setNote(res.data);
      } catch {
        alert("Note not found");
        navigate("/notes");
      } finally {
        setLoading(false);
      }
    };
    load();
  }, [id, navigate]);

  const handleDelete = async () => {
    if (!window.confirm("Delete this note?")) return;
    try {
      await deleteNote(id);
      navigate("/notes");
    } catch {
      alert("Failed to delete note");
    }
  };

  if (loading) return <div className="loading">Loading...</div>;
  if (!note) return null;

  return (
    <div className="note-detail">
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "start", marginBottom: "1rem" }}>
        <div>
          <h1>{note.chapter}</h1>
          <div className="note-meta">
            <span className="tag">{note.subject}</span>
          </div>
        </div>

      </div>

      <div className="note-tabs" style={{ display: "flex", gap: "0.3rem", flexWrap: "wrap", marginBottom: "1.5rem", borderBottom: "2px solid #e0e0e0", paddingBottom: "0.5rem" }}>
        {TABS.map((tab) => (
          <button
            key={tab.key}
            className={`btn ${activeTab === tab.key ? "btn-primary" : "btn-secondary"}`}
            style={{ fontSize: "0.85rem", padding: "0.4rem 0.8rem" }}
            onClick={() => setActiveTab(tab.key)}
          >
            {tab.label}
          </button>
        ))}
      </div>

      <div className="note-content" style={{ whiteSpace: "pre-wrap", lineHeight: "1.7", fontSize: "1rem" }}>
        {note[activeTab] || "No content for this section."}
      </div>

      <div style={{ marginTop: "2rem" }}>
        <Link to="/notes" className="btn btn-secondary">← Back to Notes</Link>
      </div>
    </div>
  );
}
