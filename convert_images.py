
import os
from PIL import Image

start_dir = "c:/Users/lucia/OneDrive/Desktop/GoldenGrove/images"
# Extensions to convert
exts = ['.jpg', '.jpeg', '.png']

print("Converting images to WebP...")
count = 0

# Walk, although images usually flat in /images, but just in case
for root, dirs, files in os.walk(start_dir):
    for file in files:
        base, ext = os.path.splitext(file)
        if ext.lower() in exts:
            img_path = os.path.join(root, file)
            webp_path = os.path.join(root, base + ".webp")
            
            # Check if webp already exists
            if os.path.exists(webp_path):
                continue
                
            try:
                with Image.open(img_path) as img:
                    img.save(webp_path, "WEBP", quality=80)
                print(f"Converted: {file} -> {base}.webp")
                count += 1
            except Exception as e:
                print(f"Failed to convert {file}: {e}")

print(f"Done. Converted {count} images.")
