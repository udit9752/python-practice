// Resume Optimizer Frontend JavaScript

class ResumeOptimizer {
    constructor() {
        this.apiBase = 'http://localhost:8000';
        this.currentFile = null;
        this.isProcessing = false;
        
        this.initializeElements();
        this.bindEvents();
        this.checkApiHealth();
    }

    initializeElements() {
        // File upload elements
        this.uploadArea = document.getElementById('uploadArea');
        this.fileInput = document.getElementById('fileInput');
        this.browseBtn = document.getElementById('browseBtn');
        this.fileInfo = document.getElementById('fileInfo');
        this.fileName = document.getElementById('fileName');
        this.fileSize = document.getElementById('fileSize');
        this.removeFile = document.getElementById('removeFile');

        // Job description elements
        this.jobDescription = document.getElementById('jobDescription');
        this.charCount = document.getElementById('charCount');

        // Options
        this.includeAnalysis = document.getElementById('includeAnalysis');

        // Action buttons
        this.optimizeBtn = document.getElementById('optimizeBtn');
        this.analyzeBtn = document.getElementById('analyzeBtn');

        // Loading elements
        this.loadingSection = document.getElementById('loadingSection');
        this.loadingTitle = document.getElementById('loadingTitle');
        this.loadingMessage = document.getElementById('loadingMessage');
        this.loadingSteps = ['step1', 'step2', 'step3', 'step4'].map(id => 
            document.getElementById(id)
        );

        // Results elements
        this.resultsSection = document.getElementById('resultsSection');
        this.analysisResults = document.getElementById('analysisResults');
        this.analysisContent = document.getElementById('analysisContent');
        this.optimizedResults = document.getElementById('optimizedResults');
        this.resumePreview = document.getElementById('resumePreview');
        this.processingInfo = document.getElementById('processingInfo');
        this.processingSteps = document.getElementById('processingSteps');

        // Result actions
        this.copyBtn = document.getElementById('copyBtn');
        this.downloadBtn = document.getElementById('downloadBtn');
        this.toggleAnalysis = document.getElementById('toggleAnalysis');
        this.newOptimization = document.getElementById('newOptimization');

        // Status and modal
        this.statusBanner = document.getElementById('statusBanner');
        this.statusMessage = document.getElementById('statusMessage');
        this.closeStatus = document.getElementById('closeStatus');
        this.modal = document.getElementById('modal');
        this.modalTitle = document.getElementById('modalTitle');
        this.modalBody = document.getElementById('modalBody');
        this.modalClose = document.getElementById('modalClose');
    }

