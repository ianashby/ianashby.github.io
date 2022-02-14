"""
Ian Ashby
Facial Recognition
"""

import cv2
from deepface import DeepFace

# Use the frontface Haar cascade to scan for face on screen.
face_cascades = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt.xml')
cv2.namedWindow("preview")
video = cv2.VideoCapture(2)

# While the camera is on and opened, the program will run. The window will close on ESC.
while video.isOpened():
    # ret is a boolean variable that returns true if the frame is available.
    # frame will get the next frame from the camera
    ret, frame = video.read()

    # Convert the image to grayscale for better detection.
    grayscale = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    # scaleFactor rescales the input image, resizing a larger face to a smaller one, and making it detectable by the algorithm.
    # minNeighbors affects the quality of detected faces. 
    face = face_cascades.detectMultiScale(grayscale, scaleFactor = 1.1, minNeighbors = 5)

    # Set the bounding box to scan the face. Create the box lines that will surround the face.
    for x,y,w,h in face:
        img = cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)

        try:
            # Analyze and print the current real-time emotion from the face on camera.
            analyze = DeepFace.analyze(frame, actions=['emotion'])
            print(analyze['dominant_emotion'])
        except:
            print('No face detected.')


    cv2.imshow("preview", frame)
    key = cv2.waitKey(1)
    # Program will close on ESC.
    if key == 27:
        break

video.release()
cv2.destroyWindow("preview")