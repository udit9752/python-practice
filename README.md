# Resume Optimization Backend System

A comprehensive backend system for optimizing resumes using AI and ATS best practices. This system uses Google's Gemini Flash API to analyze and optimize resumes for better job alignment and ATS compatibility.

## Features

- **Multi-format Support**: Parse resumes from PDF, DOCX, and TXT files
- **AI-Powered Optimization**: Uses Google Gemini Flash API for intelligent resume optimization
- **ATS Compatibility**: Ensures resumes are optimized for Applicant Tracking Systems
- **Job Alignment**: Analyzes and optimizes resumes against specific job descriptions
- **Keyword Optimization**: Naturally integrates relevant keywords from job descriptions
- **Format Standardization**: Applies consistent, ATS-friendly formatting
- **Comprehensive Analysis**: Optional detailed analysis of resume-job fit

## System Architecture

```
Resume File (PDF/DOCX/TXT) + Job Description
    ↓
File Parser (extract text content)
    ↓
Content Validation
    ↓
Gemini AI Analysis & Optimization
    ↓
ATS Formatting Enhancement
    ↓
Optimized Resume Output
```

## Installation

1. **Clone or download the project files**

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env and add your Gemini API key
   echo "GEMINI_API_KEY=your_actual_api_key_here" > .env
   ```

4. **Run the application**:
   ```bash
   python main.py
   ```

The API will be available at `http://localhost:8000`

## API Documentation

### Endpoints

#### `GET /`
Root endpoint providing API information.

**Response:**
```json
{
  "status": "healthy",
  "message": "Resume Optimization Backend API is running",
  "version": "1.0.0"
}
```

#### `GET /health`
Health check endpoint to verify system status.

#### `GET /info`
Get information about processing capabilities.

**Response:**
```json
{
  "supported_formats": ["pdf", "docx", "txt"],
  "max_file_size_mb": 10.0,
  "features": [...],
  "processing_steps": [...]
}
```

#### `POST /optimize`
Main endpoint for complete resume optimization.

**Parameters:**
- `resume_file` (file): Resume file (PDF, DOCX, or TXT)
- `job_description` (string): Target job description
- `include_analysis` (boolean, optional): Include detailed analysis in response

**Response:**
```json
{
  "success": true,
  "optimized_resume": "...optimized resume content...",
  "analysis": "...detailed analysis (if requested)...",
  "original_format": "pdf",
  "processing_steps": [
    "File parsing completed",
    "Content validation passed",
    "AI optimization completed",
    "ATS formatting applied"
  ]
}
```

#### `POST /analyze`
Endpoint for resume analysis only (without optimization).

**Parameters:**
- `resume_file` (file): Resume file (PDF, DOCX, or TXT)
- `job_description` (string): Target job description

**Response:**
```json
{
  "success": true,
  "analysis": "...detailed analysis...",
  "original_format": "pdf",
  "processing_steps": [...]
}
```

### Error Handling

The API provides comprehensive error handling with detailed error messages:

```json
{
  "success": false,
  "error": "Detailed error message",
  "step": "validation|parsing|analysis|optimization"
}
```

## Usage Examples

### Using cURL

**Optimize a resume:**
```bash
curl -X POST "http://localhost:8000/optimize" \
  -F "resume_file=@resume.pdf" \
  -F "job_description=Software Engineer position requiring Python, JavaScript, and React experience..." \
  -F "include_analysis=true"
```

**Analyze a resume:**
```bash
curl -X POST "http://localhost:8000/analyze" \
  -F "resume_file=@resume.pdf" \
  -F "job_description=Software Engineer position requiring Python, JavaScript, and React experience..."
```

### Using Python

```python
import requests

# Optimize resume
with open('resume.pdf', 'rb') as file:
    response = requests.post(
        'http://localhost:8000/optimize',
        files={'resume_file': file},
        data={
            'job_description': 'Software Engineer position...',
            'include_analysis': True
        }
    )
    
result = response.json()
if result['success']:
    print("Optimized Resume:")
    print(result['optimized_resume'])
```

## Configuration

### Environment Variables

- `GEMINI_API_KEY`: Your Google Gemini API key (required)

### Configuration Options

Edit `config.py` to modify:

- `MAX_FILE_SIZE`: Maximum file size (default: 10MB)
- `SUPPORTED_FORMATS`: Supported file formats
- `GEMINI_MODEL`: Gemini model to use
- `GENERATION_CONFIG`: AI generation parameters

## File Structure

```
├── main.py                 # FastAPI application and API endpoints
├── resume_processor.py     # Core processing pipeline
├── file_parser.py         # Multi-format file parsing
├── gemini_client.py       # Google Gemini API integration
├── ats_optimizer.py       # ATS formatting and optimization
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
└── README.md             # This file
```

## Processing Pipeline

1. **File Validation**: Check file format, size, and content
2. **Content Extraction**: Parse text from PDF, DOCX, or TXT files
3. **Content Validation**: Ensure extracted content appears to be a resume
4. **AI Analysis** (optional): Detailed analysis of resume vs job description
5. **AI Optimization**: Optimize content using Gemini Flash API
6. **ATS Enhancement**: Apply ATS-friendly formatting and structure
7. **Output Generation**: Return optimized resume with processing details

## ATS Optimization Features

- **Standard Section Headers**: Uses ATS-friendly section names
- **Clean Formatting**: Removes problematic characters and formatting
- **Consistent Date Formats**: Standardizes date presentation
- **Keyword Integration**: Natural incorporation of job-relevant keywords
- **Bullet Point Optimization**: Clean, scannable bullet points
- **Proper Spacing**: Optimal line spacing and structure

## Error Handling

The system includes comprehensive error handling for:

- Unsupported file formats
- File size limits
- Content validation failures
- API communication errors
- Processing pipeline failures
- Invalid input parameters

## Logging

The system includes detailed logging for:
- Request processing
- File parsing operations
- API interactions
- Error conditions
- Performance metrics

## Security Considerations

- File size limits to prevent abuse
- Input validation and sanitization
- Error message sanitization
- CORS configuration for frontend integration

## Future Enhancements

This backend is designed to be modular and extensible:

- Add support for additional file formats
- Implement user authentication
- Add resume templates
- Include industry-specific optimizations
- Add batch processing capabilities
- Implement caching for improved performance

## Troubleshooting

### Common Issues

1. **"GEMINI_API_KEY environment variable is required"**
   - Ensure you have set up the `.env` file with your API key

2. **"Unsupported file format"**
   - Check that your file is in PDF, DOCX, or TXT format

3. **"File size exceeds maximum allowed size"**
   - Ensure your file is under 10MB

4. **"No text could be extracted"**
   - Check that your PDF/DOCX file contains extractable text (not just images)

### Getting Help

For issues or questions:
1. Check the logs for detailed error messages
2. Verify your API key is valid and has sufficient quota
3. Test with the provided sample files
4. Check file format and content requirements

## License

This project is provided as-is for educational and development purposes.