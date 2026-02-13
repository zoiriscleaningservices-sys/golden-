
import os
import re

root_dir = "c:/Users/lucia/OneDrive/Desktop/GoldenGrove"

print("Verifying SEO Implementation (Detailed)...")
errors = 0

ignore_dirs = [".git", "node_modules", "favicon", "images", "css", "js"]
ignore_files = ["google", "robots.txt", "sitemap.xml"]

for root, dirs, files in os.walk(root_dir):
    # Skip ignored dirs
    if any(ignore in root for ignore in ignore_dirs):
        continue
    
    for file in files:
        if file.endswith(".html"):
            file_path = os.path.join(root, file)
            
            # Skip root index.html (redirect)
            if file_path == os.path.join(root_dir, "index.html"):
                continue
            
            # Skip Home/index.html (Homepage usually doesn't need breadcrumb back to itself)
            if "Home" in root and file == "index.html":
                continue

            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Check Schema
            if '"@type": "BreadcrumbList"' not in content:
                print(f"[FAIL] Missing Breadcrumb Schema: {file_path}")
                errors += 1
            else:
                # print(f"[PASS] Breadcrumb: {os.path.basename(root)}/{file}")
                pass
                
            # Check Images
            # Find all imgs
            img_tags = re.findall(r'<img[^>]+>', content)
            for img in img_tags:
                # Check src extension
                # Simple check: matches .jpg" or .png"
                if re.search(r'\.(jpg|jpeg|png)["\']', img, re.IGNORECASE):
                     # Ignore external images (http)
                     if "http" not in img and "data:" not in img:
                         print(f"[WARN] Non-WebP Image in {file_path}: {img}")
                
                # Check Alt
                if "alt=" not in img.lower() or 'alt=""' in img.lower():
                    # Check if it has aria-hidden="true" (decorative)
                    if 'aria-hidden="true"' in img.lower():
                        continue
                    print(f"[FAIL] Missing/Empty Alt in {file_path}: {img}")
                    errors += 1

if errors == 0:
    print("SUCCESS: All checks passed!")
else:
    print(f"FAILED: Found {errors} errors.")
