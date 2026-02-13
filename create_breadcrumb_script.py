
# Manual mapping based on Home/index.html analysis

# Services
# /house-cleaning-midland-tx/ -> House Cleaning
# /deep-cleaning-midland-tx/ -> Deep Cleaning
# /move-out-cleaning-midland-tx/ -> Move-In / Move-Out
# /commercial-janitorial-midland-tx/ -> Commercial Cleaning
# /airbnb-turnover-midland-tx/ -> Airbnb Turnover
# /post-construction-cleaning-midland-tx/ -> Post-Construction
# /carpet-upholstery-cleaning-midland-tx/ -> Carpet Cleaning
# /window-cleaning-midland-tx/ -> Window Cleaning

# Service Areas (Major Cities)
# /midland-tx-cleaning-services/ -> Midland, TX
# /odessa-tx-cleaning-services/ -> Odessa, TX
# /big-spring-tx-cleaning-services/ -> Big Spring, TX

# Service Areas (Nearby)
# /greenwood-tx-cleaning-services/ -> Greenwood, TX
# /stanton-tx-cleaning-services/ -> Stanton, TX
# /gardendale-tx-cleaning-services/ -> Gardendale, TX
# /andrews-tx-cleaning-services/ -> Andrews, TX

# Service Areas (Neighborhoods)
# /old-midland-tx-cleaning-services/ -> Old Midland
# /grassland-estates-tx-cleaning-services/ -> Grassland Estates
# /green-tree-park-tx-cleaning-services/ -> Green Tree Park
# /saddle-club-estates-tx-cleaning-services/ -> Saddle Club Estates
# /skyline-terrace-tx-cleaning-services/ -> Skyline Terrace

# Other
# /about-midland-tx/ -> About
# /blog-midland-tx/ -> Blog
# /gallery-midland-tx/ -> Gallery

import os
import json

root_dir = "c:/Users/lucia/OneDrive/Desktop/GoldenGrove"

# Mapping: Folder Name -> (Parent Name, Parent URL, Item Name)
# Home is root.
# Services -> Home > Services (Virtual?) > Item
# Service Areas -> Home > Service Areas (Virtual?) > Item

# Virtual parents do not have pages, so Breadcrumb usually skips them or links to a section.
# Since we don't have a /services/ page, maybe just Home > [Service Name] is better?
# Google recommends breadcrumbs reflect the URL structure or a logical hierarchy.
# Since we have "Clean URLs" like /service-name/, strictly speaking it is Home > Service Name.
# BUT, logical hierarchy "Home > Services > Service Name" looks better in SERPs.
# For the intermediate "Services" item, if there is no page, we can omit the "item" property or link to Home/#services.

# Let's use specific parents where possible.
# If I link "Services" to /Home/#services, that works.

mapping = {
    "house-cleaning-midland-tx": ("Services", "https://www.goldengrovecleaning.com/Home/#services", "House Cleaning"),
    "deep-cleaning-midland-tx": ("Services", "https://www.goldengrovecleaning.com/Home/#services", "Deep Cleaning"),
    "move-out-cleaning-midland-tx": ("Services", "https://www.goldengrovecleaning.com/Home/#services", "Move-In / Move-Out"),
    "commercial-janitorial-midland-tx": ("Services", "https://www.goldengrovecleaning.com/Home/#services", "Commercial Cleaning"),
    "airbnb-turnover-midland-tx": ("Services", "https://www.goldengrovecleaning.com/Home/#services", "Airbnb Turnover"),
    "post-construction-cleaning-midland-tx": ("Services", "https://www.goldengrovecleaning.com/Home/#services", "Post-Construction"),
    "carpet-upholstery-cleaning-midland-tx": ("Services", "https://www.goldengrovecleaning.com/Home/#services", "Carpet Cleaning"),
    "window-cleaning-midland-tx": ("Services", "https://www.goldengrovecleaning.com/Home/#services", "Window Cleaning"),
}

