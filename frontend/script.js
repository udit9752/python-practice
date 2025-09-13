// Resume Optimizer Frontend JavaScript

class ResumeOptimizer {
    constructor() {
        this.apiBaseUrl = 'http://localhost:8000';
        this.currentFile = null;
        this.originalResume = '';
        this.optimizedResume = '';
        this.jobDescription = '';
        
        this.initializeElements();
        this.attachEventListeners();
    }

    initializeElements() {
        // Upload section elements
        this.uploadArea = document.getElementById('uploadArea');
        this.fileInput = document.getElementById('fileInput');
        this.fileInfo = document.getElementById('fileInfo');
        this.fileName = document.querySelector('.file-name');
        this.removeFileBtn = document.getElementById('removeFile');
        
        // Job description elements
        this.jobDescription = document.getElementById('jobDescription');
        this.charCount = document.getElementById('charCount');
        this.backToUploadBtn = document.getElementById('backToUpload');
        this.optimizeResumeBtn = document.getElementById('optimizeResume');
        
        // Section elements
        this.uploadSection = document.getElementById('uploadSection');
        this.jobDescriptionSection = document.getElementById('jobDescriptionSection');
        this.loadingSection = document.getElementById('loadingSection');
        this.resultsSection = document.getElementById('resultsSection');
        
        // Results elements
        this.originalResumeEl = document.getElementById('originalResume');
        this.optimizedResumeEl = document.getElementById('optimizedResume');
        this.originalResumeComparison = document.getElementById('originalResumeComparison');
        this.optimizedResumeComparison = document.getElementById('optimizedResumeComparison');
        
        // Action buttons
        this.downloadOptimizedBtn = document.getElementById('downloadOptimized');
        this.copyOptimizedBtn = document.getElementById('copyOptimized');
        this.optimizeAnotherBtn = document.getElementById('optimizeAnother');
        
        // Tab elements
        this.tabBtns = document.querySelectorAll('.tab-btn');
        this.tabPanes = document.querySelectorAll('.tab-pane');
        
        // Toast container
        this.toastContainer = document.getElementById('toastContainer');
    }

    attachEventListeners() {
        // File upload events
        this.uploadArea.addEventListener('click', () => this.fileInput.click());
        this.uploadArea.addEventListener('dragover', this.handleDragOver.bind(this));
        this.uploadArea.addEventListener('dragleave', this.handleDragLeave.bind(this));
        this.uploadArea.addEventListener('drop', this.handleDrop.bind(this));
        this.fileInput.addEventListener('change', this.handleFileSelect.bind(this));
        this.removeFileBtn.addEventListener('click', this.removeFile.bind(this));
        
        // Job description events
        this.jobDescription.addEventListener('input', this.handleJobDescriptionInput.bind(this));
        this.backToUploadBtn.addEventListener('click', this.showUploadSection.bind(this));
        this.optimizeResumeBtn.addEventListener('click', this.optimizeResume.bind(this));
        
        // Results events
        this.downloadOptimizedBtn.addEventListener('click', this.downloadOptimizedResume.bind(this));
        this.copyOptimizedBtn.addEventListener('click', this.copyOptimizedResume.bind(this));
        this.optimizeAnotherBtn.addEventListener('click', this.resetApp.bind(this));
        
        // Tab events
        this.tabBtns.forEach(btn => {
            btn.addEventListener('click', () => this.switchTab(btn.dataset.tab));
        });
    }

    // File Upload Methods
    handleDragOver(e) {
        e.preventDefault();
        this.uploadArea.classList.add('dragover');
    }

    handleDragLeave(e) {
        e.preventDefault();
        this.uploadArea.classList.remove('dragover');
    }

