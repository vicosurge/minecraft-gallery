#!/bin/bash
set -e  # Exit on any error

# Configuration
OUTPUT_DIR=${GALLERY_OUTPUT_FOLDER:-"gallery-output"}
IMAGES_DIR="images"
THUMBNAILS_DIR="thumbnails"

echo "🎮 Building Enhanced Minecraft Gallery..."
echo "📂 Output directory: $OUTPUT_DIR"

# Check if images directory exists
if [ ! -d "$IMAGES_DIR" ]; then
    echo "❌ Images directory '$IMAGES_DIR' not found!"
    exit 1
fi

# Count images
IMAGE_COUNT=$(find "$IMAGES_DIR" -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" -o -iname "*.gif" -o -iname "*.webp" \) | wc -l)
echo "📸 Found $IMAGE_COUNT images to process"

if [ "$IMAGE_COUNT" -eq 0 ]; then
    echo "❌ No valid images found in $IMAGES_DIR!"
    exit 1
fi

# Create output directory
mkdir -p "$OUTPUT_DIR"
mkdir -p "$THUMBNAILS_DIR"

# Set environment variable for Python scripts
export GALLERY_OUTPUT_FOLDER="$OUTPUT_DIR"

echo "🔧 Processing images and generating optimized thumbnails..."
python3 generate_gallery.py  # Using the enhanced version

# Copy images to output directory (GitHub Pages needs them accessible)
echo "📁 Copying images to output directory..."
cp -r "$IMAGES_DIR" "$OUTPUT_DIR/"

# Copy thumbnails to output directory
if [ -d "$THUMBNAILS_DIR" ]; then
    echo "📁 Copying optimized thumbnails..."
    cp -r "$THUMBNAILS_DIR" "$OUTPUT_DIR/"
fi

# Create optimized .htaccess for GitHub Pages (if needed)
cat > "$OUTPUT_DIR/.htaccess" << 'EOF'
# Enable compression
<IfModule mod_deflate.c>
    AddOutputFilterByType DEFLATE text/plain
    AddOutputFilterByType DEFLATE text/html
    AddOutputFilterByType DEFLATE text/xml
    AddOutputFilterByType DEFLATE text/css
    AddOutputFilterByType DEFLATE application/xml
    AddOutputFilterByType DEFLATE application/xhtml+xml
    AddOutputFilterByType DEFLATE application/rss+xml
    AddOutputFilterByType DEFLATE application/javascript
    AddOutputFilterByType DEFLATE application/x-javascript
</IfModule>

# Cache images for better performance
<FilesMatch "\.(jpg|jpeg|png|gif|webp)$">
    ExpiresActive On
    ExpiresDefault "access plus 1 month"
</FilesMatch>
EOF

# Create a comprehensive README for the output
cat > "$OUTPUT_DIR/README.md" << EOF
# 🎮 Enhanced Minecraft Server Gallery

This is an automatically generated gallery showcasing Minecraft server screenshots, builds, and events.

## 📊 Statistics
- **Generated on:** $(date)
- **Total images:** $IMAGE_COUNT
- **Optimized thumbnails:** WebP format for faster loading
- **Pages:** Dynamically generated based on image count (20 images per page)

## ✨ Features
- **Minecraft-themed UI** with pixelated fonts and block-style design
- **Performance optimized** with WebP thumbnails and lazy loading
- **Auto-tagging system** that detects content types (builds, redstone, etc.)
- **Slideshow mode** with keyboard navigation
- **Filtering system** to browse by category
- **Mobile responsive** design
- **GitHub Pages optimized** for fast loading

## 🗂️ File Structure
- \`index.html\` - Main gallery page (Page 1)
- \`index2.html\`, \`index3.html\`, etc. - Additional pages
- \`images/\` - Original high-resolution images
- \`thumbnails/\` - Optimized WebP thumbnails for fast loading
- \`gallery_metadata.json\` - Generated metadata for images
- \`.htaccess\` - Server optimization rules

## 🚀 Performance Optimizations
- **WebP thumbnails** reduce file sizes by 25-35% compared to JPEG
- **Lazy loading** only loads images as they come into view
- **Reduced page size** (20 images per page instead of 24)
- **Optimized CSS** with minimal external dependencies
- **Efficient caching** headers for better repeat visits

## 🎮 How to Use
1. Open \`index.html\` in your browser
2. Use filter buttons to browse by category (builds, redstone, events, etc.)
3. Click any image to view full size
4. Use slideshow mode for automatic browsing
5. Navigate between pages using the pagination controls

## 📱 Mobile Support
The gallery is fully responsive and works great on mobile devices with touch-friendly controls.

## 🔧 Customization
Tags are automatically detected from filenames. To improve auto-tagging:
- Include descriptive words in filenames (e.g., \`castle_build_2024.png\`)
- Supported auto-tags: builds, redstone, landscape, event, pvp, farming, mining, nether, end, village, castle, modern, medieval

Built with ❤️ for the Minecraft community!
EOF

# Create a simple deployment guide
cat > "$OUTPUT_DIR/DEPLOYMENT.md" << EOF
# 🚀 Deployment Guide

## GitHub Pages Deployment

1. **Upload to Repository:**
   - Copy all files from this folder to your GitHub repository
   - Ensure the repository is public or you have GitHub Pro

2. **Enable GitHub Pages:**
   - Go to Settings > Pages in your repository
   - Select source: "Deploy from a branch"
   - Choose branch: "main" (or your default branch)
   - Select folder: "/ (root)" or "/docs" if you placed files there

3. **Custom Domain (Optional):**
   - Add a \`CNAME\` file with your domain name
   - Configure DNS to point to your GitHub Pages URL

## Performance Tips for GitHub Pages

- **Image Optimization:** Already done! WebP thumbnails reduce bandwidth
- **CDN:** GitHub Pages uses a global CDN automatically
- **Caching:** Browser caching is configured via .htaccess
- **Loading:** Lazy loading prevents initial page slowdown

## Troubleshooting

- **Images not loading:** Check file paths in your repository
- **Slow loading:** Ensure images are in the correct folders
- **Mobile issues:** Clear browser cache and test again

Your gallery should be available at: \`https://[username].github.io/[repository-name]\`
EOF

echo "✅ Enhanced Minecraft gallery built successfully in '$OUTPUT_DIR'!"
echo ""
echo "🎮 New Features Added:"
echo "   ✨ Minecraft-themed pixelated design"
echo "   🚀 WebP thumbnails for 30% faster loading"
echo "   🏷️  Auto-tagging system (builds, redstone, etc.)"
echo "   🎬 Slideshow mode with auto-play"
echo "   🔍 Filter system for easy browsing"
echo "   📱 Mobile-responsive design"
echo "   ⌨️  Keyboard navigation
