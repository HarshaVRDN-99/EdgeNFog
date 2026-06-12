from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import numpy as np
import cv2
import httpx
from sheet_counter.processing import SheetStackProcessor

EDGE_URL= "http://10.149.55.87:8003/receive_detection"
LOGGER_URL = "http://logger-server:8001/log_sheets_data/"
MAX_DIM = 1280
app = FastAPI()
processor = SheetStackProcessor()

@app.post("/count_sheets/")
async def count_sheets(file: UploadFile = File(...), visualize: bool = False):
    contents = await file.read()
    img_array = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    if img is None:
        return JSONResponse(status_code=400, content={"error": "Invalid image format"})

    # Cap resolution to avoid memory spike on Jetson Orin
    h, w = img.shape[:2]
    if max(h, w) > MAX_DIM:
        scale = MAX_DIM / max(h, w)
        img = cv2.resize(img, (int(w * scale), int(h * scale)))

    count, density, tilt = processor.count_sheets_from_image(img, visualize=visualize)

    payload = {
        "filename": file.filename,
        "sheet_count": count,
        "tilt": tilt,
        "density": density.tolist() if hasattr(density, "tolist") else density,
        
    }

    # Logger — mandatory, must complete
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            await client.post(LOGGER_URL, json=payload)
        except Exception as e:
            print(f"[!] Failed to log to logger: {e}")
            return JSONResponse(status_code=502, content={"error": f"Logger failed: {str(e)}"})

        # Edge — mandatory, must complete
        try:
            await client.post(EDGE_URL, json=payload)
        except Exception as e:
            print(f"[!] Failed to forward to edge: {e}")
            return JSONResponse(status_code=502, content={"error": f"Edge forward failed: {str(e)}"})

    return {"filename": file.filename, "sheet_count": count, "tilt": tilt}


'''
uvicorn api.server_main:app --reload
curl -X POST -F "file=@raw/nowrap_images/image1.jpeg" http://localhost:8000/count_sheets/
curl -X POST -F "file=@raw/nowrap_images/image1.jpeg" "http://localhost:8000/count_sheets/?visualize=true"
'''

"estimation_method": "ayan's edge detector"