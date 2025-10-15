#!/usr/bin/env python3
"""
Update all landing pages to include all 23 Howard County service areas
in their JSON-LD structured data.
"""

import os
import re
from pathlib import Path

# All 23 Howard County locations (with MD)
ALL_LOCATIONS_WITH_MD = [
    "Annapolis Junction MD",
    "Catonsville MD",
    "Clarksville MD",
    "Columbia MD",
    "Cooksville MD",
    "Daniels MD",
    "Dayton MD",
    "Dorsey MD",
    "Elkridge MD",
    "Ellicott City MD",
    "Fulton MD",
    "Glenelg MD",
    "Glenwood MD",
    "Hanover MD",
    "Highland MD",
    "Ilchester MD",
    "Jessup MD",
    "Laurel MD",
    "Lisbon MD",
    "Marriottsville MD",
    "Savage MD",
    "Scaggsville MD",
    "West Friendship MD"
]

# All 23 locations (without MD - for location-specific variants)
ALL_LOCATIONS_NO_MD = [loc.replace(" MD", "") for loc in ALL_LOCATIONS_WITH_MD]

# Pattern variations to match
OLD_PATTERNS = [
    # Pattern 1: Base pages with "MD" and double quotes
    '"areaServed":["Howard County MD","Ellicott City MD","Columbia MD","Elkridge MD","Laurel MD","Clarksville MD","Savage MD","Catonsville MD"]',
    
    # Pattern 2: Location-specific pages without "MD"
    '"areaServed":["Ellicott City", "Columbia", "Elkridge", "Clarksville", "Laurel", "Savage", "Catonsville"]',
    
    # Pattern 3: Single city variant (created by generate_location_variants.py)
    # Will match anything like: "areaServed":["Fulton MD"]
]

# New area served strings
NEW_AREA_SERVED_WITH_MD = '"areaServed":' + str(ALL_LOCATIONS_WITH_MD).replace("'", '"')
NEW_AREA_SERVED_NO_MD = '"areaServed":' + str(ALL_LOCATIONS_NO_MD).replace("'", '"')

def update_landing_page(file_path):
    """Update a single landing page with new service areas."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Replace pattern 1 (base pages with MD)
        if OLD_PATTERNS[0] in content:
            content = content.replace(OLD_PATTERNS[0], NEW_AREA_SERVED_WITH_MD)
        
        # Replace pattern 2 (location pages without MD)
        elif OLD_PATTERNS[1] in content:
            content = content.replace(OLD_PATTERNS[1], NEW_AREA_SERVED_NO_MD)
        
        # Replace pattern 3 (single city variants) - use regex
        else:
            # Match single city like: "areaServed":["Fulton MD"]
            pattern = r'"areaServed":\["[^"]+"\]'
            if re.search(pattern, content):
                content = re.sub(pattern, NEW_AREA_SERVED_NO_MD, content)
        
        # Check if anything changed
        if content != original_content:
            # Write back
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
    except Exception as e:
        print(f"Error updating {file_path}: {e}")
        return False

def main():
    """Update all landing pages."""
    print("🚀 Updating service areas on all landing pages")
    print("=" * 60)
    
    landing_dir = Path(__file__).parent.parent / "landing"
    
    if not landing_dir.exists():
        print("❌ Landing directory not found")
        return
    
    updated_count = 0
    skipped_count = 0
    
    # Find all index.html files in landing directory
    for index_file in landing_dir.glob("*/index.html"):
        if update_landing_page(index_file):
            updated_count += 1
            print(f"✅ Updated: {index_file.parent.name}")
        else:
            skipped_count += 1
    
    print(f"\n✅ Complete!")
    print(f"📊 Updated: {updated_count} pages")
    print(f"📊 Skipped: {skipped_count} pages (already current or different format)")
    
    print(f"\n🎯 All landing pages now show all 23 service areas:")
    for location in ALL_LOCATIONS_WITH_MD:
        print(f"   • {location}")

if __name__ == "__main__":
    main()

