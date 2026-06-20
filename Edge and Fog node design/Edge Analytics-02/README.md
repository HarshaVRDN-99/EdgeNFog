# Sprint 2 – Edge Analytics

## Overview

This sprint builds the analytics and visualisation layer on top of the Edge Pipeline (Sprint 1). It reads from the same SQLite databases (`Database.db` and `Image_Database.db`) that the receiver populates, and exposes the results through a Streamlit dashboard plus a standalone test suite.

## Folder structure

```
Edge Analytics-02/
└── Analytics Engine/
    ├── DatasetMaker.py          # Detection DB layer (shared with Edge Pipeline-01)
    ├── dashboard.py             # Streamlit dashboard — Overview, Charts, All Detections, Image Analytics
    ├── test.py                  # End-to-end test script: health check, detections, image upload, validation
    └── Edge Analytics Engine    # Sprint task notes
```

## Running locally

Install dependencies:
```bash
pip install -r ../Edge\ Pipeline-01/requirements.txt
```

Make sure the receiver from `Edge Pipeline-01` is running first (port 8003), then start the dashboard:
```bash
streamlit run dashboard.py
```

Open the dashboard in a browser at the Network URL Streamlit prints (e.g. `http://<edge-ip>:8501`).

## Running the test suite

With the receiver running, in a separate terminal:
```bash
python test.py
```

This sends 20 randomised detection records, 5 fake image uploads, and 3 validation checks against the receiver, and prints a pass/fail summary for each.

## Dashboard pages

- **Overview** — sheet count and tilt summary metrics, plus the latest detection.
- **Charts** — sheet count over time and per-record bar chart.
- **All Detections** — full table of every detection, including `drone_id`.
- **Image Analytics** — brightness and blur score metrics/trends from uploaded frames, plus the latest image record.

Auto-refresh (10s) is available as a sidebar toggle on every page.

## Notes

- `DatasetMaker.py` here must stay in sync with the copy in `Edge Pipeline-01/Data Pipeline/` — both the receiver and the dashboard read/write the same `Database.db` file, so they need matching schemas. If you change one, update the other.
- The dashboard expects `image_data.py` (from `Edge Pipeline-01/Image Pipeline/`) to be present in the same working directory when run.
