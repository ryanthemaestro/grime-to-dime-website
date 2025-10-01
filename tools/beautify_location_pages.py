#!/usr/bin/env python3
"""
Beautify location pages with enhanced aesthetics
"""

from pathlib import Path

LOCATIONS = [
    "annapolis-junction-md", "catonsville-md", "clarksville-md", "columbia-md",
    "elkridge-md", "ellicott-city-md", "laurel-md", "savage-md"
]

ENHANCED_CSS = '''
    <style>
        /* Enhanced aesthetic improvements */
        
        /* Beautiful ZIP & Cities section */
        .about-container {
            position: relative;
        }
        
        .about-container h2 {
            font-size: 2.5rem;
            text-align: center;
            margin-bottom: 3rem;
            background: linear-gradient(135deg, #333 0%, #666 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .feature-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2.5rem;
            margin-top: 2rem;
        }
        
        .feature-card {
            background: white;
            padding: 2.5rem 2rem;
            border-radius: 16px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.08);
            transition: all 0.3s ease;
            border: 2px solid transparent;
        }
        
        .feature-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 12px 36px rgba(0,0,0,0.12);
            border-color: rgba(255, 51, 51, 0.2);
        }
        
        .feature-card h3 {
            font-size: 1.5rem;
            margin-bottom: 1.5rem;
            color: #333;
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }
        
        .zip-chips {
            display: flex;
            flex-wrap: wrap;
            gap: 0.75rem;
        }
        
        .zip-chip {
            background: linear-gradient(135deg, #ff3333 0%, #cc0000 100%);
            color: white;
            padding: 0.75rem 1.5rem;
            border-radius: 25px;
            font-weight: 600;
            font-size: 1.1rem;
            box-shadow: 0 4px 12px rgba(255, 51, 51, 0.3);
            transition: all 0.3s ease;
        }
        
        .zip-chip:hover {
            transform: scale(1.05);
            box-shadow: 0 6px 16px rgba(255, 51, 51, 0.4);
        }
        
        .nearby-links {
            font-size: 1.1rem;
            line-height: 2;
        }
        
        .nearby-links a {
            color: #ff3333;
            text-decoration: none;
            font-weight: 600;
            padding: 0.5rem 1rem;
            border-radius: 8px;
            transition: all 0.3s ease;
            display: inline-block;
        }
        
        .nearby-links a:hover {
            background: rgba(255, 51, 51, 0.1);
            transform: translateX(4px);
        }
        
        /* Beautiful service cards */
        .services {
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            padding: 4rem 1rem;
        }
        
        .services h2 {
            font-size: 2.5rem;
            text-align: center;
            margin-bottom: 3rem;
            color: #333;
        }
        
        .service-grid {
            max-width: 1200px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 2rem;
        }
        
        .service-card {
            background: white;
            border-radius: 16px;
            padding: 2rem;
            box-shadow: 0 4px 16px rgba(0,0,0,0.08);
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            border: 2px solid transparent;
        }
        
        .service-card:hover {
            transform: translateY(-12px) scale(1.02);
            box-shadow: 0 12px 32px rgba(255, 51, 51, 0.2);
            border-color: #ff3333;
        }
        
        .service-icon {
            width: 80px;
            height: 80px;
            background: linear-gradient(135deg, #ff3333 0%, #cc0000 100%);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 1.5rem;
            font-size: 2rem;
            color: white;
            box-shadow: 0 8px 16px rgba(255, 51, 51, 0.3);
            transition: all 0.3s ease;
        }
        
        .service-card:hover .service-icon {
            transform: rotate(360deg) scale(1.1);
        }
        
        .service-content h3 {
            font-size: 1.5rem;
            margin-bottom: 1rem;
            color: #333;
            text-align: center;
        }
        
        .service-content p {
            color: #666;
            line-height: 1.6;
            margin-bottom: 1.5rem;
            text-align: center;
        }
        
        /* Beautiful process section */
        .process-section {
            background: white;
            padding: 4rem 1rem;
        }
        
        .process-container h2 {
            font-size: 2.5rem;
            text-align: center;
            margin-bottom: 3rem;
            color: #333;
        }
        
        .process-steps {
            max-width: 1200px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 3rem;
            position: relative;
        }
        
        .process-step {
            text-align: center;
            position: relative;
        }
        
        .process-icon {
            width: 100px;
            height: 100px;
            background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 100%);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 1.5rem;
            font-size: 2.5rem;
            color: #ff3333;
            box-shadow: 0 8px 24px rgba(15, 15, 35, 0.3);
            transition: all 0.3s ease;
            border: 4px solid #ff3333;
        }
        
        .process-step:hover .process-icon {
            transform: scale(1.15);
            box-shadow: 0 12px 32px rgba(255, 51, 51, 0.4);
        }
        
        .process-step h3 {
            font-size: 1.5rem;
            margin-bottom: 1rem;
            color: #333;
        }
        
        .process-step p {
            color: #666;
            line-height: 1.6;
        }
        
        /* Beautiful FAQ section */
        .about details {
            background: white;
            margin-bottom: 1rem;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.06);
            overflow: hidden;
            border: 2px solid transparent;
            transition: all 0.3s ease;
        }
        
        .about details:hover {
            border-color: rgba(255, 51, 51, 0.3);
            box-shadow: 0 6px 16px rgba(0,0,0,0.1);
        }
        
        .about details summary {
            padding: 1.5rem 2rem;
            cursor: pointer;
            font-weight: 600;
            font-size: 1.2rem;
            color: #333;
            list-style: none;
            display: flex;
            align-items: center;
            justify-content: space-between;
            transition: all 0.3s ease;
        }
        
        .about details summary::-webkit-details-marker {
            display: none;
        }
        
        .about details summary::after {
            content: '+';
            font-size: 2rem;
            color: #ff3333;
            transition: transform 0.3s ease;
        }
        
        .about details[open] summary::after {
            transform: rotate(45deg);
        }
        
        .about details summary:hover {
            background: rgba(255, 51, 51, 0.05);
            color: #ff3333;
        }
        
        .about details p {
            padding: 0 2rem 1.5rem 2rem;
            color: #666;
            line-height: 1.8;
            font-size: 1.05rem;
        }
        
        /* Beautiful CTA buttons */
        .cta-button {
            background: linear-gradient(135deg, #ff3333 0%, #cc0000 100%);
            color: white;
            padding: 1.25rem 3rem;
            border-radius: 50px;
            text-decoration: none;
            font-weight: 700;
            font-size: 1.2rem;
            display: inline-block;
            transition: all 0.3s ease;
            box-shadow: 0 8px 24px rgba(255, 51, 51, 0.4);
            border: none;
            cursor: pointer;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .cta-button:hover {
            transform: translateY(-3px) scale(1.05);
            box-shadow: 0 12px 32px rgba(255, 51, 51, 0.5);
        }
        
        .cta-button:active {
            transform: translateY(-1px);
        }
        
        /* Beautiful benefit cards */
        .benefits-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 2rem;
            margin-top: 2rem;
        }
        
        .benefit-card {
            background: white;
            padding: 2rem;
            border-radius: 16px;
            text-align: center;
            box-shadow: 0 4px 16px rgba(0,0,0,0.08);
            transition: all 0.3s ease;
            border: 2px solid transparent;
        }
        
        .benefit-card:hover {
            transform: translateY(-8px);
            border-color: #ff3333;
            box-shadow: 0 12px 32px rgba(255, 51, 51, 0.15);
        }
        
        .benefit-card i {
            font-size: 3rem;
            color: #ff3333;
            margin-bottom: 1rem;
            display: block;
        }
        
        .benefit-card h4 {
            font-size: 1.5rem;
            margin-bottom: 1rem;
            color: #333;
        }
        
        .benefit-card p {
            color: #666;
            line-height: 1.6;
        }
        
        /* Add subtle animations */
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .service-card,
        .benefit-card,
        .feature-card,
        .process-step {
            animation: fadeInUp 0.6s ease-out;
        }
        
        .service-card:nth-child(1) { animation-delay: 0.1s; }
        .service-card:nth-child(2) { animation-delay: 0.2s; }
        .service-card:nth-child(3) { animation-delay: 0.3s; }
        .service-card:nth-child(4) { animation-delay: 0.4s; }
        .service-card:nth-child(5) { animation-delay: 0.5s; }
        .service-card:nth-child(6) { animation-delay: 0.6s; }
    </style>
'''

def beautify_location(slug):
    """Add beautiful aesthetic CSS to location page"""
    
    file_path = Path(f"/home/nar/Documents/sawyers/locations/{slug}/index.html")
    
    if not file_path.exists():
        print(f"⚠️  Skipping {slug} - file not found")
        return
    
    with open(file_path, 'r') as f:
        html = f.read()
    
    # Skip if already beautified
    if 'Beautiful ZIP & Cities section' in html:
        print(f"⏭️  Skipping {slug} - already beautified")
        return
    
    # Insert enhanced CSS after the existing stats CSS
    html = html.replace(
        '        .stars-display {',
        f'{ENHANCED_CSS}\n        .stars-display {{'
    )
    
    print(f"✅ Beautified {slug}")
    
    with open(file_path, 'w') as f:
        f.write(html)

def main():
    """Beautify all location pages"""
    print("🎨 Beautifying all location pages...\n")
    
    for slug in LOCATIONS:
        beautify_location(slug)
    
    print("\n✨ All location pages beautified!")

if __name__ == "__main__":
    main()
