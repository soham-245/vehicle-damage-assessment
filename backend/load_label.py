import os
import cv2
import numpy as np

# Image name
image_name = "0001_JPEG.rf.8cce9bb7a46ff7494b475d1ab652324a.jpg"

# Paths
image_path = f"data/raw/damage_detection/train/images/{image_name}"
label_path = f"data/raw/damage_detection/train/labels/{image_name.replace('.jpg', '.txt')}"

# Output folder
output_dir = "outputs/crops"
os.makedirs(output_dir, exist_ok=True)

# Load image
image = cv2.imread(image_path)

if image is None:
    print("Error: Image not found")
    exit()

height, width, _ = image.shape

# Read labels
with open(label_path, "r") as file:
    lines = file.readlines()

print("Cropping regions...\n")

for idx, line in enumerate(lines):
    parts = line.strip().split()

    class_id = int(parts[0])
    coords = list(map(float, parts[1:]))

    points = []

    # Convert normalized → pixel
    for i in range(0, len(coords), 2):
        x = int(coords[i] * width)
        y = int(coords[i+1] * height)
        points.append((x, y))

    # Convert to numpy
    pts = np.array(points, dtype=np.int32)

    # Bounding box
    x_min = np.min(pts[:, 0])
    x_max = np.max(pts[:, 0])
    y_min = np.min(pts[:, 1])
    y_max = np.max(pts[:, 1])

    # Crop
    crop = image[y_min:y_max, x_min:x_max]

    # Save crop
    save_path = os.path.join(output_dir, f"{image_name}_region{idx}_class{class_id}.jpg")
    cv2.imwrite(save_path, crop)

    print(f"Saved: {save_path}")
