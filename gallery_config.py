# gallery_config.py
# Configuration file for the Enhanced Minecraft Gallery Generator

# Basic Settings
GALLERY_TITLE = "🎮 Minecraft Server Gallery"
GALLERY_DESCRIPTION = "Minecraft server screenshots, builds, and events gallery"
SERVER_NAME = "Your Server Name"  # Change this to your server name

# Performance Settings
IMAGES_PER_PAGE = 20  # Recommended: 15-25 for optimal loading
THUMBNAIL_WIDTH = 400  # Recommended: 300-500px
THUMBNAIL_HEIGHT = 300
WEBP_QUALITY = 85  # Recommended: 80-90 for good quality/size balance

# Auto-tagging Categories
# Add or remove categories based on your server's content
AVAILABLE_TAGS = [
    "builds",      # Player creations and structures
    "redstone",    # Redstone contraptions and mechanisms
    "landscape",   # Natural scenery and terrain
    "event",       # Server events and gatherings
    "pvp",         # Player vs Player content
    "farming",     # Agricultural builds and farms
    "mining",      # Underground and mining related
    "nether",      # Nether dimension content
    "end",         # End dimension content
    "village",     # Village builds and NPCs
    "castle",      # Castle and fortress builds
    "modern",      # Modern architectural style
    "medieval",    # Medieval architectural style
    "spawn",       # Spawn area screenshots
    "town",        # Town and city builds
    "port",        # Harbor and port builds
    "bridge",      # Bridge constructions
    "tower",       # Tower builds
    "underground", # Underground bases
    "sky",         # Sky builds and floating structures
]

# Color Theme (Minecraft-inspired)
THEME_COLORS = {
    "dirt": "#8B4513",      # Brown dirt color
    "stone": "#7F7F7F",     # Gray stone color
    "grass": "#7CB342",     # Green grass color
    "dark": "#2E2E2E",      # Dark background
    "light": "#F5F5F5",     # Light text
    "blue": "#4FC3F7",      # Water blue
    "gold": "#FFD700",      # Gold accent
    "diamond": "#4DD0E1",   # Diamond blue
    "emerald": "#66BB6A",   # Emerald green
    "redstone": "#DC143C",  # Redstone red
}

# GitHub Pages Optimization
ENABLE_LAZY_LOADING = True
GENERATE_WEBP_THUMBNAILS = True
INCLUDE_HTACCESS = True
OPTIMIZE_FOR_MOBILE = True

# Advanced Settings
AUTO_SLIDESHOW_INTERVAL = 3000  # Milliseconds between slides
ENABLE_KEYBOARD_NAVIGATION = True
SHOW_IMAGE_COUNT = True
ENABLE_FILTERING = True

# Custom CSS Additions (optional)
CUSTOM_CSS = """
/* Add your custom CSS here */
/* Example: Custom animation for image cards */
.image-card {
    animation: fadeInUp 0.5s ease-out;
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Custom hover effects */
.thumbnail:hover {
    filter: brightness(1.1) contrast(1.05);
}
"""

# File Naming Conventions Help
FILENAME_EXAMPLES = [
    "castle_build_2024_01_15_morning.png",
    "redstone_elevator_mechanism.jpg", 
    "nether_fortress_exploration.png",
    "medieval_village_overview.jpg",
    "modern_skyscraper_downtown.png",
    "farming_automatic_wheat.jpg"
]

# Supported Image Formats
SUPPORTED_FORMATS = ['.jpg', '.jpeg', '.png', '.gif', '.webp']

# Social Media Integration (optional)
ENABLE_SOCIAL_SHARING = False
SOCIAL_TITLE = f"{SERVER_NAME} - Minecraft Gallery"
SOCIAL_DESCRIPTION = "Check out our amazing Minecraft builds and adventures!"

# Analytics (optional - add your tracking ID)
GOOGLE_ANALYTICS_ID = ""  # Example: "GA_MEASUREMENT_ID"

# Custom Footer Text
FOOTER_TEXT = f"Built with ❤️ for {SERVER_NAME} | Powered by Enhanced Minecraft Gallery Generator"

# Development Settings
DEBUG_MODE = False
VERBOSE_LOGGING = True

print("📝 Configuration loaded successfully!")
print(f"🏷️  Available tags: {len(AVAILABLE_TAGS)} categories")
print(f"⚙️  Images per page: {IMAGES_PER_PAGE}")
print(f"🖼️  Thumbnail size: {THUMBNAIL_WIDTH}x{THUMBNAIL_HEIGHT}")
print(f"💎 Theme: Minecraft-inspired with {len(THEME_COLORS)} colors")
