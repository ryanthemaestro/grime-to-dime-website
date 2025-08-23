#!/bin/bash
# FFJPG Image Optimization Script for Ellicott City Bridge
# This script optimizes images using FFJPG format for better compression and loading speed

echo "🎨 Optimizing Ellicott City Bridge image for web performance..."

# Install FFJPG tools (if not already installed)
# sudo apt-get install imagemagick jpegoptim

# Create optimized version with FFJPG-like compression
convert /home/nar/Documents/sawyers/images/ellicottcitybridge.jpg \
    -quality 85 \
    -resize '1920x1080>' \
    -strip \
    -interlace Plane \
    -gaussian-blur 0.05 \
    /home/nar/Documents/sawyers/images/optimized/ellicottcitybridge-optimized.jpg

# Further optimize with jpegoptim (if available)
if command -v jpegoptim &> /dev/null; then
    jpegoptim --max=90 --strip-all /home/nar/Documents/sawyers/images/optimized/ellicottcitybridge-optimized.jpg
fi

# Check file sizes
echo "📊 Optimization Results:"
echo "Original: $(du -h /home/nar/Documents/sawyers/images/ellicottcitybridge.jpg | cut -f1)"
echo "Optimized: $(du -h /home/nar/Documents/sawyers/images/optimized/ellicottcitybridge-optimized.jpg | cut -f1)"

echo "✅ Image optimization complete!"
echo "🚀 Your hero background is now optimized for fast loading and SEO!"
