from __future__ import annotations

import io
from typing import Tuple

from pdfminer.high_level import extract_text as pdf_extract_text
from docx import Document

SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".txt"}


class UnsupportedFileTypeError(ValueError):
	pass


def detect_extension(filename: str) -> str:
	lower = filename.lower()
	for ext in SUPPORTED_EXTENSIONS:
		if lower.endswith(ext):
			return ext
	raise UnsupportedFileTypeError(f"Unsupported file type for '{filename}'. Supported: {', '.join(sorted(SUPPORTED_EXTENSIONS))}")


def parse_resume(file_bytes: bytes, filename: str) -> Tuple[str, str]:
	"""Return (plain_text, detected_extension). Raises on unsupported types.
	Ensures text is normalized to Unix newlines and stripped of control chars.
	"""
	ext = detect_extension(filename)
	if ext == ".pdf":
		text = _parse_pdf(file_bytes)
	elif ext == ".docx":
		text = _parse_docx(file_bytes)
	elif ext == ".txt":
		text = _parse_txt(file_bytes)
	else:
		raise UnsupportedFileTypeError(f"Unsupported file type: {ext}")

	return (_normalize_text(text), ext)


def _parse_pdf(file_bytes: bytes) -> str:
	with io.BytesIO(file_bytes) as buffer:
		text = pdf_extract_text(buffer)
	return text or ""


def _parse_docx(file_bytes: bytes) -> str:
	with io.BytesIO(file_bytes) as buffer:
		doc = Document(buffer)
		parts = []
		for paragraph in doc.paragraphs:
			parts.append(paragraph.text)
		return "\n".join(parts)


def _parse_txt(file_bytes: bytes) -> str:
	try:
		return file_bytes.decode("utf-8")
	except UnicodeDecodeError:
		# Fallback to latin-1 to avoid hard failures on odd encodings
		return file_bytes.decode("latin-1", errors="ignore")


def _normalize_text(text: str) -> str:
	# Replace Windows and Mac newlines with Unix newlines, strip nulls
	return (
		text.replace("\r\n", "\n").replace("\r", "\n").replace("\x00", "")
	)