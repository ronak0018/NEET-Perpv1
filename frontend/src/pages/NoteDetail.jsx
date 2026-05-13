import React, { useState, useEffect } from "react";
import { useParams, Link, useNavigate } from "react-router-dom";
import { getNote, deleteNote } from "../api";

export default function NoteDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [note, setNote] = useState(null);
  const [loading, setLoading] = useState(true);

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
          <h1>{note.title}</h1>
          <div className="note-meta">
            <span className="tag">{note.subject}</span>
            <span className="tag">{note.topic}</span>
          </div>
        </div>
        <div style={{ display: "flex", gap: "0.5rem" }}>
          <Link to={`/notes/${id}/edit`} className="btn btn-primary">Edit</Link>
          <button className="btn btn-danger" onClick={handleDelete}>Delete</button>
        </div>
      </div>
      <div className="note-content">{note.content}</div>
      <div style={{ marginTop: "2rem" }}>
        <Link to="/notes" className="btn btn-secondary">← Back to Notes</Link>
      </div>
    </div>
  );
}
