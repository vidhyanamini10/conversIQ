import axios from "axios";

// 🧠 Base API configuration
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000/api",
  headers: { "Content-Type": "application/json" },
});

// 🟢 Create a new conversation
export const createConversation = () => api.post("/conversations/", { title: "New Chat" });

// 🟢 Get all conversations
export const getAllConversations = () => api.get("/conversations/");

// 🟢 Add message (includes AI reply)
export const addMessage = (id, data) =>
  api.post(`/conversations/${id}/add_message/`, data);

// 🟢 End a conversation (and get summary)
export const endConversation = (id) => api.post(`/conversations/${id}/end/`);

// 🟡 Semantic search across messages
export const searchMessages = (query) =>
  api.get("/search/", { params: { q: query } });

// 🧩 Recall context from a specific conversation
export const recallContext = (query, conversationId) =>
  api.get("/recall/", { params: { q: query, conversation: conversationId } });

export default api;
