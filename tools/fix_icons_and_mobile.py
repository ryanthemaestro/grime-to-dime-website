#!/usr/bin/env python3
"""
Fix icon centering and add comprehensive mobile responsive styles
"""

from pathlib import Path

LOCATIONS = [
    "annapolis-junction-md", "catonsville-md", "clarksville-md", "columbia-md",
    "elkridge-md", "ellicott-city-md", "laurel-md", "savage-md"
]

MOBILE_FIX_CSS = '''
    <style>
        /* FIX: Center icons perfectly in circles */
        .benefit-card i {
            font-size: 3rem;
            color: #ff3333;
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            justify-content: center;
            width: 100%;
            height: 80px;
        }
        
        .service-icon i {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 100%;
            height: 100%;
        }
        
        .process-icon i {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 100%;
            height: 100%;
        }
        
        /* MOBILE RESPONSIVE STYLES */
        @media (max-width: 768px) {
            /* Hero section mobile */
            .location-hero {
                padding: 3rem 1rem;
            }
            
            .location-hero h1 {
                font-size: 2rem;
                line-height: 1.2;
            }
            
            .location-hero h2 {
                font-size: 1.2rem;
            }
            
            /* Stats bar mobile */
            .stats-bar {
                padding: 1.5rem 0.5rem;
            }
            
            .stats-container {
                grid-template-columns: repeat(2, 1fr);
                gap: 1.5rem;
            }
            
            .stat-number {
                font-size: 2rem;
            }
            
            .stat-label {
                font-size: 0.9rem;
            }
            
            /* Service cards mobile */
            .service-grid {
                grid-template-columns: 1fr;
                gap: 1.5rem;
                padding: 0 1rem;
            }
            
            .service-card {
                padding: 1.5rem;
            }
            
            .service-icon {
                width: 70px;
                height: 70px;
                font-size: 1.8rem;
            }
            
            /* Benefits mobile */
            .benefits-grid {
                grid-template-columns: 1fr;
                gap: 1.5rem;
            }
            
            .benefit-card {
                padding: 1.5rem;
            }
            
            /* Feature cards mobile */
            .feature-grid {
                grid-template-columns: 1fr;
                gap: 1.5rem;
            }
            
            .feature-card {
                padding: 2rem 1.5rem;
            }
            
            /* Process mobile */
            .process-steps {
                grid-template-columns: 1fr;
                gap: 2rem;
            }
            
            .process-icon {
                width: 80px;
                height: 80px;
                font-size: 2rem;
            }
            
            /* Testimonial mobile */
            .testimonial-card {
                padding: 2rem 1.5rem;
            }
            
            .testimonial-text {
                font-size: 1.1rem;
            }
            
            .author-avatar {
                width: 40px;
                height: 40px;
                font-size: 1.2rem;
            }
            
            /* FAQ mobile */
            .about details summary {
                padding: 1.25rem 1.5rem;
                font-size: 1.1rem;
            }
            
            .about details p {
                padding: 0 1.5rem 1.25rem 1.5rem;
                font-size: 1rem;
            }
            
            /* Typography mobile */
            .about-container h2,
            .services h2,
            .process-container h2 {
                font-size: 2rem;
                margin-bottom: 2rem;
            }
            
            /* CTA buttons mobile */
            .cta-button {
                padding: 1rem 2rem;
                font-size: 1rem;
                width: 100%;
                max-width: 300px;
                text-align: center;
            }
            
            /* ZIP chips mobile */
            .zip-chips {
                justify-content: center;
            }
            
            .zip-chip {
                padding: 0.6rem 1.2rem;
                font-size: 1rem;
            }
            
            /* Nearby links mobile */
            .nearby-links {
                text-align: center;
                font-size: 1rem;
            }
            
            /* Header mobile adjustments */
            .header-content-wrapper {
                padding: 0 1rem;
            }
            
            /* Section padding mobile */
            .services,
            .process-section,
            .testimonial-section {
                padding: 3rem 1rem;
            }
            
            /* Google rating badge mobile */
            .google-rating-badge {
                flex-direction: column;
                gap: 0.5rem;
            }
            
            /* Reduce animations on mobile for performance */
            @media (prefers-reduced-motion: reduce) {
                * {
                    animation: none !important;
                    transition: none !important;
                }
            }
        }
        
        /* Tablet landscape */
        @media (min-width: 769px) and (max-width: 1024px) {
            .stats-container {
                grid-template-columns: repeat(2, 1fr);
            }
            
            .service-grid {
                grid-template-columns: repeat(2, 1fr);
            }
            
            .benefits-grid {
                grid-template-columns: repeat(2, 1fr);
            }
            
            .process-steps {
                grid-template-columns: repeat(2, 1fr);
            }
        }
        
        /* Small mobile */
        @media (max-width: 480px) {
            .stats-container {
                grid-template-columns: 1fr;
                gap: 1rem;
            }
            
            .stat-item {
                padding: 0.5rem;
            }
            
            .location-hero h1 {
                font-size: 1.75rem;
            }
            
            .location-hero h2 {
                font-size: 1.1rem;
            }
            
            .feature-card h3,
            .benefit-card h4,
            .service-content h3 {
                font-size: 1.3rem;
            }
            
            .testimonial-card::before {
                font-size: 4rem;
                left: 10px;
            }
        }
        
        /* Landscape mobile */
        @media (max-height: 500px) and (orientation: landscape) {
            .location-hero {
                padding: 2rem 1rem;
            }
            
            .stats-bar {
                padding: 1rem 0.5rem;
            }
        }
    </style>
'''

def fix_location(slug):
    """Fix icon centering and add mobile styles"""
    
    file_path = Path(f"/home/nar/Documents/sawyers/locations/{slug}/index.html")
    
    if not file_path.exists():
        print(f"⚠️  Skipping {slug} - file not found")
        return
    
    with open(file_path, 'r') as f:
        html = f.read()
    
    # Skip if already fixed
    if 'FIX: Center icons perfectly' in html:
        print(f"⏭️  Skipping {slug} - already fixed")
        return
    
    # Insert mobile fix CSS after the beautification CSS
    # Look for the closing of the animation keyframes section
    html = html.replace(
        '        .service-card:nth-child(6) { animation-delay: 0.6s; }',
        f'        .service-card:nth-child(6) {{ animation-delay: 0.6s; }}\n{MOBILE_FIX_CSS}'
    )
    
    print(f"✅ Fixed {slug}")
    
    with open(file_path, 'w') as f:
        f.write(html)

def main():
    """Fix all location pages"""
    print("🔧 Fixing icon centering and adding mobile responsive styles...\n")
    
    for slug in LOCATIONS:
        fix_location(slug)
    
    print("\n✨ All location pages fixed and mobile-optimized!")

if __name__ == "__main__":
    main()
