from fastapi import (
    FastAPI,
    UploadFile,
    File,
    Form
)
import os
app=FastAPI()

from image_data import (
    create_image_database,
    insert_image_data
)
create_image_database()

@app.post("/upload_image")
async def upload_image(

    raw_image: UploadFile = File(...),

    processed_image: UploadFile = File(...),

    frame_count: int = Form(...),

    capture_timestamp: float = Form(...),

    width: int = Form(...),

    height: int = Form(...),

    brightness: float = Form(...),

    blur_score: float = Form(...),

    raw_size_kb: float = Form(...),

    processed_size_kb: float = Form(...)
):
    RAW_DIR = "images/raw"
    PROCESSED_DIR = "images/processed"

    os.makedirs(RAW_DIR, exist_ok=True)
    os.makedirs(PROCESSED_DIR, exist_ok=True)

    raw_path = os.path.join(
        RAW_DIR,
        raw_image.filename
    )

    processed_path = os.path.join(
        PROCESSED_DIR,
        processed_image.filename
    )

    with open(raw_path, "wb") as f:
        f.write(await raw_image.read())

    with open(processed_path, "wb") as f:
        f.write(await processed_image.read())

    insert_image_data(
        frame_count,
        capture_timestamp,
        raw_path,
        processed_path,
        width,
        height,
        brightness,
        blur_score,
        raw_size_kb,
        processed_size_kb
    )
    return {
            "status": "success",
            "frame_count": frame_count
        }

'''uvicorn receiver:app --host 0.0.0.0 --port 8003'''