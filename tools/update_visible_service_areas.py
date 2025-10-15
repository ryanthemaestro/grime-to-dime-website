#!/usr/bin/env python3
"""
Update the visible Service Areas section on all landing pages
to show all 23 Howard County locations instead of just the original 7.
"""

import re
from pathlib import Path

# All 23 Howard County locations with their slugs
LOCATIONS = [
    ("Annapolis Junction", "annapolis-junction-md"),
    ("Catonsville", "catonsville-md"),
    ("Clarksville", "clarksville-md"),
    ("Columbia", "columbia-md"),
    ("Cooksville", "cooksville-md"),
    ("Daniels", "daniels-md"),
    ("Dayton", "dayton-md"),
    ("Dorsey", "dorsey-md"),
    ("Elkridge", "elkridge-md"),
    ("Ellicott City", "ellicott-city-md"),
    ("Fulton", "fulton-md"),
    ("Glenelg", "glenelg-md"),
    ("Glenwood", "glenwood-md"),
    ("Hanover", "hanover-md"),
    ("Highland", "highland-md"),
    ("Ilchester", "ilchester-md"),
    ("Jessup", "jessup-md"),
    ("Laurel", "laurel-md"),
    ("Lisbon", "lisbon-md"),
    ("Marriottsville", "marriottsville-md"),
    ("Savage", "savage-md"),
    ("Scaggsville", "scaggsville-md"),
    ("West Friendship", "west-friendship-md")
]

# Old service areas HTML (original 7 cities)
OLD_SERVICE_AREAS = '<div style="display:flex;flex-wrap:wrap;gap:.6rem;justify-content:center"><a class="pill chip" href="/locations/ellicott-city-md/">Ellicott City</a><a class="pill chip" href="/locations/columbia-md/">Columbia</a><a class="pill chip" href="/locations/elkridge-md/">Elkridge</a><a class="pill chip" href="/locations/clarksville-md/">Clarksville</a><a class="pill chip" href="/locations/laurel-md/">Laurel</a><a class="pill chip" href="/locations/savage-md/">Savage</a><a class="pill chip" href="/locations/catonsville-md/">Catonsville</a></div>'

# Generate new service areas HTML with all 23 locations
def generate_new_service_areas():
    """Generate HTML for all 23 service areas."""
    links = []
    for name, slug in LOCATIONS:
        links.append(f'<a class="pill chip" href="/locations/{slug}/">{name}</a>')
    
    return '<div style="display:flex;flex-wrap:wrap;gap:.6rem;justify-content:center">' + ''.join(links) + '</div>'

NEW_SERVICE_AREAS = generate_new_service_areas()

def update_landing_page(file_path):
    """Update a single landing page with new visible service areas."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if it has the old service areas HTML
        if OLD_SERVICE_AREAS in content:
            # Replace with new
            updated_content = content.replace(OLD_SERVICE_AREAS, NEW_SERVICE_AREAS)
            
            # Write back
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            return True
        return False
    except Exception as e:
        print(f"Error updating {file_path}: {e}")
        return False

def main():
    """Update all landing pages."""
    print("🚀 Updating visible Service Areas on all landing pages")
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
            if updated_count <= 10:  # Show first 10
                print(f"✅ Updated: {index_file.parent.name}")
        else:
            skipped_count += 1
    
    if updated_count > 10:
        print(f"... and {updated_count - 10} more pages")
    
    print(f"\n✅ Complete!")
    print(f"📊 Updated: {updated_count} pages")
    print(f"📊 Skipped: {skipped_count} pages (no Service Areas section or already updated)")
    
    print(f"\n🎯 Visible Service Areas now show all 23 locations:")
    for name, slug in LOCATIONS:
        print(f"   • {name}")

if __name__ == "__main__":
    main()

