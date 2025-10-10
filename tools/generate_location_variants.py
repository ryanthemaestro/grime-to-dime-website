#!/usr/bin/env python3
"""
Generate location-specific variants for all existing landing pages.
Creates city-specific versions for each service across Howard County.
"""

import os
import shutil
from pathlib import Path

# Howard County cities
CITIES = [
    "catonsville-md",
    "clarksville-md", 
    "columbia-md",
    "elkridge-md",
    "ellicott-city-md",
    "laurel-md",
    "savage-md"
]

def get_base_services():
    """Get list of base service directories (non-location specific)."""
    landing_dir = Path(__file__).parent.parent / "landing"
    base_services = []
    
    for item in landing_dir.iterdir():
        if item.is_dir():
            name = item.name
            # Skip if already has city suffix
            if not any(f"-{city}" in name for city in CITIES):
                base_services.append(name)
    
    return sorted(base_services)

def create_location_variant(base_service, city):
    """Create a location-specific variant of a base service."""
    landing_dir = Path(__file__).parent.parent / "landing"
    base_dir = landing_dir / base_service
    variant_dir = landing_dir / f"{base_service}-{city}"
    
    if variant_dir.exists():
        print(f"  {variant_dir.name} already exists")
        return False
    
    if not base_dir.exists():
        print(f"  Base service {base_service} not found")
        return False
    
    # Copy the directory
    shutil.copytree(base_dir, variant_dir)
    
    # Update the HTML content
    index_file = variant_dir / "index.html"
    if index_file.exists():
        content = index_file.read_text(encoding='utf-8')
        
        # Extract city name from slug (e.g., "catonsville-md" -> "Catonsville")
        city_name = city.replace('-md', '').replace('-', ' ').title()
        
        # Update title, meta description, and canonical URL
        content = content.replace(
            f'<title>{base_service.replace("-", " ").title()} | Howard County | Grime To Dime</title>',
            f'<title>{base_service.replace("-", " ").title()} | {city_name} | Grime To Dime</title>'
        )
        
        content = content.replace(
            f'<link rel="canonical" href="https://grimetodime.com/landing/{base_service}/">',
            f'<link rel="canonical" href="https://grimetodime.com/landing/{base_service}-{city}/">'
        )
        
        # Update meta description to include city
        content = content.replace(
            'in Howard County',
            f'in {city_name}'
        )
        
        # Update JSON-LD structured data
        content = content.replace(
            '"areaServed":["Howard County MD","Ellicott City MD","Columbia MD","Elkridge MD","Laurel MD","Clarksville MD","Savage MD","Catonsville MD"]',
            f'"areaServed":["{city_name} MD"]'
        )
        
        index_file.write_text(content, encoding='utf-8')
    
    print(f"  Created {variant_dir.name}")
    return True

def main():
    """Generate location variants for all base services."""
    print("🚀 Generating location variants for all landing pages")
    print("=" * 60)
    
    base_services = get_base_services()
    print(f"Found {len(base_services)} base services")
    
    created_count = 0
    skipped_count = 0
    
    for service in base_services:
        print(f"\n📁 Processing: {service}")
        
        for city in CITIES:
            if create_location_variant(service, city):
                created_count += 1
            else:
                skipped_count += 1
    
    print(f"\n✅ Complete!")
    print(f"📊 Created: {created_count} location variants")
    print(f"📊 Skipped: {skipped_count} (already existed)")
    
    # Update sitemap
    try:
        print("\n🗺️  Updating sitemap...")
        from update_sitemap import integrate_with_generator
        integrate_with_generator()
    except Exception as e:
        print(f"⚠️  Sitemap update failed: {e}")

if __name__ == "__main__":
    main()
