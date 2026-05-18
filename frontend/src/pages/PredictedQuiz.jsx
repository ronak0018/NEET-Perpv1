import React, { useState, useEffect } from "react";
import { getPredictedQuizSets, getPredictedQuizInfo, getPredictedQuizQuestions, submitPredictedQuiz } from "../api";

export default function PredictedQuiz() {
  const [phase, setPhase] = useState("select"); // select | info | quiz | results
  const [sets, setSets] = useState([]);
  const [selectedSet, setSelectedSet] = useState(null);
  const [info, setInfo] = useState(null);
  const [questions, setQuestions] = useState([]);
  const [current, setCurrent] = useState(0);
  const [answers, setAnswers] = useState({});
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [filter, setFilter] = useState({ subject: "", limit: "" });
  const [timeLeft, setTimeLeft] = useState(null);
  const [timerRef, setTimerRef] = useState(null);

  useEffect(() => {
    getPredictedQuizSets().then((res) => setSets(res.data)).catch(() => {});
  }, []);

  useEffect(() => {
    if (phase === "quiz" && timeLeft !== null && timeLeft > 0) {
      const id = setTimeout(() => setTimeLeft((t) => t - 1), 1000);
      setTimerRef(id);
      return () => clearTimeout(id);
    }
    if (timeLeft === 0 && phase === "quiz") {
      handleSubmit();
    }
  }, [timeLeft, phase]);

  const selectSet = async (set) => {
    setSelectedSet(set);
    setLoading(true);
    try {
      const res = await getPredictedQuizInfo(set.set_id);
      setInfo(res.data);
      setPhase("info");
    } catch {
      alert("Failed to load set info.");
    } finally {
      setLoading(false);
    }
  };

  const startQuiz = async () => {
    setLoading(true);
    try {
      const params = { set_id: selectedSet.set_id };
      if (filter.subject) params.subject = filter.subject;
      if (filter.limit) params.limit = parseInt(filter.limit);
      const res = await getPredictedQuizQuestions(params);
      if (res.data.length === 0) {
        alert("No questions found.");
        return;
      }
      setQuestions(res.data);
      setAnswers({});
      setCurrent(0);
      setTimeLeft(res.data.length * 60);
      setPhase("quiz");
    } catch {
      alert("Failed to load predicted quiz.");
    } finally {
      setLoading(false);
    }
  };

  const selectAnswer = (qIndex, optIndex) => {
    setAnswers({ ...answers, [qIndex]: optIndex });
  };

  const handleSubmit = async () => {
    if (timerRef) clearTimeout(timerRef);
    const submission = {
      set_id: selectedSet.set_id,
      answers: questions.map((q, i) => ({
        question_id: q.id,
        selected: answers[i] !== undefined ? answers[i] : -1,
      })),
    };
    setLoading(true);
    try {
      const res = await submitPredictedQuiz(submission);
      setResults(res.data);
      setPhase("results");
    } catch {
      alert("Failed to submit quiz.");
    } finally {
      setLoading(false);
    }
  };

  const reset = () => {
    setPhase("select");
    setQuestions([]);
    setAnswers({});
    setResults(null);
    setCurrent(0);
    setTimeLeft(null);
    setSelectedSet(null);
    setInfo(null);
  };

  const formatTime = (s) => {
    const h = Math.floor(s / 3600);
    const m = Math.floor((s % 3600) / 60);
    const sec = s % 60;
    return `${h > 0 ? h + "h " : ""}${m}m ${sec < 10 ? "0" : ""}${sec}s`;
  };

  // SET SELECTION PHASE
  if (phase === "select") {
    return (
      <div className="predicted-quiz-info">
        <h2>🎯 NEET UG 2026 - Predicted Quiz Sets</h2>
        <p className="quiz-desc">Choose from 4 unique sets based on deep PYQ analysis (2020-2024). Each set has 180 questions with a different focus.</p>
        {sets.length > 0 ? (
          <div className="sets-grid">
            {sets.map((s) => (
              <div key={s.set_id} className="set-card" onClick={() => selectSet(s)}>
                <h3>{s.title}</h3>
                <p>{s.description}</p>
                <div className="set-meta">
                  <span>📝 {s.total_questions} Questions</span>
                  <span>⏱ {s.exam_pattern.duration_minutes} min</span>
                </div>
                <button className="btn-primary" disabled={loading}>
                  {loading ? "Loading..." : "Select →"}
                </button>
              </div>
            ))}
          </div>
        ) : (
          <p>Loading available sets...</p>
        )}
      </div>
    );
  }

  // INFO PHASE
  if (phase === "info") {
    return (
      <div className="predicted-quiz-info">
        <button className="btn-back" onClick={() => setPhase("select")}>← Back to Sets</button>
        <h2>🎯 {info.title}</h2>
        {info ? (
          <>
            <p className="quiz-desc">{info.description}</p>
            <div className="quiz-meta">
              <div className="meta-card">
                <strong>Total Questions:</strong> {info.total_questions}
              </div>
              <div className="meta-card">
                <strong>Pattern:</strong> Physics ({info.exam_pattern.physics}) | Chemistry ({info.exam_pattern.chemistry}) | Biology ({info.exam_pattern.biology})
              </div>
              <div className="meta-card">
                <strong>Marking:</strong> +{info.exam_pattern.marking.correct} / {info.exam_pattern.marking.incorrect} / {info.exam_pattern.marking.unanswered}
              </div>
              <div className="meta-card">
                <strong>Duration:</strong> {info.exam_pattern.duration_minutes} min | <strong>Max Marks:</strong> {info.exam_pattern.total_marks}
              </div>
            </div>

            {info.analysis_summary && (
              <div className="analysis-section">
                <h3>📊 PYQ Analysis - Most Repeated Topics</h3>
                <div className="analysis-grid">
                  <div>
                    <h4>Physics</h4>
                    <ul>{info.analysis_summary.most_repeated_physics.map((t, i) => <li key={i}>{t}</li>)}</ul>
                  </div>
                  <div>
                    <h4>Chemistry</h4>
                    <ul>{info.analysis_summary.most_repeated_chemistry.map((t, i) => <li key={i}>{t}</li>)}</ul>
                  </div>
                  <div>
                    <h4>Biology</h4>
                    <ul>{info.analysis_summary.most_repeated_biology.map((t, i) => <li key={i}>{t}</li>)}</ul>
                  </div>
                </div>
                {info.analysis_summary.tricky_chapters && (
                  <>
                    <h4>⚠️ Tricky Chapters</h4>
                    <p>{info.analysis_summary.tricky_chapters.join(", ")}</p>
                  </>
                )}
              </div>
            )}

            {info.deep_analysis && (
              <div className="analysis-section">
                <h3>🔬 Deep Analysis</h3>
                <p><em>{info.deep_analysis.methodology}</em></p>
                {info.deep_analysis.guaranteed_topics && (
                  <div className="analysis-grid">
                    {Object.entries(info.deep_analysis.guaranteed_topics).map(([subject, topics]) => (
                      <div key={subject}>
                        <h4>{subject}</h4>
                        <ul>{topics.map((t, i) => <li key={i}>{t}</li>)}</ul>
                      </div>
                    ))}
                  </div>
                )}
                {info.deep_analysis.tricky_patterns && (
                  <>
                    <h4>🧠 Tricky Patterns</h4>
                    <ul>{info.deep_analysis.tricky_patterns.map((p, i) => <li key={i}>{p}</li>)}</ul>
                  </>
                )}
                {info.deep_analysis.dark_horse_physics && (
                  <div className="analysis-grid">
                    <div><h4>Physics Dark Horses</h4><ul>{info.deep_analysis.dark_horse_physics.map((t, i) => <li key={i}>{t}</li>)}</ul></div>
                    <div><h4>Chemistry Dark Horses</h4><ul>{info.deep_analysis.dark_horse_chemistry.map((t, i) => <li key={i}>{t}</li>)}</ul></div>
                    <div><h4>Biology Dark Horses</h4><ul>{info.deep_analysis.dark_horse_biology.map((t, i) => <li key={i}>{t}</li>)}</ul></div>
                  </div>
                )}
              </div>
            )}

            <div className="quiz-start-form">
              <h3>Start Predicted Quiz</h3>
              <div className="form-group">
                <label>Subject (optional)</label>
                <select value={filter.subject} onChange={(e) => setFilter({ ...filter, subject: e.target.value })}>
                  <option value="">All (180 Questions)</option>
                  <option value="Physics">Physics (45)</option>
                  <option value="Chemistry">Chemistry (45)</option>
                  <option value="Biology">Biology (90)</option>
                </select>
              </div>
              <div className="form-group">
                <label>Limit Questions (optional)</label>
                <input
                  type="number"
                  min="1"
                  max="180"
                  placeholder="e.g. 20"
                  value={filter.limit}
                  onChange={(e) => setFilter({ ...filter, limit: e.target.value })}
                />
              </div>
              <button className="btn-primary" onClick={startQuiz} disabled={loading}>
                {loading ? "Loading..." : "🚀 Start Quiz"}
              </button>
            </div>
          </>
        ) : (
          <p>Loading quiz info...</p>
        )}
      </div>
    );
  }

  // QUIZ PHASE
  if (phase === "quiz") {
    const q = questions[current];
    const answered = Object.keys(answers).length;
    return (
      <div className="predicted-quiz-active">
        <div className="quiz-header">
          <div className="quiz-progress">
            Q {current + 1} / {questions.length} | Answered: {answered}
          </div>
          <div className="quiz-timer" style={{ color: timeLeft < 60 ? "#e74c3c" : "#2ecc71" }}>
            ⏱ {formatTime(timeLeft)}
          </div>
        </div>

        <div className="quiz-question-card">
          <div className="question-meta">
            <span className="badge">{q.subject}</span>
            <span className="badge badge-chapter">{q.chapter}</span>
          </div>
          <p className="question-text">{q.question}</p>
          <div className="options-list">
            {q.options.map((opt, i) => (
              <div
                key={i}
                className={`option-item ${answers[current] === i ? "selected" : ""}`}
                onClick={() => selectAnswer(current, i)}
              >
                <span className="option-label">{String.fromCharCode(65 + i)}.</span>
                <span>{opt}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="quiz-nav">
          <button disabled={current === 0} onClick={() => setCurrent(current - 1)}>← Previous</button>
          <button onClick={() => { if (answers[current] !== undefined) setAnswers(({ ...answers, [current]: undefined })); }}>
            Clear
          </button>
          {current < questions.length - 1 ? (
            <button onClick={() => setCurrent(current + 1)}>Next →</button>
          ) : (
            <button className="btn-submit" onClick={handleSubmit} disabled={loading}>
              {loading ? "Submitting..." : "Submit Quiz"}
            </button>
          )}
        </div>

        <div className="question-palette">
          {questions.map((_, i) => (
            <span
              key={i}
              className={`palette-btn ${answers[i] !== undefined ? "answered" : ""} ${i === current ? "current" : ""}`}
              onClick={() => setCurrent(i)}
            >
              {i + 1}
            </span>
          ))}
        </div>
      </div>
    );
  }

  // RESULTS PHASE
  if (phase === "results" && results) {
    return (
      <div className="predicted-quiz-results">
        <h2>📋 Quiz Results</h2>
        <div className="results-summary">
          <div className="result-card correct">✅ Correct: {results.correct}</div>
          <div className="result-card incorrect">❌ Incorrect: {results.incorrect}</div>
          <div className="result-card unanswered">⬜ Unanswered: {results.unanswered}</div>
          <div className="result-card score">
            🏆 Score: {results.total_marks} / {results.max_marks} ({results.percentage}%)
          </div>
        </div>

        <h3>Detailed Review</h3>
        <div className="results-details">
          {results.details.map((d, i) => {
            const q = questions[i];
            return (
              <div key={i} className={`review-card ${d.status}`}>
                <div className="review-header">
                  <span className="review-num">Q{i + 1}</span>
                  <span className={`review-status status-${d.status}`}>
                    {d.status === "correct" ? "✅" : d.status === "incorrect" ? "❌" : "⬜"} {d.status}
                  </span>
                  <span className="review-marks">{d.marks > 0 ? "+" : ""}{d.marks}</span>
                </div>
                <p className="review-question">{q.question}</p>
                <p className="review-correct"><strong>Correct:</strong> {d.correct_option}</p>
                <p className="review-explanation"><em>{d.explanation}</em></p>
              </div>
            );
          })}
        </div>

        <button className="btn-primary" onClick={reset}>🔄 Take Again</button>
      </div>
    );
  }

  return null;
}
