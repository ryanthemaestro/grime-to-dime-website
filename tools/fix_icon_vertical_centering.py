#!/usr/bin/env python3
"""
Fix icon vertical centering - icons are at top of circles, need to be centered
"""

from pathlib import Path

LOCATIONS = [
    "annapolis-junction-md", "catonsville-md", "clarksville-md", "columbia-md",
    "elkridge-md", "ellicott-city-md", "laurel-md", "savage-md"
]

VERTICAL_CENTER_FIX = '''
    <style>
        /* CRITICAL FIX: Vertically center icons in circles */
        .benefit-card i {
            font-size: 3rem !important;
            color: #ff3333 !important;
            margin-bottom: 1rem !important;
            display: inline-flex !important;
            align-items: center !important;
            justify-content: center !important;
            width: 80px !important;
            height: 80px !important;
            line-height: 1 !important;
            vertical-align: middle !important;
        }
        
        /* Ensure Font Awesome icons are centered */
        .benefit-card i::before,
        .service-icon i::before,
        .process-icon i::before {
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            width: 100% !important;
            height: 100% !important;
        }
        
        /* Service icons fix */
        .service-icon {
            width: 80px !important;
            height: 80px !important;
            background: linear-gradient(135deg, #ff3333 0%, #cc0000 100%) !important;
            border-radius: 50% !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            margin: 0 auto 1.5rem !important;
            font-size: 2rem !important;
            color: white !important;
            box-shadow: 0 8px 16px rgba(255, 51, 51, 0.3) !important;
            transition: all 0.3s ease !important;
        }
        
        .service-icon i {
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            width: 100% !important;
            height: 100% !important;
            margin: 0 !important;
            padding: 0 !important;
            line-height: 1 !important;
        }
        
        /* Process icons fix */
        .process-icon {
            width: 100px !important;
            height: 100px !important;
            background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 100%) !important;
            border-radius: 50% !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            margin: 0 auto 1.5rem !important;
            font-size: 2.5rem !important;
            color: #ff3333 !important;
            box-shadow: 0 8px 24px rgba(15, 15, 35, 0.3) !important;
            transition: all 0.3s ease !important;
            border: 4px solid #ff3333 !important;
        }
        
        .process-icon i {
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            width: 100% !important;
            height: 100% !important;
            margin: 0 !important;
            padding: 0 !important;
            line-height: 1 !important;
        }
        
        /* Make sure Font Awesome loads properly */
        .fas, .fab, .far {
            font-family: "Font Awesome 6 Free" !important;
            font-weight: 900 !important;
            font-style: normal !important;
            font-variant: normal !important;
            text-rendering: auto !important;
            -webkit-font-smoothing: antialiased !important;
        }
    </style>
'''

def fix_location(slug):
    """Apply vertical centering fix"""
    
    file_path = Path(f"/home/nar/Documents/sawyers/locations/{slug}/index.html")
    
    if not file_path.exists():
        print(f"⚠️  Skipping {slug} - file not found")
        return
    
    with open(file_path, 'r') as f:
        html = f.read()
    
    # Skip if already has the critical fix
    if 'CRITICAL FIX: Vertically center icons' in html:
        print(f"⏭️  Skipping {slug} - already has vertical center fix")
        return
    
    # Insert the fix right before the closing </head> tag
    html = html.replace('</head>', f'{VERTICAL_CENTER_FIX}\n</head>')
    
    print(f"✅ Fixed vertical centering for {slug}")
    
    with open(file_path, 'w') as f:
        f.write(html)

def main():
    """Fix all location pages"""
    print("🔧 Fixing icon vertical centering...\n")
    
    for slug in LOCATIONS:
        fix_location(slug)
    
    print("\n✨ All icons now perfectly centered!")

if __name__ == "__main__":
    main()
