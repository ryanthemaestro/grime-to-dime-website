#!/usr/bin/env python3
"""
Fix process icon overlap on mobile for "How It Works" section
"""

from pathlib import Path

LOCATIONS = [
    "annapolis-junction-md", "catonsville-md", "clarksville-md", "columbia-md",
    "elkridge-md", "ellicott-city-md", "laurel-md", "savage-md"
]

MOBILE_FIX_CSS = '''
        /* Mobile process icons - prevent overlap */
        @media (max-width: 768px) {
            .process-icon {
                width: 70px !important;
                height: 70px !important;
                font-size: 1.8rem !important;
                margin: 0 auto 1rem !important;
            }
            
            .process-step h3 {
                font-size: 1.25rem;
                margin-bottom: 0.75rem;
            }
            
            .process-step p {
                font-size: 0.95rem;
            }
        }
        
        @media (max-width: 480px) {
            .process-icon {
                width: 60px !important;
                height: 60px !important;
                font-size: 1.5rem !important;
                margin: 0 auto 0.75rem !important;
            }
            
            .process-step h3 {
                font-size: 1.1rem;
            }
            
            .process-step p {
                font-size: 0.9rem;
            }
        }
'''

def fix_location(slug):
    """Fix process icons mobile overlap"""
    
    file_path = Path(f"/home/nar/Documents/sawyers/locations/{slug}/index.html")
    
    if not file_path.exists():
        print(f"⚠️  Skipping {slug} - file not found")
        return
    
    with open(file_path, 'r') as f:
        html = f.read()
    
    # Check if fix already applied
    if 'Mobile process icons - prevent overlap' in html:
        print(f"⏭️  Skipping {slug} - already has mobile icon fix")
        return
    
    # Find the existing mobile process icon styles and replace them
    # Look for the @media (max-width: 768px) section with process-icon
    
    # Find where to insert - right before the closing </style> before </head>
    if '</style>\n\n    </style>' in html:
        # Insert before the second </style>
        html = html.replace(
            '</style>\n\n    </style>',
            f'{MOBILE_FIX_CSS}\n    </style>\n\n    </style>'
        )
    elif '/* Make sure Font Awesome loads properly */' in html:
        # Insert before Font Awesome section
        html = html.replace(
            '        /* Make sure Font Awesome loads properly */',
            f'{MOBILE_FIX_CSS}\n        /* Make sure Font Awesome loads properly */'
        )
    else:
        print(f"⚠️  Could not find insertion point in {slug}")
        return
    
    print(f"✅ Fixed {slug}")
    
    with open(file_path, 'w') as f:
        f.write(html)

def main():
    """Fix all location pages"""
    print("🔧 Fixing process icon overlap on mobile...\n")
    
    for slug in LOCATIONS:
        fix_location(slug)
    
    print("\n✨ All mobile process icons fixed!")

if __name__ == "__main__":
    main()
