# 🧠 ConversIQ – AI Chat with Memory

ConversIQ is a full-stack **AI chat system** built using **Django + React + LM Studio + PostgreSQL (pgvector)**.  
It remembers past conversations, performs semantic recall, and generates summaries using a local LLM.

---

##  Features
- 💬 Real-time chat interface (React + Tailwind)
- 🧠 AI remembers previous chats via vector embeddings
- 🗂️ PostgreSQL + pgvector for semantic search
- 🧾 Summarization of conversations at end
- 🤖 Local LM Studio API integration (no OpenAI API costs)
- 🔍 Context recall and message similarity search

---

## 🖥️ Screenshots

| UI Section | Screenshot |
|-------------|-------------|
| Chat Interface |  Screenshots/UI.png
| Context Recall | (Screenshots/db-1.png) |
| Conversation List | (Screenshots/chat-1.png) (Screenshots/chat-2.png) |


## Setup Instructions

### Backend (Django)
```bash
cd conversiq_backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver



+------------------+          +----------------+
|   React (Vite)   |  --->    |  Django REST  |
|  Chat Interface  |          |  API Backend  |
+--------+---------+          +-------+--------+
         |                            |
         |   POST /add_message        |
         v                            v
   +-------------+          +------------------+
   | PostgreSQL  | <------> |  pgvector Index  |
   | chatapp_msg |          | for embeddings   |
   +-------------+          +------------------+
         |
         |   Context recall & similarity
         v
   +----------------------+
   | LM Studio (Local LLM)|
   +----------------------+
