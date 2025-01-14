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
        
        // Track form submission event in GA4 using recommended event name
        const analyticsData = {
            'currency': 'USD',
            'value': 1,
            'form_name': 'quote_request',
            'form_id': 'lead-form',
            'form_destination': 'formspree'
        };

        // Use sendBeacon to ensure the event is sent even during page unload
        gtag('event', 'generate_lead', analyticsData);

        console.log('✅ GA4 event sent via sendBeacon:', {
            event_name: 'generate_lead',
            ...analyticsData
        });
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