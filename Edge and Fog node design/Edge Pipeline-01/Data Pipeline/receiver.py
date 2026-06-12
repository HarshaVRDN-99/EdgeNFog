from fastapi import FastAPI, Request
from datetime import datetime
from DatasetMaker import create_database
from fastapi.responses import JSONResponse
from DatasetMaker import insert_detected_features
from analytics import report

app = FastAPI()
create_database()

@app.post("/receive_detection")
async def receive_detection(request: Request):
    data = await request.json()
    received_timestamp = datetime.now().isoformat()
    filename = data.get("filename")
    sheet_count = data.get("sheet_count")
    tilt = data.get("tilt")
    density = data.get("density")
    estimation_method=data.get("estimation_method")

    try:
        insert_detected_features(
            filename,
            received_timestamp,
            sheet_count,
            tilt,
            density,
            estimation_method)
    except Exception as e:
        print(f"[!] DB insert failed: {e}")
        return JSONResponse(status_code=500, content={"error": f"DB insert failed: {str(e)}"})
    print("Data has reached")
    return {
        "status": "success"
    }

@app.get("/dashboard_data")
async def dashboard_data():
    return report()

'''uvicorn receiver:app --host 0.0.0.0 --port 8003'''