    handleDrop(e) {
        e.preventDefault();
        this.uploadArea.classList.remove('dragover');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            this.processFile(files[0]);
        }
    }

    handleFileSelect(e) {
        const file = e.target.files[0];
        if (file) {
            this.processFile(file);
        }
    }

    processFile(file) {
        // Validate file type
        const allowedTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'text/plain'];
        const allowedExtensions = ['.pdf', '.docx', '.txt'];
        const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
        
        if (!allowedTypes.includes(file.type) && !allowedExtensions.includes(fileExtension)) {
            this.showToast('Please upload a PDF, DOCX, or TXT file.', 'error');
            return;
        }
        
        // Validate file size (10MB limit)
        if (file.size > 10 * 1024 * 1024) {
            this.showToast('File size must be less than 10MB.', 'error');
            return;
        }
        
        this.currentFile = file;
        this.displayFileInfo(file);
        this.showJobDescriptionSection();
    }

    displayFileInfo(file) {
        this.fileName.textContent = file.name;
        this.uploadArea.classList.add('has-file');
        this.fileInfo.style.display = 'flex';
    }

    removeFile() {
        this.currentFile = null;
        this.fileInput.value = '';
        this.uploadArea.classList.remove('has-file');
        this.fileInfo.style.display = 'none';
        this.showUploadSection();
    }

    // Job Description Methods
    handleJobDescriptionInput() {
        const text = this.jobDescription.value;
        this.charCount.textContent = text.length;
        
        // Enable optimize button if we have both file and job description
        this.optimizeResumeBtn.disabled = !this.currentFile || text.trim().length < 10;
    }

    // Section Navigation Methods
    showUploadSection() {
        this.uploadSection.style.display = 'block';
        this.jobDescriptionSection.style.display = 'none';
        this.loadingSection.style.display = 'none';
        this.resultsSection.style.display = 'none';
    }

    showJobDescriptionSection() {
        this.uploadSection.style.display = 'none';
        this.jobDescriptionSection.style.display = 'block';
        this.loadingSection.style.display = 'none';
        this.resultsSection.style.display = 'none';
    }

    showLoadingSection() {
        this.uploadSection.style.display = 'none';
        this.jobDescriptionSection.style.display = 'none';
        this.loadingSection.style.display = 'block';
        this.resultsSection.style.display = 'none';
        
        // Animate progress steps
        this.animateProgressSteps();
    }

    showResultsSection() {
        this.uploadSection.style.display = 'none';
        this.jobDescriptionSection.style.display = 'none';
        this.loadingSection.style.display = 'none';
        this.resultsSection.style.display = 'block';
    }

    // Progress Animation
    animateProgressSteps() {
        const steps = document.querySelectorAll('.step');
        let currentStep = 0;
        
        const nextStep = () => {
            if (currentStep < steps.length) {
                steps[currentStep].classList.add('active');
                currentStep++;
                setTimeout(nextStep, 1000);
            }
        };
        
        nextStep();
    }

    // API Methods
    async optimizeResume() {
        if (!this.currentFile || !this.jobDescription.value.trim()) {
            this.showToast('Please upload a resume and provide a job description.', 'error');
            return;
        }

        this.showLoadingSection();
        
        try {
            const formData = new FormData();
            formData.append('resume_file', this.currentFile);
            formData.append('job_description', this.jobDescription.value.trim());
            
            const response = await fetch(`${this.apiBaseUrl}/optimize`, {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Optimization failed');
            }
            
            const result = await response.json();
            this.handleOptimizationSuccess(result);
            
        } catch (error) {
            console.error('Optimization error:', error);
            this.showToast(`Optimization failed: ${error.message}`, 'error');
            this.showJobDescriptionSection();
        }
    }

    handleOptimizationSuccess(result) {
        this.originalResume = result.original_resume;
        this.optimizedResume = result.optimized_resume;
        
        // Display results
        this.originalResumeEl.textContent = this.originalResume;
        this.optimizedResumeEl.textContent = this.optimizedResume;
        this.originalResumeComparison.textContent = this.originalResume;
        this.optimizedResumeComparison.textContent = this.optimizedResume;
        
        this.showResultsSection();
        this.showToast('Resume optimized successfully!', 'success');
    }

    // Tab Methods
    switchTab(tabName) {
        // Update tab buttons
        this.tabBtns.forEach(btn => {
            btn.classList.remove('active');
            if (btn.dataset.tab === tabName) {
                btn.classList.add('active');
            }
        });
        
        // Update tab panes
        this.tabPanes.forEach(pane => {
            pane.classList.remove('active');
            if (pane.id === tabName + 'Tab') {
                pane.classList.add('active');
            }
        });
    }

    // Action Methods
    downloadOptimizedResume() {
        const blob = new Blob([this.optimizedResume], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `optimized_resume_${new Date().getTime()}.txt`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        
        this.showToast('Optimized resume downloaded!', 'success');
    }

    async copyOptimizedResume() {
        try {
            await navigator.clipboard.writeText(this.optimizedResume);
            this.showToast('Optimized resume copied to clipboard!', 'success');
        } catch (error) {
            console.error('Copy failed:', error);
            this.showToast('Failed to copy to clipboard', 'error');
        }
    }

    resetApp() {
        // Reset form
        this.currentFile = null;
        this.fileInput.value = '';
        this.jobDescription.value = '';
        this.charCount.textContent = '0';
        this.optimizeResumeBtn.disabled = true;
        
        // Reset UI
        this.uploadArea.classList.remove('has-file');
        this.fileInfo.style.display = 'none';
        
        // Reset tabs
        this.switchTab('original');
        
        // Show upload section
        this.showUploadSection();
        
        this.showToast('Ready to optimize another resume!', 'success');
    }

    // Utility Methods
    showToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.textContent = message;
        
        this.toastContainer.appendChild(toast);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 5000);
    }

    // Health Check
    async checkApiHealth() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/health`);
            if (response.ok) {
                console.log('API is healthy');
                return true;
            }
        } catch (error) {
            console.error('API health check failed:', error);
            this.showToast('Unable to connect to the optimization service. Please ensure the backend is running.', 'error');
        }
        return false;
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const app = new ResumeOptimizer();
    
    // Check API health on load
    app.checkApiHealth();
    
    // Make app globally available for debugging
    window.resumeOptimizer = app;
});

// Add some utility functions for better UX
document.addEventListener('DOMContentLoaded', () => {
    // Add smooth scrolling
    document.documentElement.style.scrollBehavior = 'smooth';
    
    // Add loading state to buttons
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(btn => {
        btn.addEventListener('click', function() {
            if (!this.disabled && !this.classList.contains('loading')) {
                this.classList.add('loading');
                setTimeout(() => {
                    this.classList.remove('loading');
                }, 2000);
            }
        });
    });
    
    // Add keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        // Ctrl/Cmd + Enter to optimize resume
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            const optimizeBtn = document.getElementById('optimizeResume');
            if (optimizeBtn && !optimizeBtn.disabled) {
                optimizeBtn.click();
            }
        }
        
        // Escape to go back
        if (e.key === 'Escape') {
            const backBtn = document.getElementById('backToUpload');
            if (backBtn && backBtn.offsetParent !== null) {
                backBtn.click();
            }
        }
    });
    
    // Add file drag and drop visual feedback
    const uploadArea = document.getElementById('uploadArea');
    if (uploadArea) {
        uploadArea.addEventListener('dragenter', (e) => {
            e.preventDefault();
            uploadArea.style.transform = 'scale(1.02)';
        });
        
        uploadArea.addEventListener('dragleave', (e) => {
            e.preventDefault();
            uploadArea.style.transform = 'scale(1)';
        });
    }
});