# FSO Logo Instructions

## How to Add Your FSO Logo

To complete the modernized UI, you need to add the FSO logo image file to your project.

### Steps:

1. **Get the FSO logo image file** (preferably in PNG format with a transparent background)
   - Recommended size: 300x300 pixels or higher
   - Supported formats: PNG, SVG, JPG

2. **Add the logo to your project:**
   - Place the logo file in the `frontend/public/` directory
   - Rename it to `fso-logo.png` (or update the path in App.jsx if you use a different name)

3. **File location should be:**
   ```
   frontend/public/fso-logo.png
   ```

### Alternative: If you don't have a logo yet

The app includes a fallback design that displays "FSO" in a circular gradient badge if the logo image is not found. This will work automatically until you add your actual logo.

### Using a different filename or format?

If you want to use a different filename or format, update line 50 in `frontend/src/App.jsx`:

```jsx
<img 
  src="/your-logo-name.png"  // Change this line
  alt="FSO Logo" 
  className="fso-logo"
/>
```

### Tips for best results:
- Use a transparent background (PNG format)
- Keep the aspect ratio square or landscape
- The logo will automatically scale to 80px height on desktop and 60px on mobile
- Ensure good contrast with the white header background
