import React, { useState, useEffect, useRef, useCallback } from "react";
import { getExamPaperSets, startExam, submitExam } from "../api";

function formatTime(seconds) {
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  const s = seconds % 60;
  return `${h}:${String(m).padStart(2, "0")}:${String(s).padStart(2, "0")}`;
}

export default function Exam() {
  const [phase, setPhase] = useState("select"); // select | intro | exam | results
  const [paperSets, setPaperSets] = useState([]);
  const [selectedSet, setSelectedSet] = useState(null);
  const [categoryFilter, setCategoryFilter] = useState("all");
  const [examId, setExamId] = useState(null);
  const [questions, setQuestions] = useState([]);
  const [current, setCurrent] = useState(0);
  const [answers, setAnswers] = useState({});
  const [timeLeft, setTimeLeft] = useState(0);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [showNav, setShowNav] = useState(true);
  const timerRef = useRef(null);
  const startTimeRef = useRef(null);

  // Load paper sets
  useEffect(() => {
    loadPaperSets();
  }, []);

  const loadPaperSets = async () => {
    try {
      const res = await getExamPaperSets();
      setPaperSets(res.data.paper_sets);
    } catch {
      console.error("Failed to load paper sets");
    }
  };

  // Timer
  useEffect(() => {
    if (phase === "exam" && timeLeft > 0) {
      timerRef.current = setInterval(() => {
        setTimeLeft((prev) => {
          if (prev <= 1) {
            clearInterval(timerRef.current);
            handleAutoSubmit();
            return 0;
          }
          return prev - 1;
        });
      }, 1000);
      return () => clearInterval(timerRef.current);
    }
  }, [phase]);

  const handleAutoSubmit = useCallback(() => {
    handleSubmit(true);
  }, []);

  const selectPaperSet = (set) => {
    setSelectedSet(set);
    setPhase("intro");
  };

  const beginExam = async () => {
    setLoading(true);
    try {
      const res = await startExam({ paper_set_id: selectedSet.id });
      setExamId(res.data.exam_id);
      setQuestions(res.data.questions);
      setAnswers({});
      setCurrent(0);
      setTimeLeft(res.data.duration_seconds);
      startTimeRef.current = Date.now();
      setPhase("exam");
    } catch (err) {
      alert("Failed to start exam. Ensure backend is running and has enough questions.");
    } finally {
      setLoading(false);
    }
  };

  const selectAnswer = (qIndex, optIndex) => {
    if (answers[qIndex] === optIndex) {
      const newAnswers = { ...answers };
      delete newAnswers[qIndex];
      setAnswers(newAnswers);
    } else {
      setAnswers({ ...answers, [qIndex]: optIndex });
    }
  };

  const handleSubmit = async (autoSubmit = false) => {
    if (!autoSubmit) {
      const unanswered = questions.length - Object.keys(answers).length;
      if (unanswered > 0) {
        const confirm = window.confirm(
          `You have ${unanswered} unanswered questions. Unanswered = 0 marks. Submit anyway?`
        );
        if (!confirm) return;
      }
    }

    clearInterval(timerRef.current);
    setLoading(true);

    const timeTaken = Math.floor((Date.now() - startTimeRef.current) / 1000);
    const submission = {
      exam_id: examId,
      answers: questions.map((q, i) => ({
        question_id: q.id,
        selected_answer: answers[i] !== undefined ? answers[i] : null,
      })),
      time_taken_seconds: timeTaken,
    };

    try {
      const res = await submitExam(submission);
      setResults(res.data);
      setPhase("results");
    } catch {
      alert("Failed to submit exam.");
    } finally {
      setLoading(false);
    }
  };

  const resetExam = () => {
    setPhase("select");
    setQuestions([]);
    setAnswers({});
    setResults(null);
    setCurrent(0);
    setExamId(null);
    setSelectedSet(null);
  };

  // ===== SELECT PHASE: Show Paper Sets =====
  if (phase === "select") {
    const categories = [
      { key: "all", label: "All" },
      { key: "mock", label: "Mock Tests" },
      { key: "subject", label: "Subject-wise" },
      { key: "pyq", label: "PYQs / Recall" },
    ];

    const filtered = categoryFilter === "all"
      ? paperSets
      : paperSets.filter((s) => s.category === categoryFilter);

    return (
      <div className="exam-select">
        <div className="exam-select-header">
          <h1>📋 Exam Paper Sets</h1>
          <p className="exam-select-subtitle">
            Choose an exam paper set to begin your practice
          </p>
        </div>

        <div className="exam-category-tabs">
          {categories.map((cat) => (
            <button
              key={cat.key}
              className={`category-tab ${categoryFilter === cat.key ? "active" : ""}`}
              onClick={() => setCategoryFilter(cat.key)}
            >
              {cat.label}
            </button>
          ))}
        </div>

        <div className="paper-sets-grid">
          {filtered.map((set) => (
            <div
              key={set.id}
              className={`paper-set-card ${set.category}`}
              onClick={() => selectPaperSet(set)}
            >
              <div className="paper-set-icon">{set.icon}</div>
              <h3 className="paper-set-name">{set.name}</h3>
              <p className="paper-set-desc">{set.description}</p>
              <div className="paper-set-meta">
                <span className="meta-item">📝 {set.total_questions} Qs</span>
                <span className="meta-item">⏱ {set.duration_minutes} min</span>
              </div>
              <button className="btn btn-primary btn-sm paper-set-btn">
                Start Exam →
              </button>
            </div>
          ))}
        </div>
      </div>
    );
  }

  // ===== INTRO PHASE: Show exam details before starting =====
  if (phase === "intro" && selectedSet) {
    const maxMarks = selectedSet.total_questions * 4;
    return (
      <div className="exam-intro">
        <div className="exam-intro-card">
          <div className="exam-icon">{selectedSet.icon}</div>
          <h1>{selectedSet.name}</h1>
          <p className="exam-subtitle">{selectedSet.description}</p>
          <div className="exam-info-grid">
            <div className="exam-info-item">
              <span className="info-label">Total Questions</span>
              <span className="info-value">{selectedSet.total_questions}</span>
            </div>
            <div className="exam-info-item">
              <span className="info-label">Duration</span>
              <span className="info-value">{selectedSet.duration_minutes} min</span>
            </div>
            <div className="exam-info-item">
              <span className="info-label">Maximum Marks</span>
              <span className="info-value">{maxMarks}</span>
            </div>
            <div className="exam-info-item">
              <span className="info-label">Correct Answer</span>
              <span className="info-value" style={{ color: "#2ec4b6" }}>+4</span>
            </div>
            <div className="exam-info-item">
              <span className="info-label">Incorrect Answer</span>
              <span className="info-value" style={{ color: "#e63946" }}>-1</span>
            </div>
            <div className="exam-info-item">
              <span className="info-label">Unanswered</span>
              <span className="info-value">0</span>
            </div>
          </div>
          <div className="exam-rules">
            <h4>Instructions:</h4>
            <ul>
              <li>You can navigate between questions freely</li>
              <li>Click an option again to deselect (mark as unanswered)</li>
              <li>Exam auto-submits when timer reaches 0</li>
              <li>Negative marking applies for incorrect answers</li>
            </ul>
          </div>
          <div className="exam-intro-actions">
            <button className="btn btn-secondary btn-lg" onClick={() => setPhase("select")}>
              ← Back
            </button>
            <button className="btn btn-primary btn-lg" onClick={beginExam} disabled={loading}>
              {loading ? "Preparing Exam..." : "Start Exam"}
            </button>
          </div>
        </div>
      </div>
    );
  }

  // ===== EXAM PHASE =====
  if (phase === "exam") {
    const q = questions[current];
    const answeredCount = Object.keys(answers).length;
    const isTimeLow = timeLeft < 600;

    return (
      <div className="exam-container">
        <div className="exam-topbar">
          <div className="exam-topbar-left">
            <span className="exam-title">{selectedSet?.name || "Exam"}</span>
            <span className="exam-answered">
              {answeredCount}/{questions.length} answered
            </span>
          </div>
          <div className={`exam-timer ${isTimeLow ? "timer-warning" : ""}`}>
            ⏱ {formatTime(timeLeft)}
          </div>
          <div className="exam-topbar-right">
            <button
              className="btn btn-secondary btn-sm"
              onClick={() => setShowNav(!showNav)}
            >
              {showNav ? "Hide" : "Show"} Navigator
            </button>
            <button
              className="btn btn-success btn-sm"
              onClick={() => handleSubmit(false)}
              disabled={loading}
            >
              {loading ? "..." : "Submit Exam"}
            </button>
          </div>
        </div>

        <div className="exam-body">
          <div className="exam-question-panel">
            <div className="exam-q-header">
              <span className="exam-q-number">Question {current + 1}</span>
              <span className="tag">{q.subject}</span>
              <span className="tag">{q.topic}</span>
            </div>
            <h3 className="exam-q-text">{q.question}</h3>
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
            <div className="exam-q-nav">
              <button
                className="btn btn-secondary"
                onClick={() => setCurrent(Math.max(0, current - 1))}
                disabled={current === 0}
              >
                ← Prev
              </button>
              <button
                className="btn btn-secondary"
                onClick={() => {
                  const newAns = { ...answers };
                  delete newAns[current];
                  setAnswers(newAns);
                }}
                disabled={answers[current] === undefined}
              >
                Clear
              </button>
              <button
                className="btn btn-primary"
                onClick={() => setCurrent(Math.min(questions.length - 1, current + 1))}
                disabled={current === questions.length - 1}
              >
                Next →
              </button>
            </div>
          </div>

          {showNav && (
            <div className="exam-nav-panel">
              <div className="exam-nav-legend">
                <span className="legend-item"><span className="dot dot-answered"></span> Answered</span>
                <span className="legend-item"><span className="dot dot-unanswered"></span> Not Answered</span>
                <span className="legend-item"><span className="dot dot-current"></span> Current</span>
              </div>
              <div className="exam-nav-grid">
                {questions.map((_, i) => (
                  <button
                    key={i}
                    className={`nav-btn ${
                      i === current ? "nav-current" : answers[i] !== undefined ? "nav-answered" : "nav-unanswered"
                    }`}
                    onClick={() => setCurrent(i)}
                  >
                    {i + 1}
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    );
  }

  // ===== RESULTS PHASE =====
  if (phase === "results" && results) {
    const timeTakenFormatted = formatTime(results.time_taken_seconds);

    return (
      <div className="exam-results">
        <div className="exam-score-card">
          <h2>Exam Results – {selectedSet?.name}</h2>
          <div className="exam-score-main">
            <div className="exam-score-number">{results.raw_score}</div>
            <div className="exam-score-label">/ {results.max_marks}</div>
          </div>
          <div className="exam-score-percent">{results.percentage}%</div>
          <div className="exam-score-grid">
            <div className="score-box correct-box">
              <div className="score-box-num">{results.correct_count}</div>
              <div className="score-box-label">Correct (+{results.correct_count * 4})</div>
            </div>
            <div className="score-box incorrect-box">
              <div className="score-box-num">{results.incorrect_count}</div>
              <div className="score-box-label">Incorrect ({results.incorrect_count * -1})</div>
            </div>
            <div className="score-box unanswered-box">
              <div className="score-box-num">{results.unanswered_count}</div>
              <div className="score-box-label">Unanswered (0)</div>
            </div>
          </div>
          <div className="exam-time-taken">
            Time taken: <strong>{timeTakenFormatted}</strong>
          </div>
        </div>

        <h3 style={{ margin: "1.5rem 0 1rem" }}>Detailed Review</h3>
        {results.results.map((r, i) => (
          <div key={i} className={`result-item ${r.status}`}>
            <div className="question-text">
              {i + 1}. {r.question}
            </div>
            <div className="result-options">
              {r.options.map((opt, oi) => (
                <div
                  key={oi}
                  className={`result-opt ${
                    oi === r.correct_answer ? "opt-correct" : ""
                  } ${oi === r.selected_answer ? "opt-selected" : ""}`}
                >
                  <span className="option-letter">{String.fromCharCode(65 + oi)}</span>
                  {opt}
                  {oi === r.correct_answer && " ✓"}
                  {oi === r.selected_answer && oi !== r.correct_answer && " ✗"}
                </div>
              ))}
            </div>
            {r.explanation && (
              <div className="explanation">💡 {r.explanation}</div>
            )}
            <div className="result-meta">
              <span className="tag">{r.subject}</span>
              <span className="tag">{r.topic}</span>
              <span className={`tag tag-${r.status}`}>
                {r.status === "correct" ? "+4" : r.status === "incorrect" ? "-1" : "0"}
              </span>
            </div>
          </div>
        ))}

        <div style={{ marginTop: "2rem", textAlign: "center" }}>
          <button className="btn btn-primary btn-lg" onClick={resetExam}>
            Take Another Exam
          </button>
        </div>
      </div>
    );
  }

  return null;
}
