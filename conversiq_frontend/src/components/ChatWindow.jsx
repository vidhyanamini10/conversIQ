import { useEffect, useRef, useState } from "react";
import { UserIcon, CommandLineIcon } from "@heroicons/react/24/solid";
import { addMessage } from "../api";

export default function ChatWindow({ conversationId, messages, setMessages }) {
  const messagesEndRef = useRef(null);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // 🧠 Send message handler
  const handleSend = async () => {
    if (!input.trim() || !conversationId) return;
    setLoading(true);

    const userMsg = { sender: "user", content: input };
    setMessages((prev) => [...prev, userMsg]);

    try {
      const res = await addMessage(conversationId, { content: input });
      const { user_message, ai_response, context_used } = res.data;

      console.log("🧩 Recall context used:", context_used);

      setMessages((prev) => [
        ...prev,
        { sender: "ai", content: ai_response || "No response" },
      ]);
    } catch (err) {
      console.error("❌ Send failed:", err);
      setMessages((prev) => [
        ...prev,
        { sender: "ai", content: "⚠️ Error: " + err.message },
      ]);
    } finally {
      setInput("");
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !loading) handleSend();
  };

  return (
    <div className="flex flex-col flex-1 bg-[#343541]">
      {/* Chat messages */}
      <div className="flex-1 overflow-y-auto">
        {messages.length === 0 ? (
          <div className="flex items-center justify-center h-full text-gray-300">
            Start a new conversation
          </div>
        ) : (
          <div className="space-y-0">
            {messages.map((msg, i) => (
              <div
                key={i}
                className={`${
                  msg.sender === "ai" ? "bg-[#444654]" : "bg-[#343541]"
                }`}
              >
                <div className="max-w-3xl mx-auto flex gap-6 p-6">
                  <div className="w-8 h-8 rounded-sm flex-shrink-0 flex items-center justify-center">
                    {msg.sender === "user" ? (
                      <div className="bg-slate-900 text-white rounded-sm w-full h-full flex items-center justify-center">
                        <UserIcon className="h-5 w-5" />
                      </div>
                    ) : (
                      <div className="bg-teal-600 text-white rounded-sm w-full h-full flex items-center justify-center">
                        <CommandLineIcon className="h-5 w-5" />
                      </div>
                    )}
                  </div>
                  <div className="min-h-[20px] flex flex-1 flex-col items-start gap-4 whitespace-pre-wrap text-gray-100">
                    {msg.content}
                  </div>
                </div>
              </div>
            ))}
            {loading && (
              <div className="bg-[#444654]">
                <div className="max-w-3xl mx-auto flex gap-6 p-6">
                  <div className="w-8 h-8 rounded-sm flex-shrink-0 bg-teal-600 text-white flex items-center justify-center">
                    <CommandLineIcon className="h-5 w-5" />
                  </div>
                  <div className="flex gap-2">
                    <div className="w-2 h-2 rounded-full bg-gray-400 animate-bounce [animation-delay:-0.3s]" />
                    <div className="w-2 h-2 rounded-full bg-gray-400 animate-bounce [animation-delay:-0.15s]" />
                    <div className="w-2 h-2 rounded-full bg-gray-400 animate-bounce" />
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} className="h-3" />
          </div>
        )}
      </div>

      {/* Input box */}
      <div className="border-t border-gray-700 p-4 flex items-center gap-3 bg-[#40414f]">
        <input
          type="text"
          className="flex-1 bg-transparent outline-none text-white placeholder-gray-400"
          placeholder="Type your message..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={loading}
        />
        <button
          onClick={handleSend}
          disabled={loading}
          className="px-4 py-2 bg-teal-600 text-white rounded-md hover:bg-teal-500 disabled:opacity-50"
        >
          Send
        </button>
      </div>
    </div>
  );
}