    bindEvents() {
        // File upload events
        this.uploadArea.addEventListener('click', () => this.fileInput.click());
        this.browseBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            this.fileInput.click();
        });
        this.fileInput.addEventListener('change', (e) => this.handleFileSelect(e));
        this.removeFile.addEventListener('click', () => this.clearFile());

        // Drag and drop events
        this.uploadArea.addEventListener('dragover', (e) => this.handleDragOver(e));
        this.uploadArea.addEventListener('dragleave', (e) => this.handleDragLeave(e));
        this.uploadArea.addEventListener('drop', (e) => this.handleDrop(e));

        // Job description events
        this.jobDescription.addEventListener('input', () => this.updateCharCount());
        this.jobDescription.addEventListener('input', () => this.validateForm());

        // Action button events
        this.optimizeBtn.addEventListener('click', () => this.optimizeResume());
        this.analyzeBtn.addEventListener('click', () => this.analyzeResume());

        // Result action events
        this.copyBtn.addEventListener('click', () => this.copyToClipboard());
        this.downloadBtn.addEventListener('click', () => this.downloadResume());
        this.toggleAnalysis.addEventListener('click', () => this.toggleAnalysisView());
        this.newOptimization.addEventListener('click', () => this.resetForm());

        // Modal events
        this.closeStatus.addEventListener('click', () => this.hideStatus());
        this.modalClose.addEventListener('click', () => this.hideModal());
        this.modal.addEventListener('click', (e) => {
            if (e.target === this.modal) this.hideModal();
        });

        // Keyboard events
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.hideModal();
                this.hideStatus();
            }
        });

        // Form validation on input changes
        this.fileInput.addEventListener('change', () => this.validateForm());
    }

    // API Health Check
    async checkApiHealth() {
        try {
            const response = await fetch(`${this.apiBase}/health`);
            const data = await response.json();
            
            if (data.status === 'healthy') {
                this.showStatus('API is ready and operational', 'success');
            } else {
                throw new Error('API is not healthy');
            }
        } catch (error) {
            this.showStatus('Cannot connect to the backend API. Please ensure the server is running.', 'error');
            console.error('API Health Check failed:', error);
        }
    }

    // File Handling
    handleFileSelect(event) {
        const file = event.target.files[0];
        if (file) {
            this.setFile(file);
        }
    }

    handleDragOver(event) {
        event.preventDefault();
        this.uploadArea.classList.add('dragover');
    }

    handleDragLeave(event) {
        event.preventDefault();
        this.uploadArea.classList.remove('dragover');
    }

    handleDrop(event) {
        event.preventDefault();
        this.uploadArea.classList.remove('dragover');
        
        const files = event.dataTransfer.files;
        if (files.length > 0) {
            this.setFile(files[0]);
        }
    }

    setFile(file) {
        // Validate file type
        const allowedTypes = ['.pdf', '.docx', '.txt'];
        const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
        
        if (!allowedTypes.includes(fileExtension)) {
            this.showStatus('Please select a PDF, DOCX, or TXT file.', 'error');
            return;
        }

        // Validate file size (10MB limit)
        const maxSize = 10 * 1024 * 1024; // 10MB
        if (file.size > maxSize) {
            this.showStatus('File size must be less than 10MB.', 'error');
            return;
        }

        this.currentFile = file;
        this.fileName.textContent = file.name;
        this.fileSize.textContent = this.formatFileSize(file.size);
        
        this.uploadArea.style.display = 'none';
        this.fileInfo.style.display = 'block';
        
        this.validateForm();
        this.hideStatus();
    }

    clearFile() {
        this.currentFile = null;
        this.fileInput.value = '';
        this.uploadArea.style.display = 'block';
        this.fileInfo.style.display = 'none';
        this.validateForm();
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    // Form Validation
    updateCharCount() {
        const count = this.jobDescription.value.length;
        this.charCount.textContent = count.toLocaleString();
        
        if (count < 50) {
            this.charCount.style.color = 'var(--error-color)';
        } else {
            this.charCount.style.color = 'var(--text-secondary)';
        }
    }

    validateForm() {
        const hasFile = this.currentFile !== null;
        const hasJobDescription = this.jobDescription.value.trim().length >= 50;
        const isValid = hasFile && hasJobDescription && !this.isProcessing;
        
        this.optimizeBtn.disabled = !isValid;
        this.analyzeBtn.disabled = !isValid;
    }

    // API Calls
    async optimizeResume() {
        if (this.isProcessing) return;
        
        this.isProcessing = true;
        this.showLoading('Optimizing Your Resume', 'Please wait while we optimize your resume...');
        this.hideResults();
        
        try {
            const formData = new FormData();
            formData.append('resume_file', this.currentFile);
            formData.append('job_description', this.jobDescription.value.trim());
            formData.append('include_analysis', this.includeAnalysis.checked);
            
            this.simulateLoadingSteps();
            
            const response = await fetch(`${this.apiBase}/optimize`, {
                method: 'POST',
                body: formData
            });
            
            const result = await response.json();
            
            if (result.success) {
                this.showResults(result, 'optimization');
                this.showStatus('Resume optimization completed successfully!', 'success');
            } else {
                throw new Error(result.error || 'Optimization failed');
            }
        } catch (error) {
            console.error('Optimization error:', error);
            this.showStatus(`Optimization failed: ${error.message}`, 'error');
        } finally {
            this.isProcessing = false;
            this.hideLoading();
            this.validateForm();
        }
    }

    async analyzeResume() {
        if (this.isProcessing) return;
        
        this.isProcessing = true;
        this.showLoading('Analyzing Your Resume', 'Please wait while we analyze your resume...');
        this.hideResults();
        
        try {
            const formData = new FormData();
            formData.append('resume_file', this.currentFile);
            formData.append('job_description', this.jobDescription.value.trim());
            
            this.simulateLoadingSteps();
            
            const response = await fetch(`${this.apiBase}/analyze`, {
                method: 'POST',
                body: formData
            });
            
            const result = await response.json();
            
            if (result.success) {
                this.showResults(result, 'analysis');
                this.showStatus('Resume analysis completed successfully!', 'success');
            } else {
                throw new Error(result.error || 'Analysis failed');
            }
        } catch (error) {
            console.error('Analysis error:', error);
            this.showStatus(`Analysis failed: ${error.message}`, 'error');
        } finally {
            this.isProcessing = false;
            this.hideLoading();
            this.validateForm();
        }
    }

    // Loading States
    showLoading(title, message) {
        this.loadingTitle.textContent = title;
        this.loadingMessage.textContent = message;
        this.loadingSection.style.display = 'block';
        this.resetLoadingSteps();
        
        // Scroll to loading section
        this.loadingSection.scrollIntoView({ behavior: 'smooth' });
    }

    hideLoading() {
        this.loadingSection.style.display = 'none';
    }

    resetLoadingSteps() {
        this.loadingSteps.forEach(step => {
            step.classList.remove('active', 'completed');
        });
    }

    simulateLoadingSteps() {
        const steps = this.loadingSteps;
        let currentStep = 0;
        
        const activateStep = (index) => {
            if (index < steps.length) {
                steps[index].classList.add('active');
                
                setTimeout(() => {
                    steps[index].classList.remove('active');
                    steps[index].classList.add('completed');
                    activateStep(index + 1);
                }, 1000 + Math.random() * 1000);
            }
        };
        
        activateStep(0);
    }

    // Results Display
    showResults(result, type) {
        this.resultsSection.style.display = 'block';
        
        // Show processing info
        this.processingSteps.innerHTML = '';
        if (result.processing_steps) {
            result.processing_steps.forEach(step => {
                const li = document.createElement('li');
                li.textContent = step;
                this.processingSteps.appendChild(li);
            });
        }
        
        // Show analysis if available
        if (result.analysis) {
            this.analysisContent.innerHTML = this.formatAnalysis(result.analysis);
            this.analysisResults.style.display = 'block';
        } else {
            this.analysisResults.style.display = 'none';
        }
        
        // Show optimized resume if available
        if (result.optimized_resume) {
            this.resumePreview.textContent = result.optimized_resume;
            this.optimizedResults.style.display = 'block';
            this.currentOptimizedResume = result.optimized_resume;
        } else {
            this.optimizedResults.style.display = 'none';
        }
        
        // Scroll to results
        this.resultsSection.scrollIntoView({ behavior: 'smooth' });
    }

    hideResults() {
        this.resultsSection.style.display = 'none';
    }

    formatAnalysis(analysis) {
        // Convert markdown-like formatting to HTML
        return analysis
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/\n\n/g, '</p><p>')
            .replace(/\n/g, '<br>')
            .replace(/^/, '<p>')
            .replace(/$/, '</p>');
    }

    // Result Actions
    async copyToClipboard() {
        if (!this.currentOptimizedResume) return;
        
        try {
            await navigator.clipboard.writeText(this.currentOptimizedResume);
            this.showStatus('Resume copied to clipboard!', 'success');
        } catch (error) {
            console.error('Copy failed:', error);
            this.showStatus('Failed to copy to clipboard. Please select and copy manually.', 'error');
        }
    }

    downloadResume() {
        if (!this.currentOptimizedResume) return;
        
        const blob = new Blob([this.currentOptimizedResume], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'optimized_resume.txt';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        
        this.showStatus('Resume downloaded successfully!', 'success');
    }

    toggleAnalysisView() {
        const content = this.analysisContent;
        const toggle = this.toggleAnalysis;
        
        if (content.style.display === 'none') {
            content.style.display = 'block';
            toggle.innerHTML = '<i class="fas fa-chevron-up"></i>';
        } else {
            content.style.display = 'none';
            toggle.innerHTML = '<i class="fas fa-chevron-down"></i>';
        }
    }

    resetForm() {
        this.clearFile();
        this.jobDescription.value = '';
        this.updateCharCount();
        this.hideResults();
        this.hideStatus();
        
        // Scroll to top
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    // UI Helpers
    showStatus(message, type = 'info') {
        this.statusMessage.textContent = message;
        this.statusBanner.className = `status-banner ${type}`;
        this.statusBanner.style.display = 'flex';
        
        // Auto-hide success messages after 5 seconds
        if (type === 'success') {
            setTimeout(() => this.hideStatus(), 5000);
        }
    }

    hideStatus() {
        this.statusBanner.style.display = 'none';
    }

    showModal(title, content) {
        this.modalTitle.textContent = title;
        this.modalBody.innerHTML = content;
        this.modal.style.display = 'flex';
    }

    hideModal() {
        this.modal.style.display = 'none';
    }
}

// Modal Content Functions
function showAbout() {
    const content = `
        <h4>About Resume Optimizer</h4>
        <p>Resume Optimizer is an AI-powered tool that helps you create ATS-friendly resumes optimized for specific job descriptions.</p>
        
        <h4>Features:</h4>
        <ul>
            <li>Multi-format support (PDF, DOCX, TXT)</li>
            <li>AI-powered content optimization</li>
            <li>ATS compatibility enhancement</li>
            <li>Job description alignment</li>
            <li>Detailed analysis and recommendations</li>
        </ul>
        
        <h4>How it works:</h4>
        <ol>
            <li>Upload your resume in any supported format</li>
            <li>Paste the job description you're targeting</li>
            <li>Choose optimization or analysis only</li>
            <li>Get your optimized, ATS-friendly resume</li>
        </ol>
    `;
    
    window.resumeOptimizer.showModal('About Resume Optimizer', content);
}

function showPrivacy() {
    const content = `
        <h4>Privacy Policy</h4>
        <p>Your privacy is important to us. Here's how we handle your data:</p>
        
        <h4>Data Processing:</h4>
        <ul>
            <li>Resume files are processed temporarily and not stored permanently</li>
            <li>Job descriptions are used only for optimization purposes</li>
            <li>All processing is done securely on our servers</li>
            <li>No personal information is shared with third parties</li>
        </ul>
        
        <h4>Data Security:</h4>
        <ul>
            <li>All uploads are encrypted in transit</li>
            <li>Temporary files are automatically deleted after processing</li>
            <li>No resume content is logged or stored</li>
        </ul>
        
        <h4>AI Processing:</h4>
        <p>Your resume content is processed using Google's Gemini AI service to provide optimization recommendations. The AI analysis is used solely for improving your resume and is not retained.</p>
    `;
    
    window.resumeOptimizer.showModal('Privacy Policy', content);
}

function showHelp() {
    const content = `
        <h4>Help & Support</h4>
        
        <h4>Supported File Formats:</h4>
        <ul>
            <li><strong>PDF:</strong> Most common resume format</li>
            <li><strong>DOCX:</strong> Microsoft Word documents</li>
            <li><strong>TXT:</strong> Plain text files</li>
        </ul>
        
        <h4>Tips for Best Results:</h4>
        <ul>
            <li>Ensure your resume contains clear text (not just images)</li>
            <li>Provide a complete job description with requirements</li>
            <li>Include skills, responsibilities, and qualifications in the job description</li>
            <li>Review the analysis to understand optimization suggestions</li>
        </ul>
        
        <h4>Troubleshooting:</h4>
        <ul>
            <li><strong>File won't upload:</strong> Check file format and size (max 10MB)</li>
            <li><strong>Processing failed:</strong> Ensure job description is at least 50 characters</li>
            <li><strong>Poor results:</strong> Try providing a more detailed job description</li>
        </ul>
        
        <h4>Need More Help?</h4>
        <p>If you're experiencing issues, please ensure the backend server is running and accessible.</p>
    `;
    
    window.resumeOptimizer.showModal('Help & Support', content);
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.resumeOptimizer = new ResumeOptimizer();
});