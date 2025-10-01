#!/usr/bin/env python3
"""
Enhance ALL location pages with modern design improvements
"""

from pathlib import Path

# Location data
LOCATIONS = {
    "annapolis-junction-md": {
        "name": "Annapolis Junction",
        "testimonial": {"name": "David H.", "text": "Quick, professional service! They cleared out my garage in Annapolis Junction same day. Highly recommend!"}
    },
    "catonsville-md": {
        "name": "Catonsville",
        "testimonial": {"name": "Sarah M.", "text": "Great experience from start to finish. They made my Catonsville home cleanout stress-free and affordable."}
    },
    "clarksville-md": {
        "name": "Clarksville",
        "testimonial": {"name": "James P.", "text": "Excellent service! They handled our estate cleanout in Clarksville with care and professionalism."}
    },
    "columbia-md": {
        "name": "Columbia",
        "testimonial": {"name": "Lisa K.", "text": "The team was punctual, efficient, and very friendly. Made our Columbia office cleanout a breeze!"}
    },
    "elkridge-md": {
        "name": "Elkridge",
        "testimonial": {"name": "Michael R.", "text": "Local team that knows Elkridge well. Fast response and fair pricing. Will use them again!"}
    },
    "ellicott-city-md": {
        "name": "Ellicott City",
        "testimonial": {"name": "Jennifer W.", "text": "Amazing service! They removed an old hot tub from my Ellicott City backyard in no time. Very professional!"}
    },
    "laurel-md": {
        "name": "Laurel",
        "testimonial": {"name": "Robert T.", "text": "Called them for a last-minute cleanout in Laurel. They fit me in same day and did a fantastic job!"}
    },
    "savage-md": {
        "name": "Savage",
        "testimonial": {"name": "Amanda C.", "text": "Professional crew that took great care removing items from my Savage home. Highly recommend!"}
    }
}

STATS_CSS = '''
    <style>
        /* Enhanced location page styles */
        .hero {
            position: relative;
            background: linear-gradient(135deg, rgba(15,15,35,0.95) 0%, rgba(26,26,46,0.9) 100%), 
                        url('/images/optimized/warehouse-after-junk-removal-hero-q60.webp') center/cover;
            min-height: 60vh;
        }
        
        .location-hero {
            text-align: center;
            padding: 4rem 1rem;
        }
        
        .location-hero h1 {
            font-size: clamp(2rem, 5vw, 3.5rem);
            margin-bottom: 1rem;
            color: #fff;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .location-hero h2 {
            font-size: clamp(1.2rem, 3vw, 1.8rem);
            margin-bottom: 2rem;
            color: #f0f0f0;
            font-weight: 400;
        }
        
        .stats-bar {
            background: linear-gradient(135deg, #ff3333 0%, #cc0000 100%);
            padding: 1.5rem 1rem;
            margin: 0;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        .stats-container {
            max-width: 1200px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 2rem;
            text-align: center;
        }
        
        .stat-item {
            color: white;
        }
        
        .stat-number {
            font-size: 2.5rem;
            font-weight: 800;
            display: block;
            margin-bottom: 0.25rem;
        }
        
        .stat-label {
            font-size: 1rem;
            opacity: 0.95;
        }
        
        .testimonial-section {
            background: #f8f9fa;
            padding: 3rem 1rem;
            margin: 3rem 0;
        }
        
        .testimonial-card {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            padding: 2.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            position: relative;
        }
        
        .testimonial-card::before {
            content: '"';
            position: absolute;
            top: -10px;
            left: 20px;
            font-size: 6rem;
            color: #ff3333;
            opacity: 0.2;
            font-family: Georgia, serif;
        }
        
        .testimonial-text {
            font-size: 1.25rem;
            line-height: 1.8;
            color: #333;
            margin-bottom: 1.5rem;
            font-style: italic;
        }
        
        .testimonial-author {
            display: flex;
            align-items: center;
            gap: 1rem;
        }
        
        .author-avatar {
            width: 50px;
            height: 50px;
            background: linear-gradient(135deg, #ff3333 0%, #cc0000 100%);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 1.5rem;
            font-weight: bold;
        }
        
        .author-info {
            text-align: left;
        }
        
        .author-name {
            font-weight: 700;
            color: #333;
            margin-bottom: 0.25rem;
        }
        
        .author-location {
            color: #666;
            font-size: 0.9rem;
        }
        
        .stars-display {
            color: #ffc107;
            margin-bottom: 1rem;
        }
    </style>
'''

STATS_BAR = '''
    <section class="stats-bar">
        <div class="stats-container">
            <div class="stat-item">
                <span class="stat-number">100%</span>
                <span class="stat-label">Satisfaction Guaranteed</span>
            </div>
            <div class="stat-item">
                <span class="stat-number">Same Day</span>
                <span class="stat-label">Service Available</span>
            </div>
            <div class="stat-item">
                <span class="stat-number">16+</span>
                <span class="stat-label">5-Star Reviews</span>
            </div>
            <div class="stat-item">
                <span class="stat-number">Licensed</span>
                <span class="stat-label">& Fully Insured</span>
            </div>
        </div>
    </section>
'''

def enhance_location(slug, data):
    """Enhance a specific location page"""
    
    file_path = Path(f"/home/nar/Documents/sawyers/locations/{slug}/index.html")
    
    if not file_path.exists():
        print(f"⚠️  Skipping {slug} - file not found")
        return
    
    with open(file_path, 'r') as f:
        html = f.read()
    
    # Skip if already enhanced
    if '.stats-bar {' in html:
        print(f"⏭️  Skipping {slug} - already enhanced")
        return
    
    # 1. Insert CSS before </head>
    html = html.replace('</head>', f'{STATS_CSS}</head>')
    
    # 2. Add hero-content class wrapping for better centering  
    html = html.replace(
        '<div class="hero-content">',
        '<div class="hero-content location-hero">'
    )
    
    # 3. Add stats bar after hero section
    html = html.replace(
        '    </section>\n\n    <section id="about" class="about">',
        f'    </section>\n{STATS_BAR}\n    <section id="about" class="about">'
    )
    
    # 4. Add testimonial section before FAQ
    testimonial_section = f'''
    <section id="testimonial" class="testimonial-section">
        <div class="testimonial-card">
            <div class="stars-display">
                <i class="fas fa-star"></i>
                <i class="fas fa-star"></i>
                <i class="fas fa-star"></i>
                <i class="fas fa-star"></i>
                <i class="fas fa-star"></i>
            </div>
            <p class="testimonial-text">"{data["testimonial"]["text"]}"</p>
            <div class="testimonial-author">
                <div class="author-avatar">{data["testimonial"]["name"][0]}</div>
                <div class="author-info">
                    <div class="author-name">{data["testimonial"]["name"]}</div>
                    <div class="author-location">{data["name"]}, MD</div>
                </div>
            </div>
        </div>
    </section>

'''
    
    html = html.replace(
        '    <section id="faq" class="about">',
        f'{testimonial_section}    <section id="faq" class="about">'
    )
    
    # 5. Update navigation to include Reviews
    html = html.replace(
        '<li><a href="#about">About</a></li>',
        '<li><a href="#testimonial">Reviews</a></li>'
    )
    
    # Write enhanced file
    with open(file_path, 'w') as f:
        f.write(html)
    
    print(f"✅ Enhanced {slug}")

def main():
    """Enhance all location pages"""
    print("🚀 Enhancing all location pages...\n")
    
    for slug, data in LOCATIONS.items():
        enhance_location(slug, data)
    
    print("\n✨ All location pages enhanced!")

if __name__ == "__main__":
    main()
