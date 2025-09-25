# 🗺️ Sitemap Automation Guide

## Overview
Automated sitemap.xml management for programmatic SEO landing pages. Ensures all generated pages get indexed by search engines.

## Scripts

### 1. `update_sitemap.py` 
**Auto-updates sitemap with new pages**
```bash
python tools/update_sitemap.py
```
- Scans `landing/generated/` for new pages
- Adds missing URLs to existing sitemap.xml
- **Runs automatically** after landing page generation

### 2. `rebuild_sitemap.py`
**Complete sitemap rebuild from scratch**
```bash
python tools/rebuild_sitemap.py
```
- Scans entire website structure
- Rebuilds sitemap.xml completely
- Use when you want a fresh start

### 3. `generate_landing_pages.py` (Enhanced)
**Now includes automatic sitemap updates**
```bash
XAI_API_KEY="your-key" python tools/generate_landing_pages.py \
  --groups /home/nar/learning/service_location_groups.json \
  --output landing/generated \
  --skip-existing
```
- Generates landing pages
- **Automatically updates sitemap.xml** when done

## Current Sitemap Structure

✅ **38 Total URLs** in sitemap:
- **Core Pages** (7): Homepage, quote, blog, partners, legal
- **Blog Articles** (4): End-of-summer, recycling, upcycling, organization
- **Location Pages** (8): Howard County cities
- **Static Landing Pages** (13): Manual landing pages
- **Generated Landing Pages** (6): Programmatic SEO pages

## Workflow

### For New Landing Page Generation:
1. Generate pages: `python tools/generate_landing_pages.py ...`
2. Sitemap updates **automatically**
3. That's it! 🎉

### For Manual Sitemap Updates:
```bash
# Add new pages to existing sitemap
python tools/update_sitemap.py

# Complete rebuild (use sparingly)
python tools/rebuild_sitemap.py
```

## SEO Benefits

🎯 **Automatic Indexing**: New pages get found by Google faster  
📈 **Better Rankings**: Complete sitemap helps search visibility  
⚡ **Zero Manual Work**: Fully automated with page generation  
🔄 **Always Current**: Sitemap stays synchronized with content  

## Next Steps

Ready to generate all 84 location-targeted pages? Run:

```bash
cd /home/nar/Documents/sawyers
XAI_API_KEY="your-key" \
python tools/generate_landing_pages.py \
  --groups /home/nar/learning/service_location_groups.json \
  --output landing/generated \
  --skip-existing
```

Sitemap will update automatically! 🚀
