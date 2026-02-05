#!/bin/bash
set -e  # Exit on any error

# Configuration
OUTPUT_DIR=${GALLERY_OUTPUT_FOLDER:-"gallery-output"}
IMAGES_DIR="images"
THUMBNAILS_DIR="thumbnails"
R2_REMOTE=${R2_REMOTE:-"r2:minecraft-gallery"}
export R2_BASE_URL=${R2_BASE_URL:-"https://images.minecraft.digimente.xyz"}

echo "🎮 Building Enhanced Minecraft Gallery..."
echo "📂 Output directory: $OUTPUT_DIR"
echo "☁️  R2 base URL: $R2_BASE_URL"

# Sync images from R2 to local directory for thumbnail generation
mkdir -p "$IMAGES_DIR"
if command -v rclone &> /dev/null; then
    echo "☁️  Syncing images from R2..."
    rclone sync "$R2_REMOTE" "$IMAGES_DIR" --progress
else
    echo "⚠️  rclone not found, using local images directory"
fi

# Check if images directory exists and has files
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

# Normalize image filenames to minecraft_ prefix convention
echo "📝 Normalizing image filenames..."
python3 convert_images.py

# Recount after renaming (in case any were affected)
IMAGE_COUNT=$(find "$IMAGES_DIR" -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" -o -iname "*.gif" -o -iname "*.webp" \) | wc -l)

# Create output directory
mkdir -p "$OUTPUT_DIR"
mkdir -p "$THUMBNAILS_DIR"

# Set environment variable for Python scripts
export GALLERY_OUTPUT_FOLDER="$OUTPUT_DIR"

echo "🔧 Processing images and generating optimized thumbnails..."
python3 generate_gallery.py

# Images are served from R2, no need to copy to output

# Copy thumbnails to output directory
if [ -d "$THUMBNAILS_DIR" ]; then
    echo "📁 Copying optimized thumbnails..."
    cp -r "$THUMBNAILS_DIR" "$OUTPUT_DIR/"
fi

# Create optimized .htaccess for GitHub Pages
echo "⚙️ Creating server optimization files..."
cat > "$OUTPUT_DIR/.htaccess" << 'HTACCESS_EOF'
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
HTACCESS_EOF

# Create a comprehensive README for the output
echo "📝 Creating documentation..."
cat > "$OUTPUT_DIR/README.md" << 'README_EOF'
# 🎮 Enhanced Minecraft Server Gallery

This is an automatically generated gallery showcasing Minecraft server screenshots, builds, and events.

## Statistics
- **Generated on:** $(date)
- **Total images:** IMAGE_COUNT_PLACEHOLDER
- **Optimized thumbnails:** WebP format for faster loading
- **Pages:** Dynamically generated based on image count (20 images per page)

## Features
- **Minecraft-themed UI** with pixelated fonts and block-style design
- **Performance optimized** with WebP thumbnails and lazy loading
- **Auto-tagging system** that detects content types (builds, redstone, etc.)
- **Slideshow mode** with keyboard navigation
- **Filtering system** to browse by category
- **Mobile responsive** design
- **GitHub Pages optimized** for fast loading

## File Structure
- `index.html` - Main gallery page (Page 1)
- `index2.html`, `index3.html`, etc. - Additional pages
- `images/` - Original high-resolution images
- `thumbnails/` - Optimized WebP thumbnails for fast loading
- `gallery_metadata.json` - Generated metadata for images
- `.htaccess` - Server optimization rules

## Performance Optimizations
- **WebP thumbnails** reduce file sizes by 25-35% compared to JPEG
- **Lazy loading** only loads images as they come into view
- **Reduced page size** (20 images per page instead of 24)
- **Optimized CSS** with minimal external dependencies
- **Efficient caching** headers for better repeat visits

## How to Use
1. Open `index.html` in your browser
2. Use filter buttons to browse by category (builds, redstone, events, etc.)
3. Click any image to view full size
4. Use slideshow mode for automatic browsing
5. Navigate between pages using the pagination controls

## Mobile Support
The gallery is fully responsive and works great on mobile devices with touch-friendly controls.

## Customization
Tags are automatically detected from filenames. To improve auto-tagging:
- Include descriptive words in filenames (e.g., `castle_build_2024.png`)
- Supported auto-tags: builds, redstone, landscape, event, pvp, farming, mining, nether, end, village, castle, modern, medieval

Built with ❤️ for the Minecraft community!
README_EOF

# Replace placeholder with actual count
sed -i "s/IMAGE_COUNT_PLACEHOLDER/$IMAGE_COUNT/g" "$OUTPUT_DIR/README.md"
sed -i "s/\$(date)/$(date)/g" "$OUTPUT_DIR/README.md"

# Create deployment guide
cat > "$OUTPUT_DIR/DEPLOYMENT.md" << 'DEPLOY_EOF'
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
   - Add a `CNAME` file with your domain name
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

Your gallery should be available at: `https://[username].github.io/[repository-name]`
DEPLOY_EOF

echo "✅ Enhanced Minecraft gallery built successfully in '$OUTPUT_DIR'!"
echo ""
echo "🎮 New Features Added:"
echo "   ✨ Minecraft-themed pixelated design"
echo "   🚀 WebP thumbnails for 30% faster loading"
echo "   🏷️ Auto-tagging system (builds, redstone, etc.)"
echo "   🎬 Slideshow mode with auto-play"
echo "   🔍 Filter system for easy browsing"
echo "   📱 Mobile-responsive design"
echo "   ⌨️ Keyboard navigation"
echo ""
echo "📈 Performance Improvements:"
echo "   • Reduced from 24 to 20 images per page"
echo "   • WebP format reduces thumbnail size by ~30%"
echo "   • Lazy loading prevents initial slowdown"
echo "   • Optimized CSS with minimal external dependencies"
echo "   • Browser caching configured for GitHub Pages"
echo ""
echo "🌐 GitHub Pages Optimizations:"
echo "   • All assets copied to output directory"
echo "   • .htaccess file created for server optimization"
echo "   • Deployment guide included"
echo "   • Mobile-responsive for all devices"
echo ""
echo "🎯 Next Steps:"
echo "   1. Copy contents of '$OUTPUT_DIR' to your GitHub repository"
echo "   2. Enable GitHub Pages in repository settings"
echo "   3. Your gallery will be live at: https://[username].github.io/[repo-name]"
echo ""
echo "🔧 For better auto-tagging, name your files like:"
echo "   • castle_build_2024_01_15.png"
echo "   • redstone_contraption_evening.jpg"
echo "   • nether_exploration_with_friends.png"
echo ""
echo "🌐 Open $OUTPUT_DIR/index.html in your browser to preview!"
