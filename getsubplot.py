import cv2
import numpy as np
import os
import pathlib

# Load image
image = cv2.imread(r'D:\photos4yy\frame39.jpg')
if image is None:
    print("Error: Unable to load image. Please check if the file path is correct.")
    exit()

# Get image dimensions
img_height, img_width = image.shape[:2]
img_area = img_height * img_width

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Binary thresholding, adjust threshold (can be tuned based on image)
thresh_value = 50  # Suggested values: 30, 70, 100, etc.
_, thresh = cv2.threshold(gray, thresh_value, 255, cv2.THRESH_BINARY_INV)

# Check binary threshold effect (for debugging)
cv2.imshow('Threshold Image', thresh)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Find contours
contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

# Store detected rectangular regions
rectangles = []

# Set minimum area threshold (1% of image area, adjustable)
min_area = img_area * 0.01

for contour in contours:
    area = cv2.contourArea(contour)
    if area > min_area:  # Filter small area contours
        epsilon = 0.02 * cv2.arcLength(contour, True)  # Adjust epsilon
        approx = cv2.approxPolyDP(contour, epsilon, True)
        if len(approx) >= 4 and len(approx) <= 6:  # Rectangle vertex count condition
            x, y, w, h = cv2.boundingRect(contour)
            rectangles.append((x, y, w, h))

# Sort rectangles by x-coordinate
rectangles.sort(key=lambda r: r[0])

# Print number of detected rectangles
print(f"Number of detected rectangles: {len(rectangles)}")

if len(rectangles) < 3:
    print("Error: Fewer than 3 rectangles detected, please adjust parameters (e.g., min_area or thresh_value).")
    exit()

# Extract the pixel size of the first rectangle and output
rect1 = rectangles[0]
rect1_width, rect1_height = rect1[2], rect1[3]
print(f"First rectangle (rect1) pixel size: {rect1_width}x{rect1_height}")

# Extract filename from image path (without extension)
image_path = r'D:\photos4yy\frame39.jpg'
image_filename = os.path.basename(image_path)
image_name_without_ext = os.path.splitext(image_filename)[0]

# Create folder with the same name as the image
output_folder = os.path.join(os.path.dirname(image_path), image_name_without_ext)
os.makedirs(output_folder, exist_ok=True)

# Extract and save the first three rectangular regions to the specified folder
for i, (x, y, w, h) in enumerate(rectangles[:3]):
    rect_image = image[y:y+h, x:x+w]
    resized_image = cv2.resize(rect_image, (rect1_width, rect1_height))
    
    # Build output file path
    output_path = os.path.join(output_folder, f'rect_{i+1}.png')
    
    # Save as individual image file
    cv2.imwrite(output_path, resized_image)

print(f"Successfully output three images to folder {output_folder}: rect_1.png, rect_2.png, rect_3.png")