# Deployment Guide

## Deploy Backend to Render.com (Free)

### Step 1: Create Render Account
1. Go to https://render.com
2. Sign up with your GitHub account (easier)

### Step 2: Deploy the Backend
1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repo (`Resume-Parser`)
3. Fill in details:
   - **Name**: `resume-parser-backend` (or anything)
   - **Runtime**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Step 3: Add Environment Variables
1. Click **"Environment"** section
2. Add these variables (copy from your `main.env`):
   - `OPENROUTER_API_KEY=your_key_here`
   - `GEMINI_API_KEY=your_key_here`
   - `GROQ_API_KEY=your_key_here`
   - (Add any other keys from main.env)

### Step 4: Deploy
1. Click **"Create Web Service"**
2. Wait for deployment (5-10 minutes)
3. You'll get a URL like: `https://resume-parser-backend-xxxx.onrender.com`

### Step 5: Update Your HTML
Replace the `API_BASE` in `resume parser.html`:
```javascript
const API_BASE = 'https://resume-parser-backend-xxxx.onrender.com'; // Your new Render URL
```

### Step 6: Test
1. Push updated HTML to GitHub
2. Open `resume parser.html` in browser
3. Upload a PDF to test

### Important Notes
- Render free tier has limited resources, so first request might be slow
- Keep your API keys safe in environment variables (never commit them)
- The backend will auto-restart if needed

---

## Alternative: Deploy to Railway.app
1. Go to https://railway.app
2. Connect GitHub repo
3. Add `main.py` as entry point
4. Set same environment variables
5. Get the deployment URL

---

## Test Your Deployment
Once deployed, test the backend with:
```bash
curl -i https://your-deployment-url.onrender.com/
```

Should return: `{"status":"ok","message":"Resume parser backend is running."}`
