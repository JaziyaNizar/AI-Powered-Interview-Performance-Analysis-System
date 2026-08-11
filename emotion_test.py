import cv2
from deepface import DeepFace

# Load OpenCV face detector
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)  #cv2.data.haarcascades
   #----Returns the path to OpenCV's built-in Haar Cascade models.


def detect_emotion(frame):
    # Convert frame to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,  #reduces false detection
        minSize=(50, 50) #ignores images smaller than this size
    )

    # No face found
    if len(faces) == 0:
        return "No Face Detected"

    try:
        result = DeepFace.analyze(
            img_path=frame,
            actions=["emotion"],
            enforce_detection=False
        )

        if isinstance(result, list):
            result = result[0]

        return result["dominant_emotion"]

    except Exception as e:
        print("Error:", e)
        return "Unknown"






















