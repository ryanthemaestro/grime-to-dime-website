#!/bin/bash
# Simple Image Optimization Script
# Use this if you have ImageMagick installed

echo "🚀 Starting image optimization..."

# Check if ImageMagick is installed
if ! command -v convert &> /dev/null; then
    echo "❌ ImageMagick not found. Please install with: sudo apt-get install imagemagick"
    exit 1
fi

cd /home/nar/Documents/sawyers/images/optimized

# Optimize main hero image
echo "📸 Optimizing main hero image..."
convert ellicottcitybridge-optimized.jpg \
    -quality 85 \
    -resize '1920x1080>' \
    -strip \
    ellicottcitybridge-optimized.jpg

# Create responsive versions
echo "📱 Creating responsive versions..."
convert ellicottcitybridge-optimized.jpg -resize 800x temp_800.jpg && mv temp_800.jpg ellicottcitybridge-800w.jpg
convert ellicottcitybridge-optimized.jpg -resize 400x temp_400.jpg && mv temp_400.jpg ellicottcitybridge-400w.jpg

# Optimize all versions
for img in ellicottcitybridge-*.jpg; do
    convert "$img" -quality 82 -strip -interlace Plane "$img"
    echo "✅ Optimized: $img ($(du -h "$img" | cut -f1))"
done

echo "🎉 Image optimization complete!"
echo "📊 File sizes:"
ls -lh ellicottcitybridge-*.jpg
