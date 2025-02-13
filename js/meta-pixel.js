// Load environment variables
require('dotenv').config();

// Initialize Meta Pixel
!function(f,b,e,v,n,t,s) {
    if(f.fbq)return;
    n=f.fbq=function(){n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)};
    if(!f._fbq)f._fbq=n;
    n.push=n;
    n.loaded=!0;
    n.version='2.0';
    n.queue=[];
    t=b.createElement(e);
    t.async=!0;
    t.src=v;
    s=b.getElementsByTagName(e)[0];
    s.parentNode.insertBefore(t,s)
}(window, document,'script','https://connect.facebook.net/en_US/fbevents.js');

// Initialize with access token from environment variables
fbq('init', process.env.META_API_ACCESS_TOKEN);
fbq('track', 'PageView');

// Function to hash user data for privacy
function hashData(data) {
    if (!data) return null;
    return CryptoJS.SHA256(data.trim().toLowerCase()).toString();
}

// Function to track lead conversion with detailed data
function trackLeadConversion(formData) {
    const eventTime = Math.floor(Date.now() / 1000);
    
    // Hash user data for privacy
    const userData = {
        em: formData.email ? [hashData(formData.email)] : [],
        ph: formData.phone ? [hashData(formData.phone)] : []
    };

    // Prepare event data
    const eventData = {
        event_name: 'Lead',
        event_time: eventTime,
        action_source: 'website',
        user_data: userData,
        custom_data: {
            currency: 'USD',
            value: '142.52',
            content_name: 'Quote Request',
            content_category: 'Junk Removal',
            status: 'submitted',
            location: formData.location || '',
            name: formData.name || '',
            message_type: formData.message || ''
        }
    };

    // Send to Meta Pixel
    fbq('track', 'Lead', eventData);
    
    // Also track as a Purchase event
    const purchaseData = {
        ...eventData,
        event_name: 'Purchase'
    };
    fbq('track', 'Purchase', purchaseData);
} 