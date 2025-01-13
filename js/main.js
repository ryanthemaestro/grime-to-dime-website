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
        // Always prevent default form submission
        e.preventDefault();
        
        // Debug message
        console.log('🚀 Form submission intercepted');
        
        try {
            // Track form submission event in GA4
            gtag('event', 'lead_form_submit', {
                'event_category': 'Contact',
                'event_label': 'Quote Request Form',
                'form_name': 'lead-form',
                'transport_type': 'beacon'
            });

            console.log('✅ GA4 event sent successfully:', {
                'event_name': 'lead_form_submit',
                'event_category': 'Contact',
                'event_label': 'Quote Request Form',
                'form_name': 'lead-form'
            });

            // Submit form after ensuring event is tracked
            setTimeout(() => {
                console.log('📨 Submitting form to Formspree...');
                contactForm.submit();
            }, 500); // Increased delay to 500ms

        } catch (error) {
            console.error('❌ Error tracking form submission:', error);
            // Submit form anyway if tracking fails
            contactForm.submit();
        }
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