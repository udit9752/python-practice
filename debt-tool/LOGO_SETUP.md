# Logo Setup Instructions

Your logo is a crucial part of your brand identity. Here's how to properly set it up in the Debt Freedom Analyzer tool.

## Logo File

**Your logo file has been saved and should be named:** `logo.png`

### Specifications

- **Format:** PNG (recommended) or JPG
- **Size:** 200x200 pixels (recommended)
- **Background:** Transparent (for PNG) or white
- **File size:** Under 50KB (optimized for web)
- **Color mode:** RGB

## Where to Upload Your Logo

### For Standalone Website

Upload `logo.png` to these locations:

1. **Main directory:**
   ```
   /public_html/logo.png
   ```

2. **In the HTML file, verify the path:**
   ```html
   <img src="logo.png" alt="Debt Freedom Analyzer Logo" class="brand-logo">
   ```

### For WordPress Plugin

Upload `logo.png` to:

1. **Plugin assets folder:**
   ```
   /wp-content/plugins/debt-freedom-analyzer/assets/images/logo.png
   ```

2. **Also upload to WordPress uploads (backup):**
   ```
   /wp-content/uploads/logo.png
   ```

## Logo Usage in the Tool

Your logo appears in several places:

1. **Header** - Top left corner with company name
2. **Footer** - Bottom of page
3. **Print version** - Included in printed roadmaps

## Optimizing Your Logo

### Resize Logo

If your logo is too large, resize it:

**Online tools:**
- TinyPNG.com - Compress without quality loss
- Squoosh.app - Advanced image optimization
- Canva.com - Resize and edit

**Recommended dimensions:**
- **Header logo:** 60x60px (will be scaled automatically)
- **Footer logo:** 50x50px
- **Original file:** 200x200px (for quality)

### Compress Logo

Reduce file size without losing quality:

1. Use TinyPNG.com
2. Upload your logo.png
3. Download compressed version
4. Replace original file

**Target file size:** Under 50KB

## Customizing Logo Display

### Adjust Size in CSS

Edit `styles.css` to change logo size:

```css
.brand-logo {
    width: 60px;      /* Change this value */
    height: 60px;     /* Change this value */
    border-radius: 12px;
    background: white;
    padding: 5px;
}
```

### Change Logo Shape

**Circular logo:**
```css
.brand-logo {
    border-radius: 50%;  /* Makes it circular */
}
```

**Square logo (no rounding):**
```css
.brand-logo {
    border-radius: 0;  /* Sharp corners */
}
```

## Logo Color Schemes

Your logo colors should complement your site:

### Current Color Scheme

Based on your logo, we've used:
- **Primary Teal:** #0F5F5C
- **Gold Accent:** #F4C430
- **Dark Teal:** #0A3F3D

### If Your Logo Uses Different Colors

Update the color variables in `styles.css`:

```css
:root {
    /* Extract colors from your logo */
    --primary-teal: #YourColor1;
    --primary-gold: #YourColor2;
    --primary-dark: #YourColor3;
}
```

**Tools to extract colors from logo:**
- ColorZilla (browser extension)
- Adobe Color
- Coolors.co

## Logo Variations

### Dark Mode Logo (Optional)

If you have a dark mode version of your logo:

1. Save as `logo-dark.png`
2. Update CSS for dark backgrounds:

```css
@media (prefers-color-scheme: dark) {
    .brand-logo {
        content: url('logo-dark.png');
    }
}
```

### High-Resolution Displays

For Retina/4K displays, provide 2x version:

1. Create logo at 400x400px
2. Save as `logo@2x.png`
3. Update HTML:

```html
<img src="logo.png" 
     srcset="logo@2x.png 2x" 
     alt="Logo">
```

## Troubleshooting

### Logo Not Displaying

**Check these:**
1. ? File named exactly `logo.png` (lowercase)
2. ? File uploaded to correct location
3. ? File permissions set to 644
4. ? Path in code is correct
5. ? Clear browser cache (Ctrl+F5)

**Still not working?**

Replace image path with absolute URL:
```html
<img src="https://yourdomain.com/logo.png" alt="Logo">
```

### Logo Looks Blurry

**Solutions:**
1. Upload higher resolution version
2. Use PNG instead of JPG
3. Ensure original is at least 200x200px
4. Check if CSS is scaling it incorrectly

### Logo Wrong Size

**Adjust in CSS:**
```css
.brand-logo {
    max-width: 80px;   /* Maximum width */
    height: auto;      /* Maintain aspect ratio */
}
```

### Logo Background Issues

**For PNG with transparency:**
```css
.brand-logo {
    background: transparent;  /* Remove background */
    padding: 0;               /* Remove padding */
}
```

## Logo Best Practices

### ? Do:
- Use high-quality original file
- Optimize for web (compress)
- Test on different devices
- Use transparent background (PNG)
- Keep aspect ratio
- Include alt text for accessibility

### ? Don't:
- Use huge file sizes (slows site)
- Stretch or distort logo
- Use low-resolution images
- Forget mobile display
- Use complex animations (unless subtle)

## Logo Consistency

Ensure your logo matches across:
- ? Website header
- ? Website footer
- ? WordPress plugin
- ? Print version
- ? Social media (if applicable)
- ? Email templates (if applicable)

## Brand Guidelines

Create a simple brand guideline document:

1. **Logo variations:** Primary, dark, light
2. **Color palette:** Primary, secondary, accent colors
3. **Typography:** Font families used
4. **Spacing:** Minimum clear space around logo
5. **Usage:** Dos and don'ts

## Need Help?

### Logo Design Resources

If you need a logo designed or redesigned:
- Fiverr.com - Affordable designers
- 99designs.com - Design contests
- Canva.com - DIY logo maker
- Tailor Brands - AI logo generator

### Free Stock Logos

For testing purposes:
- Flaticon.com
- Icons8.com
- Noun Project

---

## Checklist

Before launching, verify:

- [ ] Logo uploaded to all necessary locations
- [ ] Logo displays correctly on homepage
- [ ] Logo displays correctly in header
- [ ] Logo displays correctly in footer
- [ ] Logo displays correctly on mobile
- [ ] Logo file size is optimized (<50KB)
- [ ] Colors match your brand
- [ ] Alt text is descriptive
- [ ] Print version includes logo

---

**Your logo represents your brand. Make sure it looks professional!** ???
