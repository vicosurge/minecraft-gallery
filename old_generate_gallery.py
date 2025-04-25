import os
from pathlib import Path
from math import ceil

IMAGE_FOLDER = "images"
OUTPUT_FOLDER = "."
OUTPUT_PREFIX = "index"
VALID_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
IMAGES_PER_PAGE = 20

def parse_filename(fname):
    name, _ = os.path.splitext(fname)
    parts = name.split("_")
    if len(parts) >= 3:
        tag = parts[0]
        date = parts[1]
        time = parts[2].replace("-", ":")
        return tag, f"{date} {time}"
    return "Unknown", "Unknown"

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
                "date": date_str
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
</head>
<body class="bg-gray-900 text-white p-4">
  <h1 class="text-3xl font-bold mb-6 text-center">Minecraft Gallery - Page {page_num}</h1>

  <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
"""

    for img in images:
        html += f"""
    <div class="image-card bg-gray-800 rounded shadow p-2">
      <img src="{img['src']}" alt="{img['alt']}" class="rounded w-full" loading="lazy" />
      <div class="text-sm mt-2 text-gray-300">
        <div><strong>{img['tag']}</strong></div>
        <div>{img['date']}</div>
      </div>
    </div>
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
    images = collect_images()
    write_pages(images)

if __name__ == "__main__":
    main()

