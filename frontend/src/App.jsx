import React, { useEffect, useState } from "react";
import { BrowserRouter, Routes, Route, Link, useLocation } from "react-router-dom";
import Home from "./pages/Home.jsx";
import Quiz from "./pages/Quiz.jsx";
import Notes from "./pages/Notes.jsx";
import NoteDetail from "./pages/NoteDetail.jsx";
import NoteForm from "./pages/NoteForm.jsx";
import Exam from "./pages/Exam.jsx";
import DetailedStudy from "./pages/DetailedStudy.jsx";
import MasterNotes from "./pages/MasterNotes.jsx";
import Admin from "./pages/Admin.jsx";
import Login from "./pages/Login.jsx";
import { trackActivity } from "./api";
import "./App.css";

function Navbar({ user, onLogout }) {
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
        <Link to="/notes" className={isActive("/notes")}>Short Notes</Link>
        <Link to="/master-notes" className={isActive("/master-notes")}>Master Notes</Link>
        <Link to="/study" className={isActive("/study")}>Study</Link>
      </div>
      <div className="navbar-user">
        <span className="navbar-username">👤 {user}</span>
        <button className="navbar-logout" onClick={onLogout}>Logout</button>
      </div>
    </nav>
  );
}

function PageTracker() {
  const location = useLocation();
  const currentUser = localStorage.getItem("neetpg_user") || "";
  useEffect(() => {
    trackActivity("page_view", location.pathname, currentUser);
  }, [location.pathname]);
  return null;
}

function App() {
  const [user, setUser] = useState(() => localStorage.getItem("neetpg_user") || "");

  const handleLogin = (username) => {
    localStorage.setItem("neetpg_user", username);
    setUser(username);
  };

  const handleLogout = () => {
    localStorage.removeItem("neetpg_user");
    setUser("");
  };

  if (!user) {
    return <Login onLogin={handleLogin} />;
  }

  return (
    <BrowserRouter>
      <div className="app">
        <Navbar user={user} onLogout={handleLogout} />
        <PageTracker />
        <div className="container">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/quiz" element={<Quiz />} />
            <Route path="/exam" element={<Exam />} />
            <Route path="/notes" element={<Notes />} />
            <Route path="/notes/new" element={<NoteForm />} />
            <Route path="/notes/:id" element={<NoteDetail />} />
            <Route path="/notes/:id/edit" element={<NoteForm />} />
            <Route path="/master-notes" element={<MasterNotes />} />
            <Route path="/study" element={<DetailedStudy />} />
            <Route path="/admin" element={<Admin />} />
          </Routes>
        </div>
      </div>
    </BrowserRouter>
  );
}

export default App;
