#!/usr/bin/env python3
"""
Build service × location matrix for programmatic SEO expansion.
Combines proven keywords with location targeting for scaled landing page generation.
"""

import json
import csv
from pathlib import Path
from typing import List, Dict, Set


# Howard County service areas (extracted from generate_landing_pages.py)
CITIES = [
    ("Ellicott City", "ellicott-city-md", "Ellicott City, MD"),
    ("Columbia", "columbia-md", "Columbia, MD"), 
    ("Elkridge", "elkridge-md", "Elkridge, MD"),
    ("Clarksville", "clarksville-md", "Clarksville, MD"),
    ("Laurel", "laurel-md", "Laurel, MD"),
    ("Savage", "savage-md", "Savage, MD"),
    ("Catonsville", "catonsville-md", "Catonsville, MD"),
]


def load_keep_keywords() -> Set[str]:
    """Load proven keywords from LLM-labeled search terms."""
    keep_keywords = set()
    
    csv_path = Path('/home/nar/learning/llm_labeled_search_terms.csv')
    if not csv_path.exists():
        print(f"❌ {csv_path} not found")
        return keep_keywords
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('final_decision') == 'KEEP':
                keyword = row.get('search_term_clean', '').strip()
                if keyword:
                    keep_keywords.add(keyword)
    
    print(f"✅ Loaded {len(keep_keywords)} KEEP keywords")
    return keep_keywords


def load_existing_groups() -> List[Dict]:
    """Load existing keyword groups from JSON."""
    json_path = Path('/home/nar/learning/keyword_groups_for_landing_pages.json')
    
    if not json_path.exists():
        print(f"❌ {json_path} not found")
        return []
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        groups = data.get('groups', [])
    
    print(f"✅ Loaded {len(groups)} existing service groups")
    return groups


def generate_location_keywords(base_keywords: List[str], city_name: str, city_slug: str) -> List[str]:
    """Generate location-specific variations of keywords."""
    location_keywords = []
    
    # Location modifiers to add
    modifiers = [
        f"{city_name}",
        f"{city_name.lower()}",
        f"in {city_name}",
        f"{city_name} area",
        f"{city_name} md",
        f"{city_name} maryland",
    ]
    
    for keyword in base_keywords:
        # Add original keyword
        location_keywords.append(keyword)
        
        # Add location variations
        for modifier in modifiers:
            # Replace "near me" with city name
            if "near me" in keyword:
                location_keywords.append(keyword.replace("near me", modifier))
                location_keywords.append(keyword.replace("near me", f"in {city_name}"))
            
            # Add city prefix/suffix variations
            if not any(city in keyword.lower() for city in [city_name.lower(), "howard county"]):
                location_keywords.append(f"{keyword} {modifier}")
                location_keywords.append(f"{modifier} {keyword}")
    
    # Remove duplicates while preserving order
    seen = set()
    unique_keywords = []
    for kw in location_keywords:
        if kw not in seen:
            seen.add(kw)
            unique_keywords.append(kw)
    
    return unique_keywords[:30]  # Limit to top 30 for each location


def build_service_location_groups(existing_groups: List[Dict], keep_keywords: Set[str]) -> List[Dict]:
    """Build service × location matrix combining existing groups with locations."""
    expanded_groups = []
    
    for service_group in existing_groups:
        service_name = service_group.get('name', '')
        service_keywords = service_group.get('keywords', [])
        primary_keyword = service_group.get('primary_keyword', '')
        
        # Filter service keywords to only include proven KEEP terms
        proven_keywords = [kw for kw in service_keywords if kw in keep_keywords]
        
        # If no proven keywords, skip this service group
        if not proven_keywords:
            print(f"⚠️  Skipping '{service_name}' - no proven keywords")
            continue
        
        print(f"🎯 Processing '{service_name}' with {len(proven_keywords)} proven keywords")
        
        # Create location-specific groups
        for city_name, city_slug, city_display in CITIES:
            # Generate location-specific name
            location_service_name = f"{service_name} | {city_display}"
            
            # Generate location-specific keywords
            location_keywords = generate_location_keywords(proven_keywords, city_name, city_slug)
            
            # Create location-specific primary keyword
            location_primary = primary_keyword
            if "near me" in primary_keyword:
                location_primary = primary_keyword.replace("near me", f"in {city_name}")
            else:
                location_primary = f"{primary_keyword} {city_name}"
            
            # Build the expanded group
            expanded_group = {
                "name": location_service_name,
                "description": service_group.get('description', '') + f" Specifically targeting customers in {city_display} and surrounding areas.",
                "primary_keyword": location_primary,
                "keywords": location_keywords,
                "service_type": service_group.get('name', ''),
                "location": {
                    "city": city_name,
                    "slug": city_slug,
                    "display": city_display
                }
            }
            
            expanded_groups.append(expanded_group)
    
    return expanded_groups


def main():
    """Main execution function."""
    print("🚀 Building Service × Location Matrix for Programmatic SEO")
    print("=" * 60)
    
    # Load data
    keep_keywords = load_keep_keywords()
    existing_groups = load_existing_groups()
    
    if not keep_keywords:
        print("❌ No KEEP keywords found - aborting")
        return
    
    if not existing_groups:
        print("❌ No existing service groups found - aborting") 
        return
    
    # Build expanded groups
    expanded_groups = build_service_location_groups(existing_groups, keep_keywords)
    
    # Save to new JSON file
    output_path = Path('/home/nar/learning/service_location_groups.json')
    output_data = {
        "meta": {
            "generated_by": "build_service_location_matrix.py",
            "total_groups": len(expanded_groups),
            "cities": len(CITIES),
            "proven_keywords_used": len(keep_keywords)
        },
        "groups": expanded_groups
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Generated {len(expanded_groups)} service × location groups")
    print(f"📁 Saved to: {output_path}")
    print("\n📊 Summary:")
    print(f"  • {len(existing_groups)} original service groups")
    print(f"  • {len(CITIES)} target cities")
    print(f"  • {len(keep_keywords)} proven keywords")
    print(f"  • {len(expanded_groups)} total landing page groups")
    
    # Show preview
    if expanded_groups:
        print(f"\n🔍 Preview of first group:")
        first_group = expanded_groups[0]
        print(f"  Name: {first_group['name']}")
        print(f"  Primary: {first_group['primary_keyword']}")
        print(f"  Keywords: {len(first_group['keywords'])} terms")
        print(f"  Sample: {', '.join(first_group['keywords'][:5])}...")


if __name__ == "__main__":
    main()
