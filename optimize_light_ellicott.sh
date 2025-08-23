#!/bin/bash
# Optimization Script for Light Ellicott City Bridge Image
# This script optimizes the light version of the Ellicott City Bridge image

echo "🌅 Optimizing Light Ellicott City Bridge image..."

cd /home/nar/Documents/sawyers/images/optimized

# Check if ImageMagick is available
if ! command -v convert &> /dev/null; then
    echo "❌ ImageMagick not found. Please install with: sudo apt-get install imagemagick"
    exit 1
fi

# Optimize main hero image
echo "📸 Optimizing main hero image..."
convert lightellicottcity-optimized.png \
    -quality 85 \
    -resize '1920x1080>' \
    -strip \
    -interlace Plane \
    -gaussian-blur 0.05 \
    lightellicottcity-optimized.png

# Create responsive versions
echo "📱 Creating responsive versions..."
convert lightellicottcity-optimized.png -resize 800x temp_800.png && mv temp_800.png lightellicottcity-800w.png
convert lightellicottcity-optimized.png -resize 400x temp_400.png && mv temp_400.png lightellicottcity-400w.png

# Further optimize with pngcrush (if available)
if command -v pngcrush &> /dev/null; then
    echo "🗜️  Running pngcrush optimization..."
    for img in lightellicottcity-*.png; do
        pngcrush -q "$img" "temp_$img" && mv "temp_$img" "$img"
    done
fi

# Display file sizes
echo "📊 Optimization Results:"
ls -lh lightellicottcity-*.png

echo "✅ Light Ellicott City Bridge image optimization complete!"
