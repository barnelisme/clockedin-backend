from flask import Flask, Response, render_template
import cv2
import face_recognition
import datetime
import pymysql

app = Flask(__name__)

# Database configuration
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "clockedin",
}

# Load known face encodings and names from the database
def load_known_faces():
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()

    query = "SELECT firstname, lastname, picture FROM users"
    cursor.execute(query)

    known_face_names = []
    known_face_encodings = []

    for firstname, lastname, picture in cursor.fetchall():
        known_face_names.append(f"{firstname} {lastname}")
        known_face_encodings.append(face_recognition.face_encodings(picture)[0])

    cursor.close()
    connection.close()

    return known_face_names, known_face_encodings

known_face_names, known_face_encodings = load_known_faces()

# Create the record table if it doesn't exist
connection = pymysql.connect(**db_config)
cursor = connection.cursor()

create_record_table = """
CREATE TABLE IF NOT EXISTS record (
    id INT AUTO_INCREMENT PRIMARY KEY,
    firstname VARCHAR(255),
    lastname VARCHAR(255),
    date DATE,
    day_of_week VARCHAR(255),
    time TIME,
    timestamp INT,
    datetime DATETIME,
    picture LONGBLOB
)
"""

cursor.execute(create_record_table)
cursor.close()
connection.close()

# Camera view and face recognition
def gen_frames():
    camera = cv2.VideoCapture(0)

    while True:
        success, frame = camera.read()

        if not success:
            break

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

                now = datetime.datetime.now()
                date = now.strftime("%d-%m-%Y")
                day_of_week = now.strftime("%A")
                time = now.strftime("%H:%M:%S")
                timestamp = int(now.timestamp())
                datetime_full = now.strftime("%d-%m-%Y %H:%M:%S")

                connection = pymysql.connect(**db_config)
                cursor = connection.cursor()

                insert_query = """
                INSERT INTO record (firstname, lastname, date, day_of_week, time, timestamp, datetime, picture)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(insert_query, (name.split()[0], name.split()[1], date, day_of_week, time, timestamp, datetime_full, frame.tobytes()))

                connection.commit()
                cursor.close()
                connection.close()

            # Rest of the code for face recognition drawing...

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Routes and app.run()...

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
