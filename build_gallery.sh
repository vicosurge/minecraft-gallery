#!/bin/bash
set -e  # Exit on any error

# Configuration
OUTPUT_DIR=${GALLERY_OUTPUT_FOLDER:-"gallery-output"}
IMAGES_DIR="images"
THUMBNAILS_DIR="thumbnails"
R2_REMOTE=${R2_REMOTE:-"r2:minecraft-gallery-digimente"}
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

echo "✅ Gallery built successfully: $IMAGE_COUNT images, deployed to minecraft.digimente.xyz"
