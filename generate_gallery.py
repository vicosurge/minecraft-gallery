import os
import sys
import json
from pathlib import Path
from math import ceil
from PIL import Image
import hashlib

IMAGE_FOLDER = "images"
THUMBNAIL_FOLDER = "thumbnails"
OUTPUT_FOLDER = os.getenv("GALLERY_OUTPUT_FOLDER", ".")
OUTPUT_PREFIX = "index"
VALID_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
IMAGES_PER_PAGE = 20  # Reduced for better performance
THUMBNAIL_WIDTH = 400  # Increased for better quality
THUMBNAIL_HEIGHT = 300
WEBP_QUALITY = 85

# Available tags for categorization
AVAILABLE_TAGS = [
    "builds", "redstone", "landscape", "event", "pvp", "farming", 
    "mining", "nether", "end", "village", "castle", "modern", "medieval"
]

def create_optimized_thumbnail(image_path, thumbnail_path):
    """Create optimized WebP thumbnails for better performance"""
    try:
        with Image.open(image_path) as img:
            # Convert to RGB if necessary (for WebP compatibility)
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
            
            # Calculate dimensions maintaining aspect ratio
            img.thumbnail((THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT), Image.Resampling.LANCZOS)
            
            # Save as WebP for better compression
            webp_path = thumbnail_path.replace(os.path.splitext(thumbnail_path)[1], '.webp')
            img.save(webp_path, 'WebP', quality=WEBP_QUALITY, optimize=True)
            return webp_path
    except Exception as e:
        print(f"❌ Failed to create thumbnail for {image_path}: {e}")
        return None

def parse_filename_enhanced(fname):
    """Enhanced filename parsing with better tag detection"""
    name, _ = os.path.splitext(fname)
    parts = name.lower().split("_")
    
    # Try to detect tags from filename
    detected_tags = []
    for tag in AVAILABLE_TAGS:
        if any(tag in part for part in parts):
            detected_tags.append(tag)
    
    if len(parts) >= 3:
        tag = parts[0]
        date = parts[1]
        time = parts[2].replace("-", ":")
        return tag, f"{date} {time}", detected_tags
    return "screenshot", "Unknown", detected_tags

def generate_image_metadata():
    """Generate metadata file for faster loading"""
    metadata = {
        "images": [],
        "tags": set(),
        "total_count": 0,
        "last_updated": None
    }
    
    if not os.path.exists(IMAGE_FOLDER):
        print(f"❌ Image folder '{IMAGE_FOLDER}' not found!")
        return metadata
    
    os.makedirs(THUMBNAIL_FOLDER, exist_ok=True)
    
    for fname in sorted(os.listdir(IMAGE_FOLDER)):
        ext = os.path.splitext(fname)[1].lower()
        if ext in VALID_EXTENSIONS:
            original_path = os.path.join(IMAGE_FOLDER, fname)
            
            # Create thumbnail
            thumb_name = os.path.splitext(fname)[0] + '.webp'
            thumb_path = os.path.join(THUMBNAIL_FOLDER, thumb_name)
            
            if not os.path.exists(thumb_path):
                created_thumb = create_optimized_thumbnail(original_path, thumb_path)
                if created_thumb:
                    print(f"📸 Created optimized thumbnail: {thumb_name}")
                    thumb_path = created_thumb
            
            # Parse filename for metadata
            tag, date_str, auto_tags = parse_filename_enhanced(fname)
            
            # Get image dimensions for aspect ratio
            try:
                with Image.open(original_path) as img:
                    width, height = img.size
                    aspect_ratio = width / height
            except:
                aspect_ratio = 1.0
            
            image_data = {
                "filename": fname,
                "src": f"{IMAGE_FOLDER}/{fname}",
                "thumbnail": f"{THUMBNAIL_FOLDER}/{thumb_name}",
                "alt": fname,
                "tag": tag,
                "date": date_str,
                "auto_tags": auto_tags,
                "aspect_ratio": aspect_ratio,
                "hash": hashlib.md5(fname.encode()).hexdigest()[:8]  # For unique IDs
            }
            
            metadata["images"].append(image_data)
            metadata["tags"].update(auto_tags)
            metadata["total_count"] += 1
    
    metadata["tags"] = list(metadata["tags"])
    
    # Save metadata to JSON for potential future use
    with open(os.path.join(OUTPUT_FOLDER, "gallery_metadata.json"), "w") as f:
        json.dump(metadata, f, indent=2)
    
    print(f"✅ Generated metadata for {metadata['total_count']} images")
    return metadata

