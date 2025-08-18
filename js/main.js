// Handle smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// GA4: Track CTA clicks on .cta-button, .service-cta, .section-cta
(function(){
  try {
    var ctaSelectors = '.cta-button, .service-cta, .section-cta';
    document.querySelectorAll(ctaSelectors).forEach(function(el){
      el.addEventListener('click', function(e){
        var href = el.getAttribute('href') || '';
        if (!href) return;
        // Hash links: fire event and let existing smooth-scroll handler run
        if (href.charAt(0) === '#') {
          if (typeof gtag === 'function') {
            gtag('event', 'select_content', {
              'content_type': 'cta',
              'event_label': 'CTA Click',
              'link_url': href
            });
          }
          return;
        }
        // Non-hash: delay navigation to ensure event send
        e.preventDefault();
        if (typeof gtagSendEvent === 'function') {
          gtagSendEvent(href);
          return;
        }
        // Fallback if helper missing
        var navigated = false;
        var done = function(){ if (!navigated) { navigated = true; window.location.href = href; } };
        if (typeof gtag === 'function') {
          gtag('event', 'select_content', {
            'content_type': 'cta',
            'event_label': 'CTA Click',
            'link_url': href,
            'event_callback': done,
            'event_timeout': 2000
          });
        } else {
          done();
        }
      }, false);
    });
  } catch (err) {
    // no-op
  }
})();

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