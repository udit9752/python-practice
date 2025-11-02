# Debt Freedom Analyzer - WordPress Plugin

Professional debt analysis and repayment roadmap tool for WordPress.

## Installation

### Method 1: WordPress Admin (Recommended)

1. Log in to WordPress admin panel
2. Go to **Plugins ? Add New ? Upload Plugin**
3. Click "Choose File" and select `debt-freedom-analyzer.zip`
4. Click "Install Now"
5. Click "Activate Plugin"

### Method 2: FTP/cPanel

1. Upload the `debt-freedom-analyzer` folder to:
   ```
   /wp-content/plugins/
   ```

2. Log in to WordPress admin
3. Go to **Plugins ? Installed Plugins**
4. Find "Debt Freedom Analyzer" and click "Activate"

## Setup

### 1. Configure Plugin

1. Go to **Debt Analyzer ? Settings** in WordPress admin
2. Enter your API Endpoint URL:
   - For PythonAnywhere: `https://username.pythonanywhere.com`
   - For Heroku: `https://your-app.herokuapp.com`
   - For custom server: `https://yourdomain.com/api`
3. Click "Save Settings"

### 2. Upload Assets

Upload these files to the plugin folder:

```
/wp-content/plugins/debt-freedom-analyzer/assets/
??? css/
?   ??? style.css        (Copy from debt-tool/styles.css)
??? js/
?   ??? script.js        (Copy from debt-tool/script.js)
??? images/
    ??? logo.png         (Your brand logo)
```

### 3. Add to Page

1. Create a new page or edit existing one
2. Add the shortcode:
   ```
   [debt_analyzer]
   ```
3. Publish the page

## Shortcode Options

### Basic Usage
```
[debt_analyzer]
```

### Without Hero Section
```
[debt_analyzer show_hero="false"]
```

### Without Resources Section
```
[debt_analyzer show_resources="false"]
```

### Minimal Version
```
[debt_analyzer show_hero="false" show_resources="false"]
```

## Customization

### Change Colors

Edit `/assets/css/style.css` and modify the CSS variables:

```css
:root {
    --primary-teal: #0F5F5C;    /* Your primary color */
    --primary-gold: #F4C430;    /* Your accent color */
    --primary-dark: #0A3F3D;    /* Dark variant */
}
```

### Change Logo

1. Upload your logo to `/assets/images/logo.png`
2. Recommended size: 200x200px
3. PNG format with transparent background

## Features

- ? **Comprehensive Debt Analysis** - Detailed metrics and insights
- ? **Three Repayment Strategies** - Avalanche, Snowball, and Hybrid methods
- ? **Personalized Roadmap** - Step-by-step action plan
- ? **Mobile Responsive** - Works on all devices
- ? **Print Friendly** - Easy to print results
- ? **No Data Storage** - Privacy-first design
- ? **Professional Design** - Matches your brand

## Requirements

- WordPress 5.0 or higher
- PHP 7.2 or higher
- Active API endpoint (see deployment guide)

## Support

### Documentation
- [User Guide](../../USER_GUIDE.md)
- [Deployment Guide](../../HOSTINGER_DEPLOYMENT_GUIDE.md)
- [Main README](../../DEBT_TOOL_README.md)

### Troubleshooting

**Plugin not showing on page**
- Check that shortcode is correct: `[debt_analyzer]`
- Verify plugin is activated
- Clear cache if using caching plugin

**Styles not loading**
- Check that style.css is in `/assets/css/`
- Clear browser cache (Ctrl+F5)
- Check file permissions (644)

**API errors**
- Verify API URL in settings
- Test API endpoint: visit `your-api-url/health`
- Check browser console for errors (F12)

## Version History

### 1.0.0
- Initial release
- Shortcode support
- WordPress REST API integration
- Admin settings page
- Responsive design

## License

GPL v2 or later

## Credits

Built with ?? to help people achieve financial freedom.
