from ultralytics import YOLO
import cv2

# Load models
detect_model = YOLO("runs/detect/train/weights/best.pt")
severity_model = YOLO("runs/classify/train/weights/best.pt")

# Input image
img_path = "data/raw/damage_detection/test/images/damage_6994_jpg.rf.83940e70eff8105f127f82d768fee37e.jpg"
img = cv2.imread(img_path)

# Detection
results = detect_model(img)[0]

if results.boxes is not None:
    for box, cls_id in zip(results.boxes.xyxy, results.boxes.cls):
        x1, y1, x2, y2 = map(int, box)

        crop = img[y1:y2, x1:x2]

        # Severity prediction
        severity_result = severity_model(crop)[0]
        severity_class = severity_result.names[severity_result.probs.top1]

        part_name = detect_model.names[int(cls_id)]

        print(f"Part: {part_name} → Severity: {severity_class}")