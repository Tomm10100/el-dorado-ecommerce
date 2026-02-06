import cv2
import numpy as np
import os

def split_product_image(image_path, prefix):
    # Read image
    img = cv2.imread(image_path)
    if img is None:
        print(f"Failed to load {image_path}")
        return []

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Threshold to get background (white) vs foreground
    # Invert so objects are white, background is black
    _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)
    
    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    saved_files = []
    count = 0
    
    # Sort contours by size to ignore noise, and by position (top to bottom, left to right)
    # Filter small contours
    valid_contours = [c for c in contours if cv2.contourArea(c) > 1000]
    
    # Sort: Top to bottom, then left to right (approximate)
    # Bounding box: x, y, w, h
    valid_contours.sort(key=lambda c: (cv2.boundingRect(c)[1] // 100, cv2.boundingRect(c)[0]))

    for c in valid_contours:
        x, y, w, h = cv2.boundingRect(c)
        
        # Add padding
        pad = 20
        h_img, w_img = img.shape[:2]
        
        y1 = max(0, y - pad)
        y2 = min(h_img, y + h + pad)
        x1 = max(0, x - pad)
        x2 = min(w_img, x + w + pad)
        
        # Crop
        crop = img[y1:y2, x1:x2]
        
        # Save
        filename = f"public/{prefix}_{count}.jpg"
        cv2.imwrite(filename, crop)
        saved_files.append(filename)
        print(f"Saved {filename}")
        count += 1
        
    return saved_files

# Process the specific files
files = [
    ("public/product-collection-1.jpg", "crop_coll1"),
    ("public/product-collection-2.jpg", "crop_coll2"),
    ("public/product-collection-3.jpg", "crop_coll3")
]

all_generated = []
for f, p in files:
    if os.path.exists(f):
        print(f"Processing {f}...")
        generated = split_product_image(f, p)
        all_generated.extend(generated)
    else:
        print(f"File not found: {f}")

print("Done.")
