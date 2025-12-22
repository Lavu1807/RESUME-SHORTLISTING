# 🚀 Deployment Checklist

Complete this checklist before deploying to production.

## Pre-Deployment

### Code Quality
- [ ] All TypeScript/Python files compile without errors
- [ ] No console warnings or errors
- [ ] Backend health endpoint works: `curl http://localhost:8000/health`
- [ ] Frontend loads without errors: http://localhost:3000
- [ ] Form validation works (try invalid inputs)
- [ ] API connection works (upload + analyze)
- [ ] Results display correctly

### Testing
- [ ] Test with sample PDF resume
- [ ] Test with sample DOCX resume
- [ ] Test error handling (invalid file, empty job description)
- [ ] Test BERT toggle (both on/off)
- [ ] Test on mobile screen sizes
- [ ] Test with different job descriptions

### Documentation
- [ ] README.md is complete
- [ ] ARCHITECTURE.md is accurate
- [ ] DEPLOYMENT.md is clear
- [ ] SCREENSHOTS.md describes features
- [ ] PROJECT_SUMMARY.md is updated
- [ ] API documentation in backend/README.md
- [ ] Comments in code are clear
- [ ] No TODOs left in production code

## Backend Preparation

### Code
- [ ] No hardcoded localhost URLs
- [ ] All imports are in requirements.txt
- [ ] requirements.txt pinned to specific versions
- [ ] Procfile is correct: `web: python -m uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
- [ ] runtime.txt exists with Python version
- [ ] No debug prints in production code
- [ ] CORS is configured correctly
- [ ] Error messages are user-friendly

### Environment Variables
- [ ] ENABLE_GPT5 documented
- [ ] No secrets in code
- [ ] .env.local is in .gitignore
- [ ] Render env vars configured

### Performance
- [ ] Text extraction is reasonably fast (< 1s for normal resumes)
- [ ] TF-IDF scoring is instant (< 100ms)
- [ ] BERT loading works (even if slow on first run)
- [ ] No memory leaks with repeated calls
- [ ] Handles large PDFs without crashing (< 10MB)

## Frontend Preparation

### Code
- [ ] No hardcoded API URLs except in .env.local
- [ ] All TypeScript types are correct
- [ ] No console.log() calls in production
- [ ] vercel.json is correct
- [ ] NEXT_PUBLIC_API_URL uses environment variable
- [ ] No sensitive data in frontend code

### Environment Variables
- [ ] .env.local created with NEXT_PUBLIC_API_URL=http://localhost:8000
- [ ] Will update to production URL after backend deployed
- [ ] No other secrets in env vars

### Assets
- [ ] All images/icons load correctly
- [ ] Fonts load properly
- [ ] CSS is optimized
- [ ] Next.js image optimization is enabled

## Deployment Steps

### 1. GitHub Setup
- [ ] Repository created
- [ ] Code committed: `git add . && git commit -m "Initial commit"`
- [ ] Pushed to main branch: `git push origin main`
- [ ] GitHub token/SSH key configured

### 2. Backend Deployment (Render)
- [ ] Render account created
- [ ] Repository connected to Render
- [ ] Build command set: `pip install -r backend/requirements.txt`
- [ ] Start command set: `python -m uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
- [ ] Environment variable ENABLE_GPT5=true added
- [ ] Deploy initiated
- [ ] [ ] Deployment successful (check dashboard)
- [ ] [ ] Health endpoint works: `curl https://resume-backend-xxx.onrender.com/health`
- [ ] [ ] Copy backend URL: `https://resume-backend-xxx.onrender.com`

### 3. Frontend Deployment (Vercel)
- [ ] Vercel account created
- [ ] Repository imported to Vercel
- [ ] Framework auto-detected as Next.js
- [ ] Build command: `npm run build` (default)
- [ ] Install command: `npm install` (default)
- [ ] Environment variable added: `NEXT_PUBLIC_API_URL=https://resume-backend-xxx.onrender.com`
- [ ] Deploy initiated
- [ ] [ ] Deployment successful (check dashboard)
- [ ] [ ] Frontend loads: https://resume-shortlisting.vercel.app
- [ ] [ ] Copy frontend URL

