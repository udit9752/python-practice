
<?php
/**
 * Plugin Name: Debt Freedom Analyzer
 * Plugin URI: https://yourwebsite.com/debt-freedom-analyzer
 * Description: Help people escape debt traps with personalized analysis and repayment roadmaps
 * Version: 1.0.0
 * Author: Your Company Name
 * Author URI: https://yourwebsite.com
 * License: GPL v2 or later
 * Text Domain: debt-freedom-analyzer
 */

// Prevent direct access
if (!defined('ABSPATH')) {
    exit;
}

// Define plugin constants
define('DFA_VERSION', '1.0.0');
define('DFA_PLUGIN_DIR', plugin_dir_path(__FILE__));
define('DFA_PLUGIN_URL', plugin_dir_url(__FILE__));

class DebtFreedomAnalyzer {
    
    private static $instance = null;
    
    public static function get_instance() {
        if (null === self::$instance) {
            self::$instance = new self();
        }
        return self::$instance;
    }
    
    private function __construct() {
        // Add hooks
        add_action('wp_enqueue_scripts', array($this, 'enqueue_scripts'));
        add_shortcode('debt_analyzer', array($this, 'render_calculator'));
        add_action('rest_api_init', array($this, 'register_rest_routes'));
        add_action('admin_menu', array($this, 'add_admin_menu'));
        
        // Add settings link on plugin page
        add_filter('plugin_action_links_' . plugin_basename(__FILE__), array($this, 'add_settings_link'));
    }
    
