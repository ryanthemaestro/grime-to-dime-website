#!/usr/bin/env python3
"""
Update all review counts from "15 reviews" to "16 reviews" across the entire website.
Includes main pages, location pages, landing pages, and all generated SEO pages.
"""

import os
import re
from pathlib import Path
from typing import List, Tuple


def find_html_files(project_root: Path) -> List[Path]:
    """Find all HTML files in the project."""
    html_files = []
    
    # Main pages
    main_files = [
        "index.html",
        "quote/index.html", 
        "thank-you.html",
        "privacy-policy.html",
        "terms.html"
    ]
    
    for file_path in main_files:
        full_path = project_root / file_path
        if full_path.exists():
            html_files.append(full_path)
    
    # Location pages
    locations_dir = project_root / "locations"
    if locations_dir.exists():
        for item in locations_dir.iterdir():
            if item.is_dir():
                index_file = item / "index.html"
                if index_file.exists():
                    html_files.append(index_file)
    
    # Static landing pages
    landing_dir = project_root / "landing"
    if landing_dir.exists():
        for item in landing_dir.iterdir():
            if item.is_dir() and item.name != "generated":
                index_file = item / "index.html"
                if index_file.exists():
                    html_files.append(index_file)
    
    # Generated landing pages (the big batch!)
    generated_dir = project_root / "landing" / "generated"
    if generated_dir.exists():
        for item in generated_dir.iterdir():
            if item.is_dir():
                index_file = item / "index.html"
                if index_file.exists():
                    html_files.append(index_file)
    
    # Blog pages
    blog_dir = project_root / "blog"
    if blog_dir.exists():
        for item in blog_dir.iterdir():
            if item.is_dir():
                index_file = item / "index.html"
                if index_file.exists():
                    html_files.append(index_file)
    
    return html_files


def update_reviews_in_file(file_path: Path) -> Tuple[bool, int]:
    """Update review counts in a single file. Returns (was_updated, num_changes)."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Update all variations of "15 reviews"
        patterns_and_replacements = [
            # Meta descriptions and SEO content
            (r'\b15 reviews\b', '16 reviews'),
            (r'\b15-review\b', '16-review'),
            (r'\bfifteen reviews\b', 'sixteen reviews'),
            (r'\bFifteen reviews\b', 'Sixteen reviews'),
            
            # JSON-LD and structured data
            (r'"reviewCount": ?15\b', '"reviewCount": 16'),
            (r'"reviewCount":"15"', '"reviewCount":"16"'),
            
            # Rating displays and badges
            (r'15 5-star reviews', '16 5-star reviews'),
            (r'15 five-star reviews', '16 five-star reviews'),
            (r'Based on 15 reviews', 'Based on 16 reviews'),
            (r'from 15 reviews', 'from 16 reviews'),
            (r'\(15 reviews\)', '(16 reviews)'),
            
            # Open Graph and Twitter meta
            (r'content="[^"]*15 reviews[^"]*"', lambda m: m.group(0).replace('15 reviews', '16 reviews')),
            
            # Any remaining instances
            (r'15(?=\s+reviews)', '16'),
        ]
        
        changes_made = 0
        
        for pattern, replacement in patterns_and_replacements:
            if callable(replacement):
                # For complex replacements like Open Graph
                new_content, count = re.subn(pattern, replacement, content)
            else:
                new_content, count = re.subn(pattern, replacement, content, flags=re.IGNORECASE)
            
            if count > 0:
                content = new_content
                changes_made += count
        
        # Write back if changes were made
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, changes_made
        
        return False, 0
        
    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")
        return False, 0


def main():
    """Main execution function."""
    print("🔄 Updating review counts from 15 to 16 across entire website")
    print("=" * 65)
    
    project_root = Path(__file__).parent.parent
    html_files = find_html_files(project_root)
    
    print(f"📁 Found {len(html_files)} HTML files to check")
    
    updated_files = []
    total_changes = 0
    
    for file_path in html_files:
        was_updated, changes_made = update_reviews_in_file(file_path)
        
        if was_updated:
            relative_path = file_path.relative_to(project_root)
            updated_files.append((relative_path, changes_made))
            total_changes += changes_made
            print(f"✅ {relative_path} - {changes_made} changes")
    
    print("\n" + "=" * 65)
    print(f"🎯 Update Summary:")
    print(f"  • Files checked: {len(html_files)}")
    print(f"  • Files updated: {len(updated_files)}")
    print(f"  • Total changes: {total_changes}")
    
    if updated_files:
        print(f"\n📈 Updated Files:")
        for file_path, changes in updated_files:
            print(f"  • {file_path} ({changes} changes)")
        
        print(f"\n🚀 All review counts updated from 15 to 16!")
        print(f"💡 Social proof increased across {len(updated_files)} pages")
        
        # Check a few categories
        main_pages = [f for f, _ in updated_files if not any(x in str(f) for x in ['locations/', 'landing/', 'blog/'])]
        location_pages = [f for f, _ in updated_files if 'locations/' in str(f)]
        static_landing_pages = [f for f, _ in updated_files if 'landing/' in str(f) and 'generated' not in str(f)]
        generated_pages = [f for f, _ in updated_files if 'landing/generated/' in str(f)]
        
        print(f"\n📊 Breakdown:")
        print(f"  • Main pages: {len(main_pages)}")
        print(f"  • Location pages: {len(location_pages)}")
        print(f"  • Static landing pages: {len(static_landing_pages)}")
        print(f"  • Generated SEO pages: {len(generated_pages)}")
        
    else:
        print("ℹ️  No files needed updating (already at 16 reviews or no review mentions found)")


if __name__ == "__main__":
    main()
