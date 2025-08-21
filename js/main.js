// Optimized main.js - Defer non-critical operations to improve performance

// Critical: Set up smooth scrolling immediately for better UX
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth' });
        }
    });
});

// GA4 navigation helper with timeout fallback - optimized
function gtagSendEvent(url) {
    if (!url) return;

    let navigated = false;
    const navigateToUrl = () => {
        if (!navigated) {
            navigated = true;
            window.location.href = url;
        }
    };

    // Set a timeout to ensure navigation happens regardless of GA state
    const navigationTimeout = setTimeout(navigateToUrl, 1000);

    if (typeof gtag === 'function') {
        const isDebug = (window.__gaDebug === true);
        try {
            gtag('event', 'select_content', {
                'content_type': 'cta',
                'event_label': 'CTA Click',
                'link_url': url,
                'debug_mode': isDebug,
                'event_callback': () => {
                    clearTimeout(navigationTimeout);
                    navigateToUrl();
                },
                'event_timeout': 900
            });
        } catch (e) {
            navigateToUrl();
        }
    } else {
        navigateToUrl();
    }
}

// Optimized CTA tracking - consolidated and deferred
function initCTATracking() {
    const ctaSelectors = '.cta-button, .service-cta, .section-cta';
    const ctaElements = document.querySelectorAll(ctaSelectors);

    if (ctaElements.length === 0) return;

    ctaElements.forEach(el => {
        el.addEventListener('click', function(e) {
            const href = el.getAttribute('href') || '';
            if (!href) return;

            const isDebug = (window.__gaDebug === true);

            // Hash links: fire event and let smooth-scroll handler run
            if (href.charAt(0) === '#') {
                if (typeof gtag === 'function') {
                    gtag('event', 'select_content', {
                        'content_type': 'cta',
                        'event_label': 'CTA Click',
                        'link_url': href,
                        'debug_mode': isDebug
                    });
                }
                return;
            }

            // Non-hash: delay navigation to ensure event send
            e.preventDefault();

            let navigated = false;
            const done = () => {
                if (!navigated) {
                    navigated = true;
                    window.location.href = href;
                }
            };

            if (typeof gtag === 'function') {
                gtag('event', 'select_content', {
                    'content_type': 'cta',
                    'event_label': 'CTA Click',
                    'link_url': href,
                    'debug_mode': isDebug,
                    'event_callback': done,
                    'event_timeout': 1000
                });
            } else {
                done();
            }
        });
    });
}

// Optimized intersection observer for animations - deferred
function initScrollAnimations() {
    const serviceCards = document.querySelectorAll('.service-card');
    if (serviceCards.length === 0) return;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate');
                // Stop observing after animation is triggered
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '50px' // Start animation slightly before element enters viewport
    });

    serviceCards.forEach(card => observer.observe(card));
}

// Defer non-critical initialization until after page load
function initNonCriticalFeatures() {
    // Use requestIdleCallback if available, otherwise requestAnimationFrame
    const scheduleWork = window.requestIdleCallback ||
                        ((callback) => requestAnimationFrame(() =>
                            setTimeout(callback, 1)));

    scheduleWork(() => {
        initCTATracking();
        initScrollAnimations();
    });
}

// Initialize non-critical features after DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initNonCriticalFeatures);
} else {
    // DOM already loaded, initialize immediately but defer
    initNonCriticalFeatures();
} 