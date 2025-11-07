# ConversIQ – AI Chat Portal with Conversation Intelligence  

> A full-stack AI-powered chat platform built with **Django REST Framework**, **PostgreSQL**, and **LM Studio (Llama)** for conversation analysis, summarization, and intelligent querying.

---

## Overview
ConversIQ enables users to chat with an AI assistant, store conversations, and later query insights or summaries from past chats.  
It integrates **LLMs (via LM Studio / OpenAI / Claude / Gemini)** to provide context-aware, summarized insights.

---

## Tech Stack

| Layer | Technology |
|-------|-------------|
| **Backend** | Django 5 + Django REST Framework |
| **Database** | PostgreSQL |
| **AI Integration** | LM Studio (local Llama 3 model) |
| **Frontend** | React + Tailwind CSS (in progress) |
| **Storage** | Local File System |
| **Language** | Python 3.13 |

---

## Folder Structure

conversiq/
│
├── chatapp/ # Core backend app
│ ├── models.py # Conversation & Message models
│ ├── serializers.py # DRF serializers
│ ├── views.py # API views (chat, end, summarize)
│ ├── urls.py # API routes
│ └── migrations/
│
├── conversiq_backend/ # Django project config
│ ├── settings.py
│ ├── urls.py
│ ├── wsgi.py
│ ├── asgi.py
│ └── .env.example # sample env file
│
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md

## Create Virtual Environment
python -m venv venv
.\venv\Scripts\activate

## Install Dependencies
pip install -r requirements.txt

## Apply Migrations
python manage.py makemigrations
python manage.py migrate

# Run the Development Server
python manage.py runserver


React Frontend  →  Django REST API  →  PostgreSQL
                           ↓
                       LM Studio API
