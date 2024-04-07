import cv2
import time

# Load the cascade classifiers
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Open the camera
cap = cv2.VideoCapture(0)
c = 0
cooldown = 0  # Cooldown period after a blink (in frames)

# Initialize the start time and it is using time record for program execution
start_time = time.time()

while True:
    # Capture frame-by-frame
    ret, img = cap.read()

    if ret:  # Check if the frame has been captured
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Detect faces in the image
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            # Draw rectangle around the face
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = img[y:y + h, x:x + w]

            # Detect eyes within the face region
            eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 5)

            # If both eyes are detected, consider it a blink
            if len(eyes) == 2 and cooldown == 0:
                c += 1
                cooldown = 10  # Set cooldown period to 10 frames
                out = "Blinks: " + str(c)
                #blink image printed on image box
                cv2.putText(img, out, (x, y + h + 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Display the resulting frame
        cv2.imshow('img', img)

        # Decrease cooldown period
        if cooldown > 0:
            cooldown -= 1

    else:
        print("Failed to capture frame")

    # Check for 'ESC' key press to exit
    k = cv2.waitKey(30) & 0xff
    if k == 27 or time.time() - start_time >= 30: 
        break

# Release the capture
cap.release()
cv2.destroyAllWindows()

# Print the total count of blinking eyes
print("Total blinks:", c)

# Determine if the user is tired or can continue based on the number of blinks
if c <= 7:
    print("You are tired")
else:
    print("You can continue")
