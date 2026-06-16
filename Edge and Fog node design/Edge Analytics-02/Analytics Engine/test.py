import httpx
import asyncio
import random
import io
import numpy as np

#  Config
EDGE_URL   = "http://localhost:8003"
DRONE_IDS  = ["drone_01", "drone_02", "drone_03"]
METHODS    = ["ayan's edge detector", "cnn_v2", "yolo_count"]
FILENAMES  = [f"image_{i:03d}.jpeg" for i in range(20)]

# Helpers

def random_payload(i):
    return {
        "filename":          FILENAMES[i % len(FILENAMES)],
        "sheet_count":       random.randint(5, 120),
        "tilt":              round(random.uniform(0.1, 25.0), 2),
        "density":           [round(random.uniform(0.1, 0.99), 2) for _ in range(10)],
        "estimation_method": random.choice(METHODS),
        "drone_id":          random.choice(DRONE_IDS),
    }

def fake_image_bytes(width=64, height=64):
    """Generate a small random JPEG-like byte payload for testing."""
    arr = np.random.randint(0, 255, (height, width, 3), dtype=np.uint8)
    import cv2
    success, buf = cv2.imencode(".jpg", arr)
    return buf.tobytes() if success else b"\xff\xd8\xff" * 100


# Test 1: Health check

async def test_health(client):
    print("\n Health Check ")
    res = await client.get(f"{EDGE_URL}/health")
    print(f"Status: {res.status_code} | {res.json()}")


# Test 2: Detection receiver

async def test_detections(client, n=20):
    print(f"\n Detection Receiver ({n} records) ")
    passed = 0
    failed = 0
    for i in range(n):
        payload = random_payload(i)
        try:
            res = await client.post(f"{EDGE_URL}/receive_detection", json=payload)
            status = "✅" if res.status_code == 200 else "❌"
            if res.status_code == 200:
                passed += 1
            else:
                failed += 1
            print(f"[{i+1:02d}/{n}] {status} {payload['drone_id']} | "
                  f"{payload['filename']} | "
                  f"sheets={payload['sheet_count']} | "
                  f"tilt={payload['tilt']} | "
                  f"{res.json()}")
        except Exception as e:
            failed += 1
            print(f"[{i+1:02d}/{n}] ❌ Request failed: {e}")

    print(f"\nDetections — passed: {passed} | failed: {failed}")


async def test_image_upload(client, n=5):
    print(f"\n Image Upload ({n} frames)")
    passed = 0
    failed = 0
    for i in range(n):
        try:
            img_bytes = fake_image_bytes()
            drone_id  = random.choice(DRONE_IDS)

            files = {
                "raw_image":       (f"raw_{i:05d}.jpg",       img_bytes, "image/jpeg"),
                "processed_image": (f"processed_{i:05d}.jpg", img_bytes, "image/jpeg"),
            }
            data = {
                "frame_count":       str(i * 10),
                "capture_timestamp": str(1700000000.0 + i * 10),
                "width":             "1920",
                "height":            "1080",
                "brightness":        str(round(random.uniform(80, 200), 2)),
                "blur_score":        str(round(random.uniform(50, 500), 2)),
                "raw_size_kb":       str(round(len(img_bytes) / 1024, 2)),
                "processed_size_kb": str(round(len(img_bytes) / 1024, 2)),
                "drone_id":          drone_id,
            }

            res = await client.post(f"{EDGE_URL}/upload_image", files=files, data=data, timeout=20)
            status = "✅" if res.status_code == 200 else "❌"
            if res.status_code == 200:
                passed += 1
            else:
                failed += 1
            print(f"[{i+1:02d}/{n}] {status} {drone_id} | frame={i*10} | {res.json()}")

        except Exception as e:
            failed += 1
            print(f"[{i+1:02d}/{n}] ❌ Upload failed: {e}")

    print(f"\nImage uploads — passed: {passed} | failed: {failed}")

async def test_validation(client):
    print("\nValidation Check ")

    tests = [
        ("Missing sheet_count", {"filename": "bad.jpg"}),
        ("Missing filename", {"sheet_count": 10}),
        ("Empty body", {}),
    ]

    passed = 0
    failed = 0

    for name, payload in tests:
        res = await client.post(
            f"{EDGE_URL}/receive_detection",
            json=payload
        )

        if res.status_code == 422:
            passed += 1
            print(f"✅ {name}")
        else:
            failed += 1
            print(
                f"❌ {name} | Expected 422, got {res.status_code} | {res.text}"
            )

    print(f"Validation — passed: {passed} | failed: {failed}")

async def main():
    async with httpx.AsyncClient(timeout=15.0) as client:
        await test_health(client)
        await test_detections(client, n=20)
        await test_image_upload(client, n=5)
        await test_validation(client)
    print("\n All tests complete")

asyncio.run(main())

'''
To be run with:
    python test_edge.py

    uvicorn edge_app:app --host 0.0.0.0 --port 8003
'''