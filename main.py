import os
import re
import pypdf
import google.generativeai as genai
from dotenv import load_dotenv
from openai import OpenAI
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

load_dotenv(dotenv_path="main.env")
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SYSTEM_PROMPT = "You are an expert HR assistant. Extract candidate name, email, skills, and work history from this text into clean JSON format."

# Load API keys from main.env and use them in the parser.
OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
GROQ_KEY = os.getenv("GROQ_API_KEY")
DEEPSEEK_KEY = os.getenv("DEEPSEEK_API_KEY")
NVIDIA_KEY = os.getenv("NVIDIA_API_KEY")

def extract_text_from_pdf(file) -> str:
    reader = pypdf.PdfReader(file)
    extracted_text = ""
    for page in reader.pages:
        extracted_text += page.extract_text() or ""
    return extracted_text

def get_chat_response_text(response) -> str:
    if not response or not getattr(response, "choices", None):
        return ""
    first_choice = response.choices[0]
    message = getattr(first_choice, "message", None)
    if message is None and isinstance(first_choice, dict):
        message = first_choice.get("message")
    if isinstance(message, dict):
        return message.get("content", "") or ""
    return getattr(message, "content", "") or ""


def find_email(text: str) -> str:
    match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    return match.group(0) if match else ""


def find_phone(text: str) -> str:
    match = re.search(r"(?:\+\d{1,3}[ \-])?(?:\(?\d{2,4}\)?[ \-]?)?\d{3,4}[ \-]?\d{3,4}", text)
    return match.group(0) if match else ""


def find_name(lines: list[str], text: str) -> str:
    for line in lines[:5]:
        if re.search(r"\bName\b[:\-]", line, re.IGNORECASE):
            return re.sub(r".*\bName\b[:\-]?\s*", "", line, flags=re.IGNORECASE).strip()
    if lines:
        first = lines[0].strip()
        if re.match(r"^[A-Z][a-z]+(?:[\s\-][A-Z][a-z]+){1,3}$", first):
            return first
    if match := re.search(r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})\b", text):
        return match.group(1)
    return ""


def extract_section(lines: list[str], start_patterns: list[str], stop_patterns: list[str] | None = None) -> list[str]:
    start_index = -1
    for i, line in enumerate(lines):
        for pattern in start_patterns:
            if re.search(pattern, line, re.IGNORECASE):
                start_index = i + 1
                break
        if start_index != -1:
            break
    if start_index == -1:
        return []
    stop_index = len(lines)
    if stop_patterns:
        for i in range(start_index, len(lines)):
            for pattern in stop_patterns:
                if re.search(pattern, lines[i], re.IGNORECASE):
                    stop_index = i
                    break
            if stop_index != len(lines):
                break
    return [line for line in lines[start_index:stop_index] if line]


def find_skills(lines: list[str], text: str) -> list[str]:
    skill_lines = []
    for line in lines:
        if re.search(r"\bskills?\b", line, re.IGNORECASE):
            skill_lines.append(line)
    if not skill_lines:
        section = extract_section(lines, [r"\bskills?\b"], [r"\bexperience\b", r"\beducation\b", r"\bprojects?\b"])
        skill_lines.extend(section)
    skills = []
    for line in skill_lines:
        pieces = re.split(r"[,;\|]\s*", line)
        for piece in pieces:
            cleaned = re.sub(r"^.*\bskills?\b[:\-]?\s*", "", piece, flags=re.IGNORECASE).strip()
            if cleaned and len(cleaned) > 1:
                skills.append(cleaned)
    return sorted(set(skills), key=skills.index)


def find_work_history(lines: list[str]) -> list[str]:
    section = extract_section(lines, [r"\b(work experience|experience|employment history|professional history)\b"], [r"\beducation\b", r"\bskills?\b", r"\bprojects?\b", r"\bcertifications?\b"])
    return section[:12]


def parse_text_locally(text: str) -> dict:
    lines = [line.strip() for line in re.split(r"\r?\n", text) if line.strip()]
    return {
        "name": find_name(lines, text),
        "email": find_email(text),
        "phone": find_phone(text),
        "skills": find_skills(lines, text),
        "work_history": find_work_history(lines),
        "source": "local_fallback"
    }


def try_openrouter_free_model(text: str) -> str:
    if not OPENROUTER_KEY:
        raise ValueError("OpenRouter API key is not configured.")

    client = OpenAI(base_url="https://openrouter.ai", api_key=OPENROUTER_KEY)
    response = client.chat.completions.create(
        model="google/gemini-2.5-flash:free",
        messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": text}],
        timeout=12.0
    )

    parsed_text = get_chat_response_text(response)
    if not parsed_text:
        raise ValueError("OpenRouter response did not return parser text.")
    return parsed_text


def try_gemini(text: str) -> str:
    if not GEMINI_KEY or GEMINI_KEY.startswith("your_"):
        raise ValueError("Invalid Gemini Key")
    genai.configure(api_key=GEMINI_KEY)
    model = genai.GenerativeModel(model_name="gemini-1.5-flash", system_instruction=SYSTEM_PROMPT)
    response = model.generate_content(text)
    return response.text

def try_groq(text: str) -> str:
    if not GROQ_KEY:
        raise ValueError("Groq API key is not configured.")

    client = OpenAI(base_url="https://groq.com", api_key=GROQ_KEY)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": text}],
        timeout=8.0
    )

    parsed_text = get_chat_response_text(response)
    if not parsed_text:
        raise ValueError("Groq response did not return parser text.")
    return parsed_text

@app.post("/parse-resume")
async def parse_resume_endpoint(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only standard PDF files are supported.")
        
    resume_text = extract_text_from_pdf(file.file)
    if not resume_text.strip():
        raise HTTPException(status_code=400, detail="Could not read text inside the uploaded PDF.")

    # Prioritizing OpenRouter Free Model to ensure the project runs without credit barriers
    providers = [
        ("OpenRouter Free Model", try_openrouter_free_model),
        ("Google Gemini", try_gemini),
        ("Groq Llama", try_groq)
    ]

    provider_errors = []
    for name, provider_function in providers:
        try:
            print(f"[TRYING] Sending file payload to {name}...")
            result_data = provider_function(resume_text)
            print(f"[SUCCESS] {name} processed the file successfully!")
            return {"success": True, "provider_used": name, "data": result_data}
        except Exception as error:
            error_message = str(error) or repr(error)
            provider_errors.append({"provider": name, "error": error_message})
            print(f"[FAILED] {name} encountered an error: {error_message}. Shifting fallback target...")
            continue

    fallback_data = parse_text_locally(resume_text)
    if fallback_data["email"] or fallback_data["skills"] or fallback_data["work_history"]:
        return {
            "success": True,
            "provider_used": "Local parser fallback",
            "data": fallback_data,
            "fallback_details": provider_errors
        }

    raise HTTPException(
        status_code=503,
        detail={
            "message": "All AI providers failed and the local fallback could not extract useful resume data.",
            "provider_errors": provider_errors
        }
    )

@app.get("/")
async def root():
    return {"status": "ok", "message": "Resume parser backend is running."}
