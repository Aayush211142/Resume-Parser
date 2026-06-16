# Resume Parser AI

An AI-powered resume parser that automatically extracts structured data from PDF resumes. Uses multiple AI providers (OpenRouter, Gemini, Groq) with a local fallback parser.

## Features

- 🚀 Upload PDF resumes and extract key information instantly
- 🤖 AI-powered extraction using multiple providers
- 📊 Fallback local parser when AI services are unavailable
- 🛡️ Clean, secure CORS-enabled backend
- 💻 Simple, responsive web interface

## Extracted Data

- Candidate name
- Email address
- Phone number
- Skills
- Work history
- Additional resume content

## Quick Start (Any Device)

### Prerequisites

- Python 3.8+
- Git

### Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/resume-parser.git
   cd resume-parser
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Copy the example file
   cp main.env.example main.env
   
   # Edit main.env with your API keys (optional)
   # The parser will still work with the local fallback if keys are missing
   ```

   > **Security note:** Do not commit `main.env` to GitHub. This file contains your private API keys.
   > If you accidentally add it to git, remove it and rotate the keys immediately.
   >
   > To remove a committed `main.env` file from git history locally, run:
   >
   > ```bash
   > git rm --cached main.env
   > git commit -m "Remove local env from repository"
   > git push
   > ```

5. **Start the backend server**
   ```bash
   python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
   ```
   You should see: `INFO:     Uvicorn running on http://127.0.0.1:8000`

6. **Start the frontend server** (in a new terminal)
   ```bash
   # Windows
   python -m http.server 8001
   
   # macOS/Linux
   python3 -m http.server 8001
   ```

7. **Open in your browser**
   ```
   http://127.0.0.1:8001/resume%20parser.html
   ```

## Usage

1. Click **"Try Now!"** button on the page
2. Select a PDF resume file
3. Wait for processing (shows status messages)
4. View extracted resume data in JSON format

## How It Works

### AI Providers (Tried in order)

1. **OpenRouter Free Model** - Uses Gemini 2.5 Flash for free
2. **Google Gemini** - Requires GEMINI_API_KEY
3. **Groq Llama** - Requires GROQ_API_KEY
4. **Local Fallback Parser** - Works offline, no API key needed

If all AI providers fail, the local parser automatically extracts text using regex patterns.

## File Structure

```
resume-parser/
├── main.py                 # FastAPI backend
├── resume parser.html      # Frontend UI
├── main.env               # API keys (local only, ignored by git)
├── main.env.example       # Template for API keys
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

> `main.env` is excluded from source control by `.gitignore`. Never upload it to GitHub.

## Getting API Keys (Optional)

The parser works WITHOUT API keys using the local fallback. To enable AI parsing:

### OpenRouter (Recommended - Easiest)
1. Go to [openrouter.ai](https://openrouter.ai)
2. Sign up for free
3. Get your API key from dashboard
4. Add to `main.env`: `OPENROUTER_API_KEY=your_key_here`

### Google Gemini
1. Go to [ai.google.dev](https://ai.google.dev)
2. Click "Get API Key"
3. Add to `main.env`: `GEMINI_API_KEY=your_key_here`

### Groq
1. Go to [console.groq.com](https://console.groq.com)
2. Create account and get API key
3. Add to `main.env`: `GROQ_API_KEY=your_key_here`

## Troubleshooting

### "Connection Refused" Error
- Make sure backend server is running: `python -m uvicorn main:app --host 127.0.0.1 --port 8000`
- Make sure frontend server is running: `python -m http.server 8001`
- Open http://127.0.0.1:8001/resume%20parser.html (not file://)

### "Could not read text inside the uploaded PDF"
- The PDF might be a scanned image without embedded text
- Try uploading a text-based PDF resume

### No extraction results
- The local fallback parser will still work for basic data
- Check that the PDF contains readable text
- Check browser console (F12) for detailed error messages

## Deployment (Production)

### Deploy to Heroku

```bash
heroku create your-app-name
heroku config:set OPENROUTER_API_KEY=your_key_here
heroku config:set GEMINI_API_KEY=your_key_here
git push heroku main
```

### Deploy to Vercel (Frontend Only)

```bash
npm i -g vercel
vercel
```

Then update frontend URL to your deployed backend.

## System Requirements

- **Minimum**: 100MB disk space, 512MB RAM
- **Recommended**: 1GB RAM, 500MB disk space
- **Python**: 3.8 or higher
- **Supported OS**: Windows, macOS, Linux

## Development

To contribute:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Test locally
5. Push and create a Pull Request

## License

MIT License - See LICENSE file for details

## Support

For issues, questions, or suggestions:
- Open an GitHub Issue
- Check existing issues first
- Include error messages and your OS/Python version

## Roadmap

- [ ] Support for .docx files
- [ ] CSV export of parsed data
- [ ] Batch upload multiple resumes
- [ ] Custom parsing rules
- [ ] Dark mode UI
- [ ] Resume validation scores

---

**Made with ❤️ for HR teams and developers**
