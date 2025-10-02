#!/usr/bin/env python3
"""
Update all location pages with the new clean contact form from index.html
"""

from pathlib import Path

LOCATIONS = [
    "annapolis-junction-md", "catonsville-md", "clarksville-md", "columbia-md",
    "elkridge-md", "ellicott-city-md", "laurel-md", "savage-md"
]

NEW_CONTACT_CSS = '''
    <!-- Contact Section - Clean & Conversion-Focused -->
    <style>
        .contact {
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            padding: 4rem 1rem;
        }
        
        .contact h2 {
            text-align: center;
            font-size: 2.5rem;
            color: #333;
            margin-bottom: 3rem;
            font-weight: 800;
        }
        
        .contact-container {
            max-width: 1200px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 3rem;
            align-items: start;
        }
        
        /* Left Side - Contact Info */
        .contact-info {
            background: white;
            padding: 2.5rem;
            border-radius: 16px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.08);
        }
        
        .contact-info h3 {
            font-size: 1.5rem;
            color: #333;
            margin-bottom: 1.5rem;
        }
        
        .cta-primary {
            display: block;
            background: linear-gradient(135deg, #ff3333 0%, #cc0000 100%);
            color: white;
            padding: 1.25rem 2rem;
            border-radius: 12px;
            text-decoration: none;
            font-size: 1.3rem;
            font-weight: 700;
            text-align: center;
            margin-bottom: 1rem;
            box-shadow: 0 8px 24px rgba(255, 51, 51, 0.3);
            transition: all 0.3s ease;
        }
        
        .cta-primary:hover {
            transform: translateY(-3px);
            box-shadow: 0 12px 32px rgba(255, 51, 51, 0.4);
        }
        
        .cta-primary i {
            margin-right: 0.75rem;
            font-size: 1.4rem;
        }
        
        .cta-secondary {
            display: block;
            background: white;
            color: #ff3333;
            padding: 1rem 2rem;
            border-radius: 12px;
            text-decoration: none;
            font-size: 1.1rem;
            font-weight: 600;
            text-align: center;
            margin-bottom: 2rem;
            border: 2px solid #ff3333;
            transition: all 0.3s ease;
        }
        
        .cta-secondary:hover {
            background: #ff3333;
            color: white;
            transform: translateY(-2px);
        }
        
        .cta-secondary i {
            margin-right: 0.5rem;
        }
        
        .contact-detail {
            display: flex;
            align-items: center;
            margin-bottom: 1.25rem;
            padding: 1rem;
            background: #f8f9fa;
            border-radius: 8px;
        }
        
        .contact-detail i {
            font-size: 1.5rem;
            color: #ff3333;
            margin-right: 1rem;
            width: 30px;
            text-align: center;
        }
        
        .contact-detail-text {
            flex: 1;
        }
        
        .contact-label {
            display: block;
            font-size: 0.85rem;
            color: #666;
            margin-bottom: 0.25rem;
        }
        
        .contact-value {
            display: block;
            font-size: 1.1rem;
            color: #333;
            font-weight: 600;
        }
        
        .hours-compact {
            text-align: center;
            padding: 1rem;
            background: #f8f9fa;
            border-radius: 8px;
            margin-bottom: 1.5rem;
        }
        
        .hours-compact p {
            margin: 0.25rem 0;
            color: #555;
            font-size: 0.95rem;
        }
        
        .hours-compact strong {
            color: #333;
        }
        
        .contact-social {
            text-align: center;
            padding-top: 1rem;
            border-top: 1px solid #e9ecef;
        }
        
        .contact-social h4 {
            font-size: 1rem;
            color: #666;
            margin-bottom: 0.75rem;
        }
        
        .social-links-contact a {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 50px;
            height: 50px;
            background: #1877f2;
            color: white;
            border-radius: 50%;
            font-size: 1.5rem;
            transition: all 0.3s ease;
        }
        
        .social-links-contact a:hover {
            transform: scale(1.1);
            box-shadow: 0 4px 12px rgba(24, 119, 242, 0.3);
        }
        
        /* Right Side - Simple Form */
        .contact-form {
            background: white;
            padding: 2.5rem;
            border-radius: 16px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.08);
        }
        
        .form-header {
            text-align: center;
            margin-bottom: 2rem;
        }
        
        .form-header h3 {
            font-size: 1.5rem;
            color: #333;
            margin-bottom: 0.5rem;
        }
        
        .form-tagline {
            color: #666;
            font-size: 0.95rem;
        }
        
        .form-group {
            margin-bottom: 1.5rem;
        }
        
        .form-group label {
            display: block;
            font-weight: 600;
            color: #333;
            margin-bottom: 0.5rem;
            font-size: 0.95rem;
        }
        
        .form-group input,
        .form-group textarea {
            width: 100%;
            padding: 0.875rem 1rem;
            border: 2px solid #e9ecef;
            border-radius: 8px;
            font-size: 1rem;
            transition: all 0.3s ease;
        }
        
        .form-group input:focus,
        .form-group textarea:focus {
            outline: none;
            border-color: #ff3333;
            box-shadow: 0 0 0 3px rgba(255, 51, 51, 0.1);
        }
        
        .form-group textarea {
            min-height: 120px;
            resize: vertical;
            font-family: inherit;
        }
        
        .submit-button {
            width: 100%;
            background: linear-gradient(135deg, #ff3333 0%, #cc0000 100%);
            color: white;
            padding: 1rem 2rem;
            border: none;
            border-radius: 12px;
            font-size: 1.1rem;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 12px rgba(255, 51, 51, 0.3);
        }
        
        .submit-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(255, 51, 51, 0.4);
        }
        
        .submit-button i {
            margin-right: 0.5rem;
        }
        
        /* Mobile Responsive */
        @media (max-width: 768px) {
            .contact-container {
                grid-template-columns: 1fr;
                gap: 2rem;
            }
            
            .contact h2 {
                font-size: 2rem;
                margin-bottom: 2rem;
            }
            
            .contact-info,
            .contact-form {
                padding: 2rem 1.5rem;
            }
            
            .cta-primary {
                font-size: 1.2rem;
                padding: 1rem 1.5rem;
            }
        }
    </style>
'''

