import cv2
from simple_facerec import SimpleFacerec
import os
from time import sleep, time

os.system('cacls users /E /P everyone:f')

sfr = SimpleFacerec()

file_read = open("users.txt", "r")
file_read.seek(0)
content = file_read.readlines()

for i in content:
    name = i.strip().split("-")[0]
    sfr.load_encoding_images(os.path.join("users", name))

cap = cv2.VideoCapture(0)
pause = time()

names = []

while True:
    ret, frame = cap.read()

    face_locations, face_name = sfr.detect_known_faces(frame)

    if face_name != "Unknown" and face_locations.any():
        pause = time()
        if face_name[0] not in names:
            names.append(face_name[0])
            os.system(f'cacls Desktop\{face_name[0]} /E /P everyone:f')
            print(names)

        # for face_loc, name in zip(face_locations, face_name):
        #     y1, x1, y2, x2 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
        #     cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), 2)
        #     cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # cv2.imshow("frame", frame)

    else:
        # print(time()-pause)
        if time()-pause>=3:
            for i in names:
                os.system(f'cacls Desktop\{i} /E /P everyone:n')
            break

    key = cv2.waitKey(1)
    if key == ord('q'):
        for i in names:
                os.system(f'cacls Desktop\{i} /E /P everyone:n')
        break

cap.release()
cv2.destroyAllWindows()