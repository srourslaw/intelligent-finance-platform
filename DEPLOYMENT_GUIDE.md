# Deployment Guide

## Overview
This application uses a split deployment architecture:
- **Frontend**: Deployed on Vercel (React + Vite)
- **Backend**: Deployed on Render (FastAPI + Python)

---

## Backend Deployment (Render)

### 1. Create Render Account
- Go to https://render.com
- Sign up or log in with your GitHub account

### 2. Create New Web Service
1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository: `srourslaw/intelligent-finance-platform`
3. Configure the service:
   - **Name**: `intelligent-finance-platform-backend`
   - **Region**: Oregon (or closest to you)
   - **Branch**: `main`
   - **Root Directory**: Leave blank (render.yaml handles this)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install --upgrade pip && pip install -r backend/requirements.txt`
   - **Start Command**: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### 3. Set Environment Variables
In Render dashboard → Environment → Add the following:
```
SECRET_KEY=<generate-a-random-32-char-string>
ENVIRONMENT=production
PYTHON_VERSION=3.11.0
```

### 4. Deploy
- Click **"Create Web Service"**
- Render will automatically deploy your backend
- Wait for deployment to complete (5-10 minutes)
- Copy the backend URL (e.g., `https://intelligent-finance-platform-backend.onrender.com`)

### 5. Verify Backend is Running
Visit: `https://intelligent-finance-platform-backend.onrender.com/api/health`

Should return:
```json
{
  "status": "healthy",
  "message": "API is running"
}
```

---

## Frontend Deployment (Vercel)

### 1. Configure Environment Variable
1. Go to Vercel dashboard: https://vercel.com/hussein-srours-projects/intelligent-finance-platform
2. Click **Settings** → **Environment Variables**
3. Add new variable:
   - **Name**: `VITE_API_URL`
   - **Value**: `https://intelligent-finance-platform-backend.onrender.com/api`
   - **Environment**: Production, Preview, Development (select all)
4. Click **Save**

### 2. Trigger Redeployment
1. Go to **Deployments** tab
2. Click on the latest deployment
3. Click **"Redeploy"** → **"Redeploy"**
4. Wait for deployment to complete (2-3 minutes)

### 3. Verify Frontend is Working
1. Visit: https://intelligent-finance-platform.vercel.app
2. Open browser console (F12)
3. Try logging in
4. Check that API requests go to Render backend URL

---

## Update CORS in Backend

After getting your Render URL, update `backend/app/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "https://intelligent-finance-platform.vercel.app",
        "https://intelligent-finance-platform-git-main-hussein-srours-projects.vercel.app",
        "https://intelligent-finance-platform-*.vercel.app",
        # Add your custom Vercel domains here
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Then commit and push:
```bash
git add backend/app/main.py
git commit -m "feat: add Render CORS configuration"
git push origin main
```

Render will auto-deploy the update.

---

## Troubleshooting

### Frontend shows "Failed to fetch"
- Check Vercel environment variable `VITE_API_URL` is set correctly
- Verify Render backend is running (visit health endpoint)
- Check browser console for CORS errors

### Backend shows CORS errors
- Add your Vercel URL to `allow_origins` in `backend/app/main.py`
- Make sure to include both production and preview URLs

### Render free tier sleeps after 15 minutes
- First request after sleep takes 30-60 seconds
- Consider upgrading to paid plan for always-on service
- Or implement a keep-alive ping from frontend

---

## Environment Variables Summary

### Vercel (Frontend)
```
VITE_API_URL=https://intelligent-finance-platform-backend.onrender.com/api
```

### Render (Backend)
```
SECRET_KEY=<random-32-char-string>
ENVIRONMENT=production
PYTHON_VERSION=3.11.0
```

---

## Deployment Checklist

- [ ] Backend deployed to Render
- [ ] Backend health endpoint returns 200
- [ ] Vercel environment variable `VITE_API_URL` configured
- [ ] Frontend redeployed with new environment variable
- [ ] CORS configured in backend for Vercel domains
- [ ] Test login functionality
- [ ] Test project selection
- [ ] Test dashboard data loading
- [ ] Test document viewer
- [ ] Test budget breakdown

---

## Monitoring

### Check Backend Logs
Render Dashboard → Your Service → Logs

### Check Frontend Logs
Vercel Dashboard → Deployments → Click deployment → Function Logs

### Check API Health
```bash
curl https://intelligent-finance-platform-backend.onrender.com/api/health
```

---

## Automatic Deployments

Both services are configured for automatic deployment:
- **Vercel**: Auto-deploys on every push to `main` branch
- **Render**: Auto-deploys on every push to `main` branch

Make sure `render.yaml` is in the repository root for automatic configuration.
