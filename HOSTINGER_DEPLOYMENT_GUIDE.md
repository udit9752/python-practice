# Debt Freedom Analyzer - Hostinger Shared Hosting Deployment Guide

This comprehensive guide will help you deploy the Debt Freedom Analyzer tool on Hostinger shared hosting and integrate it with your WordPress site.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Backend API Deployment](#backend-api-deployment)
3. [WordPress Plugin Installation](#wordpress-plugin-installation)
4. [Configuration](#configuration)
5. [Testing](#testing)
6. [Troubleshooting](#troubleshooting)
7. [Maintenance](#maintenance)

---

## Prerequisites

### What You Need
- Hostinger shared hosting account (Business or Premium plan recommended)
- WordPress site installed on Hostinger
- FTP/SFTP access credentials
- SSH access (if available on your plan)
- Your brand logo file (logo.png)

### Account Setup
1. Log in to your Hostinger control panel (hPanel)
2. Ensure Python 3.7+ is available (check in hPanel ? Advanced ? Select PHP Version)
3. Note your domain name (e.g., yourdomain.com)

---

## Backend API Deployment

### Option 1: Using Python on Shared Hosting (Recommended if SSH available)

#### Step 1: Upload Backend Files via FTP

1. **Connect to FTP:**
   - Host: ftp.yourdomain.com
   - Username: Your Hostinger username
   - Password: Your Hostinger password
   - Port: 21 (or 22 for SFTP)

2. **Create Directory Structure:**
   ```
   /home/username/public_html/
   ??? api/                    # API backend folder
   ?   ??? debt_analyzer.py
   ?   ??? debt_api.py
   ?   ??? requirements.txt
   ?   ??? .htaccess
   ```

3. **Upload Files:**
   - Upload `debt_analyzer.py` to `/api/` folder
   - Upload `debt_api.py` to `/api/` folder
   - Upload `requirements.txt` to `/api/` folder

#### Step 2: Create .htaccess for API

Create `/api/.htaccess` with the following content:

```apache
# Rewrite rules for FastAPI
RewriteEngine On
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^(.*)$ /api/index.cgi/$1 [QSA,L]

# Allow CORS
<IfModule mod_headers.c>
    Header set Access-Control-Allow-Origin "*"
    Header set Access-Control-Allow-Methods "GET, POST, OPTIONS"
    Header set Access-Control-Allow-Headers "Content-Type, Authorization"
</IfModule>
```

#### Step 3: Install Python Dependencies

1. **Via SSH (if available):**
```bash
ssh username@yourdomain.com
cd ~/public_html/api
python3 -m pip install --user -r requirements.txt
```

2. **Via hPanel:**
   - Go to Advanced ? Terminal
   - Navigate to your api folder
   - Run: `python3 -m pip install --user fastapi uvicorn pydantic`

#### Step 4: Create CGI Wrapper

Create `/api/index.cgi`:

```python
#!/usr/bin/env python3
import sys
import os

# Add the API directory to Python path
sys.path.insert(0, '/home/username/public_html/api')

# Set environment variables
os.environ['PYTHONPATH'] = '/home/username/public_html/api'

# Import and run the FastAPI app
from debt_api import app
import uvicorn

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

Make it executable:
```bash
chmod +x /home/username/public_html/api/index.cgi
```

### Option 2: Using External API Service (Easier Alternative)

If your Hostinger plan doesn't support Python well, deploy the backend to a free service:

#### Deploy to PythonAnywhere (Free Tier)

1. **Sign up at pythonanywhere.com** (free account)

2. **Upload your files:**
   - Go to Files tab
   - Create folder: `debt-analyzer`
   - Upload `debt_analyzer.py` and `debt_api.py`

3. **Install dependencies:**
   - Open Bash console
   - Run: `pip3 install --user fastapi uvicorn pydantic`

4. **Configure Web App:**
   - Go to Web tab ? Add a new web app
   - Choose Manual configuration ? Python 3.10
   - Set source code: `/home/username/debt-analyzer`
   - Set WSGI file to point to your FastAPI app

5. **Get your API URL:**
   - Your API will be at: `https://username.pythonanywhere.com/`
   - Test: `https://username.pythonanywhere.com/health`

#### Deploy to Heroku (Free/Paid)

1. **Create Heroku account** at heroku.com

2. **Create Procfile:**
```
web: uvicorn debt_api:app --host 0.0.0.0 --port $PORT
```

3. **Deploy:**
```bash
heroku login
heroku create debt-analyzer-your-name
git init
git add .
git commit -m "Initial commit"
git push heroku main
```

4. **Your API URL:** `https://debt-analyzer-your-name.herokuapp.com`

---

## WordPress Plugin Installation

### Step 1: Upload Plugin to WordPress

1. **Via WordPress Admin (Recommended):**
   - Log in to WordPress admin panel
   - Go to Plugins ? Add New ? Upload Plugin
   - Upload the `debt-freedom-analyzer.zip` file
   - Click "Install Now" ? "Activate"

2. **Via FTP:**
   - Upload the `debt-freedom-analyzer` folder to:
     `/public_html/wp-content/plugins/`
   - Go to WordPress admin ? Plugins ? Activate "Debt Freedom Analyzer"

### Step 2: Upload Assets

1. **Upload CSS:**
   - Copy `styles.css` to:
     `/wp-content/plugins/debt-freedom-analyzer/assets/css/style.css`

2. **Upload JavaScript:**
   - Copy `script.js` to:
     `/wp-content/plugins/debt-freedom-analyzer/assets/js/script.js`

3. **Upload Logo:**
   - Copy your `logo.png` to:
     `/wp-content/plugins/debt-freedom-analyzer/assets/images/logo.png`
   - Also upload to: `/wp-content/uploads/logo.png`

### Step 3: Configure WordPress Plugin

1. Go to WordPress Admin ? Debt Analyzer ? Settings

2. **Set API Endpoint URL:**
   - If using shared hosting API: `https://yourdomain.com/api`
   - If using PythonAnywhere: `https://username.pythonanywhere.com`
   - If using Heroku: `https://your-app.herokuapp.com`

3. Click "Save Settings"

### Step 4: Add to Your Website

1. **Create a new page:**
   - Go to Pages ? Add New
   - Title: "Debt Freedom Calculator" (or your choice)
   
2. **Add the shortcode:**
   ```
   [debt_analyzer]
   ```

3. **Publish the page**

4. **Add to menu:**
   - Go to Appearance ? Menus
   - Add your new page to the navigation menu

---

## Configuration

### Customize Branding

#### Update Logo Throughout Site

1. **Edit plugin files** to use your logo:
   - Navigate to plugin folder
   - Update all instances of `logo.png` with your actual logo filename

2. **Update colors** (optional):
   - Edit `/assets/css/style.css`
   - Find `:root` section
   - Change color variables to match your brand:
     ```css
     :root {
         --primary-teal: #0F5F5C;  /* Your primary color */
         --primary-gold: #F4C430;  /* Your accent color */
     }
     ```

### Performance Optimization

#### Enable Caching (hPanel)

1. Go to hPanel ? Website ? Performance
2. Enable "LiteSpeed Cache"
3. Set cache expiration to 1 hour for API responses

#### Optimize Images

1. Compress your logo using tools like TinyPNG
2. Recommended logo size: 200x200px (max 50KB)

### Security Settings

#### Protect API Endpoint

Create `/api/.htaccess`:

```apache
# Rate limiting (if available)
<IfModule mod_ratelimit.c>
    <Location /api>
        SetOutputFilter RATE_LIMIT
        SetEnv rate-limit 400
    </Location>
</IfModule>

# Block bad bots
RewriteEngine On
RewriteCond %{HTTP_USER_AGENT} ^$ [OR]
RewriteCond %{HTTP_USER_AGENT} (bot|crawl|spider) [NC]
RewriteRule ^api - [F,L]
```

---

## Testing

### Test Backend API

1. **Health Check:**
   ```
   Visit: https://yourdomain.com/api/health
   Should return: {"status": "healthy", ...}
   ```

2. **Test Analysis Endpoint:**
   ```bash
   curl -X POST https://yourdomain.com/api/analyze \
     -H "Content-Type: application/json" \
     -d '{
       "debts": [{
         "name": "Test Card",
         "balance": 5000,
         "interest_rate": 19.99,
         "minimum_payment": 150,
         "debt_type": "credit_card"
       }],
       "monthly_budget": 500
     }'
   ```

3. **Expected Response:**
   - JSON with `success: true`
   - Detailed analysis data

### Test WordPress Integration

1. **Visit your calculator page:**
   - Should load without errors
   - Form should be visible and styled correctly

2. **Submit test data:**
   - Add one debt
   - Set monthly budget
   - Click "Analyze My Debts"
   - Should show results within 5-10 seconds

3. **Check browser console:**
   - Press F12 ? Console
   - Should have no errors
   - Look for "Debt Freedom Analyzer loaded successfully"

---

## Troubleshooting

### Common Issues

#### "API Error: Failed to connect"

**Solutions:**
1. Verify API URL in WordPress settings
2. Check if API is accessible: visit `your-api-url/health`
3. Check .htaccess file is correct
4. Ensure CORS headers are enabled

#### "500 Internal Server Error"

**Solutions:**
1. Check error logs in hPanel ? Files ? Error Log
2. Verify Python version: `python3 --version`
3. Check file permissions (755 for directories, 644 for files)
4. Verify all dependencies are installed

#### Styles not loading

**Solutions:**
1. Clear WordPress cache (if using cache plugin)
2. Clear browser cache (Ctrl+F5)
3. Check CSS file path in plugin
4. Verify file uploaded to correct location

#### Logo not displaying

**Solutions:**
1. Check logo file path in code
2. Verify logo file uploaded to `/wp-content/uploads/`
3. Check file permissions (644)
4. Use absolute URL in img src if needed

### Performance Issues

#### Slow API Response

**Solutions:**
1. Increase PHP memory limit (hPanel ? PHP Configuration)
2. Optimize database queries
3. Enable caching
4. Consider upgrading hosting plan

#### Page Load Slow

**Solutions:**
1. Minify CSS/JS files
2. Enable GZIP compression
3. Use CDN for Font Awesome
4. Optimize images

---

## Maintenance

### Regular Updates

#### Weekly Tasks
- Check error logs for issues
- Monitor API response times
- Review user feedback

#### Monthly Tasks
- Update WordPress and plugins
- Check for security updates
- Backup website and database
- Review and optimize database

### Backups

#### Automated Backups (Hostinger)

1. Go to hPanel ? Backups
2. Enable automatic backups
3. Set backup frequency: Weekly
4. Include files and database

#### Manual Backup

1. **Files:**
   - Download `/wp-content/plugins/debt-freedom-analyzer/`
   - Download `/api/` folder

2. **Database:**
   - hPanel ? Databases ? phpMyAdmin
   - Export your WordPress database

### Monitoring

#### Setup Uptime Monitoring

Use free services:
- UptimeRobot.com
- Pingdom
- StatusCake

Monitor:
- Main website URL
- API health endpoint
- Calculator page

### Support

#### Get Help

1. **Hostinger Support:**
   - Live chat 24/7
   - Help center: support.hostinger.com

2. **Community:**
   - WordPress forums
   - Stack Overflow

3. **Documentation:**
   - This guide
   - WordPress codex
   - FastAPI documentation

---

## Additional Resources

### Useful Links

- **Hostinger Knowledge Base:** https://support.hostinger.com
- **WordPress Codex:** https://codex.wordpress.org
- **FastAPI Documentation:** https://fastapi.tiangolo.com
- **Python Documentation:** https://docs.python.org

### Recommended Plugins

1. **WP Rocket** - Caching and performance
2. **Wordfence Security** - Security and firewall
3. **UpdraftPlus** - Backup solution
4. **Contact Form 7** - For support inquiries

---

## Conclusion

You now have a professional debt analysis tool deployed on your Hostinger WordPress site! 

### Next Steps

1. ? Test thoroughly with different debt scenarios
2. ? Customize branding to match your website
3. ? Add privacy policy and disclaimer
4. ? Promote your tool on social media
5. ? Collect user feedback for improvements

### Need Help?

If you encounter any issues not covered in this guide:
1. Check the troubleshooting section
2. Review error logs
3. Contact Hostinger support
4. Consult WordPress forums

**Good luck with your debt freedom tool! You're helping people change their lives!** ??
