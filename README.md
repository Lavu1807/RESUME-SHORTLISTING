
# Resume Shortlisting Application

A full-stack resume screening system with AI-powered candidate matching. Upload resumes (PDF/DOCX) and job descriptions to get instant match scores with detailed skill analysis and experience detection.

## 🚀 Quick Start

### Prerequisites
- Python 3.13+
- Node.js 18+

### Backend Setup
```bash
pip install -r backend/requirements.txt
python -m uvicorn backend.main:app --reload --port 8000
```

### Frontend Setup
```bash
npm install
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
npm run dev
```

Open **[http://localhost:3000](http://localhost:3000)** in your browser.

## ✨ Features

- **Smart Resume Matching**: TF-IDF keyword matching (fast) + optional BERT semantic matching (accurate)
- **Skill Detection**: Automatically detects 20+ technical skills
- **Experience Extraction**: Estimates years of experience from resume
- **Multi-Format Support**: Handles PDF and DOCX files
- **AI-Powered Scoring**: 0-100% match score with recommendation logic
- **Real-Time Validation**: Instant feedback on file uploads
- **Cloud-Ready**: Deploy to Vercel (frontend) + Render (backend)

## 📋 How It Works

1. **Upload Resume**: Drag-and-drop PDF or DOCX file
2. **Enter Job Description**: Paste job requirements
3. **Choose Matching Method**:
   - Default: TF-IDF (fast, < 1 second)
   - Optional: BERT semantic matching (accurate, 3-5 seconds)
4. **View Results**:
   - Match score (0-100%)
   - Detected skills
   - Estimated experience
   - Top job keywords
   - Hiring recommendation

## 🏗️ Architecture

See **[ARCHITECTURE.md](ARCHITECTURE.md)** for detailed system design, data flows, and technology stack.

## 🎨 Screenshots & Features

See **[SCREENSHOTS.md](SCREENSHOTS.md)** for screen descriptions, user flows, and feature highlights.

## 🌐 Deployment

See **[DEPLOYMENT.md](DEPLOYMENT.md)** for step-by-step instructions to deploy to Vercel + Render.

## 📚 API Endpoints

### POST /score
Score a resume against job description.

**Response**:
```json
{
  "score": 78.5,
  "top_keywords": ["python", "fastapi", "sql"],
  "skills_matched": ["python", "fastapi"],
  "years_experience": 5.0,
  "method_used": "tfidf"
}
```

See [backend/README.md](backend/README.md) for complete API documentation.

## 🛠️ Tech Stack

**Frontend**: Next.js 14, React 18, TypeScript, Tailwind CSS
**Backend**: FastAPI, NLTK, scikit-learn, transformers (BERT)
**Deploy**: Vercel (frontend), Render (backend)

## 📁 Project Structure

```
├── README.md                # This file
├── ARCHITECTURE.md          # System design
├── DEPLOYMENT.md            # Deployment guide
├── SCREENSHOTS.md           # Feature descriptions
├── app/                     # Next.js pages
├── components/              # React components
├── lib/api.ts              # API client
└── backend/                # FastAPI server
    ├── main.py
    ├── services/
    └── requirements.txt
```

## 🚀 Next Steps

1. **Try locally**: Run both servers
2. **Deploy**: Follow [DEPLOYMENT.md](DEPLOYMENT.md)
3. **Customize**: Add skills, adjust weights
4. **Enhance**: Batch processing, history, database

---

**Ready to screen resumes efficiently?** Start at http://localhost:3000 🎯

# RESUME-SHORTLISTING
An end-to-end AI-driven resume shortlisting platform that automatically analyzes resumes, compares them with job descriptions, and ranks candidates using NLP-based similarity matching and machine learning techniques.

