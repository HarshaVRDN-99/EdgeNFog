from DatasetMaker import (
    get_total_detections,
    get_average_sheet_count,
    get_max_sheet_count,
    get_min_sheet_count,
    get_latest_detection,
    get_min_tilt,
    get_max_tilt,
    get_avg_tilt
)
import sqlite3

def sheet_count_summary():
        return {
            "total_detections": get_total_detections(),
            "average_sheet_count": get_average_sheet_count(),
            "max_sheet_count": get_max_sheet_count(),
            "min_sheet_count": get_min_sheet_count()
        }

def tilt_summary():
    return {
        "max tilt:": get_max_tilt(),
        "min tilt:": get_min_tilt(),
        "avg tilt:": get_avg_tilt()
    }

def latest_detection_summary():
    latest = get_latest_detection()
    return {
        "latest_record": latest
    }

def report():
    return {
        "Sheet count analytics": sheet_count_summary(),
        "Tilt summary": tilt_summary(),
        "Latest detection": latest_detection_summary()
    }








