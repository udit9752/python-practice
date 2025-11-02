<?php
/**
 * Calculator Template
 * This template contains the HTML structure for the debt calculator
 */

// Prevent direct access
if (!defined('ABSPATH')) {
    exit;
}

$show_hero = isset($atts['show_hero']) && $atts['show_hero'] === 'true';
$show_resources = isset($atts['show_resources']) && $atts['show_resources'] === 'true';
?>

<div class="debt-freedom-analyzer">
    
    <?php if ($show_hero): ?>
    <!-- Hero Section -->
    <section class="dfa-hero">
        <div class="dfa-container">
            <div class="dfa-hero-content">
                <div class="dfa-hero-text">
                    <h2 class="dfa-hero-title">Break Free from the <span class="dfa-highlight">Debt Trap</span></h2>
                    <p class="dfa-hero-subtitle">Get a personalized debt repayment roadmap in minutes. Analyze your debts, discover where you're losing money, and get a proven strategy to become debt-free.</p>
                </div>
            </div>
        </div>
    </section>
    <?php endif; ?>

    <!-- Calculator Section -->
    <section class="dfa-calculator-section">
        <div class="dfa-container">
            <div class="dfa-section-header">
                <h2 class="dfa-section-title">Debt Freedom Calculator</h2>
                <p class="dfa-section-subtitle">Enter your debts below to get started</p>
            </div>

            <!-- Debt Input Form -->
            <div class="dfa-calculator-container">
                <!-- Monthly Budget Input -->
                <div class="dfa-budget-input-section dfa-card">
                    <div class="dfa-card-header">
                        <h3><i class="fas fa-wallet"></i> Monthly Budget</h3>
                        <p>How much can you pay toward debts each month?</p>
                    </div>
                    <div class="dfa-card-body">
                        <div class="dfa-input-group">
                            <span class="dfa-input-prefix">$</span>
                            <input type="number" id="dfa-monthly-budget" class="dfa-form-input" placeholder="1000" min="0" step="10">
                            <span class="dfa-input-hint">Total amount available for all debt payments</span>
                        </div>
                    </div>
                </div>

                <!-- Debts Section -->
                <div class="dfa-debts-section dfa-card">
                    <div class="dfa-card-header">
                        <h3><i class="fas fa-credit-card"></i> Your Debts</h3>
                        <p>Add each of your debts below</p>
                    </div>
                    <div class="dfa-card-body">
                        <div id="dfa-debts-container">
                            <!-- Debt items will be added here dynamically -->
                        </div>
                        <button type="button" class="dfa-btn dfa-btn-secondary" id="dfa-add-debt-btn">
                            <i class="fas fa-plus"></i> Add Another Debt
                        </button>
                    </div>
                </div>

                <!-- Action Buttons -->
                <div class="dfa-action-buttons">
                    <button type="button" class="dfa-btn dfa-btn-primary dfa-btn-lg" id="dfa-analyze-btn">
                        <i class="fas fa-chart-bar"></i>
                        Analyze My Debts
                    </button>
                    <button type="button" class="dfa-btn dfa-btn-outline dfa-btn-lg" id="dfa-reset-btn">
                        <i class="fas fa-redo"></i>
                        Reset
                    </button>
                </div>
            </div>

            <!-- Loading State -->
            <div id="dfa-loading-state" class="dfa-loading-state" style="display: none;">
                <div class="dfa-spinner"></div>
                <p>Analyzing your debts...</p>
            </div>

            <!-- Results Section -->
            <div id="dfa-results-section" class="dfa-results-section" style="display: none;">
                <!-- Results content will be dynamically inserted here -->
            </div>
        </div>
    </section>

    <?php if ($show_resources): ?>
    <!-- Resources Section -->
    <section class="dfa-resources-section">
        <div class="dfa-container">
            <div class="dfa-section-header">
                <h2 class="dfa-section-title">Helpful Resources</h2>
                <p class="dfa-section-subtitle">Tools and information to support your debt-free journey</p>
            </div>
            <div class="dfa-resources-grid">
                <div class="dfa-resource-card">
                    <div class="dfa-resource-icon">
                        <i class="fas fa-book-open"></i>
                    </div>
                    <h3>Debt Management Guide</h3>
                    <p>Learn proven strategies for managing and eliminating debt effectively</p>
                </div>
                <div class="dfa-resource-card">
                    <div class="dfa-resource-icon">
                        <i class="fas fa-file-alt"></i>
                    </div>
                    <h3>Budget Template</h3>
                    <p>Download our free budget template to track your expenses and income</p>
                </div>
                <div class="dfa-resource-card">
                    <div class="dfa-resource-icon">
                        <i class="fas fa-users"></i>
                    </div>
                    <h3>Support Community</h3>
                    <p>Join others on their debt-free journey for support and motivation</p>
                </div>
                <div class="dfa-resource-card">
                    <div class="dfa-resource-icon">
                        <i class="fas fa-video"></i>
                    </div>
                    <h3>Video Tutorials</h3>
                    <p>Watch step-by-step videos on debt management and financial planning</p>
                </div>
            </div>
        </div>
    </section>
    <?php endif; ?>
    
</div>

<script>
// WordPress-specific initialization
jQuery(document).ready(function($) {
    if (typeof window.DebtFreedomAnalyzer !== 'undefined') {
        window.DebtFreedomAnalyzer.init({
            apiUrl: dfaData.restUrl,
            nonce: dfaData.nonce
        });
    }
});
</script>
