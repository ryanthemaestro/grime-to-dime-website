#!/usr/bin/env python3
"""
Fix HTML structure issues and Font Awesome icon loading
"""

from pathlib import Path
import re

LOCATIONS = [
    "annapolis-junction-md", "catonsville-md", "clarksville-md", "columbia-md",
    "elkridge-md", "ellicott-city-md", "laurel-md", "savage-md"
]

def fix_location(slug):
    """Fix HTML structure and icon loading"""
    
    file_path = Path(f"/home/nar/Documents/sawyers/locations/{slug}/index.html")
    
    if not file_path.exists():
        print(f"⚠️  Skipping {slug} - file not found")
        return
    
    with open(file_path, 'r') as f:
        html = f.read()
    
    # Fix 1: Remove duplicate/broken </style> tags
    # Find the section between first </style> and </head>
    # There should be multiple style blocks that are broken
    
    # Remove orphan style tags and content
    html = re.sub(r'</style>\s*</style>', '</style>', html)
    html = re.sub(r'</style>\s*\.stars-display\s*\{[^}]+\}\s*</style>', '</style>', html)
    
    # Fix 2: Change Font Awesome from lazy load to immediate load
    html = html.replace(
        '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" integrity="sha512-9usAa10IRO0HhonpyAIVpjrylPvoDwiPUiKdWk5t3PyolY1cOd4DSE0Ga+ri4AuTroPR5aQvXU9xC6qOPnzFeg==" crossorigin="anonymous" media="print" onload="this.media=\'all\'">',
        '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" integrity="sha512-9usAa10IRO0HhonpyAIVpjrylPvoDwiPUiKdWk5t3PyolY1cOd4DSE0Ga+ri4AuTroPR5aQvXU9xC6qOPnzFeg==" crossorigin="anonymous">'
    )
    
    # Add noscript fallback for Font Awesome
    if '<noscript><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome' not in html:
        html = html.replace(
            '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"',
            '''<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" integrity="sha512-9usAa10IRO0HhonpyAIVpjrylPvoDwiPUiKdWk5t3PyolY1cOd4DSE0Ga+ri4AuTroPR5aQvXU9xC6qOPnzFeg==" crossorigin="anonymous">
    <noscript><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"'''
        )
    
    print(f"✅ Fixed {slug}")
    
    with open(file_path, 'w') as f:
        f.write(html)

def main():
    """Fix all location pages"""
    print("🔧 Fixing HTML structure and Font Awesome loading...\n")
    
    for slug in LOCATIONS:
        fix_location(slug)
    
    print("\n✨ All pages fixed!")

if __name__ == "__main__":
    main()
