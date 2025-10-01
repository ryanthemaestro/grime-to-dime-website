#!/usr/bin/env python3
"""
Fix hero to be full viewport height and properly load Font Awesome brands icons
"""

from pathlib import Path

LOCATIONS = [
    "annapolis-junction-md", "catonsville-md", "clarksville-md", "columbia-md",
    "elkridge-md", "ellicott-city-md", "laurel-md", "savage-md"
]

def fix_location(slug):
    """Fix hero height and Font Awesome"""
    
    file_path = Path(f"/home/nar/Documents/sawyers/locations/{slug}/index.html")
    
    if not file_path.exists():
        print(f"⚠️  Skipping {slug} - file not found")
        return
    
    with open(file_path, 'r') as f:
        html = f.read()
    
    # Fix 1: Make hero full viewport height
    # Replace the existing hero min-height style
    html = html.replace(
        '            min-height: 60vh;',
        '            min-height: 100vh;'
    )
    
    # Fix 2: Add specific mobile override for hero height
    # Find the mobile hero section and ensure it's 100vh
    if '/* Hero section mobile */' in html:
        # Add full viewport height for mobile hero
        html = html.replace(
            '            /* Hero section mobile */',
            '''            /* Hero section mobile */
            .hero {
                min-height: 100vh !important;
            }
            '''
        )
    
    # Fix 3: Ensure Font Awesome Brands loads properly
    # Update the noscript tag to be properly closed
    html = html.replace(
        '<noscript><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" integrity="sha512-9usAa10IRO0HhonpyAIVpjrylPvoDwiPUiKdWk5t3PyolY1cOd4DSE0Ga+ri4AuTroPR5aQvXU9xC6qOPnzFeg==" crossorigin="anonymous">',
        '<noscript><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" integrity="sha512-9usAa10IRO0HhonpyAIVpjrylPvoDwiPUiKdWk5t3PyolY1cOd4DSE0Ga+ri4AuTroPR5aQvXU9xC6qOPnzFeg==" crossorigin="anonymous"></noscript>'
    )
    
    # Fix 4: Add explicit Font Awesome CSS for brands
    if '/* Make sure Font Awesome loads properly */' in html:
        html = html.replace(
            '        /* Make sure Font Awesome loads properly */',
            '''        /* Make sure Font Awesome loads properly */
        @font-face {
            font-family: 'Font Awesome 6 Brands';
            src: url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/webfonts/fa-brands-400.woff2') format('woff2');
            font-weight: 400;
            font-display: block;
        }
        '''
        )
        
        html = html.replace(
            '        .fas, .fab, .far {',
            '''        .fab {
            font-family: "Font Awesome 6 Brands" !important;
            font-weight: 400 !important;
        }
        
        .fas, .far {'''
        )
    
    print(f"✅ Fixed {slug}")
    
    with open(file_path, 'w') as f:
        f.write(html)

def main():
    """Fix all location pages"""
    print("🔧 Fixing hero full-screen and Font Awesome icons...\n")
    
    for slug in LOCATIONS:
        fix_location(slug)
    
    print("\n✨ All pages fixed!")

if __name__ == "__main__":
    main()
