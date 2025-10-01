#!/usr/bin/env python3
"""
Remove Instagram icon and update testimonials with real reviews from quote page
"""

from pathlib import Path

LOCATIONS = {
    "annapolis-junction-md": {
        "name": "Annapolis Junction",
        "testimonial": {
            "name": "Edie",
            "location": "Columbia, MD",
            "text": "Great experience with Grime to Dime. They were on time, reasonably priced, and professional. Will definitely recommend."
        }
    },
    "catonsville-md": {
        "name": "Catonsville",
        "testimonial": {
            "name": "Robert Mcmillen",
            "location": "Odenton, MD",
            "text": "They were prompt, worked with my schedule, and fantastic with their price. I will not only use them again, but will happily recommend them to anyone in the future."
        }
    },
    "clarksville-md": {
        "name": "Clarksville",
        "testimonial": {
            "name": "David P.",
            "location": "Baltimore, MD",
            "text": "Timely, good communication, and very polite. Accepted Venmo. Performed the job well quickly. Definitely recommend."
        }
    },
    "columbia-md": {
        "name": "Columbia",
        "testimonial": {
            "name": "Edie",
            "location": "Columbia, MD",
            "text": "Great experience with Grime to Dime. They were on time, reasonably priced, and professional. Will definitely recommend."
        }
    },
    "elkridge-md": {
        "name": "Elkridge",
        "testimonial": {
            "name": "Robert Mcmillen",
            "location": "Odenton, MD",
            "text": "They were prompt, worked with my schedule, and fantastic with their price. I will not only use them again, but will happily recommend them to anyone in the future."
        }
    },
    "ellicott-city-md": {
        "name": "Ellicott City",
        "testimonial": {
            "name": "David P.",
            "location": "Baltimore, MD",
            "text": "Timely, good communication, and very polite. Accepted Venmo. Performed the job well quickly. Definitely recommend."
        }
    },
    "laurel-md": {
        "name": "Laurel",
        "testimonial": {
            "name": "Edie",
            "location": "Columbia, MD",
            "text": "Great experience with Grime to Dime. They were on time, reasonably priced, and professional. Will definitely recommend."
        }
    },
    "savage-md": {
        "name": "Savage",
        "testimonial": {
            "name": "Robert Mcmillen",
            "location": "Odenton, MD",
            "text": "They were prompt, worked with my schedule, and fantastic with their price. I will not only use them again, but will happily recommend them to anyone in the future."
        }
    }
}

def update_location(slug, data):
    """Remove Instagram and update testimonials"""
    
    file_path = Path(f"/home/nar/Documents/sawyers/locations/{slug}/index.html")
    
    if not file_path.exists():
        print(f"⚠️  Skipping {slug} - file not found")
        return
    
    with open(file_path, 'r') as f:
        html = f.read()
    
    # Fix 1: Remove Instagram icon link
    # Find and remove the entire Instagram link
    html = html.replace(
        '                        <a href="#" style="color:#ff6666"><i class="fab fa-instagram"></i></a>',
        ''
    )
    
    # Also remove any standalone Instagram references
    html = html.replace(
        '<a href="#" style="color:#ff6666"><i class="fab fa-instagram"></i></a>',
        ''
    )
    
    # Fix 2: Update testimonial with real review from quote page
    # Find the testimonial section and replace it
    
    # Build the new testimonial HTML
    first_initial = data["testimonial"]["name"][0]
    new_testimonial = f'''    <section id="testimonial" class="testimonial-section">
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
                <div class="author-avatar">{first_initial}</div>
                <div class="author-info">
                    <div class="author-name">{data["testimonial"]["name"]}</div>
                    <div class="author-location">{data["testimonial"]["location"]}</div>
                </div>
            </div>
        </div>
    </section>

'''
    
    # Replace the testimonial section using regex to find it
    import re
    pattern = r'    <section id="testimonial" class="testimonial-section">.*?</section>\n\n'
    html = re.sub(pattern, new_testimonial, html, flags=re.DOTALL)
    
    print(f"✅ Updated {slug}")
    
    with open(file_path, 'w') as f:
        f.write(html)

def main():
    """Update all location pages"""
    print("🔧 Removing Instagram and updating testimonials...\n")
    
    for slug, data in LOCATIONS.items():
        update_location(slug, data)
    
    print("\n✨ All pages updated with real reviews!")

if __name__ == "__main__":
    main()
