import cv2
import numpy as np

# Load the pre-trained face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Load the pre-trained age estimation model
age_net = cv2.dnn.readNetFromCaffe('deploy_age.prototxt', 'age_net.caffemodel')

# Define the age groups
age_groups = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']

# Initialize the webcam
cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Draw rectangles around the detected faces and estimate age
    for (x, y, w, h) in faces:
        # Extract the face region
        face_img = frame[y:y+h, x:x+w].copy()

        # Preprocess the face image for age estimation
        blob = cv2.dnn.blobFromImage(face_img, scalefactor=1.0, size=(227, 227), mean=(78.4263377603, 87.7689143744, 114.895847746), swapRB=False)

        # Pass the face image through the age estimation model
        age_net.setInput(blob)
        age_preds = age_net.forward()

        # Get the predicted age group
        age_index = np.argmax(age_preds)
        age = age_groups[age_index]

        # Draw rectangles around the detected faces and display the age
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, f'Age: {age}', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('Face Scanner', frame)

    # Exit the program if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
