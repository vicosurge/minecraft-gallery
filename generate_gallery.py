import os
from pathlib import Path
from math import ceil
from PIL import Image

IMAGE_FOLDER = "images"
THUMBNAIL_FOLDER = "thumbnails"
OUTPUT_FOLDER = "."
OUTPUT_PREFIX = "index"
VALID_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
IMAGES_PER_PAGE = 24
THUMBNAIL_WIDTH = 300

def parse_filename(fname):
    name, _ = os.path.splitext(fname)
    parts = name.split("_")
    if len(parts) >= 3:
        tag = parts[0]
        date = parts[1]
        time = parts[2].replace("-", ":")
        return tag, f"{date} {time}"
    return "Unknown", "Unknown"

def create_thumbnail(image_path, thumbnail_path):
    try:
        with Image.open(image_path) as img:
            img.thumbnail((THUMBNAIL_WIDTH, THUMBNAIL_WIDTH))
            img.save(thumbnail_path)
    except Exception as e:
        print(f"❌ Failed to create thumbnail for {image_path}: {e}")

def ensure_thumbnails():
    os.makedirs(THUMBNAIL_FOLDER, exist_ok=True)
    for fname in os.listdir(IMAGE_FOLDER):
        ext = os.path.splitext(fname)[1].lower()
        if ext in VALID_EXTENSIONS:
            original_path = os.path.join(IMAGE_FOLDER, fname)
            thumb_path = os.path.join(THUMBNAIL_FOLDER, fname)
            if not os.path.exists(thumb_path):
                create_thumbnail(original_path, thumb_path)

def collect_images():
    images = []
    for fname in sorted(os.listdir(IMAGE_FOLDER)):
        ext = os.path.splitext(fname)[1].lower()
        if ext in VALID_EXTENSIONS:
            tag, date_str = parse_filename(fname)
            images.append({
                "src": f"{IMAGE_FOLDER}/{fname}",
                "alt": fname,
                "tag": tag,
                "date": date_str,
                "thumbnail": f"{THUMBNAIL_FOLDER}/{fname}"
            })
    return images

def generate_html(images, page_num, total_pages):
    nav = '<div class="mt-6 flex justify-center space-x-4">'
    if page_num > 1:
        nav += f'<a href="{OUTPUT_PREFIX}{"" if page_num == 2 else page_num - 1}.html" class="px-4 py-2 bg-gray-800 rounded hover:bg-gray-700">⬅ Prev</a>'
    if page_num < total_pages:
        nav += f'<a href="{OUTPUT_PREFIX}{page_num + 1}.html" class="px-4 py-2 bg-gray-800 rounded hover:bg-gray-700">Next ➡</a>'
    nav += '</div>'

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Minecraft Gallery - Page {page_num}</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    dialog::backdrop {{
      background-color: rgba(0, 0, 0, 0.8);
    }}
    dialog img {{
      max-width: 90vw;
      max-height: 90vh;
      border-radius: 10px;
      box-shadow: 0 0 20px #000;
    }}
    .thumbnail {{
      width: 100%;
      cursor: pointer;
      border-radius: 6px;
      transition: transform 0.2s;
    }}
    .thumbnail:hover {{
      transform: scale(1.05);
    }}
    .gallery {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
      gap: 1rem;
    }}
  </style>
</head>
<body class="bg-gray-900 text-white p-4">
  <h1 class="text-3xl font-bold mb-6 text-center">Minecraft Gallery - Page {page_num}</h1>

  <div class="gallery">
"""

    for img in images:
        html += f"""
    <div class="image-card bg-gray-800 rounded shadow p-2">
      <img src="{img['thumbnail']}" alt="{img['alt']}" class="thumbnail" onclick="document.getElementById('dialog-{img['alt']}').showModal();">
      <div class="text-sm mt-2 text-gray-300">
        <div><strong>{img['tag']}</strong></div>
        <div>{img['date']}</div>
      </div>
    </div>

    <!-- Dialog for full-size image -->
    <dialog id="dialog-{img['alt']}" onclick="this.close();">
      <img src="{img['src']}" alt="Full size {img['alt']}">
    </dialog>
"""

    html += f"""  </div>\n{nav}\n</body>\n</html>"""
    return html

def write_pages(images):
    total = len(images)
    total_pages = ceil(total / IMAGES_PER_PAGE)
    for page_num in range(1, total_pages + 1):
        start = (page_num - 1) * IMAGES_PER_PAGE
        end = start + IMAGES_PER_PAGE
        page_images = images[start:end]
        html = generate_html(page_images, page_num, total_pages)
        suffix = "" if page_num == 1 else str(page_num)
        filename = os.path.join(OUTPUT_FOLDER, f"{OUTPUT_PREFIX}{suffix}.html")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html)
    print(f"✅ {total_pages} page(s) generated with {total} images.")

def main():
    ensure_thumbnails()
    images = collect_images()
    write_pages(images)

if __name__ == "__main__":
    main()

