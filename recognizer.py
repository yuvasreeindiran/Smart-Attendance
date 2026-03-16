# recognizer.py (optional improvement)
import face_recognition
import cv2
import pickle
import os
from datetime import datetime

def mark_attendance(name):
    folder = "attendance"
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    filename = f"{folder}/{datetime.now().date()}.csv"
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            f.write('Name,Time\n')
    with open(filename, 'r+') as f:
        lines = f.readlines()
        names = [line.split(',')[0] for line in lines]
        if name not in names:
            now = datetime.now().strftime("%H:%M:%S")
            f.write(f'{name},{now}\n')

def recognize_faces():
    with open('models/encodings.pickle', 'rb') as f:
        data = pickle.load(f)

    cam = cv2.VideoCapture(0)
    while True:
        ret, frame = cam.read()
        if not ret:
            break
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        faces = face_recognition.face_locations(rgb_frame)
        encodings = face_recognition.face_encodings(rgb_frame, faces)

        for encoding, face_location in zip(encodings, faces):
            matches = face_recognition.compare_faces(data['encodings'], encoding)
            name = "Unknown"
            if True in matches:
                matched_idx = matches.index(True)
                name = data['names'][matched_idx]
                mark_attendance(name)

            top, right, bottom, left = face_location
            cv2.rectangle(frame, (left, top), (right, bottom), (0,255,0), 2)
            cv2.putText(frame, name, (left, top-10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255,255,255), 2)

        cv2.imshow("Face Attendance", frame)
        if cv2.waitKey(1) == ord('q'):
            break
    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    recognize_faces()