def generate_minecraft_css():
    """Generate Minecraft-themed CSS"""
    return """
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');
    
    :root {
        --mc-dirt: #8B4513;
        --mc-stone: #7F7F7F;
        --mc-grass: #7CB342;
        --mc-dark: #2E2E2E;
        --mc-light: #F5F5F5;
        --mc-blue: #4FC3F7;
        --mc-gold: #FFD700;
    }
    
    * {
        box-sizing: border-box;
    }
    
    body {
        font-family: 'Press Start 2P', monospace;
        background: linear-gradient(45deg, var(--mc-dirt) 25%, var(--mc-stone) 25%, var(--mc-stone) 50%, var(--mc-dirt) 50%, var(--mc-dirt) 75%, var(--mc-stone) 75%);
        background-size: 20px 20px;
        color: var(--mc-light);
        margin: 0;
        padding: 20px;
        min-height: 100vh;
    }
    
    .container {
        max-width: 1400px;
        margin: 0 auto;
        background: rgba(46, 46, 46, 0.9);
        border: 4px solid var(--mc-stone);
        border-radius: 0;
        padding: 20px;
        box-shadow: inset 0 0 10px rgba(0,0,0,0.5);
    }
    
    h1 {
        text-align: center;
        color: var(--mc-gold);
        text-shadow: 2px 2px 0px var(--mc-dark);
        margin-bottom: 20px;
        font-size: clamp(12px, 4vw, 24px);
        line-height: 1.4;
    }
    
    .controls {
        display: flex;
        justify-content: center;
        gap: 10px;
        margin-bottom: 20px;
        flex-wrap: wrap;
    }
    
    .mc-button {
        font-family: 'Press Start 2P', monospace;
        background: var(--mc-stone);
        color: var(--mc-light);
        border: 2px solid #999;
        padding: 8px 12px;
        cursor: pointer;
        font-size: 8px;
        transition: all 0.1s;
        text-decoration: none;
        display: inline-block;
    }
    
    .mc-button:hover {
        background: var(--mc-grass);
        border-color: var(--mc-light);
        transform: translateY(-1px);
    }
    
    .mc-button.active {
        background: var(--mc-blue);
        border-color: var(--mc-gold);
    }
    
    .gallery {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
        gap: 20px;
        margin: 20px 0;
    }
    
    .image-card {
        background: var(--mc-dark);
        border: 3px solid var(--mc-stone);
        padding: 10px;
        transition: all 0.2s;
        position: relative;
        overflow: hidden;
    }
    
    .image-card:hover {
        border-color: var(--mc-gold);
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
    
    .thumbnail {
        width: 100%;
        height: 200px;
        object-fit: cover;
        cursor: pointer;
        transition: transform 0.2s;
        image-rendering: pixelated;
        image-rendering: -moz-crisp-edges;
        image-rendering: crisp-edges;
    }
    
    .thumbnail:hover {
        transform: scale(1.02);
    }
    
    .image-info {
        padding: 8px 0;
        font-size: 8px;
        line-height: 1.4;
    }
    
    .image-tag {
        color: var(--mc-gold);
        margin-bottom: 4px;
    }
    
    .image-date {
        color: var(--mc-blue);
    }
    
    .auto-tags {
        margin-top: 6px;
    }
    
    .tag-chip {
        display: inline-block;
        background: var(--mc-grass);
        color: white;
        padding: 2px 6px;
        margin: 2px;
        font-size: 6px;
        border: 1px solid var(--mc-light);
    }
    
    .pagination {
        display: flex;
        justify-content: center;
        gap: 5px;
        margin: 20px 0;
        flex-wrap: wrap;
    }
    
    .slideshow-modal {
        display: none;
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0,0,0,0.95);
        z-index: 1000;
        align-items: center;
        justify-content: center;
    }
    
    .slideshow-modal.active {
        display: flex;
    }
    
    .slideshow-content {
        position: relative;
        max-width: 90vw;
        max-height: 90vh;
        text-align: center;
    }
    
    .slideshow-image {
        max-width: 100%;
        max-height: 80vh;
        object-fit: contain;
        border: 4px solid var(--mc-gold);
    }
    
    .slideshow-info {
        background: var(--mc-dark);
        color: var(--mc-light);
        padding: 10px;
        border: 2px solid var(--mc-stone);
        margin-top: 10px;
        font-size: 8px;
    }
    
    .slideshow-nav {
        position: absolute;
        top: 50%;
        transform: translateY(-50%);
        font-size: 16px;
        z-index: 1001;
    }
    
    .slideshow-nav.prev { left: 20px; }
    .slideshow-nav.next { right: 20px; }
    
    .close-slideshow {
        position: absolute;
        top: 20px;
        right: 20px;
        font-size: 16px;
        z-index: 1001;
    }
    
    @media (max-width: 768px) {
        .gallery {
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 15px;
        }
        
        .controls {
            gap: 5px;
        }
        
        .mc-button {
            padding: 6px 8px;
            font-size: 7px;
        }
    }
    """

