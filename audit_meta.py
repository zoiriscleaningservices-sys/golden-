
import os
import re

root_dir = "c:/Users/lucia/OneDrive/Desktop/GoldenGrove"
base_url = "https://www.goldengrovecleaning.com"

print("Auditing Content & Meta...")
print(f"{'File':<40} | {'Canonical':<10} | {'Title':<30} | {'Desc Length':<5} | {'H1':<5}")
print("-" * 100)

ignore_dirs = [".git", "node_modules", "favicon", "images", "css", "js"]

for root, dirs, files in os.walk(root_dir):
    if any(ignore in root for ignore in ignore_dirs):
        continue
        
    for file in files:
        if file.endswith(".html"):
            # Skip redirects
            if file == "index.html" and root == root_dir: continue # Root index
            
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, root_dir).replace("\\", "/")
            
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Canonical
            canonical_match = re.search(r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', content)
            canonical_status = "MISSING"
            if canonical_match:
                canonical_href = canonical_match.group(1)
                # Check if it matches expected clean URL
                # Expected: https://www.goldengrovecleaning.com/folder/
                # or https://www.goldengrovecleaning.com/Home/
                
                # Determine expected path
                if "Home" in relative_path:
                    expected_suffix = "/Home/"
                else:
                    folder = os.path.dirname(relative_path)
                    expected_suffix = f"/{folder}/"
                
                if expected_suffix in canonical_href:
                    canonical_status = "OK"
                else:
                    canonical_status = "MISMATCH"
            
            # Title
            title_match = re.search(r'<title>(.*?)</title>', content)
            title = title_match.group(1)[:28] + ".." if title_match else "MISSING"
            
            # Meta Description
            # Capture content inside double quotes (ignoring single quotes/apostrophes inside)
            desc_match = re.search(r'<meta\s+name=["\']description["\']\s+content="([^"]+)"', content, re.IGNORECASE | re.DOTALL)
            desc_len = len(desc_match.group(1)) if desc_match else 0
            
            # H1
            h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.DOTALL)
            h1_status = "OK" if h1_match else "MISSING"
            
            print(f"{relative_path[:40]:<40} | {canonical_status:<10} | {title:<30} | {str(desc_len):<11} | {h1_status:<5}")

