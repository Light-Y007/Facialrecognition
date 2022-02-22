# Team 13
# Team members:-
# Abhiram V. Joshi - 20BCE0504
# Gauri Gupta - 20BCE0495
# Paarth Agrawal - 20BCE500
# Shashank Suresh - 20BCE0484


from imutils.video import VideoStream
import argparse
import imutils
import time
import cv2
import os


ap = argparse.ArgumentParser()

# Argument parser for linking the haarcascade classifier
ap.add_argument("-c", "--cascade", required=True,
	help = "path to where the face cascade resides")

args = vars(ap.parse_args()) 

# Load the classifier
detector = cv2.CascadeClassifier(args["cascade"])

# Name of the current user
name = input("Enter your name: ")


print("Starting video stream")
vs = VideoStream(src=0).start()
time.sleep(1)

total = 0

# Creating a file for storing user data
if not os.path.exists("users.txt"):
	with open("users.txt", "w") as file:
		pass

# Opening the file containing the existing users in read mode
file_read = open("users.txt", "r")
file_read.seek(0)
content = file_read.readlines()

# Dictionary for storing the data of the current user
data = {"line_name":None, "line_image_count":None, "index":None}

# user_exists variable to check if the user was created
user_exists=0

# Extracting the data of the user from the file
for i in range(len(content)):
	line = content[i]
	
	# Extracting the name in the (i+1)th line
	line_name = line.rstrip().split("-")[0]

	# If the user exists
	if line_name==name:
		data["line_name"] = name
		data["line_image_count"] = int(line.rstrip().split("-")[1])
		data["index"] = i
		user_exists=1
		break

# If the user doesn't exist
if user_exists==0:
	data["line_name"] = name
	data["line_image_count"] = 0
	data["index"] = len(content)
	content.append(f"{data['line_name']}-{data['line_image_count']}\n")

# Closing the file
file_read.flush()
file_read.close()

# Opening the file containing the existing users in write mode
file_write = open("users.txt", "w")

while True:

	# Sets a limit to the number of images that one user can store
	image_count_limit=5

	# Checks if the user has already reached the maximum number of allowed images
	if data["line_image_count"]>=image_count_limit:
		print("Can't add more images!")
		break

	file_write.seek(0)

	# Running the video stream
	frame = vs.read()
	orig = frame.copy()
	frame = imutils.resize(frame, width=400)

	# Detecting faces using the classifier
	rects = detector.detectMultiScale(
		cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), scaleFactor=1.1, 
		minNeighbors=5, minSize=(30, 30))

	# Drawing a rectangle around the detected faces
	for (x, y, w, h) in rects:
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
	cv2.imshow("Frame", frame)

	# Waits for a keypress for one millisecond
	key=cv2.waitKey(1)

	# Creates a path to the user's folder
	path = os.path.join("users",name)
	
	# If the user captures an image by pressing c
	if key == ord("c"):
		
		# Creates user's folder if it doesn't exist
		if not os.path.exists("users"):
			os.system('cacls users /E /P everyone:f')
			os.makedirs("users")
			os.system('cacls users /E /P everyone:n')
		
		# Creates a folder for the user if it doesn't already exist
		if not os.path.exists(path):
			os.system('cacls users /E /P everyone:f')
			os.makedirs(path)
			os.system('cacls users /E /P everyone:n')
		
		# Creates a desktop for the user if it doesn't already exist
		if not os.path.exists(os.path.join('Desktop', name)):
			os.system(f'cacls Desktop\{name} /E /P everyone:f')
			os.makedirs(os.path.join('Desktop', name))
			os.system(f'cacls Desktop\{name} /E /P everyone:n')

		# Creates a path to the next image file
		p = os.path.join(path, f"{name}{data['line_image_count']}.png")
		
		# Writes data to the file
		os.system('cacls users /E /P everyone:f')
		cv2.imwrite(p, orig)
		os.system('cacls users /E /P everyone:n')
		total+=1

		# Updates the file
		data["line_image_count"]+=1
		content[data["index"]] = f"{data['line_name']}-{data['line_image_count']}\n"

	# Quit the process if the user presses q
	if key == ord("q"):
		break
	
file_write.writelines(content)
file_write.close()

print(f"{total} images were captured and stored")
cv2.destroyAllWindows()
vs.stop()

