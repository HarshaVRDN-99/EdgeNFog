from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import JSONResponse
from datetime import datetime
import os
from DatasetMaker import create_database, insert_detected_features
from image_data import create_image_database, insert_image_data

app = FastAPI()

create_database()
create_image_database()

RAW_DIR = "images/raw"
PROCESSED_DIR = "images/processed"
os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)


#Health check

@app.get("/health")
async def health():
    return {"status": "ok", "timestamp": datetime.now().isoformat()}

@app.post("/receive_detection")
async def receive_detection(request: Request):
    try:
        data = await request.json()

        received_timestamp = datetime.now().isoformat()
        filename = data.get("filename")
        sheet_count = data.get("sheet_count")
        tilt = data.get("tilt")
        density = data.get("density")
        estimation_method = data.get("estimation_method")
        drone_id = data.get("drone_id", "unknown")

        if filename is None or sheet_count is None:
            return JSONResponse(
                status_code=422,
                content={"error": "filename and sheet_count are required"}
            )

        insert_detected_features(
            filename, received_timestamp, sheet_count,
            tilt, density, estimation_method, drone_id
        )

        print(f"[detection] {drone_id} | {filename} | count={sheet_count} | tilt={tilt}")
        return {"status": "success", "filename": filename, "sheet_count": sheet_count}

    except Exception as e:
        print(f"[detection] ERROR: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})

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
        processed_size_kb: float = Form(...),
        drone_id: str = Form(default="unknown"),
):
    try:

        raw_filename = f"{drone_id}_{raw_image.filename}"
        processed_filename = f"{drone_id}_{processed_image.filename}"

        raw_path = os.path.join(RAW_DIR, raw_filename)
        processed_path = os.path.join(PROCESSED_DIR, processed_filename)

        with open(raw_path, "wb") as f:
            f.write(await raw_image.read())

        with open(processed_path, "wb") as f:
            f.write(await processed_image.read())

        insert_image_data(
            frame_count, capture_timestamp, raw_path, processed_path,
            width, height, brightness, blur_score, raw_size_kb, processed_size_kb
        )

        print(f"[image] {drone_id} | frame={frame_count} | brightness={brightness:.1f} | blur={blur_score:.1f}")
        return {"status": "success", "frame_count": frame_count}

    except Exception as e:
        print(f"[image] ERROR: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})


'''
    uvicorn edge_app:app --host 0.0.0.0 --port 8003

Test detection:
    curl -X POST http://localhost:8003/receive_detection \
      -H "Content-Type: application/json" \
      -d '{"filename":"test.jpg","sheet_count":42,"tilt":1.2,"density":[0.1,0.2],"estimation_method":"ayan edge detector"}'

Test health:
    curl http://localhost:8003/health'''