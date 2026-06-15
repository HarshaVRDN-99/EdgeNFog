import httpx
import asyncio
import random

filenames = [f"image_{i}.jpeg" for i in range(100)]
methods = ["ayan's edge detector", "cnn_v2", "yolo_count"]

test_data = [
    {
        "filename": filenames[i],
        "sheet_count": random.randint(5, 120),
        "tilt": round(random.uniform(0.1, 25.0), 2),
        "density": [round(random.uniform(0.1, 0.99), 2) for _ in range(5)],
        "estimation_method": random.choice(methods)
    }
    for i in range(100)
]

async def test():
    async with httpx.AsyncClient() as client:
        for i, payload in enumerate(test_data):
            res = await client.post("http://localhost:8003/receive_detection", json=payload)
            print(f"[{i+1}/100] {payload['filename']} | sheets: {payload['sheet_count']} | tilt: {payload['tilt']} | {res.json()}")

asyncio.run(test())