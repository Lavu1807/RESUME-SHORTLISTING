# System Architecture

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      Resume Shortlisting System                  │
└─────────────────────────────────────────────────────────────────┘

                            ┌──────────────┐
                            │   User       │
                            │  (Browser)   │
                            └──────┬───────┘
                                   │ HTTP/HTTPS
                ┌──────────────────┴──────────────────┐
                │                                     │
         ┌──────▼──────┐                       ┌──────▼──────┐
         │ Next.js App │                       │  FastAPI    │
         │ (Vercel)    │◄─────────────────────►│  (Render)   │
         │ Port 3000   │    REST JSON API      │  Port 8000  │
         └─────────────┘                       └──────┬──────┘
                │                                     │
         ┌──────▼──────────────┐            ┌────────▼─────────┐
         │   React Components  │            │ Python Services  │
         │   - Upload Form     │            ├──────────────────┤
         │   - Results View    │            │ Text Extraction  │
         │   - UI Components   │            │ - pdfplumber     │
         └─────────────────────┘            │ - python-docx    │
                │                           │                  │
         ┌──────▼──────────────┐            │ ML Scoring       │
         │  Fetch API Client   │            │ - TF-IDF         │
         │ (lib/api.ts)        │            │ - BERT (optional)│
         └─────────────────────┘            │ - NLTK           │
                │                           │ - scikit-learn   │
         ┌──────▼──────────────┐            │                  │
         │  Environment Config  │            │ Skill Detection  │
         │ .env.local           │            │ Experience Est.  │
         │ NEXT_PUBLIC_API_URL  │            └──────────────────┘
         └─────────────────────┘
```

## Frontend Architecture (Next.js)

```
frontend/
├── app/
│   ├── layout.tsx          # Root layout, header
│   ├── page.tsx            # Home page with upload form
│   ├── results/
│   │   └── page.tsx        # Results display page
│   └── globals.css         # Global styles
├── components/
│   ├── resume-upload-form.tsx   # Form with validation & API calls
│   ├── results-view.tsx         # Results display with charts
│   ├── label.tsx                # Custom label component
│   ├── progress.tsx             # Progress bar component
│   ├── textarea.tsx             # Custom textarea component
│   └── ui/
│       ├── badge.tsx            # Badge component
│       ├── button.tsx           # Button component
│       ├── card.tsx             # Card container
│       ├── label.tsx            # Form label
│       ├── progress.tsx         # Progress indicator
│       └── textarea.tsx         # Text input
├── lib/
│   ├── api.ts              # Fetch API client functions
│   └── utils.ts            # Utility functions
└── public/                 # Static assets
```

### Data Flow (Frontend)

```
User Upload
    │
    ├─► Drag & Drop / File Input
    │        │
    │        ▼
    └─► Form Validation
         │
         ├─► Resume file check (PDF/DOCX, < 10MB)
         ├─► Job description check (non-empty)
         │
         ▼
    API Call (scoreResume)
         │
         ├─► FormData: resume + job_description
         ├─► POST to /score endpoint
         │
         ▼
    Response Handling
         │
         ├─► Success: Store in sessionStorage
         ├─► Display: results page with data
         │
         └─► Error: Show error message
```

## Backend Architecture (FastAPI)

```
backend/
├── main.py                 # FastAPI app, route definitions
├── schemas.py              # Pydantic models (request/response)
├── requirements.txt        # Python dependencies
├── Procfile               # Render deployment config
├── runtime.txt            # Python version
└── services/
    ├── text_extraction.py  # PDF/DOCX text extraction
    └── ml_logic.py         # Matching algorithms & skill detection
```

### Backend Routes

```
POST /score
├─ Input: File (resume) + String (job_description)
├─ Optional: use_bert query param
│
├─ Validation:
│   ├─ File type (PDF/DOCX)
│   ├─ File size (< 10 MB)
│   └─ Non-empty job description
│
├─ Processing:
│   ├─ Extract text from file
│   ├─ Clean & preprocess text
│   ├─ Compute TF-IDF similarity
│   ├─ Optional: BERT semantic similarity
│   ├─ Detect technical skills
│   └─ Extract experience level
│
└─ Output: ScoreResponse
   ├─ score (0-100)
   ├─ top_keywords
   ├─ skills_matched
   ├─ years_experience
   └─ method_used

GET /health
└─ Output: {"status": "ok"}

GET /config
└─ Output: {"enable_gpt5": true/false}
```

### Data Processing Pipeline

```
Resume File (PDF/DOCX)
    │
    ▼
Text Extraction
├─► pdfplumber (PDF)
├─► python-docx (DOCX)
    │
    ▼
Text Cleaning
├─► Remove extra whitespace
├─► Normalize newlines
├─► UTF-8 encoding
    │
    ▼
Preprocessing
├─► Lowercase
├─► NLTK tokenization
├─► Porter stemming
├─► Stopword removal
    │
    ├───────────┬──────────────┐
    │           │              │
    ▼           ▼              ▼
