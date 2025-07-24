#!/bin/bash
set -e  # Exit on any error

# Configuration
OUTPUT_DIR=${GALLERY_OUTPUT_FOLDER:-"gallery-output"}
IMAGES_DIR="images"

echo "🚀 Building Minecraft Gallery..."
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

# Set environment variable for Python scripts
export GALLERY_OUTPUT_FOLDER="$OUTPUT_DIR"

echo "🔧 Fixing image filenames..."
python3 convert_images.py

echo "🏗️  Building static gallery..."
python3 generate_gallery.py

# Copy additional resources to output directory
if [ -d "thumbnails" ]; then
    echo "📁 Copying thumbnails..."
    cp -r thumbnails "$OUTPUT_DIR/"
fi

if [ -d "$IMAGES_DIR" ]; then
    echo "📁 Copying images..."
    cp -r "$IMAGES_DIR" "$OUTPUT_DIR/"
fi

# Create a simple README for the output
cat > "$OUTPUT_DIR/README.md" << EOF
# Minecraft Gallery

This is an automatically generated gallery containing $IMAGE_COUNT Minecraft screenshots.

- **Generated on:** $(date)
- **Total images:** $IMAGE_COUNT
- **Pages:** Generated dynamically based on image count

## Files:
- \`index.html\` - Main gallery page
- \`index2.html\`, \`index3.html\`, etc. - Additional pages if needed
- \`images/\` - Original images
- \`thumbnails/\` - Optimized thumbnails

Open \`index.html\` in your browser to view the gallery.
EOF

echo "✅ Gallery built successfully in '$OUTPUT_DIR'!"
echo "🌐 Open $OUTPUT_DIR/index.html in your browser to view the gallery"
