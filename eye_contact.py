import cv2
import mediapipe as mp
import math

# MEDIAPIPE FACE MESH
mp_face_mesh = mp.solutions.face_mesh.FaceMesh(
    refine_landmarks=True,
    max_num_faces=1
)

# EYE LANDMARKS
# Left eye
LEFT_EYE_LEFT = 33
LEFT_EYE_RIGHT = 133
LEFT_EYE_TOP = 159
LEFT_EYE_BOTTOM = 145
LEFT_IRIS = 468

# Right eye
RIGHT_EYE_LEFT = 362
RIGHT_EYE_RIGHT = 263
RIGHT_EYE_TOP = 386
RIGHT_EYE_BOTTOM = 374
RIGHT_IRIS = 473

# DISTANCE FUNCTION
def distance(p1, p2):

    return math.sqrt(
        (p1.x - p2.x) ** 2 +
        (p1.y - p2.y) ** 2
    )

# EYE CONTACT DETECTION
def detect_eye_contact(frame):

    rgb = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    results = mp_face_mesh.process(rgb)

    # No face
    if not results.multi_face_landmarks:
        return False

    face = results.multi_face_landmarks[0]

    # LEFT EYE
    left_outer = face.landmark[LEFT_EYE_LEFT]
    left_inner = face.landmark[LEFT_EYE_RIGHT]

    left_top = face.landmark[LEFT_EYE_TOP]
    left_bottom = face.landmark[LEFT_EYE_BOTTOM]

    left_iris = face.landmark[LEFT_IRIS]

    # Eye width
    left_eye_width = distance(
        left_outer,
        left_inner
    )

    # Eye height
    left_eye_height = distance(
        left_top,
        left_bottom
    )

    # RIGHT EYE
    right_outer = face.landmark[RIGHT_EYE_LEFT]
    right_inner = face.landmark[RIGHT_EYE_RIGHT]

    right_top = face.landmark[RIGHT_EYE_TOP]
    right_bottom = face.landmark[RIGHT_EYE_BOTTOM]

    right_iris = face.landmark[RIGHT_IRIS]

    # Eye width
    right_eye_width = distance(
        right_outer,
        right_inner
    )

    # Eye height
    right_eye_height = distance(
        right_top,
        right_bottom
    )

    # Prevent division by zero
    if (
        left_eye_width == 0
        or right_eye_width == 0
    ):
        return False

    # EYE ASPECT RATIO
    left_ear = (
        left_eye_height /
        left_eye_width
    )

    right_ear = (
        right_eye_height /
        right_eye_width
    )

    avg_ear = (
        left_ear +
        right_ear
    ) / 2


    # CHECK WHETHER EYES ARE OPEN
    # If eyes are closed, immediately return False
    if avg_ear < 0.20:
        return False

    # LEFT IRIS POSITION
    left_ratio = (
        left_iris.x - left_outer.x
    ) / (
        left_inner.x - left_outer.x
    )

    # RIGHT IRIS POSITION
    right_ratio = (
        right_iris.x - right_outer.x
    ) / (
        right_inner.x - right_outer.x
    )


    # AVERAGE IRIS POSITION
    avg_ratio = (
        left_ratio +
        right_ratio
    ) / 2

    # EYE CONTACT
    if 0.35 <= avg_ratio <= 0.65:

        return True

    return False
