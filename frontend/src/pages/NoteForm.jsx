import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { createNote, getNote, updateNote } from "../api";

export default function NoteForm() {
  const { id } = useParams();
  const navigate = useNavigate();
  const isEdit = Boolean(id);
  const [form, setForm] = useState({ subject: "", topic: "", title: "", content: "" });
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (isEdit) {
      getNote(id).then((res) => setForm(res.data));
    }
  }, [id, isEdit]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!form.subject || !form.topic || !form.title || !form.content) {
      alert("Please fill all fields");
      return;
    }
    setLoading(true);
    try {
      if (isEdit) {
        await updateNote(id, {
          subject: form.subject,
          topic: form.topic,
          title: form.title,
          content: form.content,
        });
      } else {
        await createNote(form);
      }
      navigate("/notes");
    } catch {
      alert("Failed to save note");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="note-form">
      <h2>{isEdit ? "Edit Note" : "Create New Note"}</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Subject</label>
          <input
            type="text"
            value={form.subject}
            onChange={(e) => setForm({ ...form, subject: e.target.value })}
            placeholder="e.g., Anatomy, Physiology"
          />
        </div>
        <div className="form-group">
          <label>Topic</label>
          <input
            type="text"
            value={form.topic}
            onChange={(e) => setForm({ ...form, topic: e.target.value })}
            placeholder="e.g., Brachial Plexus, Cardiac Cycle"
          />
        </div>
        <div className="form-group">
          <label>Title</label>
          <input
            type="text"
            value={form.title}
            onChange={(e) => setForm({ ...form, title: e.target.value })}
            placeholder="Note title"
          />
        </div>
        <div className="form-group">
          <label>Content</label>
          <textarea
            value={form.content}
            onChange={(e) => setForm({ ...form, content: e.target.value })}
            placeholder="Write your notes here..."
          />
        </div>
        <div className="form-actions">
          <button type="submit" className="btn btn-success" disabled={loading}>
            {loading ? "Saving..." : isEdit ? "Update Note" : "Create Note"}
          </button>
          <button type="button" className="btn btn-secondary" onClick={() => navigate("/notes")}>
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
}