TF-IDF      BERT         Skill Detection
├─ Vectorize ├─ Embed     ├─ Regex patterns
├─ Cosine    ├─ Transform │   for 20+ skills
│  similarity│ vectors    │
│  50-100ms  │ 3-5s       ├─ Experience
└─ Score     └─ Score     │  extraction
   0-100        0-100     │
                          └─ Years estimate
                             │
                             ▼
                          ScoreResponse
```

## Technology Stack

### Frontend
- **Framework**: Next.js 14 (React 18)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Components**: Shadcn UI
- **HTTP Client**: Fetch API
- **State**: React Hooks + SessionStorage

### Backend
- **Framework**: FastAPI
- **Server**: Uvicorn
- **Language**: Python 3.13
- **Text Extraction**:
  - pdfplumber (PDF parsing)
  - python-docx (DOCX parsing)
- **NLP & ML**:
  - NLTK (tokenization, stemming, stopwords)
  - scikit-learn (TF-IDF, cosine similarity)
  - transformers (BERT embeddings)
  - PyTorch (neural network backend)
- **Validation**: Pydantic

### Infrastructure
- **Frontend Hosting**: Vercel (CDN, serverless functions)
- **Backend Hosting**: Render (Docker containers, auto-scaling)
- **Database**: None (stateless, compute-only)
- **API Communication**: REST JSON over HTTPS

## Performance Characteristics

### Response Times (Local)
- TF-IDF: ~50-100ms
- BERT: ~3-5 seconds (CPU)
- API Overhead: ~200-500ms

### Memory Usage
- Frontend: ~2-5 MB (React bundle)
- Backend: ~500 MB (NLTK + scikit-learn)
- BERT Model: ~400 MB (lazy loaded on first use)

### Deployment Sizes
- Frontend Docker: ~100 MB
- Backend Python: ~500 MB + dependencies
- Vercel: Zero-config deployment
- Render: Automatic Docker build

## Security Considerations

### Input Validation
- ✅ File type whitelist (PDF, DOCX only)
- ✅ File size limit (10 MB)
- ✅ Text length validation
- ✅ Pydantic schema validation

### CORS
- ✅ Configured for localhost:3000 (dev)
- ✅ Production: Add deployed domain

### API Security
- ⚠️ No authentication (public API)
- 💡 Consider adding API keys for production
- 💡 Rate limiting for high-traffic scenarios

### Data Privacy
- ✅ No data persistence (stateless)
- ✅ Resume data not stored
- ✅ Processing in-memory only

## Scalability

### Horizontal Scaling
- **Frontend**: Vercel CDN automatically handles scaling
- **Backend**: Render Pro tier supports multiple instances
- **Load Balancing**: Automatic via hosting provider

### Optimization Opportunities
1. **Caching**:
   - Cache BERT model after first load
   - Cache extracted text for same resume
   - Browser caching for static assets

2. **Async Processing**:
   - Background jobs for BERT processing
   - Queue system for batch resume analysis
   - WebSocket updates for long-running tasks

3. **Database**:
   - PostgreSQL for caching results
   - Store resume hash + score
   - Historical analytics

## Deployment Flow

```
GitHub Push
    │
    ├──► Vercel Auto-Deploy
    │        │
    │        ├─ Build: npm run build
    │        ├─ Test: Run tests (optional)
    │        ├─ Deploy: Upload to CDN
    │        │
    │        └─► live at *.vercel.app
    │
    └──► Render Auto-Deploy
         │
         ├─ Detect: backend/requirements.txt
         ├─ Build: pip install dependencies
         ├─ Test: (optional)
         ├─ Deploy: Docker container
         │
         └─► live at *.onrender.com
```

## Key Design Decisions

| Decision | Why |
|----------|-----|
| Fetch API (not Axios) | Lighter, built-in, no extra dependencies |
| SessionStorage (not Redux) | Simple state for single task, fast load |
| TF-IDF Default | Fast, efficient, good for keyword matching |
| BERT Optional | Better semantics, slower, user-controlled |
| Stateless Backend | Simpler deployment, auto-scaling ready |
| FastAPI (not Django) | Lighter, faster, async-friendly |
| No Database | Keeps deployment simple, cost-free |

## Future Architecture Improvements

1. **Add Database**:
   - PostgreSQL for result caching
   - Historical analytics
   - User management

2. **Message Queue**:
   - Celery + Redis for async jobs
   - Batch processing
   - Job status tracking

3. **Caching Layer**:
   - Redis for BERT model caching
   - Resume extraction cache
   - API response caching

4. **Monitoring**:
   - Sentry for error tracking
   - DataDog for performance monitoring
   - Logs aggregation (ELK stack)

5. **Advanced ML**:
   - Fine-tuned BERT on resume domain
   - Custom skill extraction models
   - Ranking model for best matches

---

**Architecture Summary**:
- Simple, stateless, cloud-native design
- Separates concerns: frontend vs backend
- Easy to scale and deploy independently
- Minimal cost: free tier supports full functionality
- Ready for production with enterprise features
