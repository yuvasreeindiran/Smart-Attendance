# models/encode_faces.py
import face_recognition
import os
import pickle

def encode_faces(dataset_path='dataset'):
    known_encodings = []
    known_names = []

    for filename in os.listdir(dataset_path):
        if filename.endswith(('.jpg', '.png')):
            image = face_recognition.load_image_file(os.path.join(dataset_path, filename))
            encodings = face_recognition.face_encodings(image)
            if encodings:
                known_encodings.append(encodings[0])
                known_names.append(os.path.splitext(filename)[0])
    
    data = {'encodings': known_encodings, 'names': known_names}
    with open('models/encodings.pickle', 'wb') as f:
        pickle.dump(data, f)

if __name__ == "__main__":
    encode_faces()

