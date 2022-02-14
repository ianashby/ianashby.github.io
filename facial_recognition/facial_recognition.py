"""
Ian Ashby
Facial Recognition

Use CV2 to detect face, then use Deepface to analyze the emotion being displayed. 
"""

import cv2
from deepface import DeepFace
from collections import Counter

# Use the frontalface Haar cascade to scan for face on screen.
face_cascades = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt.xml')
cv2.namedWindow("Emotion Analysis")
video = cv2.VideoCapture(2)

# This list will store all the emotions detected while the video is open.
emotions = ['happy', 'happy', 'sad', 'neutral', 'sad']

# While the camera is on and opened, the program will run. The window will close on ESC.
while video.isOpened():
    # ret is a boolean variable that returns true if the frame is available.
    # frame will get the next frame from the camera
    ret, frame = video.read()

    # Convert the image to grayscale for better detection.
    grayscale = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    # scaleFactor rescales the input image, resizing a larger face to a smaller one, and making it detectable by the algorithm.
    # minNeighbors affects the quality of detected faces. 
    face_detection = face_cascades.detectMultiScale(grayscale, scaleFactor = 1.4, minNeighbors = 5)

    # Set the bounding box to scan the face. Create the box lines that will surround the face.
    for x,y,w,h in face_detection:
        img = cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)

        try:
            # Analyze, save, and print the current real-time emotion from the face on camera.
            analyze = DeepFace.analyze(frame, actions=['emotion'])
            emotions.append(analyze['dominant_emotion'])
            print(analyze['dominant_emotion'])
        except:
            print('No face detected.')


    cv2.imshow("Emotion Analysis", frame)
    key = cv2.waitKey(1)
    # Program will close on ESC.
    if key == 27:
        break

video.release()
cv2.destroyWindow("Emotion Analysis")

# Create a dictionary to store how many times each emotion was displayed.
counter = collections.Counter(emotions)
total_sum = len(emotions)
happy_percentage = counter['happy'] / total_sum * 100
neutral_percentage = counter['neutral'] / total_sum * 100
sad_percentage = counter['sad'] / total_sum * 100

print("\nPercentage of happy, neutral, and sad emotions: ")
print(f"Happy Percentage: {happy_percentage:.2f}%")
print(f"Neutral Percentage: {neutral_percentage:.2f}%")
print(f"Sad Percentage: {sad_percentage:.2f}%\n")