import React from "react";
import { BrowserRouter, Routes, Route, Link, useLocation } from "react-router-dom";
import Home from "./pages/Home.jsx";
import Quiz from "./pages/Quiz.jsx";
import Notes from "./pages/Notes.jsx";
import NoteDetail from "./pages/NoteDetail.jsx";
import NoteForm from "./pages/NoteForm.jsx";
import Exam from "./pages/Exam.jsx";
import "./App.css";

function Navbar() {
  const location = useLocation();
  const isActive = (path) => location.pathname.startsWith(path) ? "active" : "";

  return (
    <nav className="navbar">
      <Link to="/" className="navbar-brand">
        🩺 NEET PG Prep
      </Link>
      <div className="navbar-links">
        <Link to="/quiz" className={isActive("/quiz")}>Quiz</Link>
        <Link to="/exam" className={isActive("/exam")}>Exam</Link>
        <Link to="/notes" className={isActive("/notes")}>Notes</Link>
      </div>
    </nav>
  );
}

function App() {
  return (
    <BrowserRouter>
      <div className="app">
        <Navbar />
        <div className="container">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/quiz" element={<Quiz />} />
            <Route path="/exam" element={<Exam />} />
            <Route path="/notes" element={<Notes />} />
            <Route path="/notes/new" element={<NoteForm />} />
            <Route path="/notes/:id" element={<NoteDetail />} />
            <Route path="/notes/:id/edit" element={<NoteForm />} />
          </Routes>
        </div>
      </div>
    </BrowserRouter>
  );
}

export default App;
