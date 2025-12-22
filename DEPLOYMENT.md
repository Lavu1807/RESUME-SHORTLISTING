# Deployment Guide

Complete step-by-step instructions for deploying Resume Shortlisting to production.

## Overview

```
┌─────────────────────────────────────────────────────┐
│           Resume Shortlisting App                   │
├─────────────────────────────────────────────────────┤
│  Frontend (Next.js) ──┐                             │
│  Deployed to Vercel  │                             │
│                      ├──> Backend (FastAPI)        │
│  http://app.vercel.com          Deployed to Render │
│                      │      http://api.onrender.com│
│                      └───────────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

## Prerequisites

- GitHub account (for code hosting)
- Vercel account (free at https://vercel.com)
- Render account (free at https://render.com)

## Part 1: Prepare for Deployment

### 1.1 Add .gitignore (if not present)

```bash
# Frontend
node_modules/
.next/
.env.local
.env.*.local

# Backend
__pycache__/
*.pyc
*.pyo
.Python
venv/
.venv/
*.egg-info/
dist/
build/
```

### 1.2 Create GitHub Repository

```bash
git init
git add .
git commit -m "Initial commit: Resume Shortlisting App"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/resume-shortlisting.git
git push -u origin main
```

## Part 2: Deploy Backend to Render

### 2.1 Create Render Service

1. Go to https://render.com and sign up/login
2. Click **New +** → **Web Service**
3. Connect your GitHub repository
4. Configure:
   - **Name**: `resume-backend`
   - **Environment**: Python 3
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `python -m uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
   - **Region**: Choose closest to you

### 2.2 Add Environment Variables

In Render dashboard, go to **Environment** and add:

```
ENABLE_GPT5=true
```

### 2.3 Deploy

Click **Deploy**. Wait for build to complete (~3-5 minutes).

Once deployed, you'll get a URL like:
```
https://resume-backend-xxxxx.onrender.com
```

**Test backend**:
```bash
curl https://resume-backend-xxxxx.onrender.com/health
# Should return: {"status":"ok"}
```

## Part 3: Deploy Frontend to Vercel

### 3.1 Connect to Vercel

1. Go to https://vercel.com and sign up/login
2. Click **Add New...** → **Project**
3. Select your GitHub repository
4. Framework preset should auto-detect **Next.js**

### 3.2 Configure Environment Variables

In Vercel project settings → **Environment Variables**, add:

```
NEXT_PUBLIC_API_URL=https://resume-backend-xxxxx.onrender.com
```

Replace `resume-backend-xxxxx` with your actual Render backend URL.

### 3.3 Deploy

Click **Deploy**. Wait for build to complete (~2-3 minutes).

Once deployed, you'll get a URL like:
```
https://resume-shortlisting.vercel.app
```

## Part 4: Verify Deployment

### 4.1 Test Frontend

Open `https://resume-shortlisting.vercel.app` in your browser.

### 4.2 Test Full Flow

1. Upload a PDF resume
2. Enter a job description
3. Click "Analyze Resume"
4. Verify results display

### 4.3 Check Logs

**Backend logs** (Render):
- Dashboard → Service → Logs

**Frontend logs** (Vercel):
- Dashboard → Deployments → Logs

## Part 5: Custom Domain (Optional)

### Vercel Custom Domain

1. Go to project **Settings** → **Domains**
2. Add your domain (e.g., `resume-app.com`)
3. Follow DNS instructions

### Render Custom Domain

1. Go to service **Settings** → **Custom Domain**
2. Add your domain (e.g., `api.resume-app.com`)
3. Follow DNS instructions

## Troubleshooting

### Backend Connection Error

**Error**: "Could not reach backend at http://localhost:8000"

**Solution**: 
- Verify `NEXT_PUBLIC_API_URL` env var in Vercel is set to your Render backend URL
- Ensure Render backend is fully deployed and healthy
- Check CORS settings (should be enabled in `backend/main.py`)

### PDF Upload Fails

**Error**: "Could not extract text from PDF"

**Solution**:
- Ensure file is valid PDF (< 10 MB)
- Check backend logs for extraction errors
- Try a different PDF

### BERT Model Loading Timeout

**Error**: BERT model takes > 30 seconds to load

**Solution**:
- Use TF-IDF matching (default) instead of BERT for faster response
- BERT downloads ~400 MB model on first run
- Consider using backend with more memory

### Environment Variables Not Working

**Solution**:
- Vercel: Restart deployment after adding env vars
- Render: Restart service after adding env vars
- Check spelling and values match config

## Scaling Considerations

### Render Tier Upgrade

For production with high traffic:
- Upgrade from **Free** to **Pro** tier ($7/month)
- Add **PostgreSQL** database for caching results
- Enable **auto-scaling** for multiple instances

### Vercel Scaling

- Pro plan ($20/month) for higher limits
- Serverless functions auto-scale automatically

## Cost Estimates

| Service | Free Tier | Pro Tier | Notes |
|---------|-----------|----------|-------|
| Vercel Frontend | ✅ Included | $20/mo | Auto-scaling |
| Render Backend | ✅ Included (hibernates) | $7/mo | Persistent |
| **Total** | **Free** | **$27/mo** | Production-ready |

## Continuous Deployment

Both Vercel and Render support automatic deployments:

1. Push code to GitHub `main` branch
2. Vercel/Render automatically detects changes
3. New build and deployment starts automatically
4. Takes ~3-5 minutes total

No additional configuration needed!

## Rollback

**If deployment breaks:**

**Vercel**:
- Go to Deployments
- Click on previous working deployment
- Click **Promote to Production**

**Render**:
- Go to Deploys
- Click on previous successful deploy
- Click **Redeploy**

## Monitoring

### Render Monitoring

- **Logs**: Real-time error tracking
- **Metrics**: CPU, memory, bandwidth
- **Alerts**: Email on service failure

### Vercel Monitoring

- **Logs**: Build and runtime logs
- **Analytics**: Page performance, CLS, LCP
- **Alerts**: Build failures, performance issues

## Next Steps

1. ✅ Deploy backend to Render
2. ✅ Deploy frontend to Vercel
3. 🔗 Connect with backend API URL
4. 📝 Monitor logs and performance
5. 🚀 Share with team: https://resume-shortlisting.vercel.app

## Support & Resources

- **Vercel Docs**: https://vercel.com/docs
- **Render Docs**: https://render.com/docs
- **Next.js Deployment**: https://nextjs.org/learn/basics/deploying-nextjs-app
- **FastAPI Deployment**: https://fastapi.tiangolo.com/deployment/

---

**Happy Deploying!** 🚀
