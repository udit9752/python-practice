# Resume Optimizer Frontend

A modern, responsive web application for resume optimization powered by AI.

## Features

- **Drag & Drop Upload**: Easy file upload with visual feedback
- **Multi-format Support**: PDF, DOCX, and TXT files
- **Real-time Validation**: File type and size validation
- **Job Description Input**: Rich textarea for job requirements
- **AI Optimization**: Integration with backend API for resume enhancement
- **Side-by-side Comparison**: View original vs optimized resume
- **Download & Copy**: Export optimized resume in multiple ways
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Loading States**: Beautiful progress indicators
- **Toast Notifications**: User feedback for all actions

## Quick Start

### Option 1: Using Python Server (Recommended)
```bash
# Navigate to frontend directory
cd frontend

# Start the server
python3 server.py

# Or specify a custom port
python3 server.py 8080
```

### Option 2: Using Any Web Server
Simply serve the `index.html` file using any web server:
- Apache
- Nginx
- Live Server (VS Code extension)
- Any static file server

## Prerequisites

1. **Backend API Running**: Ensure the resume optimization backend is running on `http://localhost:8000`
2. **Modern Browser**: Chrome, Firefox, Safari, or Edge with JavaScript enabled
3. **Python 3.x**: For the simple server (optional)

## File Structure

```
frontend/
├── index.html          # Main HTML file
├── styles.css          # CSS styles and responsive design
├── script.js           # JavaScript functionality
├── server.py           # Simple Python HTTP server
└── README.md           # This file
```

## Usage

### 1. Upload Resume
- Drag and drop a resume file onto the upload area
- Or click to browse and select a file
- Supported formats: PDF, DOCX, TXT
- Maximum file size: 10MB

### 2. Enter Job Description
- Paste the job description you're applying for
- Minimum 10 characters required
- The more detailed, the better the optimization

### 3. Optimize Resume
- Click "Optimize Resume" button
- Watch the progress as AI analyzes and enhances your resume
- Process typically takes 10-30 seconds

### 4. Review Results
- View original resume
- View optimized resume
- Compare side-by-side
- Download or copy the optimized version

## API Integration

The frontend communicates with the backend API at `http://localhost:8000`:

- `GET /health` - Health check
- `POST /optimize` - Optimize resume
- `POST /parse-resume` - Parse resume only

## Customization

### Changing API URL
Edit the `apiBaseUrl` in `script.js`:
```javascript
this.apiBaseUrl = 'http://your-api-server:port';
```

### Styling
Modify `styles.css` to customize:
- Colors and themes
- Layout and spacing
- Typography
- Responsive breakpoints

### Functionality
Extend `script.js` to add:
- New file formats
- Additional export options
- Custom validation rules
- Enhanced UI features

## Browser Support

- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## Responsive Design

The application is fully responsive with breakpoints at:
- Desktop: 1200px+
- Tablet: 768px - 1199px
- Mobile: 320px - 767px

## Keyboard Shortcuts

- `Ctrl/Cmd + Enter`: Optimize resume (when in job description)
- `Escape`: Go back to previous step

## Error Handling

The application handles various error scenarios:
- Invalid file formats
- File size limits
- Network errors
- API failures
- Browser compatibility issues

## Performance

- Optimized for fast loading
- Lazy loading of heavy content
- Efficient DOM manipulation
- Minimal external dependencies

## Security

- Client-side validation
- File type verification
- Size limits enforced
- No sensitive data stored locally

## Development

### Local Development
1. Start the backend API
2. Start the frontend server
3. Open browser to `http://localhost:3000`
4. Make changes and refresh

### Testing
- Test with different file formats
- Test with various job descriptions
- Test responsive design on different devices
- Test error scenarios

## Troubleshooting

### Common Issues

1. **"Unable to connect to optimization service"**
   - Ensure backend API is running on port 8000
   - Check API URL in script.js

2. **File upload not working**
   - Check file format (PDF, DOCX, TXT only)
   - Check file size (max 10MB)
   - Try refreshing the page

3. **Optimization fails**
   - Check browser console for errors
   - Verify job description is provided
   - Check backend API logs

4. **Styling issues**
   - Clear browser cache
   - Check CSS file is loading
   - Verify responsive breakpoints

### Debug Mode
Open browser developer tools and check:
- Console for JavaScript errors
- Network tab for API calls
- Application tab for local storage

## License

This project is part of the Resume Optimizer system.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review browser console for errors
3. Verify backend API is running
4. Test with different browsers