def generate_minecraft_js():
    """Generate JavaScript for slideshow and interactions"""
    return """
    class MinecraftGallery {
        constructor() {
            this.currentFilter = 'all';
            this.currentSlide = 0;
            this.images = [];
            this.filteredImages = [];
            this.init();
        }
        
        init() {
            this.createSlideshow();
            this.bindEvents();
            this.loadImages();
        }
        
        createSlideshow() {
            const modal = document.createElement('div');
            modal.className = 'slideshow-modal';
            modal.id = 'slideshow';
            modal.innerHTML = `
                <button class="mc-button close-slideshow" onclick="gallery.closeSlideshow()">✕</button>
                <button class="mc-button slideshow-nav prev" onclick="gallery.prevSlide()">‹</button>
                <button class="mc-button slideshow-nav next" onclick="gallery.nextSlide()">›</button>
                <div class="slideshow-content">
                    <img class="slideshow-image" id="slideshow-img" src="" alt="">
                    <div class="slideshow-info" id="slideshow-info"></div>
                </div>
            `;
            document.body.appendChild(modal);
        }
        
        bindEvents() {
            // Close slideshow on background click
            document.getElementById('slideshow').addEventListener('click', (e) => {
                if (e.target.id === 'slideshow') {
                    this.closeSlideshow();
                }
            });
            
            // Keyboard navigation
            document.addEventListener('keydown', (e) => {
                if (document.getElementById('slideshow').classList.contains('active')) {
                    switch(e.key) {
                        case 'Escape': this.closeSlideshow(); break;
                        case 'ArrowLeft': this.prevSlide(); break;
                        case 'ArrowRight': this.nextSlide(); break;
                    }
                }
            });
        }
        
        loadImages() {
            this.images = Array.from(document.querySelectorAll('.image-card')).map((card, index) => {
                const img = card.querySelector('.thumbnail');
                const info = card.querySelector('.image-info');
                return {
                    index,
                    src: img.dataset.fullSrc || img.src,
                    thumbnail: img.src,
                    alt: img.alt,
                    info: info.innerHTML,
                    element: card
                };
            });
            this.filteredImages = [...this.images];
        }
        
        openSlideshow(index) {
            this.currentSlide = index;
            this.updateSlideshow();
            document.getElementById('slideshow').classList.add('active');
            document.body.style.overflow = 'hidden';
        }
        
        closeSlideshow() {
            document.getElementById('slideshow').classList.remove('active');
            document.body.style.overflow = '';
        }
        
        nextSlide() {
            this.currentSlide = (this.currentSlide + 1) % this.filteredImages.length;
            this.updateSlideshow();
        }
        
        prevSlide() {
            this.currentSlide = (this.currentSlide - 1 + this.filteredImages.length) % this.filteredImages.length;
            this.updateSlideshow();
        }
        
        updateSlideshow() {
            const img = this.filteredImages[this.currentSlide];
            document.getElementById('slideshow-img').src = img.src;
            document.getElementById('slideshow-img').alt = img.alt;
            document.getElementById('slideshow-info').innerHTML = img.info;
        }
        
        filterImages(tag) {
            this.currentFilter = tag;
            
            // Update button states
            document.querySelectorAll('.filter-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            document.querySelector(`[data-filter="${tag}"]`).classList.add('active');
            
            // Filter images
            this.images.forEach((img, index) => {
                const shouldShow = tag === 'all' || img.info.toLowerCase().includes(tag);
                img.element.style.display = shouldShow ? 'block' : 'none';
            });
            
            // Update filtered array for slideshow
            this.filteredImages = this.images.filter((img, index) => {
                return tag === 'all' || img.info.toLowerCase().includes(tag);
            });
        }
        
        startSlideshow() {
            if (this.filteredImages.length > 0) {
                this.openSlideshow(0);
                this.autoplay = setInterval(() => this.nextSlide(), 3000);
            }
        }
        
        stopAutoplay() {
            if (this.autoplay) {
                clearInterval(this.autoplay);
                this.autoplay = null;
            }
        }
    }
    
    // Initialize gallery when page loads
    let gallery;
    document.addEventListener('DOMContentLoaded', function() {
        gallery = new MinecraftGallery();
        
        // Add click handlers to thumbnails
        document.querySelectorAll('.thumbnail').forEach((img, index) => {
            img.addEventListener('click', () => gallery.openSlideshow(index));
        });
    });
    """