### 4. Integration Testing
- [ ] Open production frontend URL
- [ ] Upload PDF to production
- [ ] View results in production
- [ ] Check browser console for errors
- [ ] Check Vercel deployment logs for errors
- [ ] Check Render service logs for errors

## Post-Deployment

### Monitoring
- [ ] Set up Vercel notifications for failed deployments
- [ ] Set up Render notifications for service issues
- [ ] Bookmark Render backend dashboard
- [ ] Bookmark Vercel frontend dashboard
- [ ] Monitor first few hours for errors

### Communication
- [ ] Share production URL with team/stakeholders
- [ ] Document the deployment in project notes
- [ ] Update any external documentation
- [ ] Provide feedback form/contact info

### Optimization (Optional)
- [ ] Enable Vercel Analytics
- [ ] Enable Render monitoring
- [ ] Add custom domain (if applicable)
- [ ] Configure custom CORS if needed
- [ ] Set up rate limiting (if needed)

## Rollback Plan

### If Frontend Breaks
1. Go to Vercel Dashboard → Deployments
2. Click on previous working deployment
3. Click "Promote to Production"
4. Verify fix

### If Backend Breaks
1. Go to Render Dashboard → Deploys
2. Click on previous successful deploy
3. Click "Redeploy"
4. Verify fix

### If API Connection Breaks
1. Check NEXT_PUBLIC_API_URL in Vercel env vars
2. Verify Render backend is running (check logs)
3. Test CORS: `curl -H "Origin: https://vercel-url" https://render-url/health`
4. Check for 10-second cold start delay from Render

## Launch Checklist

### Before Public Launch
- [ ] Test full user flow one more time
- [ ] Verify all features work
- [ ] Check on mobile and desktop
- [ ] Confirm analytics are working (optional)
- [ ] Review error logs one more time
- [ ] Have rollback plan ready

### Launch Day
- [ ] Announce production URL
- [ ] Monitor for errors (first hour)
- [ ] Have support contact info ready
- [ ] Be prepared to rollback if issues

### Post-Launch
- [ ] Gather user feedback
- [ ] Monitor performance metrics
- [ ] Plan for improvements
- [ ] Document any production issues
- [ ] Schedule regular maintenance

---

## URLs to Save

**Production Frontend**: 
```
https://resume-shortlisting.vercel.app
```

**Production Backend**: 
```
https://resume-backend-xxx.onrender.com
```

**Backend Health Check**: 
```
https://resume-backend-xxx.onrender.com/health
```

**Vercel Dashboard**: 
```
https://vercel.com/dashboard
```

**Render Dashboard**: 
```
https://dashboard.render.com
```

---

## Quick Reference: Common Issues & Fixes

| Issue | Fix |
|-------|-----|
| "Could not reach backend" | Check NEXT_PUBLIC_API_URL in Vercel env, restart deploy |
| PDF extraction fails | Ensure PDF is valid, < 10MB, starts with %PDF |
| BERT timeout | First run downloads model, wait 30+ seconds or use TF-IDF |
| 502 Bad Gateway | Render service crashed, check logs, restart service |
| CORS error | Check CORS origins in `backend/main.py`, restart backend |
| Environment vars not working | Commit changes, push to GitHub, wait for redeploy |

---

## Final Sign-Off

- [ ] Project owner reviewed
- [ ] All tests passed
- [ ] Documentation complete
- [ ] Ready for production
- [ ] Team approved

**Deployed by**: ________________  
**Date**: ________________  
**Notes**: ________________  

---

**Good luck with your deployment!** 🚀

Need help? Check:
1. [DEPLOYMENT.md](DEPLOYMENT.md) - Detailed deployment guide
2. [ARCHITECTURE.md](ARCHITECTURE.md) - System design
3. Vercel + Render dashboards for logs
4. Project README for quick reference
