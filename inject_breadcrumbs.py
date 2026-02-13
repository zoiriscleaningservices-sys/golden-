
import os
import json

root_dir = "c:/Users/lucia/OneDrive/Desktop/GoldenGrove"
base_url = "https://www.goldengrovecleaning.com"

# MAPPING DEFINITION
mapping = {
    # Services
    "house-cleaning-midland-tx": {"parent": "Services", "parent_url": "/Home/#services", "name": "House Cleaning"},
    "deep-cleaning-midland-tx": {"parent": "Services", "parent_url": "/Home/#services", "name": "Deep Cleaning"},
    "move-out-cleaning-midland-tx": {"parent": "Services", "parent_url": "/Home/#services", "name": "Move-In / Move-Out"},
    "commercial-janitorial-midland-tx": {"parent": "Services", "parent_url": "/Home/#services", "name": "Commercial Cleaning"},
    "airbnb-turnover-midland-tx": {"parent": "Services", "parent_url": "/Home/#services", "name": "Airbnb Turnover"},
    "post-construction-cleaning-midland-tx": {"parent": "Services", "parent_url": "/Home/#services", "name": "Post-Construction"},
    "carpet-upholstery-cleaning-midland-tx": {"parent": "Services", "parent_url": "/Home/#services", "name": "Carpet Cleaning"},
    "window-cleaning-midland-tx": {"parent": "Services", "parent_url": "/Home/#services", "name": "Window Cleaning"},
    
    # Overview Pages
    "locations-midland-tx": {"parent": None, "parent_url": None, "name": "Service Areas"},

    # Major Cities (Parent is now Locations page)
    "midland-tx-cleaning-services": {"parent": "Service Areas", "parent_url": "/locations-midland-tx/", "name": "Midland, TX"},
    "odessa-tx-cleaning-services": {"parent": "Service Areas", "parent_url": "/locations-midland-tx/", "name": "Odessa, TX"},
    "big-spring-tx-cleaning-services": {"parent": "Service Areas", "parent_url": "/locations-midland-tx/", "name": "Big Spring, TX"},
    
    # Nearby Areas
    "greenwood-tx-cleaning-services": {"parent": "Service Areas", "parent_url": "/locations-midland-tx/", "name": "Greenwood, TX"},
    "stanton-tx-cleaning-services": {"parent": "Service Areas", "parent_url": "/locations-midland-tx/", "name": "Stanton, TX"},
    "gardendale-tx-cleaning-services": {"parent": "Service Areas", "parent_url": "/locations-midland-tx/", "name": "Gardendale, TX"},
    "andrews-tx-cleaning-services": {"parent": "Service Areas", "parent_url": "/locations-midland-tx/", "name": "Andrews, TX"},
    
    # Neighborhoods
    "old-midland-tx-cleaning-services": {"parent": "Service Areas", "parent_url": "/locations-midland-tx/", "name": "Old Midland"},
    "grassland-estates-tx-cleaning-services": {"parent": "Service Areas", "parent_url": "/locations-midland-tx/", "name": "Grassland Estates"},
    "green-tree-park-tx-cleaning-services": {"parent": "Service Areas", "parent_url": "/locations-midland-tx/", "name": "Green Tree Park"},
    "saddle-club-estates-tx-cleaning-services": {"parent": "Service Areas", "parent_url": "/locations-midland-tx/", "name": "Saddle Club Estates"},
    "skyline-terrace-tx-cleaning-services": {"parent": "Service Areas", "parent_url": "/locations-midland-tx/", "name": "Skyline Terrace"},
    
    # Standard Pages
    "about-midland-tx": {"parent": None, "parent_url": None, "name": "About Us"},
    "blog-midland-tx": {"parent": None, "parent_url": None, "name": "Blog"},
    "gallery-midland-tx": {"parent": None, "parent_url": None, "name": "Gallery"},
}

def generate_breadcrumb_json(folder_name):
    if folder_name not in mapping:
        return None
        
    info = mapping[folder_name]
    current_url = f"{base_url}/{folder_name}/"
    
    # Base structure
    schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": 1,
                "name": "Home",
                "item": f"{base_url}/" # Home
            }
        ]
    }
    
    # Intermediate Step (Services / Service Areas)
    position = 2
    if info["parent"]:
        schema["itemListElement"].append({
            "@type": "ListItem",
            "position": position,
            "name": info["parent"],
            "item": f"{base_url}{info['parent_url']}"
        })
        position += 1
        
    # Current Page
    schema["itemListElement"].append({
        "@type": "ListItem",
        "position": position,
        "name": info["name"],
        "item": current_url
    })
    
    return json.dumps(schema, indent=2)

print("Injecting Breadcrumb Schema (Retry)...")

for root, dirs, files in os.walk(root_dir):
    if ".git" in root or "node_modules" in root: continue
    
    folder_name = os.path.basename(root)
    
    if folder_name in mapping:
        for file in files:
            if file == "index.html":
                file_path = os.path.join(root, file)
                breadcrumb_json = generate_breadcrumb_json(folder_name)
                
                if breadcrumb_json:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    
                    # Remove existing breadcrumb schema if it exists to update it
                    # Regex to find existing BreadcrumbList script block
                    # <script type="application/ld+json">...BreadcrumbList...</script>
                    # This is hard to regex reliably.
                    # Simplest approach: formatting is consistent because I wrote it.
                    # It starts with \n    <!-- Breadcrumb Schema -->\n    <script ...
                    # And ends with ...\n    </script>\n
                    
                    if '<!-- Breadcrumb Schema -->' in content:
                        # Find the start
                        start_marker = '<!-- Breadcrumb Schema -->'
                        end_marker = '</script>'
                        
                        start_idx = content.find(start_marker)
                        if start_idx != -1:
                            # Search for end script AFTER the marker
                            # Need to find the closing </script> of that specific block
                            # Since I injected it immediately after the marker...
                            # The marker is followed by <script...> ... </script>
                            
                            # Let's locate the substring to remove.
                            # It's basically everything from start_marker to the next </script> + newline?
                            # My injection: f'\n    <!-- Breadcrumb Schema -->\n    <script type="application/ld+json">\n{breadcrumb_json}\n    </script>\n'
                            
                            # I will iterate to find the end
                            rest_of_content = content[start_idx:]
                            end_script_idx = rest_of_content.find('</script>')
                            if end_script_idx != -1:
                                full_remove_len = end_script_idx + len('</script>')
                                # Remove it
                                content = content[:start_idx] + content[start_idx + full_remove_len:]
                                # Clean up extra newline if needed?
                                # The original replacement replaced </head> with {script}</head>
                                # So if I remove it, I should be left with </head> (wait, no, I didn't touch </head> in the remove logic, I just removed the block)
                                # The block was BEFORE </head>.
                                # So removing it restores state to just before injection (mostly).
                                pass

                    # Injection logic: Before </head>
                    script_tag = f'\n    <!-- Breadcrumb Schema -->\n    <script type="application/ld+json">\n{breadcrumb_json}\n    </script>\n'
                    
                    if "</head>" in content:
                        new_content = content.replace("</head>", f"{script_tag}</head>")
                        with open(file_path, "w", encoding="utf-8") as f:
                            f.write(new_content)
                        print(f"Updated {folder_name}")
                    else:
                        print(f"Error: {folder_name} (No </head>)")

print("Done.")
