# 📋 Resume Parser - Teacher Demo Guide

## GitHub Repository
**Link**: https://github.com/Aayush211142/Resume-Parser

---

## 🚀 Quick Start for Your Teacher

Your teacher can try the project in **2 ways**:

### **Option 1: Try Online (Easiest)**
1. Go to: https://github.com/Aayush211142/Resume-Parser
2. Click **"Resume parser.html"** file
3. Click **Raw** button
4. Your browser will show the page
5. Click upload button and try a PDF

*Note: This requires the backend to be deployed (see deployment status below)*

---

### **Option 2: Run Locally (Full Setup)**
1. **Clone the repo**:
   ```bash
   git clone https://github.com/Aayush211142/Resume-Parser.git
   cd Resume-Parser
   ```

2. **Set up virtual environment**:
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Create `main.env` file** with API keys:
   ```
   OPENROUTER_API_KEY=your_key
   GEMINI_API_KEY=your_key
   GROQ_API_KEY=your_key
   ```

5. **Start the backend**:
   ```bash
   uvicorn main:app --reload
   ```

6. **Open the frontend**:
   - Open `resume parser.html` in your browser
   - Upload a PDF resume

---

## ✨ Features to Show

- ✅ **Upload PDF** → Resume is parsed instantly
- ✅ **AI-Powered** → Extracts name, email, phone, skills, work history
- ✅ **Multiple AI Providers** → Falls back automatically if one fails
- ✅ **Local Fallback** → Regex-based parsing when AI is unavailable
- ✅ **Responsive UI** → Works on desktop and mobile

---

## 🔑 API Keys Used

The app uses **multiple free AI providers** for parsing:
1. **OpenRouter** (Free tier: Gemini 2.5 Flash)
2. **Google Gemini** (Free tier available)
3. **Groq Llama** (Free tier)
4. **Local Parser** (No API key needed - fallback)

---

## 📁 Project Structure

```
Resume-Parser/
├── main.py                 # FastAPI backend
├── resume parser.html      # Web interface
├── requirements.txt        # Dependencies
├── main.env.example        # Template for API keys
├── README.md              # Full documentation
└── DEPLOYMENT.md          # How to deploy to cloud
```

---

## 🎯 What Makes This Project Cool

1. **AI Integration**: Uses cutting-edge LLMs for parsing
2. **Graceful Fallbacks**: Multiple AI providers + local parsing
3. **Full Stack**: Both frontend and backend
4. **Production Ready**: CORS, error handling, deployable
5. **No Database Needed**: Everything in JSON response

---

## 📝 Questions Your Teacher Might Ask

**Q: How does it extract resume data?**
- Uses AI (Gemini/Groq) to parse PDFs intelligently
- Falls back to regex patterns if AI fails

**Q: Are API keys stored safely?**
- Yes! API keys are in `.env` file (not committed to GitHub)
- Only deployed backend needs the real keys

**Q: Can it be deployed?**
- Yes! See `DEPLOYMENT.md` for Render.com setup

**Q: What if both AI and local parser fail?**
- Shows error message with details about what happened

---

## 🌟 Live Demo (If Deployed)

Once you deploy to Render/Railway, your teacher can test it live without any setup!

---

## Need Help?
Check the README.md or DEPLOYMENT.md files in the repo.
