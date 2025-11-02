// ===================================
// Debt Freedom Analyzer - Main JavaScript
// ===================================

// API Configuration
const API_URL = 'http://localhost:8000'; // Change this to your production URL

// State Management
let debts = [];
let analysisResult = null;

// Initialize App
document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
});

function initializeApp() {
    // Add initial debt form
    addDebtForm();
    
    // Setup event listeners
    document.getElementById('addDebtBtn').addEventListener('click', addDebtForm);
    document.getElementById('analyzeBtn').addEventListener('click', analyzeDebts);
    document.getElementById('resetBtn').addEventListener('click', resetForm);
    
    // Smooth scrolling for navigation
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
    
    console.log('Debt Freedom Analyzer initialized');
}

// ===================================
// Debt Form Management
// ===================================

let debtCounter = 0;

function addDebtForm() {
    debtCounter++;
    const debtsContainer = document.getElementById('debtsContainer');
    
    const debtItem = document.createElement('div');
    debtItem.className = 'debt-item';
    debtItem.id = `debt-${debtCounter}`;
    debtItem.innerHTML = `
        <div class="debt-item-header">
            <span class="debt-number">Debt #${debtCounter}</span>
            <button type="button" class="remove-debt-btn" onclick="removeDebt(${debtCounter})">
                <i class="fas fa-times"></i> Remove
            </button>
        </div>
        <div class="debt-inputs">
            <div class="input-field">
                <label>Debt Name *</label>
                <input type="text" 
                       class="form-input debt-name" 
                       placeholder="e.g., Visa Credit Card"
                       required>
            </div>
            <div class="input-field">
                <label>Debt Type *</label>
                <select class="form-input debt-type" required>
                    <option value="credit_card">Credit Card</option>
                    <option value="personal_loan">Personal Loan</option>
                    <option value="auto_loan">Auto Loan</option>
                    <option value="student_loan">Student Loan</option>
                    <option value="mortgage">Mortgage</option>
                    <option value="medical">Medical Debt</option>
                    <option value="other">Other</option>
                </select>
            </div>
            <div class="input-field">
                <label>Current Balance ($) *</label>
                <input type="number" 
                       class="form-input debt-balance" 
                       placeholder="5000.00"
                       min="0"
                       step="0.01"
                       required>
            </div>
            <div class="input-field">
                <label>Interest Rate (%) *</label>
                <input type="number" 
                       class="form-input debt-rate" 
                       placeholder="19.99"
                       min="0"
                       max="100"
                       step="0.01"
                       required>
            </div>
            <div class="input-field">
                <label>Minimum Payment ($) *</label>
                <input type="number" 
                       class="form-input debt-minimum" 
                       placeholder="150.00"
                       min="0"
                       step="0.01"
                       required>
            </div>
        </div>
    `;
    
    debtsContainer.appendChild(debtItem);
    
    // Animate in
    debtItem.style.opacity = '0';
    debtItem.style.transform = 'translateY(-20px)';
    setTimeout(() => {
        debtItem.style.transition = 'all 0.3s ease';
        debtItem.style.opacity = '1';
        debtItem.style.transform = 'translateY(0)';
    }, 10);
}

function removeDebt(debtId) {
    const debtElement = document.getElementById(`debt-${debtId}`);
    if (debtElement) {
        debtElement.style.transition = 'all 0.3s ease';
        debtElement.style.opacity = '0';
        debtElement.style.transform = 'translateX(-100%)';
        setTimeout(() => {
            debtElement.remove();
            // If no debts left, add one
            if (document.querySelectorAll('.debt-item').length === 0) {
                addDebtForm();
            }
        }, 300);
    }
}

function resetForm() {
    if (confirm('Are you sure you want to reset all data?')) {
        document.getElementById('monthlyBudget').value = '';
        document.getElementById('debtsContainer').innerHTML = '';
        document.getElementById('resultsSection').style.display = 'none';
        debtCounter = 0;
        addDebtForm();
        
        // Scroll to top of calculator
        document.getElementById('calculator').scrollIntoView({ behavior: 'smooth' });
    }
}