# Add Service Areas
service_areas = [
    ("midland-tx-cleaning-services", "Midland, TX"),
    ("odessa-tx-cleaning-services", "Odessa, TX"),
    ("big-spring-tx-cleaning-services", "Big Spring, TX"),
    ("greenwood-tx-cleaning-services", "Greenwood, TX"),
    ("stanton-tx-cleaning-services", "Stanton, TX"),
    ("gardendale-tx-cleaning-services", "Gardendale, TX"),
    ("andrews-tx-cleaning-services", "Andrews, TX"),
    ("old-midland-tx-cleaning-services", "Old Midland"),
    ("grassland-estates-tx-cleaning-services", "Grassland Estates"),
    ("green-tree-park-tx-cleaning-services", "Green Tree Park"),
    ("saddle-club-estates-tx-cleaning-services", "Saddle Club Estates"),
    ("skyline-terrace-tx-cleaning-services", "Skyline Terrace"),
]

for folder, name in service_areas:
    mapping[folder] = ("Service Areas", "https://www.goldengrovecleaning.com/Home/#service-areas", name)

# Others
mapping["about-midland-tx"] = ("About", "https://www.goldengrovecleaning.com/about-midland-tx/", "About Us") # Self is parent? No. Home > About
mapping["blog-midland-tx"] = ("Blog", "https://www.goldengrovecleaning.com/blog-midland-tx/", "Blog")
mapping["gallery-midland-tx"] = ("Gallery", "https://www.goldengrovecleaning.com/gallery-midland-tx/", "Gallery")

print("Generating Breadcrumb Injection Script...")

# The script itself
script_content = r'''
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
    
    # Major Cities
    "midland-tx-cleaning-services": {"parent": "Service Areas", "parent_url": "/Home/#service-areas", "name": "Midland, TX"},
    "odessa-tx-cleaning-services": {"parent": "Service Areas", "parent_url": "/Home/#service-areas", "name": "Odessa, TX"},
    "big-spring-tx-cleaning-services": {"parent": "Service Areas", "parent_url": "/Home/#service-areas", "name": "Big Spring, TX"},
    
    # Nearby Areas
    "greenwood-tx-cleaning-services": {"parent": "Service Areas", "parent_url": "/Home/#service-areas", "name": "Greenwood, TX"},
    "stanton-tx-cleaning-services": {"parent": "Service Areas", "parent_url": "/Home/#service-areas", "name": "Stanton, TX"},
    "gardendale-tx-cleaning-services": {"parent": "Service Areas", "parent_url": "/Home/#service-areas", "name": "Gardendale, TX"},
    "andrews-tx-cleaning-services": {"parent": "Service Areas", "parent_url": "/Home/#service-areas", "name": "Andrews, TX"},
    
    # Neighborhoods
    "old-midland-tx-cleaning-services": {"parent": "Service Areas", "parent_url": "/Home/#service-areas", "name": "Old Midland"},
    "grassland-estates-tx-cleaning-services": {"parent": "Service Areas", "parent_url": "/Home/#service-areas", "name": "Grassland Estates"},
    "green-tree-park-tx-cleaning-services": {"parent": "Service Areas", "parent_url": "/Home/#service-areas", "name": "Green Tree Park"},
    "saddle-club-estates-tx-cleaning-services": {"parent": "Service Areas", "parent_url": "/Home/#service-areas", "name": "Saddle Club Estates"},
    "skyline-terrace-tx-cleaning-services": {"parent": "Service Areas", "parent_url": "/Home/#service-areas", "name": "Skyline Terrace"},
    
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

print("Injecting Breadcrumb Schema...")

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
                    
                    # Check if breadcrumb ID is already there (avoid dupes)
                    if '"@type": "BreadcrumbList"' in content:
                        print(f"Skipping {folder_name} (Breadcrumb already exists)")
                        continue

                    # Injection logic: Before </head>
                    script_tag = f'\n    <!-- Breadcrumb Schema -->\n    <script type="application/ld+json">\n{breadcrumb_json}\n    </script>\n'
                    
                    if "</head>" in content:
                        new_content = content.replace("</head>", f"{script_tag}</head>")
                        with open(file_path, "w", encoding="utf-8") as f:
                            f.write(new_content)
                        print(f"Updates {folder_name}")
                    else:
                        print(f"Error: {folder_name} (No </head>)")

print("Done.")
'''

with open("c:/Users/lucia/OneDrive/Desktop/GoldenGrove/inject_breadcrumbs.py", "w") as f:
    f.write(script_content)