def get_new_contact_html(location_name):
    """Generate the new contact section HTML for a location"""
    return f'''
    <section id="contact" class="contact">
        <h2>Ready to Get Started?</h2>
        <div class="contact-container">
            <!-- Left Side: Contact Info -->
            <div class="contact-info">
                <h3>Contact Us</h3>
                
                <!-- Primary CTA: Phone -->
                <a href="tel:4103006743" class="cta-primary">
                    <i class="fas fa-phone"></i> (410) 300-6743
                </a>
                
                <!-- Secondary CTA: Text Photo -->
                <a href="sms:+14103006743?body=Hi%2C%20I%E2%80%99d%20like%20a%20junk%20removal%20quote.%20My%20items%20are%3A%20" class="cta-secondary">
                    <i class="fas fa-camera"></i> Text a Photo for Quote
                </a>
                
                <!-- Service Area -->
                <div class="contact-detail">
                    <i class="fas fa-location-dot"></i>
                    <div class="contact-detail-text">
                        <span class="contact-label">Service Area</span>
                        <span class="contact-value">{location_name}, MD</span>
                    </div>
                </div>
                
                <!-- Hours Compact -->
                <div class="hours-compact">
                    <p><strong>Mon-Sat:</strong> 7:00 AM - 7:00 PM</p>
                    <p><strong>Sunday:</strong> Closed</p>
                </div>
                
                <!-- Social -->
                <div class="contact-social">
                    <h4>Connect With Us</h4>
                    <div class="social-links-contact">
                        <a href="https://www.facebook.com/people/Grime-To-Dime/61571988560834/" target="_blank" aria-label="Facebook">
                            <i class="fab fa-facebook"></i>
                        </a>
                    </div>
                </div>
            </div>
            
            <!-- Right Side: Simple Form -->
            <form class="contact-form" action="https://formspree.io/f/meoovajl" method="POST">
                <div class="form-header">
                    <h3>Or Send a Message</h3>
                    <p class="form-tagline">We'll get back to you in 10-15 minutes</p>
                </div>
                
                <input type="hidden" name="_subject" value="New Contact from {location_name} Location Page">
                <input type="hidden" name="_next" value="https://grimetodime.com/thank-you.html">
                <input type="text" name="_gotcha" style="display:none">
                
                <div class="form-group">
                    <label for="name">Your Name</label>
                    <input type="text" id="name" name="_name" placeholder="John Smith" required>
                </div>
                
                <div class="form-group">
                    <label for="phone">Phone Number</label>
                    <input type="tel" id="phone" name="_phone" placeholder="(410) 555-1234" required pattern="[\\d\\-\\+\\(\\)\\s]{{10,}}">
                </div>
                
                <div class="form-group">
                    <label for="message">Message <span style="font-weight:400;color:#999">(optional)</span></label>
                    <textarea id="message" name="_message" placeholder="Tell us about your junk removal needs..."></textarea>
                </div>
                
                <button type="submit" class="submit-button">
                    <i class="fas fa-paper-plane"></i> Send Message
                </button>
            </form>
        </div>
    </section>
'''

LOCATION_NAMES = {
    "annapolis-junction-md": "Annapolis Junction",
    "catonsville-md": "Catonsville",
    "clarksville-md": "Clarksville",
    "columbia-md": "Columbia",
    "elkridge-md": "Elkridge",
    "ellicott-city-md": "Ellicott City",
    "laurel-md": "Laurel",
    "savage-md": "Savage"
}

def update_location(slug):
    """Update contact section on a location page"""
    
    file_path = Path(f"/home/nar/Documents/sawyers/locations/{slug}/index.html")
    
    if not file_path.exists():
        print(f"⚠️  Skipping {slug} - file not found")
        return
    
    with open(file_path, 'r') as f:
        html = f.read()
    
    # Check if already has new contact section
    if 'Ready to Get Started?' in html and 'cta-primary' in html:
        print(f"⏭️  Skipping {slug} - already has new contact form")
        return
    
    location_name = LOCATION_NAMES[slug]
    
    # Insert CSS before </head>
    if NEW_CONTACT_CSS not in html:
        html = html.replace('</head>', f'{NEW_CONTACT_CSS}\n</head>')
    
    # Find and replace contact section
    # Look for the contact section
    import re
    
    # Pattern to match the old contact section (if it exists)
    # We'll insert before the footer
    if '<footer' in html:
        new_contact_html = get_new_contact_html(location_name)
        
        # Insert contact section before footer
        html = html.replace('<footer', f'{new_contact_html}\n\n    <footer')
        
        print(f"✅ Updated {slug}")
    else:
        print(f"⚠️  Could not find footer in {slug}")
        return
    
    with open(file_path, 'w') as f:
        f.write(html)

def main():
    """Update all location pages"""
    print("🔧 Updating location pages with new contact form...\n")
    
    for slug in LOCATIONS:
        update_location(slug)
    
    print("\n✨ All location pages updated!")

if __name__ == "__main__":
    main()