// ===================================
// Data Collection & Validation
// ===================================

function collectDebtData() {
    const monthlyBudget = parseFloat(document.getElementById('monthlyBudget').value);
    
    if (!monthlyBudget || monthlyBudget <= 0) {
        throw new Error('Please enter a valid monthly budget');
    }
    
    const debtElements = document.querySelectorAll('.debt-item');
    const debts = [];
    
    debtElements.forEach((element, index) => {
        const name = element.querySelector('.debt-name').value.trim();
        const type = element.querySelector('.debt-type').value;
        const balance = parseFloat(element.querySelector('.debt-balance').value);
        const rate = parseFloat(element.querySelector('.debt-rate').value);
        const minimum = parseFloat(element.querySelector('.debt-minimum').value);
        
        // Validation
        if (!name) {
            throw new Error(`Please enter a name for Debt #${index + 1}`);
        }
        if (!balance || balance <= 0) {
            throw new Error(`Please enter a valid balance for ${name}`);
        }
        if (rate < 0 || rate > 100) {
            throw new Error(`Interest rate for ${name} must be between 0 and 100`);
        }
        if (!minimum || minimum <= 0) {
            throw new Error(`Please enter a valid minimum payment for ${name}`);
        }
        if (minimum > balance) {
            throw new Error(`Minimum payment for ${name} cannot exceed the balance`);
        }
        
        debts.push({
            name,
            debt_type: type,
            balance,
            interest_rate: rate,
            minimum_payment: minimum
        });
    });
    
    if (debts.length === 0) {
        throw new Error('Please add at least one debt');
    }
    
    // Check if budget covers minimum payments
    const totalMinimum = debts.reduce((sum, debt) => sum + debt.minimum_payment, 0);
    if (monthlyBudget < totalMinimum) {
        throw new Error(`Monthly budget ($${monthlyBudget.toFixed(2)}) must be at least $${totalMinimum.toFixed(2)} to cover all minimum payments`);
    }
    
    return { debts, monthly_budget: monthlyBudget };
}

// ===================================
// API Communication
// ===================================

async function analyzeDebts() {
    try {
        // Collect and validate data
        const data = collectDebtData();
        
        // Show loading state
        document.getElementById('loadingState').style.display = 'block';
        document.getElementById('resultsSection').style.display = 'none';
        
        // Scroll to loading
        document.getElementById('loadingState').scrollIntoView({ behavior: 'smooth' });
        
        // Call API
        const response = await fetch(`${API_URL}/api/analyze`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to analyze debts');
        }
        
        const result = await response.json();
        
        if (!result.success) {
            throw new Error(result.error || 'Analysis failed');
        }
        
        // Store result
        analysisResult = result.data;
        
        // Display results
        displayResults(result.data);
        
        // Hide loading, show results
        document.getElementById('loadingState').style.display = 'none';
        document.getElementById('resultsSection').style.display = 'block';
        
        // Scroll to results
        setTimeout(() => {
            document.getElementById('resultsSection').scrollIntoView({ behavior: 'smooth' });
        }, 300);
        
    } catch (error) {
        // Hide loading
        document.getElementById('loadingState').style.display = 'none';
        
        // Show error
        alert(`Error: ${error.message}`);
        console.error('Analysis error:', error);
    }
}

// ===================================
// Results Display
// ===================================

function displayResults(data) {
    displayAnalysisOverview(data.analysis);
    displayProblems(data.problems);
    displayStrategies(data.repayment_strategies, data.comparison);
    displayRecommendedStrategy(data.recommended_strategy);
    displayActionPlan(data.action_plan);
    displayMilestones(data.milestones);
    displayTips(data.tips);
    
    setupResultsEventListeners();
}

