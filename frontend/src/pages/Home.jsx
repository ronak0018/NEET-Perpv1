import React from "react";
import { Link } from "react-router-dom";

export default function Home() {
  return (
    <div className="home">
      <h1>NEET PG Prep</h1>
      <p>Your complete preparation companion for NEET PG examination</p>
      <div className="home-cards">
        <Link to="/quiz" className="home-card">
          <div className="icon">📝</div>
          <h3>Practice Quiz</h3>
          <p>Test your knowledge with subject-wise MCQs with explanations</p>
        </Link>
        <Link to="/exam" className="home-card">
          <div className="icon">🏥</div>
          <h3>Mock Exam</h3>
          <p>Full 200-question NEET PG simulation with 3:30 hr timer and scoring</p>
        </Link>
        <Link to="/notes" className="home-card">
          <div className="icon">📖</div>
          <h3>Study Notes</h3>
          <p>Browse and create high-yield revision notes</p>
        </Link>
        <Link to="/study" className="home-card">
          <div className="icon">📚</div>
          <h3>Detailed Study</h3>
          <p>Comprehensive chapter-wise master notes for deep learning</p>
        </Link>
      </div>
    </div>
  );
}
