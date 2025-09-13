from __future__ import annotations

import traceback
from typing import Optional

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse

from app.services.parsers import parse_resume, UnsupportedFileTypeError
from app.services.gemini_service import GeminiClient
from app.utils.docx_export import render_text_to_docx

MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10MB

app = FastAPI(title="Resume Optimizer Backend", version="0.1.0")

gemini_client: Optional[GeminiClient] = None


@app.on_event("startup")
async def startup_event() -> None:
	global gemini_client
	try:
		gemini_client = GeminiClient()
	except Exception as e:
		# Do not crash startup; allow health checks to work and return explicit error on use
		print("Failed to initialize GeminiClient:", e)


@app.post("/optimize")
async def optimize_resume_endpoint(
	file: UploadFile = File(..., description="Resume file: PDF, DOCX, or TXT"),
	job_description: str = Form(..., description="Job description text"),
	output_format: str = Form("text", description="Return 'text' (JSON) or 'docx'"),
):
	if not file or not file.filename:
		raise HTTPException(status_code=400, detail="No file uploaded")
	if not job_description or not job_description.strip():
		raise HTTPException(status_code=400, detail="Job description is required")

	try:
		file_bytes = await file.read()
		if len(file_bytes) > MAX_FILE_SIZE_BYTES:
			raise HTTPException(status_code=413, detail="File too large. Max 10MB.")
		resume_text, ext = parse_resume(file_bytes, file.filename)
		if not resume_text.strip():
			raise HTTPException(status_code=400, detail="Could not extract text from the resume. Please upload a text-based PDF/DOCX/TXT.")
		if gemini_client is None:
			raise HTTPException(status_code=500, detail="Gemini client not initialized. Ensure GOOGLE_API_KEY is set.")

		optimized_text = gemini_client.optimize_resume(resume_text=resume_text, job_description=job_description)

		fmt = (output_format or "text").lower()
		if fmt == "text":
			return JSONResponse({"optimized_resume": optimized_text})
		elif fmt == "docx":
			docx_bytes = render_text_to_docx(optimized_text)
			return StreamingResponse(
				iter([docx_bytes]),
				media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
				headers={
					"Content-Disposition": f"attachment; filename=optimized_resume.docx"
				},
			)
		else:
			raise HTTPException(status_code=400, detail="Invalid output_format. Use 'text' or 'docx'.")

	except UnsupportedFileTypeError as e:
		raise HTTPException(status_code=415, detail=str(e))
	except HTTPException:
		raise
	except Exception as e:
		print("Unhandled error in /optimize:", e)
		traceback.print_exc()
		raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/health")
async def health() -> dict:
	return {"status": "ok"}