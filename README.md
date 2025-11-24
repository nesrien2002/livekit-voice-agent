# LiveKit Voice Agent with Gemini and RAG

A real-time AI voice agent built with LiveKit, Google Gemini API, and Retrieval-Augmented Generation (RAG) for context-aware responses.

## 🎯 Project Overview

This project implements a voice-enabled AI agent that:
- Connects to LiveKit rooms for real-time communication
- Uses Google Gemini 2.5 Flash for natural language understanding
- Implements RAG with FAISS for knowledge-grounded responses
- Provides a web interface for user interaction

## 🏗️ Architecture

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   Frontend  │ ◄─────► │  Token       │ ◄─────► │  LiveKit    │
│  (React)    │         │  Server      │         │  Cloud      │
└─────────────┘         └──────────────┘         └─────────────┘
                                                         │
                                                         ▼
                        ┌──────────────────────────────────┐
                        │     Voice Agent (Python)         │
                        │  ┌────────────┐  ┌────────────┐ │
                        │  │   Gemini   │  │    RAG     │ │
                        │  │  2.5 Flash │  │   FAISS    │ │
                        │  └────────────┘  └────────────┘ │
                        └──────────────────────────────────┘
                                      │
                                      ▼
                              ┌──────────────┐
                              │  Knowledge   │
                              │     Base     │
                              └──────────────┘
```

## ✨ Features

### Implemented
- ✅ LiveKit integration for real-time communication
- ✅ Google Gemini 2.5 Flash for language generation
- ✅ RAG system with FAISS vector database
- ✅ Sentence-transformers for semantic search
- ✅ Token-based authentication
- ✅ React web interface
- ✅ Real-time connection management
- ✅ Knowledge base with FAQs

### Current Limitations
- ⚠️ Text-based interaction (STT/TTS pipeline needs implementation)
- ⚠️ Audio streaming requires additional integration with Gemini Live API

## 📋 Requirements

### Python Dependencies
```
livekit>=0.11.0
livekit-agents>=0.8.0
livekit-api>=0.6.0
google-generativeai>=0.3.0
faiss-cpu>=1.7.4
sentence-transformers>=2.2.0
python-dotenv>=1.0.0
numpy>=1.24.0
flask>=3.0.0
flask-cors>=4.0.0
aiohttp==3.9.5
```

### Frontend Dependencies
```
react
livekit-client
```

## 🚀 Setup Instructions

### 1. Clone and Setup Environment

```bash
# Clone repository
git clone <your-repo-url>
cd livekit-voice-agent

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the project root:

```env
# LiveKit Configuration
LIVEKIT_URL=wss://your-project.livekit.cloud
LIVEKIT_API_KEY=your_livekit_api_key
LIVEKIT_API_SECRET=your_livekit_api_secret

# Google Gemini API
GEMINI_API_KEY=your_gemini_api_key

# Optional Configuration
EMBEDDING_MODEL=all-MiniLM-L6-v2
KNOWLEDGE_BASE_PATH=./knowledge_base
RAG_TOP_K=3
```

### 3. Prepare Knowledge Base

Create a `knowledge_base` directory and add your documents:

```bash
mkdir -p knowledge_base
# Add .txt files with your FAQs, documentation, etc.
```

### 4. Setup Frontend

```bash
cd frontend
npm install
```

Create `frontend/.env`:
```env
REACT_APP_LIVEKIT_URL=wss://your-project.livekit.cloud
REACT_APP_BACKEND_URL=http://localhost:8000
```

## 🏃 Running the Application

You need **3 terminals** running simultaneously:

### Terminal 1: Voice Agent
```bash
python voice_agent.py dev
```

### Terminal 2: Token Server
```bash
python token_server.py
```

### Terminal 3: Frontend
```bash
cd frontend
npm start
```

The app will open at `http://localhost:3000`

## 🧪 Testing

### Test Complete System
```python
from voice_agent import VoiceAgent
import asyncio

async def test():
    agent = VoiceAgent()
    response = await agent.process_user_input('What are your business hours?')
    print(response)

asyncio.run(test())
```

## 📝 Example Interactions

### Question: Business Hours
**Input:** "What are your business hours?"

**RAG Retrieval:** Retrieved from faqs.txt (score: 1.14)

**Response:** "Our customer support team is here to help Monday through Friday, from 9:00 AM to 6:00 PM EST. For our enterprise customers with urgent technical issues, we also offer 24/7 emergency support."

### Question: Pricing
**Input:** "What pricing plans do you offer?"

**Response:** "We offer three pricing plans: the Starter Plan at $99 per month, the Professional Plan for $299 per month, and a custom Enterprise Plan for unlimited usage."

## 🔧 How It Works

### RAG Integration

1. **Retrieve** relevant context from knowledge base using FAISS
2. **Augment** the prompt with retrieved context
3. **Generate** response using Gemini with context awareness

### Vector Search

- Uses sentence-transformers (all-MiniLM-L6-v2) for embeddings
- FAISS for efficient similarity search
- Returns top-k most relevant documents with similarity scores

## 📊 Project Structure

```
livekit-voice-agent/
├── voice_agent.py          # Main agent implementation
├── rag_system.py          # RAG with FAISS
├── token_server.py        # Authentication server
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
├── knowledge_base/        # Knowledge base documents
│   └── faqs.txt
├── frontend/              # React application
│   ├── src/
│   │   ├── App.js
│   │   └── App.css
│   └── package.json
└── README.md
```

## 🐛 Troubleshooting

### Gemini API Issues
- Verify API key is correct
- Check quota at https://ai.dev/usage
- Use `models/gemini-2.5-flash` model

### LiveKit Connection Failed
- Check `.env` credentials
- Ensure URL starts with `wss://`

### Port Already in Use
```bash
sudo lsof -ti:8000 | xargs kill -9
```

## 📈 Performance

- **RAG Retrieval:** ~15ms per query
- **Gemini Response:** ~500-1000ms
- **Total Response Time:** ~1-2 seconds
- **Knowledge Base:** 7 documents, 7 vectors

## 🚀 Future Enhancements

1. **Audio Processing:** Integrate STT/TTS for full voice interaction
2. **Advanced RAG:** Support PDF, DOCX, chunking strategies
3. **Production:** Docker, load balancing, monitoring

## 📚 Resources

- [LiveKit Documentation](https://docs.livekit.io/)
- [Gemini API Documentation](https://ai.google.dev/docs)
- [FAISS Documentation](https://faiss.ai/)

---

# Project Demo

![Demo Image](https://drive.google.com/uc?export=view&id=1lND2J3DuUw8wf2ueqwfUSiE-C1VLIj_9)

Click image to watch demo:

[![Demo Video](https://drive.google.com/uc?export=view&id=1lND2J3DuUw8wf2ueqwfUSiE-C1VLIj_9)](https://drive.google.com/file/d/11rcsX6iCFMaRcaHoyDZYauYjHHAftvZt/view?usp=sharing)


**Built for AI Engineer / Voice Agent Developer Assessment**

