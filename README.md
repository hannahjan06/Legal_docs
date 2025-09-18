# 📜 Legal document AI (demo) – AI-Powered Legal Document Simplifier

Making complex legal docs simple, clear, and accessible for everyone. 🚀

---
### 🌟 Overview

LegalEase is a web application that helps users upload legal documents (like rental agreements, loan contracts, ToS, etc.) and instantly receive:

✅ Simplified summaries in plain language

✅ Visual flowcharts of key terms and clauses

✅ Highlighted risk flags (legal, financial, compliance, privacy)

Built for the Google Cloud Hackathon, this project leverages Google Cloud Generative AI (Gemini API) + custom ML agents to make legal knowledge accessible.

---
### 🖥️ Features

User Authentication → Signup/Login with a clean, modern UI
PDF Upload Support → Upload contracts, agreements, and other docs

---
### AI Agents Pipeline:

📄 PDF Reader Agent → Extracts text (OCR via pytesseract + pdf2image)

✍️ Summarization Agent → Clause-level summaries + TL;DR

⚠️ Structuring Agent → Identifies risks (legal, compliance, financial, privacy)

📊 Flowchart Agent → Generates an easy-to-follow flowchart of key terms

Chatbot Interface → Users can ask questions about their document

Light Brown Aesthetic → Minimal, warm UI for clarity

---
### 🏗️ Tech Stack

Frontend:
Next.js / React
TailwindCSS
(Gemini CLI-generated base UI, with agent integration placeholders)

Backend / AI Agents:
Python (FastAPI/Flask for APIs)
Pytesseract + pdf2image (OCR for PDFs)
Google Cloud Storage (for raw & processed docs)
Gemini API (for summarization, structuring, flowchart generation)

Cloud:
Google Cloud Platform (GCP)
Vertex AI / Generative AI Studio
GCS for document storage
---
### ⚙️ Installation
1️⃣ Clone the repo
```git clone https://github.com/your-username/legalease.git
cd legalease
```

2️⃣ Setup Frontend
```cd frontend
npm install
npm run dev
```

3️⃣ Setup Backend
```cd backend
pip install -r requirements.txt
uvicorn app:main --reload
```

### 📂 Project Structure
```/frontend
   /components   → UI components (chatbot, auth, upload)
   /pages        → login, signup, dashboard
   /styles       → Tailwind config
/backend
   /agents       → PDF Reader, Summarizer, Structurer, Flowchart
   /utils        → GCS helpers, error handling
   app.py        → FastAPI entry point
```
---
### 🚦 Workflow
1. User signs up / logs in
2. Uploads PDF → saved in Google Cloud Storage
3. PDF Reader Agent extracts text → saves to processed bucket
4. Summarization Agent simplifies text
5. Structuring Agent flags risks → JSON output
6. Flowchart Agent creates visual explanation
7. User views simplified doc + flowchart in chatbot UI
