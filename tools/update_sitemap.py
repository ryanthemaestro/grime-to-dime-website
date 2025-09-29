#!/usr/bin/env python3
"""
Automated sitemap.xml generator for programmatic SEO landing pages.
Scans landing/generated directory and adds new pages to sitemap.xml
"""

import os
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime
from typing import List, Set


def get_existing_urls(sitemap_path: Path) -> Set[str]:
    """Extract existing URLs from current sitemap."""
    existing_urls = set()
    
    if not sitemap_path.exists():
        print(f"⚠️  Sitemap not found at {sitemap_path}")
        return existing_urls
    
    try:
        tree = ET.parse(sitemap_path)
        root = tree.getroot()
        
        # Handle XML namespace
        namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        
        for url in root.findall('.//ns:url', namespace):
            loc = url.find('ns:loc', namespace)
            if loc is not None:
                existing_urls.add(loc.text)
        
        print(f"✅ Found {len(existing_urls)} existing URLs in sitemap")
        return existing_urls
        
    except ET.ParseError as e:
        print(f"❌ Error parsing sitemap: {e}")
        return existing_urls


def scan_generated_landing_pages(landing_dir: Path) -> List[dict]:
    """Scan landing directory for SEO landing pages (exclude static pages)."""
    landing_pages = []
    
    if not landing_dir.exists():
        print(f"⚠️  Landing directory not found: {landing_dir}")
        return landing_pages
    
    # Static pages to exclude (manually created)
    static_pages = {
        'appliance-removal', 'basement-cleanout', 'construction-debris-removal',
        'estate-cleanout', 'exact', 'garage-cleanout', 'hot-tub', 'local',
        'mattress-disposal', 'sofa-removal', 'storage-unit-cleanout',
        'treadmill-removal', 'tv-disposal'
    }
    
    for page_dir in landing_dir.iterdir():
        if page_dir.is_dir() and page_dir.name not in static_pages:
            index_file = page_dir / "index.html"
            if index_file.exists():
                # Create URL from directory name
                url = f"https://grimetodime.com/landing/{page_dir.name}/"
                
                # Get last modified time
                stat = index_file.stat()
                lastmod = datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d')
                
                landing_pages.append({
                    'url': url,
                    'lastmod': lastmod,
                    'changefreq': 'monthly',
                    'priority': '0.7'
                })
    
    print(f"✅ Found {len(landing_pages)} generated landing pages")
    return landing_pages


def create_sitemap_entry(url: str, lastmod: str, changefreq: str, priority: str) -> str:
    """Create XML entry for a single URL."""
    return f"""  <url>
    <loc>{url}</loc>
    <lastmod>{lastmod}</lastmod>
    <changefreq>{changefreq}</changefreq>
    <priority>{priority}</priority>
  </url>"""


def update_sitemap(sitemap_path: Path, landing_dir: Path):
    """Update sitemap.xml with new generated landing pages."""
    print("🚀 Updating sitemap.xml with generated landing pages")
    print("=" * 60)
    
    # Get existing URLs and new pages
    existing_urls = get_existing_urls(sitemap_path)
    new_pages = scan_generated_landing_pages(landing_dir)
    
    # Filter out pages that already exist
    new_urls = [page for page in new_pages if page['url'] not in existing_urls]
    
    if not new_urls:
        print("✅ No new pages to add - sitemap is up to date")
        return
    
    print(f"📝 Adding {len(new_urls)} new URLs to sitemap:")
    for page in new_urls:
        print(f"  • {page['url']}")
    
    # Read current sitemap content
    with open(sitemap_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find insertion point (before closing </urlset>)
    closing_tag = '</urlset>'
    insertion_point = content.rfind(closing_tag)
    
    if insertion_point == -1:
        print("❌ Could not find </urlset> tag in sitemap")
        return
    
    # Create new entries
    new_entries = []
    new_entries.append("\n  <!-- Generated Landing Pages -->")
    
    for page in new_urls:
        entry = create_sitemap_entry(
            page['url'], 
            page['lastmod'], 
            page['changefreq'], 
            page['priority']
        )
        new_entries.append(entry)
    
    # Insert new entries
    new_content = (
        content[:insertion_point] + 
        '\n'.join(new_entries) + 
        '\n\n' + 
        content[insertion_point:]
    )
    
    # Write updated sitemap
    with open(sitemap_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ Updated sitemap with {len(new_urls)} new URLs")
    print(f"📁 Sitemap saved to: {sitemap_path}")


def main():
    """Main execution function."""
    # Paths
    project_root = Path(__file__).parent.parent
    sitemap_path = project_root / "sitemap.xml"
    landing_dir = project_root / "landing"
    
    # Update sitemap
    update_sitemap(sitemap_path, landing_dir)
    
    print("\n🎯 Sitemap automation complete!")
    print("💡 Tip: Run this after generating new landing pages")


def integrate_with_generator():
    """Integration hook for the landing page generator."""
    main()


if __name__ == "__main__":
    main()
