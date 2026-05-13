import React, { useState, useEffect, useCallback } from "react";
import { getSubjects, getTopics, getQuiz, submitQuiz } from "../api";

export default function Quiz() {
  const [phase, setPhase] = useState("setup"); // setup | quiz | results
  const [subjects, setSubjects] = useState([]);
  const [topics, setTopics] = useState([]);
  const [filters, setFilters] = useState({ subject: "", topic: "", difficulty: "", count: 10 });
  const [questions, setQuestions] = useState([]);
  const [current, setCurrent] = useState(0);
  const [answers, setAnswers] = useState({});
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    getSubjects().then((res) => setSubjects(res.data));
  }, []);

  const loadTopics = useCallback(async (subject) => {
    if (subject) {
      const res = await getTopics(subject);
      setTopics(res.data);
    } else {
      setTopics([]);
    }
  }, []);

  const startQuiz = async () => {
    setLoading(true);
    try {
      const params = {};
      if (filters.subject) params.subject = filters.subject;
      if (filters.topic) params.topic = filters.topic;
      if (filters.difficulty) params.difficulty = filters.difficulty;
      params.count = filters.count;
      const res = await getQuiz(params);
      if (res.data.length === 0) {
        alert("No questions found for selected filters. Try different options.");
        return;
      }
      setQuestions(res.data);
      setAnswers({});
      setCurrent(0);
      setPhase("quiz");
    } catch {
      alert("Failed to load quiz. Make sure the backend is running.");
    } finally {
      setLoading(false);
    }
  };

  const selectAnswer = (qIndex, optIndex) => {
    setAnswers({ ...answers, [qIndex]: optIndex });
  };

  const handleSubmit = async () => {
    const submissions = questions.map((q, i) => ({
      question_id: q.id,
      selected_answer: answers[i] !== undefined ? answers[i] : -1,
    }));
    setLoading(true);
    try {
      const res = await submitQuiz(submissions);
      setResults(res.data);
      setPhase("results");
    } catch {
      alert("Failed to submit quiz.");
    } finally {
      setLoading(false);
    }
  };

  const resetQuiz = () => {
    setPhase("setup");
    setQuestions([]);
    setAnswers({});
    setResults(null);
    setCurrent(0);
  };

  // Setup Phase
  if (phase === "setup") {
    return (
      <div className="quiz-setup">
        <h2>Start a Quiz</h2>
        <div className="form-group">
          <label>Subject</label>
          <select
            value={filters.subject}
            onChange={(e) => {
              setFilters({ ...filters, subject: e.target.value, topic: "" });
              loadTopics(e.target.value);
            }}
          >
            <option value="">All Subjects</option>
            {subjects.map((s) => (
              <option key={s} value={s}>{s}</option>
            ))}
          </select>
        </div>
        <div className="form-group">
          <label>Topic</label>
          <select
            value={filters.topic}
            onChange={(e) => setFilters({ ...filters, topic: e.target.value })}
          >
            <option value="">All Topics</option>
            {topics.map((t) => (
              <option key={t} value={t}>{t}</option>
            ))}
          </select>
        </div>
        <div className="form-group">
          <label>Difficulty</label>
          <select
            value={filters.difficulty}
            onChange={(e) => setFilters({ ...filters, difficulty: e.target.value })}
          >
            <option value="">All Levels</option>
            <option value="easy">Easy</option>
            <option value="medium">Medium</option>
            <option value="hard">Hard</option>
          </select>
        </div>
        <div className="form-group">
          <label>Number of Questions</label>
          <select
            value={filters.count}
            onChange={(e) => setFilters({ ...filters, count: Number(e.target.value) })}
          >
            <option value={5}>5</option>
            <option value={10}>10</option>
            <option value={20}>20</option>
            <option value={30}>30</option>
          </select>
        </div>
        <button className="btn btn-primary" onClick={startQuiz} disabled={loading}>
          {loading ? "Loading..." : "Start Quiz"}
        </button>
      </div>
    );
  }

  // Quiz Phase
  if (phase === "quiz") {
    const q = questions[current];
    const progress = ((current + 1) / questions.length) * 100;
    const answeredCount = Object.keys(answers).length;

    return (
      <div className="quiz-question">
        <div className="quiz-progress">
          <span>Question {current + 1} of {questions.length}</span>
          <span>{answeredCount} answered</span>
        </div>
        <div className="progress-bar">
          <div className="progress-fill" style={{ width: `${progress}%` }} />
        </div>
        <div style={{ marginBottom: "0.5rem" }}>
          <span className="tag">{q.subject}</span>{" "}
          <span className="tag">{q.topic}</span>{" "}
          <span className="tag">{q.difficulty}</span>
        </div>
        <h3>{q.question}</h3>
        <div className="options">
          {q.options.map((opt, i) => (
            <div
              key={i}
              className={`option ${answers[current] === i ? "selected" : ""}`}
              onClick={() => selectAnswer(current, i)}
            >
              <span className="option-letter">
                {String.fromCharCode(65 + i)}
              </span>
              <span>{opt}</span>
            </div>
          ))}
        </div>
        <div className="quiz-nav">
          <button
            className="btn btn-secondary"
            onClick={() => setCurrent(current - 1)}
            disabled={current === 0}
          >
            ← Previous
          </button>
          {current < questions.length - 1 ? (
            <button
              className="btn btn-primary"
              onClick={() => setCurrent(current + 1)}
            >
              Next →
            </button>
          ) : (
            <button
              className="btn btn-success"
              onClick={handleSubmit}
              disabled={loading}
            >
              {loading ? "Submitting..." : "Submit Quiz"}
            </button>
          )}
        </div>
      </div>
    );
  }

  // Results Phase
  if (phase === "results" && results) {
    return (
      <div className="results">
        <div className="score-card">
          <div className="score">{results.score_percentage}%</div>
          <div className="score-label">Your Score</div>
          <div className="score-stats">
            <div>
              <div className="stat-num">{results.total_questions}</div>
              <div>Total</div>
            </div>
            <div>
              <div className="stat-num" style={{ color: "#2ec4b6" }}>{results.correct_answers}</div>
              <div>Correct</div>
            </div>
            <div>
              <div className="stat-num" style={{ color: "#e63946" }}>{results.wrong_answers}</div>
              <div>Wrong</div>
            </div>
          </div>
        </div>
        <h3 style={{ marginBottom: "1rem" }}>Detailed Review</h3>
        {results.results.map((r, i) => (
          <div key={i} className={`result-item ${r.is_correct ? "correct" : "wrong"}`}>
            <div className="question-text">
              {i + 1}. {r.question}
            </div>
            <div>
              Your answer: <strong>{String.fromCharCode(65 + r.selected_answer)}</strong>
              {" | "}
              Correct: <strong>{String.fromCharCode(65 + r.correct_answer)}</strong>
              {" "}
              {r.is_correct ? "✅" : "❌"}
            </div>
            <div className="explanation">💡 {r.explanation}</div>
          </div>
        ))}
        <div style={{ marginTop: "1.5rem", textAlign: "center" }}>
          <button className="btn btn-primary" onClick={resetQuiz}>
            Take Another Quiz
          </button>
        </div>
      </div>
    );
  }

  return null;
}
