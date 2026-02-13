
import os
import re

root_dir = "c:/Users/lucia/OneDrive/Desktop/GoldenGrove"

# Define unique, optimized meta descriptions for ALL pages
meta_map = {
    # Home
    "Home": "Golden Grove Cleaning is Midland & Odessa's #1 rated cleaning service. We offer premium house cleaning, commercial janitorial, deep cleaning, and move-in/out services. Bonded & Insured.",
    
    # Core Services
    "house-cleaning-midland-tx": "Top-rated house cleaning in Midland, TX. Our professional maids provide recurring weekly, bi-weekly, or monthly cleaning services tailored to your home's needs.",
    "deep-cleaning-midland-tx": "Experience the deepest clean for your Midland home. Our deep cleaning service removes hidden dust, allergens, and grime from top to bottom. Perfect for spring cleaning!",
    "move-out-cleaning-midland-tx": "Guaranteed move-out cleaning in Midland & Odessa. We ensure you get your deposit back with our thorough move-in / move-out checklist. Landlord approved.",
    "commercial-janitorial-midland-tx": "Reliable commercial cleaning & janitorial services in Midland/Odessa. Offices, medical facilities, and retail spaces. Licensed, bonded, and insured for your business.",
    "airbnb-turnover-midland-tx": "Fast & reliable Airbnb turnover cleaning in Midland, TX. We make your vacation rental guest-ready with linen service, restocking, and 5-star standard cleaning.",
    "post-construction-cleaning-midland-tx": "Professional post-construction cleaning in Midland, TX. We remove drywall dust, debris, and construction residue to make your new build or remodel shine.",
    "carpet-upholstery-cleaning-midland-tx": "Revive your carpets and furniture with expert cleaning in Midland. Remove stains, odors, and pet dander with our professional carpet & upholstery services.",
    "window-cleaning-midland-tx": "Crystal clear window cleaning for Midland homes and businesses. Interior and exterior window washing for a streak-free shine. Satisfaction guaranteed.",

    # Locations - Major Cities
    "midland-tx-cleaning-services": "Premier cleaning services in Midland, TX. Trusted by outstanding local homeowners for excellence in house cleaning, maid service, and janitorial solutions.",
    "odessa-tx-cleaning-services": "Top-ranked cleaning services in Odessa, TX. Golden Grove delivers professional house cleaning and commercial janitorial services to the entire Odessa community.",
    "big-spring-tx-cleaning-services": "Golden Grove brings professional cleaning to Big Spring, TX. Experienced local cleaners for residential homes and commercial businesses. Get a free quote!",
    
    # Locations - Nearby Areas
    "andrews-tx-cleaning-services": "The best house cleaning and maid services in Andrews, TX. Reliable, background-checked cleaners dedicated to keeping your Andrews home spotless.",
    "greenwood-tx-cleaning-services": "Serving Greenwood, TX with exceptional home cleaning. Our local team provides deep cleaning, standard maintenance, and move-out services for Greenwood residents.",
    "stanton-tx-cleaning-services": "Professional cleaning services available in Stanton, TX. From office janitorial to detailed house cleaning, Golden Grove is your trusted local partner.",
    "gardendale-tx-cleaning-services": "Gardendale's choice for premium cleaning. We offer weekly and bi-weekly maid services to keep your Gardendale home beautiful and dust-free.",
    
    # Locations - Neighborhoods
    "old-midland-tx-cleaning-services": "Specialized cleaning for Old Midland homes. We treat your historic or luxury property with the utmost care and attention to detail. Bonded & Insured.",
    "grassland-estates-tx-cleaning-services": "Trusted house cleaners for Grassland Estates. Join your neighbors in choosing Golden Grove for reliable, high-quality maid services.",
    "green-tree-park-tx-cleaning-services": "Green Tree Country Club area cleaning specialists. Premium home cleaning services designed for the discerning residents of Green Tree Park.",
    "saddle-club-estates-tx-cleaning-services": "Saddle Club Estates' favorite cleaning service. We provide consistent, high-standard housekeeping and deep cleaning for your beautiful home.",
    "skyline-terrace-tx-cleaning-services": "Professional maid service in Skyline Terrace. Experience the Golden Grove difference with our thorough, reliable, and friendly cleaning team.",

    # Other Pages
    "about-midland-tx": "Learn about Golden Grove Cleaning, West Texas's leading woman-owned cleaning company. Discover our mission, our values, and why we are the top choice for Midland/Odessa.",
    "blog-midland-tx": "Expert cleaning tips, local news, and home maintenance advice from Golden Grove Cleaning. Stay updated with the best practices for keeping your Midland home fresh.",
    "gallery-midland-tx": "View our work! See before & after photos of our house cleaning, deep cleaning, and commercial projects in Midland and Odessa, TX.",
    "locations-midland-tx": "Golden Grove Cleaning serves the entire Permian Basin. Check our service areas including Midland, Odessa, Big Spring, Andrews, Greenwood, and more.",
}

print("Updating Meta Descriptions for ALL pages...")

for root, dirs, files in os.walk(root_dir):
    if ".git" in root or "node_modules" in root: continue
    
    folder_name = os.path.basename(root)
    
    for file in files:
        if file == "index.html":
            # Identify the key for this file
            key = None
            if root == root_dir: 
                continue # Skip root index (redirect)
            elif "Home" in root:
                key = "Home"
            else:
                key = folder_name
            
            if key in meta_map:
                new_desc = meta_map[key]
                file_path = os.path.join(root, file)
                
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # Regex to replace meta description content
                # We assume standard double quotes for the content attribute based on file analysis
                # <meta name="description" content="..." />
                
                # This regex captures:
                # Group 1: <meta name="description" ... content="
                # Group 2: The content inside the quotes (non-greedy match until the next double quote)
                # Group 3: "
                pattern = re.compile(r'(<meta\s+name=["\']description["\']\s+content=")([^"]*)(")', re.IGNORECASE | re.DOTALL)
                
                if pattern.search(content):
                    new_content = pattern.sub(f'\\g<1>{new_desc}\\g<3>', content)
                    
                    if new_content != content:
                        with open(file_path, "w", encoding="utf-8") as f:
                            f.write(new_content)
                        print(f"Updated: {key}")
                    else:
                        print(f"Skipped: {key} (Already matches)")
                else:
                    print(f"Warning: No meta description tag found in {key}")

print("Bulk update complete.")