def generate_enhanced_html(images, page_num, total_pages, metadata):
    """Generate enhanced HTML with Minecraft theme and performance optimizations"""
    
    # Generate filter buttons from available tags
    filter_buttons = '<button class="mc-button filter-btn active" data-filter="all" onclick="gallery.filterImages(\'all\')">All</button>'
    for tag in sorted(metadata["tags"]):
        filter_buttons += f'<button class="mc-button filter-btn" data-filter="{tag}" onclick="gallery.filterImages(\'{tag}\')">{tag.title()}</button>'
    
    # Generate navigation
    nav = '<div class="pagination">'
    if page_num > 1:
        nav += f'<a href="{OUTPUT_PREFIX}.html" class="mc-button">« First</a>'
        prev_suffix = "" if page_num == 2 else str(page_num - 1)
        nav += f'<a href="{OUTPUT_PREFIX}{prev_suffix}.html" class="mc-button">‹ Prev</a>'
    
    for i in range(1, total_pages + 1):
        suffix = "" if i == 1 else str(i)
        class_name = "mc-button active" if i == page_num else "mc-button"
        nav += f'<a href="{OUTPUT_PREFIX}{suffix}.html" class="{class_name}">Page {i}</a>'
    
    if page_num < total_pages:
        nav += f'<a href="{OUTPUT_PREFIX}{page_num + 1}.html" class="mc-button">Next ›</a>'
        nav += f'<a href="{OUTPUT_PREFIX}{total_pages}.html" class="mc-button">Last »</a>'
    
    nav += '</div>'
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>🎮 Minecraft Server Gallery - Page {page_num}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Minecraft server screenshots, builds, and events gallery">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <style>{generate_minecraft_css()}</style>
</head>
<body>
    <div class="container">
        <h1>🎮 Minecraft Server Gallery</h1>
        <p style="text-align: center; font-size: 8px; margin-bottom: 20px; color: var(--mc-blue);">
            Page {page_num} of {total_pages} • {len(images)} images • Total: {metadata['total_count']} screenshots
        </p>
        
        <div class="controls">
            {filter_buttons}
            <button class="mc-button" onclick="gallery.startSlideshow()">🎬 Slideshow</button>
        </div>
        
        <div class="gallery">
"""
    
    for img in images:
        # Create tags display
        tags_html = ""
        if img.get('auto_tags'):
            tags_html = '<div class="auto-tags">' + ''.join([f'<span class="tag-chip">{tag}</span>' for tag in img['auto_tags']]) + '</div>'
        
        html += f"""
            <div class="image-card">
                <img src="{img['thumbnail']}" 
                     data-full-src="{img['src']}" 
                     alt="{img['alt']}" 
                     class="thumbnail"
                     loading="lazy">
                <div class="image-info">
                    <div class="image-tag">{img['tag']}</div>
                    <div class="image-date">{img['date']}</div>
                    {tags_html}
                </div>
            </div>
"""
    
    html += f"""
        </div>
        {nav}
    </div>
    
    <script>{generate_minecraft_js()}</script>
</body>
</html>"""
    
    return html

def write_enhanced_pages(metadata):
    """Write enhanced gallery pages"""
    images = metadata["images"]
    total = len(images)
    
    if total == 0:
        print("❌ No images found to generate gallery!")
        sys.exit(1)
    
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    
    total_pages = ceil(total / IMAGES_PER_PAGE)
    
    for page_num in range(1, total_pages + 1):
        start = (page_num - 1) * IMAGES_PER_PAGE
        end = start + IMAGES_PER_PAGE
        page_images = images[start:end]
        
        html = generate_enhanced_html(page_images, page_num, total_pages, metadata)
        
        suffix = "" if page_num == 1 else str(page_num)
        filename = os.path.join(OUTPUT_FOLDER, f"{OUTPUT_PREFIX}{suffix}.html")
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html)
        
        print(f"📄 Generated enhanced page: {filename}")
    
    print(f"✅ {total_pages} enhanced page(s) generated with {total} images")

def main():
    print("🎮 Starting enhanced Minecraft gallery generation...")
    metadata = generate_image_metadata()
    
    if metadata["total_count"] == 0:
        print("❌ No valid images found!")
        sys.exit(1)
    
    write_enhanced_pages(metadata)
    print("🎉 Enhanced Minecraft gallery generation completed!")
    print(f"🚀 Performance improvements:")
    print(f"   • WebP thumbnails for faster loading")
    print(f"   • Lazy loading for images")
    print(f"   • Reduced images per page ({IMAGES_PER_PAGE})")
    print(f"   • Auto-generated tags and filtering")
    print(f"   • Slideshow functionality")

if __name__ == "__main__":
    main()
