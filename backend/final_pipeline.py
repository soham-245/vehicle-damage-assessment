from ultralytics import YOLO
import cv2
import os

# Load models (loaded once globally)
detect_model = YOLO("runs/detect/train/weights/best.pt")
severity_model = YOLO("runs/classify/train/weights/best.pt")


def process_image(img_path):
    img = cv2.imread(img_path)

    if img is None:
        return []

    results = detect_model(img)[0]

    output = []

    # create folder for crops
    os.makedirs("temp_crops", exist_ok=True)

    if results.boxes is not None:
        for i, (box, cls_id) in enumerate(zip(results.boxes.xyxy, results.boxes.cls)):
            x1, y1, x2, y2 = map(int, box)

            crop = img[y1:y2, x1:x2]

            # skip invalid crops
            if crop is None or crop.size == 0:
                continue

            # save crop
            crop_filename = f"temp_crops/crop_{i}.jpg"
            cv2.imwrite(crop_filename, crop)

            # Severity prediction
            severity_result = severity_model(crop)[0]

            probs = severity_result.probs.data
            confidence = float(probs.max())

            severity_class = severity_result.names[severity_result.probs.top1]

            part_name = detect_model.names[int(cls_id)]

            # temporary logic (with confidence handling)
            if confidence < 0.5:
                severity_class = "Moderate"

            if severity_class.lower() == "severe":
                action = "Replace"
                cost = 8000
            elif severity_class.lower() == "moderate":
                action = "Repair"
                cost = 5000
            else:
                action = "Repair"
                cost = 2000

            # debug print (useful for you)
            print(part_name, severity_class, confidence)

            output.append({
                "part": part_name,
                "severity": severity_class,
                "action": action,
                "cost": cost,
                "image_path": crop_filename
            })

    return output