function displayAnalysisOverview(analysis) {
    document.getElementById('totalDebt').textContent = `$${analysis.total_debt.toLocaleString()}`;
    document.getElementById('debtCount').textContent = analysis.number_of_debts;
    document.getElementById('avgRate').textContent = `${analysis.weighted_avg_interest_rate}%`;
    document.getElementById('yearlyInterest').textContent = `$${analysis.yearly_interest_cost.toLocaleString()}`;
    document.getElementById('budgetUtil').textContent = `${analysis.budget_utilization_percentage}%`;
    
    const severityElement = document.getElementById('severity');
    severityElement.textContent = analysis.severity;
    
    // Color code severity
    severityElement.style.background = getSeverityColor(analysis.severity);
    severityElement.style.color = 'white';
    
    document.getElementById('severityMessage').textContent = analysis.severity_message;
}

function getSeverityColor(severity) {
    const colors = {
        'Low': '#10B981',
        'Moderate': '#F59E0B',
        'High': '#F97316',
        'Critical': '#EF4444'
    };
    return colors[severity] || '#6B7280';
}

function displayProblems(problems) {
    const problemsCard = document.getElementById('problemsCard');
    const problemsList = document.getElementById('problemsList');
    
    if (problems.length === 0) {
        problemsCard.style.display = 'none';
        return;
    }
    
    problemsCard.style.display = 'block';
    problemsList.innerHTML = '';
    
    problems.forEach(problem => {
        const problemItem = document.createElement('div');
        problemItem.className = `problem-item severity-${problem.severity}`;
        problemItem.innerHTML = `
            <div class="problem-header">
                <i class="fas fa-exclamation-circle"></i>
                <span class="problem-type">${problem.type}</span>
            </div>
            <div class="problem-description">${problem.description}</div>
            <div class="problem-recommendation">
                <i class="fas fa-lightbulb"></i> ${problem.recommendation}
            </div>
        `;
        problemsList.appendChild(problemItem);
    });
}

function displayStrategies(strategies, comparison) {
    // Avalanche
    displayStrategyCard('avalanche', strategies.avalanche);
    
    // Snowball
    displayStrategyCard('snowball', strategies.snowball);
    
    // Hybrid
    displayStrategyCard('hybrid', strategies.hybrid);
    
    // Comparison text
    const savedMonths = comparison.time_saved_avalanche_vs_snowball;
    const savedMoney = comparison.interest_saved_avalanche_vs_snowball;
    
    const comparisonText = document.getElementById('comparisonText');
    comparisonText.innerHTML = `
        <strong>Key Insight:</strong> The Avalanche method will save you 
        <strong>$${Math.abs(savedMoney).toLocaleString()}</strong> in interest 
        and get you debt-free <strong>${Math.abs(savedMonths)} months ${savedMonths > 0 ? 'faster' : 'slower'}</strong> 
        compared to the Snowball method. However, the Snowball method provides quicker psychological wins 
        by eliminating debts faster.
    `;
}

function displayStrategyCard(strategyName, strategyData) {
    document.getElementById(`${strategyName}-time`).textContent = strategyData.time_to_debt_free;
    document.getElementById(`${strategyName}-interest`).textContent = `$${strategyData.total_interest_paid.toLocaleString()}`;
    document.getElementById(`${strategyName}-total`).textContent = `$${strategyData.total_amount_paid.toLocaleString()}`;
}

function displayRecommendedStrategy(recommended) {
    const method = recommended.method;
    const reason = recommended.reason;
    
    document.getElementById('recommendedMethodName').textContent = method.method_name;
    document.getElementById('recommendationReason').innerHTML = `
        <i class="fas fa-star"></i> ${reason}
    `;
    
    // Display payoff timeline
    const timelineContainer = document.getElementById('timelineContainer');
    timelineContainer.innerHTML = '';
    
    if (method.payoff_timeline && method.payoff_timeline.length > 0) {
        method.payoff_timeline.forEach((item, index) => {
            const timelineItem = document.createElement('div');
            timelineItem.className = 'timeline-item';
            timelineItem.innerHTML = `
                <div class="timeline-debt-name">
                    ${index + 1}. ${item.debt_name}
                </div>
                <div class="timeline-date">
                    <i class="fas fa-calendar"></i> Paid off in ${item.years_months}
                </div>
            `;
            timelineContainer.appendChild(timelineItem);
        });
    }
}

