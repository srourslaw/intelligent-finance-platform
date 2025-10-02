# Render Backend Deployment - AUTOMATED

## Current Status
- ✅ GitHub repo: https://github.com/srourslaw/intelligent-finance-platform
- ✅ `render.yaml` configured and pushed
- ❌ Backend service NOT yet created on Render

## Quick Deploy (5 minutes)

### Option 1: Blueprint Deployment (Recommended)
1. Go to **https://render.com/dashboard**
2. Click **"New +"** → **"Blueprint"**
3. Connect GitHub repo: `srourslaw/intelligent-finance-platform`
4. Render auto-detects `render.yaml` → Click **"Apply"**
5. Wait 5-10 minutes for build
6. Copy backend URL: `https://intelligent-finance-platform-backend.onrender.com`

### Option 2: Manual Web Service
1. Go to **https://render.com/dashboard**
2. Click **"New +"** → **"Web Service"**
3. Connect repo: `srourslaw/intelligent-finance-platform`
4. Settings:
   - **Name**: `intelligent-finance-platform-backend`
   - **Region**: Oregon (US West)
   - **Branch**: `main`
   - **Root Directory**: Leave empty
   - **Environment**: Python 3
   - **Build Command**: `pip install --upgrade pip && pip install -r backend/requirements.txt`
   - **Start Command**: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Environment Variables:
   - `PYTHON_VERSION` = `3.11.0`
   - `SECRET_KEY` = (auto-generate)
   - `ENVIRONMENT` = `production`
6. Click **"Create Web Service"**
7. Wait for deployment

## After Deployment

### Configure Vercel
1. Go to: https://vercel.com/hussein-srours-projects/intelligent-finance-platform/settings/environment-variables
2. Add/Update:
   - **Key**: `VITE_API_URL`
   - **Value**: `https://intelligent-finance-platform-backend.onrender.com/api`
   - **Scope**: Production, Preview, Development
3. Redeploy frontend from Vercel dashboard

### Verify Deployment
```bash
# Check backend health
curl https://intelligent-finance-platform-backend.onrender.com/api/health

# Expected response:
# {"status":"healthy","message":"API is running"}
```

## Files Already Configured
- ✅ `render.yaml` - Blueprint configuration
- ✅ `backend/requirements.txt` - Python dependencies
- ✅ `backend/app/main.py` - CORS configured for Vercel
- ✅ All project data in `backend/projects/`

## Auto-Deploy on Git Push
Once Render service is created:
- Any `git push origin main` will trigger auto-deployment
- Build time: ~3-5 minutes
- Free tier: sleeps after 15min inactivity (30s cold start)

---

**Status**: Ready to deploy ✅
**Next**: Create Render service via dashboard
