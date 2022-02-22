import face_recognition # Used for face recognition
import cv2 # Used for face detection
import os # Used for file management
import glob # Used for finding paths
import numpy as np # Used for array operations

class SimpleFacerec:
    def __init__(self):
        # Creating the arrays for the encodings and the names
        self.known_face_encodings = []
        self.known_face_names = []

        # Resize frame for a faster speed
        self.frame_resizing = 0.25

    def load_encoding_images(self, images_path):
        # Load all the images of known faces stored in the "users" database
        images_path = glob.glob(os.path.join(images_path, "*.*"))

        # Print the number of images loaded
        # print("{} images found".format(len(images_path)))

        for img_path in images_path:
            # Read the image into "img"
            img = cv2.imread(img_path)
            # Convert the image stored in "img" to RGB to be able to process it using the face_recognition module
            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # Get the file name of the image at the image path
            basename = os.path.basename(img_path)
            # Split the file name into the name and the extension 
            (filename, ext) = os.path.splitext(basename)

            # Get encoding of "rgb_img" to compare against the known encodings
            img_encoding = face_recognition.face_encodings(rgb_img)[0]

            # Store the image encoding as face encoding and the file name as face name (after removing the number at the end)
            self.known_face_encodings.append(img_encoding)
            self.known_face_names.append(filename[:-1])
        print("Encoding images loaded")

    def detect_known_faces(self, frame):
        # Resizing the frame after increasing the width and height by 0 and applying a scaling factor of 0.25 across both dimensions
        small_frame = cv2.resize(frame, (0, 0), fx=self.frame_resizing, fy=self.frame_resizing)

        # Find all the faces and face encodings in the given frame stored in "small_frame" after resizing
        # Convert the image from BGR color to RGB color used by the face_recognition module
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        # Finds the top, right, bottom, left coordinates of the frame in which the face is located
        face_locations = face_recognition.face_locations(rgb_small_frame)
        # Get encoding of the frame stored in "rgb_small_frame" to compare against the known encodings
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        # Create an array to store the names of the people detected
        face_names = []
        for face_encoding in face_encodings:
            # Get an array of boolean values for each known face encoding saying if the face encoding is a match or not
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            name = "Unknown"

            # Get the euclidean distance(s) between the face encoding and the known face encoding(s)
            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            # Get the index of the minimum distance
            best_match_index = np.argmin(face_distances)
            # Check if the index is a match
            if matches[best_match_index]:
                # If it is a match, get the name of the person at the index of the minimum distance and store it in "name"
                name = self.known_face_names[best_match_index]
            # Append the name to the array of names
            face_names.append(name)

        # Convert to numpy array to adjust coordinates with frame resizing
        face_locations = np.array(face_locations)
        face_locations = face_locations / self.frame_resizing
        
        # Return the face locations and the names of the people detected
        return face_locations.astype(int), face_names