import cv2
import requests
import time
import json
import os
import numpy as np

# =========================
# CONFIG
# =========================
API_URL = "http://localhost:8000/count_sheets/?visualize=false"
SEND_EVERY_N_FRAMES = 1
SAVE_EVERY_N_FRAMES = 10
JPEG_QUALITY = 95
SAVE_DIR = "/tmp/edge-detection"
EDGE_IMAGE_URL = "http://10.149.55.87:8003/upload_image"

# Create save directory
os.makedirs(SAVE_DIR, exist_ok=True)

# =========================
# 1080p CSI Camera pipeline
# =========================
gst_pipeline = (
    "nvarguscamerasrc sensor-id=0 ! "
    "video/x-raw(memory:NVMM), width=1920, height=1080, framerate=5/1, format=NV12 ! "
    "nvvidconv flip-method=1 ! "
    "video/x-raw, width=1920, height=1080, format=BGRx ! "
    "videoconvert ! "
    "video/x-raw, format=BGR ! "
    "appsink drop=1 max-buffers=1"
)

print("📷 Opening CSI camera (1080p)...")
cap = cv2.VideoCapture(gst_pipeline, cv2.CAP_GSTREAMER)

if not cap.isOpened():
    print("❌ Failed to open CSI camera")
    exit()

print("✅ Camera opened")
print(f"💾 Saving frames to: {SAVE_DIR}")

frame_count = 0
prev_time = time.time()

while True:
    ret, frame = cap.read()
    if not ret or frame is None:
        print("⚠️ Failed to read frame")
        time.sleep(0.1)
        continue

    frame_count += 1

    # =========================
    # Fix orientation
    # =========================
    frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

    # =========================
    # Save FULL HD raw frame
    # =========================
    if frame_count % SAVE_EVERY_N_FRAMES == 0:
        raw_path = os.path.join(SAVE_DIR, f"raw_{frame_count:05d}.jpg")
        cv2.imwrite(raw_path, frame)
        success, raw_buffer = cv2.imencode(
            ".jpg",
            frame,
            [int(cv2.IMWRITE_JPEG_QUALITY), JPEG_QUALITY]
        )
        if not success:
            print("❌ Failed to encode raw image")
            continue
        print(f"💾 Saved raw frame: {raw_path}")

    # =========================
    # Keep input 1080p / 16:9
    # =========================
    infer_frame = cv2.resize(frame, (1920, 1080))

    # =========================
    # Preprocessing for edge detection model
    # =========================

    # LAB contrast enhancement
    lab = cv2.cvtColor(infer_frame, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    l = clahe.apply(l)

    lab = cv2.merge((l, a, b))
    infer_frame = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

    # Sharpen
    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]])
    infer_frame = cv2.filter2D(infer_frame, -1, kernel)

    # Brightness boost
    infer_frame = cv2.convertScaleAbs(infer_frame, alpha=1.2, beta=10)

    # =========================
    # Save processed frame
    # =========================
    if frame_count % SAVE_EVERY_N_FRAMES == 0:
        processed_path = os.path.join(SAVE_DIR, f"processed_{frame_count:05d}.jpg")
        cv2.imwrite(processed_path, infer_frame)
        success, processed_buffer = cv2.imencode(
            ".jpg",
            infer_frame,
            [int(cv2.IMWRITE_JPEG_QUALITY), JPEG_QUALITY]
        )
        if not success:
            print("❌ Failed to encode processed image")
            continue
        print(f"🛠️ Saved processed frame: {processed_path}")

        try:

            height, width = frame.shape[:2]

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            brightness = float(np.mean(gray))

            blur_score = float(
                cv2.Laplacian(
                    gray,
                    cv2.CV_64F
                ).var()
            )

            raw_size_kb = len(raw_buffer.tobytes()) / 1024

            processed_size_kb = (
                    len(processed_buffer.tobytes()) / 1024
            )

            files = {
                "raw_image": (
                    f"raw_{frame_count:05d}.jpg",
                    raw_buffer.tobytes(),
                    "image/jpeg"
                ),

                "processed_image": (
                    f"processed_{frame_count:05d}.jpg",
                    processed_buffer.tobytes(),
                    "image/jpeg"
                )
            }

            data = {
                "frame_count": frame_count,
                "capture_timestamp": time.time(),

                "width": width,
                "height": height,

                "brightness": brightness,
                "blur_score": blur_score,

                "raw_size_kb": raw_size_kb,
                "processed_size_kb": processed_size_kb
            }

            image_response = requests.post(
                EDGE_IMAGE_URL,
                files=files,
                data=data,
                timeout=20
            )

            print(
                f"📤 Image Upload Status: "
                f"{image_response.status_code}"
            )

        except Exception as e:

            print(
                f"❌ Edge Image Upload Failed: {e}"
            )

    # =========================
    # Send to OpenCV API
    # =========================

    if frame_count % SEND_EVERY_N_FRAMES == 0:
        try:
            success, buffer = cv2.imencode(
                ".jpg",
                infer_frame,
                [int(cv2.IMWRITE_JPEG_QUALITY), JPEG_QUALITY]
            )

            if not success:
                print("❌ Failed to encode frame")
                continue

            # Save exact frame sent to API
            sent_path = os.path.join(SAVE_DIR, "last_sent_frame.jpg")
            cv2.imwrite(sent_path, infer_frame)

            files = {
                "file": ("live_frame.jpg", buffer.tobytes(), "image/jpeg")
            }

            start = time.time()
            response = requests.post(API_URL, files=files, timeout=20)
            latency = time.time() - start

            curr_time = time.time()
            fps = 1 / (curr_time - prev_time)
            prev_time = curr_time

            if response.status_code == 200:
                try:
                    result = response.json()

                    print("\n" + "="*70)
                    print(f"📦 Frame: {frame_count} | FPS: {fps:.2f} | API Roundtrip: {latency:.2f}s")
                    print(f"📄 Sheet Count : {result.get('sheet_count', 'N/A')}")
                    print(f"📐 Tilt        : {result.get('tilt', 'N/A')}")
                    print("📨 Full API Response:")
                    print(json.dumps(result, indent=2))

                    # Save JSON result
                    result_path = os.path.join(SAVE_DIR, f"result_{frame_count:05d}.json")
                    with open(result_path, "w") as f:
                        json.dump(result, f, indent=2)

                except Exception:
                    print("⚠️ Non-JSON response:")
                    print(response.text)
            else:
                print(f"❌ API Error {response.status_code}: {response.text}")

        except Exception as e:
            print(f"❌ Request failed: {e}")

cap.release()
