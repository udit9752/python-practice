# Resume Optimizer Backend (FastAPI)

Backend-only service to parse a resume (PDF/DOCX/TXT), analyze it against a Job Description (JD) using Google's Gemini 1.5 Flash, and return an ATS-friendly optimized resume text or DOCX.

## Features
- PDF/DOCX/TXT parsing
- Gemini Flash optimization (ATS-friendly)
- Returns optimized text (JSON) or DOCX file
- Modular, extendable architecture

## Quickstart

1. Create environment
```bash
cd /workspace
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Configure environment variables
```bash
cp .env.example .env
# Edit .env and set GOOGLE_API_KEY
```

3. Run the server
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

4. Test the API
- Optimize and return JSON text
```bash
curl -X POST "http://localhost:8000/optimize" \
  -F "file=@/path/to/resume.pdf" \
  -F "job_description=$(cat /path/to/JD.txt)" \
  -F "output_format=text"
```

- Optimize and return DOCX file
```bash
curl -X POST "http://localhost:8000/optimize" \
  -F "file=@/path/to/resume.docx" \
  -F "job_description=$(cat /path/to/JD.txt)" \
  -F "output_format=docx" \
  -o optimized_resume.docx
```

## Notes
- Supported file types: PDF, DOCX, TXT.
- The service avoids fabricating content; it restructures, prioritizes, and highlights relevant experience and skills to match the JD.
- Output is designed to be ATS-friendly: clear sections, simple formatting, keyword alignment, and machine-readable text.

## Project Structure
```
app/
  main.py
  config.py
  services/
    parsers.py
    gemini_service.py
  utils/
    docx_export.py
```
