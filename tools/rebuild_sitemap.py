#!/usr/bin/env python3
"""
Complete sitemap.xml rebuilder that scans the entire website.
Use this to rebuild sitemap from scratch or when you want a full refresh.
"""

import os
from pathlib import Path
from datetime import datetime
from typing import List


def scan_website_pages(project_root: Path) -> List[dict]:
    """Scan entire website for pages to include in sitemap."""
    pages = []
    
    # Core pages
    core_pages = [
        {"path": "", "priority": "1.0", "changefreq": "weekly"},  # Homepage
        {"path": "quote/", "priority": "0.9", "changefreq": "monthly"},
        {"path": "blog/", "priority": "0.8", "changefreq": "weekly"},
        {"path": "partners/", "priority": "0.6", "changefreq": "monthly"},
        {"path": "thank-you.html", "priority": "0.3", "changefreq": "yearly"},
        {"path": "privacy-policy.html", "priority": "0.4", "changefreq": "yearly"},
        {"path": "terms.html", "priority": "0.4", "changefreq": "yearly"},
    ]
    
    for page in core_pages:
        full_path = project_root / page["path"] if page["path"] else project_root / "index.html"
        if full_path.exists() or page["path"] == "":  # Homepage always exists
            pages.append({
                "url": f"https://grimetodime.com/{page['path']}",
                "lastmod": datetime.now().strftime('%Y-%m-%d'),
                "changefreq": page["changefreq"],
                "priority": page["priority"],
                "category": "core"
            })
    
    # Blog posts
    blog_dir = project_root / "blog"
    if blog_dir.exists():
        for item in blog_dir.iterdir():
            if item.is_dir() and (item / "index.html").exists():
                pages.append({
                    "url": f"https://grimetodime.com/blog/{item.name}/",
                    "lastmod": datetime.now().strftime('%Y-%m-%d'),
                    "changefreq": "monthly",
                    "priority": "0.7",
                    "category": "blog"
                })
    
    # Location pages
    locations_dir = project_root / "locations"
    if locations_dir.exists():
        for item in locations_dir.iterdir():
            if item.is_dir() and (item / "index.html").exists():
                pages.append({
                    "url": f"https://grimetodime.com/locations/{item.name}/",
                    "lastmod": datetime.now().strftime('%Y-%m-%d'),
                    "changefreq": "monthly",
                    "priority": "0.7",
                    "category": "locations"
                })
    
    # Static landing pages
    landing_dir = project_root / "landing"
    if landing_dir.exists():
        for item in landing_dir.iterdir():
            if item.is_dir() and item.name != "generated" and (item / "index.html").exists():
                pages.append({
                    "url": f"https://grimetodime.com/landing/{item.name}/",
                    "lastmod": datetime.now().strftime('%Y-%m-%d'),
                    "changefreq": "monthly",
                    "priority": "0.7",
                    "category": "landing_static"
                })
    
    # Generated landing pages
    generated_dir = project_root / "landing" / "generated"
    if generated_dir.exists():
        for item in generated_dir.iterdir():
            if item.is_dir() and (item / "index.html").exists():
                stat = (item / "index.html").stat()
                lastmod = datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d')
                
                pages.append({
                    "url": f"https://grimetodime.com/landing/{item.name}/",
                    "lastmod": lastmod,
                    "changefreq": "monthly",
                    "priority": "0.7",
                    "category": "landing_generated"
                })
    
    return pages


def generate_sitemap_xml(pages: List[dict]) -> str:
    """Generate complete sitemap.xml content."""
    xml_header = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'''
    
    xml_footer = '''</urlset>'''
    
    # Group pages by category
    categories = {
        "core": "Core Pages",
        "blog": "Blog Articles", 
        "landing_static": "Static Landing Pages",
        "landing_generated": "Generated Landing Pages",
        "locations": "Service Areas"
    }
    
    xml_content = [xml_header]
    
    for category, title in categories.items():
        category_pages = [p for p in pages if p.get("category") == category]
        if category_pages:
            xml_content.append(f"\n  <!-- {title} -->")
            
            for page in sorted(category_pages, key=lambda x: x["url"]):
                xml_content.append(f'''  <url>
    <loc>{page["url"]}</loc>
    <lastmod>{page["lastmod"]}</lastmod>
    <changefreq>{page["changefreq"]}</changefreq>
    <priority>{page["priority"]}</priority>
  </url>''')
    
    xml_content.append(xml_footer)
    xml_content.append('')  # Final newline
    
    return '\n'.join(xml_content)


def main():
    """Main execution function."""
    print("🗺️  Rebuilding complete sitemap.xml")
    print("=" * 50)
    
    project_root = Path(__file__).parent.parent
    sitemap_path = project_root / "sitemap.xml"
    
    # Scan website
    pages = scan_website_pages(project_root)
    
    # Generate sitemap
    sitemap_xml = generate_sitemap_xml(pages)
    
    # Write sitemap
    with open(sitemap_path, 'w', encoding='utf-8') as f:
        f.write(sitemap_xml)
    
    print(f"✅ Generated sitemap with {len(pages)} URLs")
    print(f"📁 Saved to: {sitemap_path}")
    
    # Show summary by category
    categories = {}
    for page in pages:
        cat = page.get("category", "unknown")
        categories[cat] = categories.get(cat, 0) + 1
    
    print("\n📊 URL breakdown:")
    for category, count in categories.items():
        print(f"  • {category}: {count} pages")
    
    print("\n🎯 Sitemap rebuild complete!")


if __name__ == "__main__":
    main()
