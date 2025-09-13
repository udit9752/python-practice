from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
	google_api_key: str = Field(default="", validation_alias="GOOGLE_API_KEY")
	gemini_model: str = Field(default="gemini-1.5-flash", validation_alias="GEMINI_MODEL")
	generation_temperature: float = Field(default=0.3, validation_alias="GENERATION_TEMPERATURE")
	max_output_tokens: int = Field(default=8192, validation_alias="MAX_OUTPUT_TOKENS")

	class Config:
		env_file = ".env"
		env_file_encoding = "utf-8"