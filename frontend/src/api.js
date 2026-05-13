import axios from "axios";

const API = axios.create({ baseURL: "/api" });

// Questions
export const getSubjects = () => API.get("/questions/subjects");
export const getTopics = (subject) => API.get(`/questions/topics/${subject}`);
export const getQuiz = (params) => API.get("/questions/quiz", { params });
export const submitQuiz = (submissions) =>
  API.post("/questions/submit-quiz", submissions);
export const getQuestions = (params) => API.get("/questions/", { params });
export const createQuestion = (data) => API.post("/questions/", data);

// Notes
export const getNotes = (params) => API.get("/notes/", { params });
export const getNote = (id) => API.get(`/notes/${id}`);
export const createNote = (data) => API.post("/notes/", data);
export const updateNote = (id, data) => API.put(`/notes/${id}`, data);
export const deleteNote = (id) => API.delete(`/notes/${id}`);
export const getNoteSubjects = () => API.get("/notes/subjects");

// Exam
export const getExamPaperSets = () => API.get("/exam/paper-sets");
export const startExam = (data) => API.post("/exam/start", data);
export const submitExam = (data) => API.post("/exam/submit", data);
export const getExamHistory = () => API.get("/exam/history");