function displayActionPlan(actionPlan) {
    const container = document.getElementById('actionStepsContainer');
    container.innerHTML = '';
    
    // Group by priority
    const priorities = {
        'immediate': [],
        'week_1': [],
        'month_1': [],
        'ongoing': []
    };
    
    actionPlan.forEach(step => {
        if (priorities[step.priority]) {
            priorities[step.priority].push(step);
        }
    });
    
    // Display each priority group
    Object.keys(priorities).forEach(priority => {
        if (priorities[priority].length > 0) {
            priorities[priority].forEach(step => {
                const stepElement = document.createElement('div');
                stepElement.className = 'action-step';
                stepElement.innerHTML = `
                    <div class="step-priority ${step.priority}">${step.priority.replace('_', ' ')}</div>
                    <div class="step-title">${step.title}</div>
                    <div class="step-description">${step.description}</div>
                    <div class="step-timeline"><i class="fas fa-clock"></i> ${step.timeline}</div>
                `;
                container.appendChild(stepElement);
            });
        }
    });
}

function displayMilestones(milestones) {
    const container = document.getElementById('milestonesContainer');
    container.innerHTML = '';
    
    milestones.forEach(milestone => {
        const milestoneElement = document.createElement('div');
        milestoneElement.className = 'milestone';
        milestoneElement.innerHTML = `
            <div class="milestone-title">${milestone.title}</div>
            <div class="milestone-timeline"><i class="fas fa-calendar-check"></i> ${milestone.timeline}</div>
            <div class="milestone-description">${milestone.description}</div>
            <div class="milestone-celebration"><i class="fas fa-gift"></i> ${milestone.celebration}</div>
        `;
        container.appendChild(milestoneElement);
    });
}

function displayTips(tips) {
    const container = document.getElementById('tipsContainer');
    container.innerHTML = '';
    
    tips.forEach(tip => {
        const tipElement = document.createElement('div');
        tipElement.className = 'tip-item';
        tipElement.innerHTML = `
            <div class="tip-icon">
                <i class="fas fa-check"></i>
            </div>
            <div class="tip-text">${tip}</div>
        `;
        container.appendChild(tipElement);
    });
}

// ===================================
// Results Actions
// ===================================

function setupResultsEventListeners() {
    // Print button
    const printBtn = document.getElementById('printPlanBtn');
    if (printBtn) {
        printBtn.onclick = () => window.print();
    }
    
    // Download button
    const downloadBtn = document.getElementById('downloadPlanBtn');
    if (downloadBtn) {
        downloadBtn.onclick = downloadPDF;
    }
    
    // New analysis button
    const newAnalysisBtn = document.getElementById('newAnalysisBtn');
    if (newAnalysisBtn) {
        newAnalysisBtn.onclick = resetForm;
    }
}

function downloadPDF() {
    // For a simple solution, we'll create a downloadable JSON file
    // In production, you'd integrate with a PDF library
    const dataStr = JSON.stringify(analysisResult, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `debt-roadmap-${new Date().toISOString().split('T')[0]}.json`;
    link.click();
    URL.revokeObjectURL(url);
    
    alert('Your debt repayment roadmap has been downloaded! For a formatted PDF, please use the Print button and "Save as PDF" option.');
}

// ===================================
// Utility Functions
// ===================================

function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

function formatPercent(value) {
    return `${value.toFixed(2)}%`;
}

// ===================================
// Error Handling
// ===================================

window.addEventListener('error', (event) => {
    console.error('Global error:', event.error);
});

window.addEventListener('unhandledrejection', (event) => {
    console.error('Unhandled promise rejection:', event.reason);
});

console.log('Debt Freedom Analyzer loaded successfully');
