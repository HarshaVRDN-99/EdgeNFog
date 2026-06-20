# Sprint 1 – Edge Pipeline

## Overview

This sprint implements the Edge Pipeline responsible for receiving images from the drone, performing preprocessing operations, and forwarding processed data to the Fog layer.

## Processing Tasks

- Image reception
- Image validation
- Storing metadata in database
- Edge detection
- Data packaging
- Edge-to-Fog transmission

## Folder structure

```
Edge Pipeline-01/
├── Data Pipeline/
│   ├── DatasetMaker.py   # SQLite layer for detection records (Database.db)
│   ├── receiver.py       # FastAPI app — receives detections + images from drone
│   └── sender.py         # Drone-side FastAPI app — runs SheetCounter, posts to edge
└── Image Pipeline/
    ├── image_data.py     # SQLite layer for image metadata (Image_Database.db)
    └── Far_edge_image.py # Drone-side capture loop — camera, preprocessing, upload
```

## Running locally

Install dependencies:
```bash
pip install -r requirements.txt
```

Start the edge receiver (run from `Data Pipeline/`, with `image_data.py` copied alongside `receiver.py`):
```bash
uvicorn receiver:app --host 0.0.0.0 --port 8003
```

Health check:
```bash
curl http://localhost:8003/health
```

## Notes

- `receiver.py` exposes two routes: `/receive_detection` (JSON detection results) and `/upload_image` (multipart raw + processed frames).
- `sender.py` and `Far_edge_image.py` run on the drone (Jetson), not on the edge node — they're included here for reference on the payload shapes the edge expects.
- `EDGE_URL` in `sender.py` and `EDGE_IMAGE_URL` in `Far_edge_image.py` are hardcoded to a LAN IP — update these to match your edge laptop's address before running.


