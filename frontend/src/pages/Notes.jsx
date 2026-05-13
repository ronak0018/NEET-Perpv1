import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { getNotes, getNoteSubjects, deleteNote } from "../api";

export default function Notes() {
  const [notes, setNotes] = useState([]);
  const [subjects, setSubjects] = useState([]);
  const [filter, setFilter] = useState({ subject: "", search: "" });
  const [loading, setLoading] = useState(true);

  const loadNotes = async () => {
    setLoading(true);
    try {
      const params = {};
      if (filter.subject) params.subject = filter.subject;
      if (filter.search) params.search = filter.search;
      const res = await getNotes(params);
      setNotes(res.data);
    } catch {
      console.error("Failed to load notes");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    getNoteSubjects().then((res) => setSubjects(res.data));
  }, []);

  useEffect(() => {
    loadNotes();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [filter.subject]);

  const handleSearch = (e) => {
    e.preventDefault();
    loadNotes();
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Delete this note?")) return;
    try {
      await deleteNote(id);
      loadNotes();
    } catch {
      alert("Failed to delete note");
    }
  };

  return (
    <div>
      <div className="notes-header">
        <h2>Study Notes</h2>
        <Link to="/notes/new" className="btn btn-primary">+ New Note</Link>
      </div>

      <div className="notes-filter">
        <select
          value={filter.subject}
          onChange={(e) => setFilter({ ...filter, subject: e.target.value })}
          style={{ padding: "0.5rem", borderRadius: "8px", border: "2px solid #e0e0e0" }}
        >
          <option value="">All Subjects</option>
          {subjects.map((s) => (
            <option key={s} value={s}>{s}</option>
          ))}
        </select>
        <form onSubmit={handleSearch} style={{ display: "flex", gap: "0.5rem", flex: 1 }}>
          <input
            type="text"
            placeholder="Search notes..."
            value={filter.search}
            onChange={(e) => setFilter({ ...filter, search: e.target.value })}
            style={{ flex: 1, padding: "0.5rem", borderRadius: "8px", border: "2px solid #e0e0e0" }}
          />
          <button type="submit" className="btn btn-primary">Search</button>
        </form>
      </div>

      {loading ? (
        <div className="loading">Loading notes...</div>
      ) : notes.length === 0 ? (
        <div className="empty-state">
          <div className="icon">📖</div>
          <p>No notes found. Create your first note!</p>
        </div>
      ) : (
        <div className="notes-grid">
          {notes.map((note) => (
            <div key={note.id} className="note-card">
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "start" }}>
                <Link to={`/notes/${note.id}`} style={{ textDecoration: "none", color: "inherit", flex: 1 }}>
                  <h3>{note.title}</h3>
                  <div className="note-meta">
                    <span className="tag">{note.subject}</span>
                    <span className="tag">{note.topic}</span>
                  </div>
                </Link>
                <div style={{ display: "flex", gap: "0.4rem" }}>
                  <Link to={`/notes/${note.id}/edit`} className="btn btn-secondary" style={{ padding: "0.3rem 0.7rem", fontSize: "0.85rem" }}>
                    Edit
                  </Link>
                  <button
                    className="btn btn-danger"
                    style={{ padding: "0.3rem 0.7rem", fontSize: "0.85rem" }}
                    onClick={() => handleDelete(note.id)}
                  >
                    Delete
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
