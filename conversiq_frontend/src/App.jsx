import { useState, useEffect } from "react";
import {
  ChatBubbleLeftRightIcon,
  PlusCircleIcon,
  TrashIcon,
  PencilSquareIcon,
  PaperAirplaneIcon,
  StopCircleIcon,
} from "@heroicons/react/24/solid";
import {
  createConversation,
  getAllConversations,
  addMessage,
  endConversation,
} from "./services/api.js";

export default function App() {
  const [conversations, setConversations] = useState([]);
  const [activeConversation, setActiveConversation] = useState(null);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [editingId, setEditingId] = useState(null);
  const [editTitle, setEditTitle] = useState("");

  // Load all chats initially
  useEffect(() => {
    loadConversations();
  }, []);

  const loadConversations = async () => {
    try {
      const res = await getAllConversations();
      setConversations(res.data);
    } catch (e) {
      console.error("Failed to load conversations:", e);
    }
  };

  // Load messages for one chat
  const loadMessages = async (id) => {
    const res = await fetch(`http://127.0.0.1:8000/api/conversations/${id}/`);
    const data = await res.json();
    setMessages(data.messages || []);
    setActiveConversation(data);
  };

  // Stop AI typing simulation
  const handleStopAI = () => {
    if (loading) {
      setLoading(false);
      setMessages((prev) => [
        ...prev,
        {
          sender: "system",
          content: "⚠️ AI response stopped by user.",
        },
      ]);
    }
  };

  // Create new chat
  const startConversation = async () => {
    try {
      const res = await createConversation();
      const data = res.data;
      setActiveConversation(data);
      setMessages([]);
      setConversations((prev) => [data, ...prev]);
    } catch (e) {
      console.error("Create chat failed:", e);
    }
  };

  // Rename chat
  const renameConversation = async (id, newTitle) => {
    await fetch(`http://127.0.0.1:8000/api/conversations/${id}/`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title: newTitle }),
    });

    setConversations((prev) =>
      prev.map((conv) =>
        conv.id === id ? { ...conv, title: newTitle } : conv
      )
    );

    if (activeConversation?.id === id) {
      setActiveConversation({ ...activeConversation, title: newTitle });
    }

    setEditingId(null);
  };

  // Delete chat
  const deleteConversation = async (id) => {
    const confirmDelete = window.confirm(
      "Are you sure you want to delete this chat?"
    );
    if (!confirmDelete) return;

    await fetch(`http://127.0.0.1:8000/api/conversations/${id}/`, {
      method: "DELETE",
    });

    setConversations((prev) => prev.filter((conv) => conv.id !== id));

    if (activeConversation?.id === id) {
      setActiveConversation(null);
      setMessages([]);
    }
  };

  // ✉️ Send message (with AI memory recall)
  const sendMessage = async () => {
    if (!input.trim() || !activeConversation || loading) return;

    const userMsg = { sender: "user", content: input };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setLoading(true);

    try {
      const res = await addMessage(activeConversation.id, { content: input });
      const { user_message, ai_response, context_used } = res.data;

      console.log("🧠 Recall context used:", context_used);

      setMessages((prev) => [
        ...prev,
        { sender: "ai", content: ai_response || "No response." },
      ]);
    } catch (e) {
      console.error("Send failed:", e);
      setMessages((prev) => [
        ...prev,
        { sender: "ai", content: "⚠️ Error: " + e.message },
      ]);
    } finally {
      setLoading(false);
    }
  };

  // 🏁 End chat and summarize
  const handleEndConversation = async () => {
    if (!activeConversation) return;
    try {
      const res = await endConversation(activeConversation.id);
      alert(`Conversation ended.\n\n${res.data.summary}`);
      setActiveConversation(null);
      setMessages([]);
    } catch (e) {
      console.error("End failed:", e);
    }
  };

  return (
    <div className="h-screen flex bg-gray-100 text-gray-800">
      {/* Sidebar */}
      <aside className="w-64 bg-gray-900 text-white flex flex-col">
        <div className="p-4 flex items-center justify-between border-b border-gray-700">
          <h1 className="text-xl font-bold">ConversIQ</h1>
        </div>

        {/* Only one New Chat button */}
        <button
          onClick={startConversation}
          className="flex items-center justify-center gap-2 m-3 py-2 bg-indigo-600 hover:bg-indigo-700 rounded-lg w-full"
        >
          <PlusCircleIcon className="h-5 w-5" />
          New Chat
        </button>

        {/* Chat list */}
        <div className="flex-1 overflow-y-auto px-2 pb-4 space-y-1">
          {conversations.length === 0 && (
            <p className="text-gray-400 text-sm mt-3 text-center">
              No chats yet
            </p>
          )}
          {conversations.map((conv) => (
            <div
              key={conv.id}
              className={`group flex items-center justify-between p-2 rounded-lg cursor-pointer ${
                activeConversation?.id === conv.id
                  ? "bg-indigo-600 text-white"
                  : "hover:bg-gray-800"
              }`}
            >
              {/* Title / Rename */}
              <div
                onClick={() => loadMessages(conv.id)}
                className="flex items-center gap-2 flex-1"
              >
                <ChatBubbleLeftRightIcon className="h-4 w-4" />
                {editingId === conv.id ? (
                  <input
                    type="text"
                    value={editTitle}
                    onChange={(e) => setEditTitle(e.target.value)}
                    onBlur={() => renameConversation(conv.id, editTitle)}
                    onKeyDown={(e) =>
                      e.key === "Enter" && renameConversation(conv.id, editTitle)
                    }
                    autoFocus
                    className="text-sm text-gray-800 px-1 rounded outline-none w-full"
                  />
                ) : (
                  <span
                    className="truncate text-sm"
                    onDoubleClick={() => {
                      setEditingId(conv.id);
                      setEditTitle(conv.title);
                    }}
                  >
                    {conv.title}
                  </span>
                )}
              </div>

              {/* Action Icons */}
              <div className="flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                <PencilSquareIcon
                  className="h-4 w-4 text-gray-300 hover:text-yellow-400 cursor-pointer"
                  onClick={() => {
                    setEditingId(conv.id);
                    setEditTitle(conv.title);
                  }}
                />
                <TrashIcon
                  className="h-4 w-4 text-gray-300 hover:text-red-400 cursor-pointer"
                  onClick={() => deleteConversation(conv.id)}
                />
              </div>
            </div>
          ))}
        </div>
      </aside>

      {/* Chat Area */}
      <main className="flex-1 flex flex-col">
        {/* Header */}
        <div className="p-4 border-b bg-white">
          <h2 className="text-lg font-semibold">
            {activeConversation
              ? activeConversation.title
              : "Start a new conversation"}
          </h2>
        </div>

        {/* Chat messages */}
        <div className="flex-1 overflow-y-auto p-6 space-y-3 bg-gray-50">
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`flex ${
                msg.sender === "user" ? "justify-end" : "justify-start"
              }`}
            >
              <div
                className={`max-w-[70%] px-4 py-2 rounded-2xl shadow ${
                  msg.sender === "user"
                    ? "bg-indigo-600 text-white"
                    : "bg-white text-gray-800"
                }`}
              >
                {msg.content}
              </div>
            </div>
          ))}
          {loading && (
            <div className="text-gray-500 italic animate-pulse">
              AI is typing...
            </div>
          )}
        </div>

        {/* Input Area */}
        {activeConversation && (
          <div className="flex items-center gap-2 p-4 border-t bg-white">
            <input
              type="text"
              placeholder={
                loading ? "AI is responding..." : "Send a message..."
              }
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && !loading && sendMessage()}
              className="flex-1 border rounded-full px-4 py-2 focus:ring-2 focus:ring-indigo-400 outline-none disabled:bg-gray-100"
              disabled={loading}
            />

            {/* Send / Stop buttons */}
            <div className="flex items-center gap-2">
              {!loading && (
                <button
                  onClick={sendMessage}
                  disabled={loading}
                  title="Send message"
                  className="p-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-full transition-all"
                >
                  <PaperAirplaneIcon className="h-5 w-5" />
                </button>
              )}

              <button
                onClick={loading ? handleStopAI : handleEndConversation}
                title={loading ? "Stop AI Response" : "End Conversation"}
                className={`p-2 text-white rounded-full transition-all ${
                  loading
                    ? "bg-yellow-500 hover:bg-yellow-600"
                    : "bg-red-500 hover:bg-red-600"
                }`}
              >
                <StopCircleIcon className="h-5 w-5" />
              </button>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
