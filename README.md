# Resume Optimization Backend API

A powerful backend system for resume optimization using Google Gemini Flash API. This system analyzes resumes against job descriptions and provides ATS-friendly optimized versions.

## Features

- **Multi-format Resume Parsing**: Supports PDF, DOCX, and TXT files
- **AI-Powered Analysis**: Uses Google Gemini Flash API for intelligent resume analysis
- **Job Description Matching**: Compares resumes against job descriptions for optimization
- **ATS-Friendly Output**: Ensures optimized resumes are compatible with Applicant Tracking Systems
- **Modular Architecture**: Extensible design for easy frontend integration
- **Comprehensive Error Handling**: Robust error handling for various edge cases

## System Requirements

- Python 3.8+
- Google Gemini API key
- Required Python packages (see requirements.txt)

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd resume-optimization-backend
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env and add your Gemini API key
   ```

4. **Configure your API key**:
   ```bash
   # In .env file
   GEMINI_API_KEY=your_actual_gemini_api_key_here
   ```

## Usage

### Starting the Server

```bash
python main.py
```

The API will be available at `http://localhost:8000`

### API Endpoints

#### 1. Health Check
```http
GET /
GET /health
```

#### 2. Optimize Resume
```http
POST /optimize
Content-Type: multipart/form-data

Form Data:
- resume_file: Resume file (PDF, DOCX, or TXT)
- job_description: Job description text
```

**Response**:
```json
{
  "original_resume": "Original resume content...",
  "optimized_resume": "Optimized resume content...",
  "job_description": "Job description used...",
  "status": "success"
}
```

#### 3. Parse Resume Only
```http
POST /parse-resume
Content-Type: multipart/form-data

Form Data:
- resume_file: Resume file (PDF, DOCX, or TXT)
```

**Response**:
```json
{
  "resume_content": "Extracted resume content...",
  "file_name": "resume.pdf",
  "file_type": "pdf",
  "status": "success"
}
```

### Example Usage with cURL

```bash
# Optimize a resume
curl -X POST "http://localhost:8000/optimize" \
  -F "resume_file=@/path/to/resume.pdf" \
  -F "job_description=Software Engineer position requiring Python, React, and AWS experience..."

# Parse resume only
curl -X POST "http://localhost:8000/parse-resume" \
  -F "resume_file=@/path/to/resume.pdf"
```

## Architecture

### Core Components

1. **Resume Parser** (`src/resume_parser.py`)
   - Handles PDF, DOCX, and TXT file parsing
   - Extracts and cleans text content
   - Identifies resume sections

2. **Gemini Client** (`src/gemini_client.py`)
   - Interfaces with Google Gemini Flash API
   - Performs resume-JD analysis
   - Generates optimized content

3. **Resume Optimizer** (`src/resume_optimizer.py`)
   - Orchestrates the optimization pipeline
   - Applies ATS-friendly formatting
   - Validates output quality

4. **Models** (`src/models.py`)
   - Pydantic models for request/response validation
   - Type definitions for API contracts

5. **Configuration** (`src/config.py`)
   - Centralized configuration management
   - Environment variable handling

### Optimization Pipeline

1. **File Upload & Parsing**
   - Validate file format and size
   - Extract text content using appropriate parser
   - Clean and normalize text

2. **Analysis Phase**
   - Compare resume against job description
   - Identify missing keywords and skills
   - Calculate match percentages
   - Generate improvement suggestions

3. **Optimization Phase**
   - Incorporate missing keywords naturally
   - Highlight relevant experience
   - Improve action verbs and quantifiable achievements
   - Enhance overall content structure

4. **ATS Formatting**
   - Apply ATS-friendly formatting
   - Ensure proper section headers
   - Optimize for machine readability
   - Validate compatibility

5. **Final Validation**
   - Check ATS compatibility
   - Ensure proper length and structure
   - Apply final formatting touches

## Configuration

### Environment Variables

- `GEMINI_API_KEY`: Your Google Gemini API key (required)
- `PORT`: Server port (default: 8000)
- `HOST`: Server host (default: 0.0.0.0)

### File Upload Limits

- Maximum file size: 10MB
- Supported formats: PDF, DOCX, TXT
- Minimum resume length: 100 characters
- Maximum resume length: 10,000 characters

## Error Handling

The API provides comprehensive error handling for:

- Unsupported file formats
- File size limits
- API key issues
- Parsing errors
- Gemini API failures
- Invalid input data

## Development

### Project Structure

```
resume-optimization-backend/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── .env                   # Environment variables (create this)
├── README.md              # This file
└── src/
    ├── __init__.py
    ├── models.py          # Pydantic models
    ├── config.py          # Configuration management
    ├── resume_parser.py   # File parsing logic
    ├── gemini_client.py   # Gemini API client
    └── resume_optimizer.py # Main optimization logic
```

### Adding New Features

1. **New File Formats**: Extend `ResumeParser` class
2. **Additional Analysis**: Add methods to `GeminiClient`
3. **Custom Formatting**: Modify `ResumeOptimizer` formatting methods
4. **New Endpoints**: Add routes in `main.py`

## Testing

### Manual Testing

1. Start the server: `python main.py`
2. Use the provided cURL examples
3. Test with different file formats
4. Verify error handling with invalid inputs

### Test Files

Create test files in different formats:
- `test_resume.pdf`
- `test_resume.docx`
- `test_resume.txt`

## Production Deployment

### Docker (Optional)

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "main.py"]
```

### Environment Setup

1. Set production environment variables
2. Configure reverse proxy (nginx)
3. Set up SSL certificates
4. Configure logging and monitoring

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Troubleshooting

### Common Issues

1. **API Key Error**: Ensure `GEMINI_API_KEY` is set correctly
2. **File Upload Fails**: Check file size and format
3. **Parsing Errors**: Verify file is not corrupted
4. **Optimization Fails**: Check Gemini API quota and limits

### Logs

Check console output for detailed error messages and debugging information.

## License

This project is licensed under the MIT License.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review API documentation
3. Create an issue in the repository