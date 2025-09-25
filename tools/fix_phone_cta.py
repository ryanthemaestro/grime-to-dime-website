#!/usr/bin/env python3
"""
Fix the landing page generator to use phone links for Call Now buttons
"""

from pathlib import Path

def main():
    path = Path('tools/generate_landing_pages.py')
    text = path.read_text()
    
    # Find the CTA button in the HTML template and change it from form link to phone link
    old_cta = '<a href="#quoteForm" class="cta-button">{cta_button_label}</a>'
    new_cta = '<a href="tel:+14103006743" class="cta-button gfn">{cta_button_label}</a>'
    
    if old_cta in text:
        text = text.replace(old_cta, new_cta)
        path.write_text(text)
        print("✅ Updated CTA button to use phone link!")
    else:
        print("❌ Could not find CTA button pattern in template")

if __name__ == "__main__":
    main()
