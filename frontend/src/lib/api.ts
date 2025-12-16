import axios from "axios";

const API_URL = "http://127.0.0.1:8000";

const api = axios.create({
  baseURL: API_URL,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const getQuestions = async () => (await api.get("/questions/")).data;
export const postQuestion = async (content: string) => (await api.post("/questions/", { content })).data;
export const markAnswered = async (id: number, answer: string) => 
  (await api.patch(`/questions/${id}/answer?answer_text=${encodeURIComponent(answer)}`)).data;
export const loginUser = async (formData: FormData) => (await api.post("/auth/login", formData)).data;
export const registerUser = async (data: { username: string; email: string; password: string }) => 
  (await api.post("/auth/register", data)).data;

export const postReply = async (questionId: number, content: string) => 
  (await api.post(`/questions/${questionId}/reply`, { content })).data;

export const updateStatus = async (questionId: number, status: string) => 
  (await api.patch(`/questions/${questionId}/status?status=${status}`)).data;

export const WS_URL = "ws://127.0.0.1:8000/questions/ws";