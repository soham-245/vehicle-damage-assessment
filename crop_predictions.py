from ultralytics import YOLO
import cv2
import os

# Load model
model = YOLO("runs/detect/train/weights/best.pt")

# Input and output folders
input_folder = "data/raw/damage_detection/test/images"
output_folder = "cropped_outputs"

os.makedirs(output_folder, exist_ok=True)

for img_name in os.listdir(input_folder):
    img_path = os.path.join(input_folder, img_name)
    img = cv2.imread(img_path)

    results = model(img)[0]

    if results.boxes is None:
        continue

    for i, (box, cls_id) in enumerate(zip(results.boxes.xyxy, results.boxes.cls)):
        x1, y1, x2, y2 = map(int, box)

        crop = img[y1:y2, x1:x2]

        class_name = model.names[int(cls_id)]

        save_path = os.path.join(output_folder, f"{class_name}_{img_name}_{i}.jpg")
        cv2.imwrite(save_path, crop)

print("Done")