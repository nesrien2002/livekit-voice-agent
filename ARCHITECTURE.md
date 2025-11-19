# System Architecture

## Overview

This document explains the architecture and design decisions for the LiveKit Voice Agent with Gemini and RAG.

## Components

### 1. Voice Agent (voice_agent.py)

**Purpose:** Core intelligence of the system

**Responsibilities:**
- Connect to LiveKit rooms
- Process user queries
- Integrate with RAG system
- Generate responses using Gemini
- Manage conversation state

**Key Classes:**
```python
class VoiceAgent:
    - __init__(): Initialize RAG and Gemini model
    - process_user_input(): Main processing pipeline
    - get_conversation_history(): Track conversations
```

**Processing Pipeline:**
```
User Input
    ↓
RAG Retrieval (top-k=3)
    ↓
Context Extraction
    ↓
Prompt Engineering
    ↓
Gemini Generation
    ↓
Response
```

### 2. RAG System (rag_system.py)

**Purpose:** Knowledge retrieval and semantic search

**Components:**
- **Embedding Model:** all-MiniLM-L6-v2 (384 dimensions)
- **Vector Store:** FAISS IndexFlatL2
- **Documents:** Text chunks from knowledge base

**Workflow:**
```python
1. Load documents from knowledge_base/
2. Generate embeddings using sentence-transformers
3. Build FAISS index
4. Query: embed → search → return top-k results
```

**Performance Considerations:**
- GPU acceleration (CUDA) when available
- In-memory index for fast retrieval
- Batch processing for embeddings

### 3. Token Server (token_server.py)

**Purpose:** Authentication and authorization

**Endpoints:**
- `GET /get-token`: Generate LiveKit JWT tokens
- `GET /health`: Health check

**Security:**
- Uses LiveKit API key and secret
- Generates JWT with room and user permissions
- CORS enabled for frontend

### 4. Frontend (React)

**Purpose:** User interface

**Components:**
- **App.js:** Main component with connection logic
- **App.css:** Styling and animations
- **LiveKit Client:** Room management

**State Management:**
```javascript
- userName: User identity
- roomName: LiveKit room to join
- connected: Connection status
- transcripts: Activity log
- Room instance via useRef
```

## Data Flow

### Connection Flow

```
1. User enters name → Frontend
2. Click "Connect" → Request token from backend
3. Backend generates JWT → Returns to frontend
4. Frontend connects to LiveKit with token
5. Voice agent detects participant join
6. Session established
```

### Query Flow

```
1. User speaks (audio input)
2. [STT - To be implemented]
3. Text sent to Voice Agent
4. Agent queries RAG system
5. RAG returns relevant documents
6. Agent builds prompt with context
7. Gemini generates response
8. [TTS - To be implemented]
9. Audio response played to user
```

### Current Implementation (Text-based)

```
1. User input text
2. RAG retrieval
3. Gemini generation
4. Text response
```

## Technology Stack

### Backend
- **Python 3.12**
- **LiveKit SDK:** Real-time communication
- **Google Generative AI:** Language generation
- **FAISS:** Vector similarity search
- **Sentence Transformers:** Embeddings
- **Flask:** HTTP server
- **asyncio:** Async operations

### Frontend
- **React 18**
- **LiveKit Client SDK**
- **Modern JavaScript (ES6+)**

### Infrastructure
- **LiveKit Cloud:** WebRTC infrastructure
- **Google AI Studio:** Gemini API

## Design Decisions

### Why FAISS?
- **Fast:** O(log n) search with proper indexing
- **Efficient:** Low memory footprint
- **Simple:** Easy to implement and maintain
- **Scalable:** Can handle millions of vectors

### Why Gemini 2.5 Flash?
- **Fast:** Low latency (~500-1000ms)
- **Cost-effective:** Free tier available
- **Capable:** Good understanding and generation
- **Safety:** Built-in content filtering

### Why Sentence-Transformers?
- **Quality:** State-of-the-art embeddings
- **Lightweight:** 384-dimensional vectors
- **Fast:** GPU-accelerated
- **Semantic:** Captures meaning, not just keywords

### Why LiveKit?
- **WebRTC:** Industry standard for real-time media
- **Scalable:** Cloud infrastructure
- **Features:** Built-in room management
- **SDKs:** Good Python and JavaScript support

## Security Considerations

### Implemented
✅ Environment variables for secrets
✅ JWT-based authentication
✅ CORS configuration
✅ API key validation

### Recommended for Production
🔒 HTTPS/WSS only
🔒 Rate limiting
🔒 Input validation and sanitization
🔒 User authentication (OAuth, etc.)
🔒 Audit logging
🔒 Secret rotation

## Scalability

### Current Capacity
- **Single instance:** ~10-50 concurrent users
- **Knowledge base:** ~1000 documents
- **Response time:** ~1-2 seconds

### Scaling Options

**Horizontal Scaling:**
- Deploy multiple voice agent workers
- Load balancer for token server
- Shared knowledge base (Redis/PostgreSQL)

**Vertical Scaling:**
- Better GPU for embeddings
- More memory for larger FAISS index
- Faster CPU for Gemini API calls

**Optimization:**
- Cache common queries
- Precompute embeddings
- Use approximate search (IndexIVFFlat)
- Batch processing

## Error Handling

### Agent Level
```python
try:
    # Process query
except Exception as e:
    logger.error(f"Error: {e}")
    return fallback_response
```

### Frontend Level
```javascript
try {
    // Connect to room
} catch (error) {
    console.error(error);
    showError("Connection failed");
}
```

### Token Server Level
```python
@app.errorhandler(500)
def handle_error(e):
    return jsonify({'error': str(e)}), 500
```

## Monitoring

### Logging
- **INFO:** Normal operations
- **ERROR:** Failures and exceptions
- **DEBUG:** Detailed execution flow

### Metrics to Track
- Response latency
- RAG retrieval time
- Gemini API latency
- Error rates
- Active connections

## Future Architecture

### Phase 1: Audio Integration
```
User Voice → STT → Text → Agent → TTS → Audio Response
```

### Phase 2: Streaming
```
User Voice → Streaming STT → Chunks → Agent → Streaming TTS → Audio
```

### Phase 3: Multimodal
```
Voice + Screen + Documents → Agent → Voice + Visual Responses
```

## Development Guidelines

### Code Organization
- One responsibility per module
- Clear naming conventions
- Type hints where applicable
- Comprehensive docstrings

### Testing Strategy
- Unit tests for RAG system
- Integration tests for agent
- End-to-end tests for full flow

### Deployment
1. Docker containerization
2. Environment-specific configs
3. CI/CD pipeline
4. Health checks and monitoring

---

**Last Updated:** November 2025