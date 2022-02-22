# BCI3006 - Biometrics J Component

## How to save images of yourself
### Step 1 - Install the necessary modules
```
pip install imutils
pip install opencv-contrib-python
```

### Step 2 - Run data_collection.py
```
python data_collection.py --cascade haarcascade_frontalface_default.xml --output dataset
```

Note: You can replace `dataset` with the name of your own output folder, however we recommend against it

### Step 3 - Take images
By pressing the 'k' key, you can take an image of yourself

### Step 4 - Quit the program
By pressing the 'q' key, you can close the camera and quit the program at any time after the video stream begins

### Step 5 - Rename the image
The images taken by `data_collection.py` are saved as 00000.png, 00001.png, 00002.png, and so on.

If you do not want to be labelled as such during the face recognition process, please rename your image file.

## How to run Face Recognition feature
### Step 1 - Install the necessary modules
```
pip install imutils
pip install opencv-contrib-python
pip install dlib
pip install face_recognition
```

Note: You may face issues with the installation of the `dlib` module

### Step 1 - Face enrollment
Follow the steps provided above to take a picture of yourself and automatically save it to the appropriate folder.

### Step 2 - Starting the program
Open command prompt and type the following:  
```
python faceRecognition.py
```

### Step 3 - Face recognition
Hold up different faces in front of the camera to see whether a match exists or not.

If a match exists then a rectangle with the name of the file to which it matches will be displayed.

If there is no match, then a rectangle with the text "unknown" will be displayed.