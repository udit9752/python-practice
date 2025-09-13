from __future__ import annotations

import os
from typing import Optional, Dict, Any

import google.generativeai as genai
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from app.config import Settings


class GeminiClient:
	def __init__(self, settings: Optional[Settings] = None) -> None:
		self.settings = settings or Settings()
		api_key = self.settings.google_api_key or os.getenv("GOOGLE_API_KEY", "")
		if not api_key:
			raise ValueError("GOOGLE_API_KEY is not set. Provide it in environment or .env")

		genai.configure(api_key=api_key)
		self.model_name = self.settings.gemini_model
		self.generation_config = {
			"temperature": float(self.settings.generation_temperature),
			"max_output_tokens": int(self.settings.max_output_tokens),
			"response_mime_type": "text/plain",
		}
		self.model = genai.GenerativeModel(model_name=self.model_name, generation_config=self.generation_config)

	@retry(
		stop=stop_after_attempt(3),
		wait=wait_exponential(multiplier=1, min=1, max=8),
		retry=retry_if_exception_type(Exception),
	)
	def optimize_resume(self, resume_text: str, job_description: str) -> str:
		"""Optimize resume text against JD. Returns ATS-friendly plain text.
		The prompt enforces simple structure, keywords inclusion, and measurable impact statements.
		"""
		system_instructions = (
			"You are an expert resume optimization assistant focused on ATS compliance. "
			"Rewrite and reorganize the provided resume to align with the job description while preserving truthfulness. "
			"Use simple, machine-readable formatting: clear section headers (SUMMARY, EXPERIENCE, EDUCATION, SKILLS, PROJECTS), "
			"bullet points with hyphens, consistent spacing, no tables, no text boxes, no images. "
			"Include relevant keywords from the job description naturally. "
			"Use action verbs and quantify impact where possible. Maintain or improve clarity and consistency. "
			"Do not invent experience or credentials. If information is missing, omit it."
		)

		user_prompt = f"""
JOB DESCRIPTION:
{job_description}

RESUME:
{resume_text}

TASK:
- Produce an ATS-friendly optimized resume as plain text.
- Keep to standard sections (SUMMARY, EXPERIENCE, EDUCATION, SKILLS, PROJECTS, CERTIFICATIONS if applicable).
- Prefer concise bullet points that reflect outcomes and responsibilities aligned with the JD.
- Ensure correct spelling of technologies; include critical keywords when truthful.
- Keep contact info minimal and generic if not provided (e.g., Name, Email, City, State).
- Avoid tables, columns, headers/footers, images, or unusual characters.
- Use simple hyphen bullets like: "- Managed X resulting in Y".
"""

		response = self.model.generate_content([system_instructions, user_prompt])
		text = (response.text or "").strip()
		return text