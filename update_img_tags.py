
import os
import re

root_dir = "c:/Users/lucia/OneDrive/Desktop/GoldenGrove"
images_dir = "c:/Users/lucia/OneDrive/Desktop/GoldenGrove/images"

def make_alt_text(filename):
    # house-cleaning-midland.jpg -> House Cleaning Midland
    base = os.path.splitext(filename)[0]
    # Remove separators
    text = base.replace("-", " ").replace("_", " ")
    # Title case
    return text.title()

print("Updating HTML <img> tags...")

img_regex = re.compile(r'<img\s+([^>]*)src=["\']([^"\']+)["\']([^>]*)>', re.IGNORECASE)

files_updated = 0

for root, dirs, files in os.walk(root_dir):
    if ".git" in root or "node_modules" in root: continue
    
    for file in files:
        if file.endswith(".html"):
            file_path = os.path.join(root, file)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            original_content = content
            
            def replace_img(match):
                attrs_prefix = match.group(1)
                src = match.group(2)
                attrs_suffix = match.group(3)
                
                # Check if src is local and susceptible to webp
                # src might be absolute url or relative
                # If it starts with http, skip? Or check if it's our domain?
                # Let's target local images in images/
                
                new_src = src
                
                # Check for image extension
                base, ext = os.path.splitext(src)
                if ext.lower() in ['.jpg', '.jpeg', '.png']:
                    # Check if corresponding .webp exists
                    # This is tricky with paths. src often links to /images/foo.jpg
                    # We need to resolve that to local path.
                    
                    # Assume /images/ -> c:/.../images/
                    # Use simple logic: if filename.webp exists in images dir
                    filename = os.path.basename(src)
                    filename_no_ext = os.path.splitext(filename)[0]
                    webp_filename = filename_no_ext + ".webp"
                    
                    if os.path.exists(os.path.join(images_dir, webp_filename)):
                        # Replace extension in src
                        new_src = base + ".webp"
                
                # Check ALT tag
                full_tag = match.group(0)
                has_alt = "alt=" in full_tag.lower()
                
                new_attrs_prefix = attrs_prefix
                new_attrs_suffix = attrs_suffix
                
                if not has_alt:
                    # Generate alt
                    filename = os.path.basename(src) # Use original filename for alt
                    alt_text = make_alt_text(filename)
                    # Append alt to suffix
                    new_attrs_suffix = f' alt="{alt_text}"{attrs_suffix}'
                
                return f'<img {new_attrs_prefix}src="{new_src}"{new_attrs_suffix}>'

            new_content = img_regex.sub(replace_img, content)
            
            if new_content != original_content:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"Updated: {file}")
                # print diff?
                files_updated += 1

print(f"Done. Updated {files_updated} files.")