    /**
     * Enqueue CSS and JavaScript
     */
    public function enqueue_scripts() {
        if (is_singular() && has_shortcode(get_post()->post_content, 'debt_analyzer')) {
            // Enqueue Font Awesome
            wp_enqueue_style('font-awesome', 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css', array(), '6.4.0');
            
            // Enqueue Google Fonts
            wp_enqueue_style('google-fonts-inter', 'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap', array(), null);
            
            // Enqueue plugin CSS
            wp_enqueue_style('debt-analyzer-style', DFA_PLUGIN_URL . 'assets/css/style.css', array(), DFA_VERSION);
            
            // Enqueue plugin JavaScript
            wp_enqueue_script('debt-analyzer-script', DFA_PLUGIN_URL . 'assets/js/script.js', array(), DFA_VERSION, true);
            
            // Pass AJAX URL and nonce to JavaScript
            wp_localize_script('debt-analyzer-script', 'dfaData', array(
                'ajaxUrl' => admin_url('admin-ajax.php'),
                'nonce' => wp_create_nonce('dfa_nonce'),
                'restUrl' => rest_url('debt-analyzer/v1/')
            ));
        }
    }
    
    /**
     * Render calculator shortcode
     */
    public function render_calculator($atts) {
        $atts = shortcode_atts(array(
            'show_hero' => 'true',
            'show_resources' => 'true'
        ), $atts);
        
        ob_start();
        include DFA_PLUGIN_DIR . 'templates/calculator.php';
        return ob_get_clean();
    }
    
    /**
     * Register REST API routes
     */
    public function register_rest_routes() {
        register_rest_route('debt-analyzer/v1', '/analyze', array(
            'methods' => 'POST',
            'callback' => array($this, 'analyze_debts'),
            'permission_callback' => '__return_true', // Allow public access
            'args' => array(
                'debts' => array(
                    'required' => true,
                    'validate_callback' => array($this, 'validate_debts')
                ),
                'monthly_budget' => array(
                    'required' => true,
                    'validate_callback' => function($param) {
                        return is_numeric($param) && $param > 0;
                    }
                )
            )
        ));
    }
    
    /**
     * Validate debts data
     */
    public function validate_debts($param, $request, $key) {
        if (!is_array($param) || empty($param)) {
            return false;
        }
        
        foreach ($param as $debt) {
            if (!isset($debt['name']) || !isset($debt['balance']) || 
                !isset($debt['interest_rate']) || !isset($debt['minimum_payment'])) {
                return false;
            }
        }
        
        return true;
    }
    
    /**
     * Analyze debts (REST API callback)
     */
    public function analyze_debts($request) {
        try {
            $debts = $request->get_param('debts');
            $monthly_budget = $request->get_param('monthly_budget');
            
            // Process analysis (call external API or use PHP processing)
            $api_url = get_option('dfa_api_url', 'http://localhost:8000');
            
            $response = wp_remote_post($api_url . '/api/analyze', array(
                'headers' => array('Content-Type' => 'application/json'),
                'body' => json_encode(array(
                    'debts' => $debts,
                    'monthly_budget' => $monthly_budget
                )),
                'timeout' => 30
            ));
            
            if (is_wp_error($response)) {
                return new WP_Error('api_error', 'Failed to connect to analysis service', array('status' => 500));
            }
            
            $body = wp_remote_retrieve_body($response);
            $data = json_decode($body, true);
            
            return new WP_REST_Response($data, 200);
            
        } catch (Exception $e) {
            return new WP_Error('processing_error', $e->getMessage(), array('status' => 500));
        }
    }
    
    /**
     * Add admin menu
     */
    public function add_admin_menu() {
        add_menu_page(
            'Debt Freedom Analyzer',
            'Debt Analyzer',
            'manage_options',
            'debt-freedom-analyzer',
            array($this, 'admin_page'),
            'dashicons-chart-line',
            30
        );
    }
    
    /**
     * Admin page
     */
    public function admin_page() {
        // Save settings
        if (isset($_POST['dfa_save_settings']) && check_admin_referer('dfa_settings_nonce')) {
            update_option('dfa_api_url', sanitize_text_field($_POST['dfa_api_url']));
            echo '<div class="notice notice-success"><p>Settings saved successfully!</p></div>';
        }
        
        $api_url = get_option('dfa_api_url', 'http://localhost:8000');
        
        ?>
        <div class="wrap">
            <h1>Debt Freedom Analyzer Settings</h1>
            
            <div class="card" style="max-width: 800px;">
                <h2>Setup Instructions</h2>
                <p>To use the Debt Freedom Analyzer on your WordPress site:</p>
                <ol>
                    <li>Add the shortcode <code>[debt_analyzer]</code> to any page or post</li>
                    <li>Configure your API endpoint below (if using external processing)</li>
                    <li>Customize the appearance using WordPress customizer or CSS</li>
                </ol>
            </div>
            
            <form method="post" action="" style="max-width: 800px; margin-top: 20px;">
                <?php wp_nonce_field('dfa_settings_nonce'); ?>
                
                <table class="form-table">
                    <tr>
                        <th scope="row">
                            <label for="dfa_api_url">API Endpoint URL</label>
                        </th>
                        <td>
                            <input type="url" 
                                   name="dfa_api_url" 
                                   id="dfa_api_url" 
                                   value="<?php echo esc_attr($api_url); ?>" 
                                   class="regular-text">
                            <p class="description">URL of your debt analysis backend API</p>
                        </td>
                    </tr>
                </table>
                
                <p class="submit">
                    <input type="submit" 
                           name="dfa_save_settings" 
                           class="button button-primary" 
                           value="Save Settings">
                </p>
            </form>
            
            <div class="card" style="max-width: 800px; margin-top: 20px;">
                <h2>Usage Examples</h2>
                <h3>Basic Usage:</h3>
                <code>[debt_analyzer]</code>
                
                <h3>Without Hero Section:</h3>
                <code>[debt_analyzer show_hero="false"]</code>
                
                <h3>Without Resources Section:</h3>
                <code>[debt_analyzer show_resources="false"]</code>
            </div>
        </div>
        <?php
    }
    
    /**
     * Add settings link on plugins page
     */
    public function add_settings_link($links) {
        $settings_link = '<a href="admin.php?page=debt-freedom-analyzer">Settings</a>';
        array_unshift($links, $settings_link);
        return $links;
    }
}

// Initialize plugin
function dfa_init() {
    return DebtFreedomAnalyzer::get_instance();
}

// Start the plugin
add_action('plugins_loaded', 'dfa_init');

/**
 * Activation hook
 */
register_activation_hook(__FILE__, 'dfa_activate');
function dfa_activate() {
    // Set default options
    add_option('dfa_api_url', 'http://localhost:8000');
    
    // Flush rewrite rules
    flush_rewrite_rules();
}

/**
 * Deactivation hook
 */
register_deactivation_hook(__FILE__, 'dfa_deactivate');
function dfa_deactivate() {
    // Flush rewrite rules
    flush_rewrite_rules();
}
