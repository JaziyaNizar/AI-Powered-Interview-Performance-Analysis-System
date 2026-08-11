import cv2
import mediapipe as mp

mp_face_mesh = mp.solutions.face_mesh.FaceMesh(
    refine_landmarks=True
)

# Key facial landmark points
NOSE_TIP = 1
CHIN = 152
LEFT_EYE = 33
RIGHT_EYE = 263
FOREHEAD = 10


def get_head_pose(frame):
    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = mp_face_mesh.process(rgb)

    if not results.multi_face_landmarks:
        return "No Face"

    face = results.multi_face_landmarks[0].landmark

    nose = face[NOSE_TIP]
    left_eye = face[LEFT_EYE]
    right_eye = face[RIGHT_EYE]
    chin = face[CHIN]
    forehead = face[FOREHEAD]


    nose_x, nose_y = nose.x * w, nose.y * h
    left_x = left_eye.x * w
    right_x = right_eye.x * w
    chin_y = chin.y * h
    forehead_y = forehead.y * h

    #  HEAD LEFT / RIGHT 
    eye_center = (left_x + right_x) / 2

    if nose_x < eye_center - 10:
        return "left"
    elif nose_x > eye_center + 10:
        return "right"

    #  HEAD UP / DOWN 
    face_height_center = (forehead_y + chin_y) / 2

    if nose_y < face_height_center - 10:
        return "up"
    elif nose_y > face_height_center + 10:
        return "down"

    return "center"
