import sqlite3


def create_image_database():
    global connection, cursor
    connection = sqlite3.connect('Image_Database.db', check_same_thread=False, timeout=10)
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS image_data (
            id                   INTEGER PRIMARY KEY AUTOINCREMENT,
            frame_count          INTEGER,
            capture_timestamp    TEXT,
            raw_image_path       TEXT,
            processed_image_path TEXT,
            width                INTEGER,
            height               INTEGER,
            brightness           REAL,
            blur_score           REAL,
            raw_size_kb          REAL,
            processed_size_kb    REAL
        )
    ''')
    connection.commit()
    print("[DB] Image_Database.db ready")

def insert_image_data(
    frame_count, capture_timestamp, raw_image_path, processed_image_path,
    width, height, brightness, blur_score, raw_size_kb, processed_size_kb
):
    cursor.execute('''
        INSERT INTO image_data (
            frame_count, capture_timestamp, raw_image_path, processed_image_path,
            width, height, brightness, blur_score, raw_size_kb, processed_size_kb
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        frame_count, capture_timestamp, raw_image_path, processed_image_path,
        width, height, brightness, blur_score, raw_size_kb, processed_size_kb
    ))
    connection.commit()

def get_all_image_data():
    cursor.execute("SELECT * FROM image_data ORDER BY id DESC")
    return cursor.fetchall()

def get_latest_image():
    cursor.execute("SELECT * FROM image_data ORDER BY id DESC LIMIT 1")
    return cursor.fetchone()

def brightness_avg():
    cursor.execute("SELECT ROUND(AVG(brightness), 2) FROM image_data")
    return cursor.fetchone()[0]

def brightness_max():
    cursor.execute("SELECT MAX(brightness) FROM image_data")
    return cursor.fetchone()[0]

def brightness_min():
    cursor.execute("SELECT MIN(brightness) FROM image_data")
    return cursor.fetchone()[0]

def blur_score_avg():
    cursor.execute("SELECT ROUND(AVG(blur_score), 2) FROM image_data")
    return cursor.fetchone()[0]

def blur_score_max():
    cursor.execute("SELECT MAX(blur_score) FROM image_data")
    return cursor.fetchone()[0]

def blur_score_min():
    cursor.execute("SELECT MIN(blur_score) FROM image_data")
    return cursor.fetchone()[0]

create_image_database()
