// Handle smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Handle contact form submission and tracking
const contactForm = document.querySelector('.contact-form');
if (contactForm) {
    contactForm.addEventListener('submit', function(e) {
        // Debug message
        console.log('🚀 Form submission started');
        
        // Track form submission event in GA4 using sendBeacon
        const analyticsData = {
            'event_name': 'form_submit',
            'form_name': 'quote_request',
            'form_id': 'lead-form',
            'form_destination': 'formspree'
        };

        // Use sendBeacon to ensure the event is sent even during page unload
        gtag('event', 'form_submit', {
            'form_name': 'quote_request',
            'form_id': 'lead-form',
            'form_destination': 'formspree',
            'transport_type': 'beacon'
        });

        console.log('✅ GA4 event sent via sendBeacon:', analyticsData);
    });
}

// Add scroll-based animations for service cards
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('animate');
        }
    });
}, {
    threshold: 0.1
});

document.querySelectorAll('.service-card').forEach((card) => {
    observer.observe(card);
}); 