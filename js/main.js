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
        // Prevent the default form submission temporarily
        e.preventDefault();
        
        console.log('Form submitted - Sending event to GA4...');
        
        // Track form submission event in GA4
        gtag('event', 'lead_form_submit', {
            'event_category': 'Contact',
            'event_label': 'Quote Request Form',
            'form_name': 'lead-form',
            'transport_type': 'beacon'
        });

        console.log('GA4 event sent:', {
            'event_name': 'lead_form_submit',
            'event_category': 'Contact',
            'event_label': 'Quote Request Form',
            'form_name': 'lead-form'
        });

        // Submit the form after a small delay to ensure the event is sent
        setTimeout(() => {
            contactForm.submit();
        }, 100);
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