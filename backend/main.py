from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import base64
import os

from final_pipeline import process_image

app = FastAPI()

# Enable CORS (for frontend connection)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/analyze")
async def analyze(file: UploadFile = File(...), car_model: str = Form(...)):
    # Save uploaded image temporarily
    file_path = f"temp_{file.filename}"

    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Run ML pipeline
    results = process_image(file_path)

    # Convert cropped images to base64
    processed_results = []

    for item in results:
        try:
            with open(item["image_path"], "rb") as img_file:
                encoded = base64.b64encode(img_file.read()).decode("utf-8")

            processed_results.append({
                "part": item["part"],
                "severity": item["severity"],
                "action": item["action"],
                "cost": item["cost"],
                "image": encoded
            })

        except Exception as e:
            print("Error reading crop:", e)

    # Cleanup uploaded image (optional)
    if os.path.exists(file_path):
        os.remove(file_path)

    return {"results": processed_results}