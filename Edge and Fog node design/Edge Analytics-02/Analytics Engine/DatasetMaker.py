import sqlite3
import json

def insert_detected_features(
    filename,
    received_timestamp,
    sheet_count,
    tilt,
    density,
    estimation_method,drone_id=None):

    cursor.execute('''
    INSERT INTO detected_features(filename,received_timestamp,sheet_count,tilt,density,estimation_method,drone_id)
       values(?,?,?,?,?,?,?)
    ''',
                   (filename,
    received_timestamp,
    sheet_count,
    tilt,
    json.dumps(density),
    estimation_method,drone_id)
    )
    connection.commit()

def get_data():
    cursor.execute("SELECT * from detected_features")
    data=cursor.fetchall()
    return data

def get_latest_detection():
    cursor.execute("SELECT * FROM detected_features ORDER BY id DESC LIMIT 1")
    latest_record = cursor.fetchone()
    return latest_record

def get_total_detections():
    cursor.execute("SELECT COUNT(*) FROM detected_features")
    row = cursor.fetchone()
    return row[0] if row else 0

def get_average_sheet_count():
    cursor.execute("""SELECT ROUND(AVG(sheet_count),2) FROM detected_features""")
    return cursor.fetchone()[0]

def get_max_sheet_count():
    cursor.execute("""SELECT MAX(sheet_count) FROM detected_features""")
    return cursor.fetchone()[0]

def get_min_sheet_count():
    cursor.execute("""SELECT MIN(sheet_count) FROM detected_features""")
    return cursor.fetchone()[0]

def get_max_tilt():
    cursor.execute("SELECT MAX(tilt) FROM detected_features")
    return cursor.fetchone()[0]

def get_min_tilt():
    cursor.execute("SELECT MIN(tilt) FROM detected_features")
    return cursor.fetchone()[0]

def get_avg_tilt():
    cursor.execute("SELECT ROUND(AVG(tilt),2) FROM detected_features")
    return cursor.fetchone()[0]

def create_database():
     global connection, cursor
     connection = sqlite3.connect('Database.db', check_same_thread=False, timeout=10)
     cursor = connection.cursor()
     cursor.execute('''
     CREATE TABLE IF NOT EXISTS detected_features(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            received_timestamp TEXT NOT NULL,
            sheet_count INTEGER,
            tilt REAL,
            density TEXT,
            estimation_method TEXT,
            drone_id TEXT
            )
       ''')
     connection.commit()

def clear_database():
    cursor.execute("DELETE FROM detected_features")
    connection.commit()

create_database()
