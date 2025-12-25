
# Resume Shortlisting Application

A full-stack resume screening system with AI-powered candidate matching. Upload resumes (PDF/DOCX) and job descriptions to get instant match scores with detailed skill analysis and experience detection.

## 🚀 Quick Start
# Resume Shortlisting Application

An end-to-end AI-driven resume shortlisting platform that analyzes resumes, compares them with job descriptions, and ranks candidates using fast TF-IDF matching with optional BERT-based semantic similarity.

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

Open [http://localhost:3000](http://localhost:3000) in your browser.

## ✨ Features

- Smart resume matching: TF-IDF (fast) + optional BERT (accurate)
- Skill detection and experience estimation
- PDF and DOCX support
- AI-powered scoring (0–100%) with recommendations
- Real-time validation and cloud-ready deployment

## 📚 API

See [backend/README.md](backend/README.md) for endpoints and examples.

## 📁 Project Structure

```
├── README.md
├── ARCHITECTURE.md
├── DEPLOYMENT.md
├── SCREENSHOTS.md
├── app/
├── components/
├── lib/
└── backend/
```

## Next Steps

- Try locally (backend + frontend)
- Deploy (see DEPLOYMENT.md)
- Customize skills and weights


## 📚 API Endpoints
