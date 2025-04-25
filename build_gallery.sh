echo "Fix all images in case there are dangling ones"
python3 convert_images.py
echo "Build static gallery"
python3 generate_gallery.py
