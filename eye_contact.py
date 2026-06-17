import cv2
import mediapipe as mp

mp_face_mesh = mp.solutions.face_mesh.FaceMesh(
    refine_landmarks=True,
    max_num_faces=1
)

# Left eye landmarks
LEFT_EYE_LEFT = 33
LEFT_EYE_RIGHT = 133
LEFT_IRIS = 468

# Right eye landmarks
RIGHT_EYE_LEFT = 362
RIGHT_EYE_RIGHT = 263
RIGHT_IRIS = 473


def detect_eye_contact(frame):

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = mp_face_mesh.process(rgb)

    if not results.multi_face_landmarks:
        return False

    face = results.multi_face_landmarks[0]

    h, w, _ = frame.shape

    #  LEFT EYE 

    left_corner = face.landmark[LEFT_EYE_LEFT]
    right_corner = face.landmark[LEFT_EYE_RIGHT]
    left_iris = face.landmark[LEFT_IRIS]

    left_x = int(left_corner.x * w)
    right_x = int(right_corner.x * w)
    iris_x = int(left_iris.x * w)

    left_eye_width = abs(right_x - left_x)

    if left_eye_width == 0:
        return False
    
    #calculating the iris position ratio
    left_ratio = abs(iris_x - left_x) / left_eye_width  

    #  RIGHT EYE 

    left_corner_r = face.landmark[RIGHT_EYE_LEFT]
    right_corner_r = face.landmark[RIGHT_EYE_RIGHT]
    right_iris = face.landmark[RIGHT_IRIS]

    left_x_r = int(left_corner_r.x * w)
    right_x_r = int(right_corner_r.x * w)
    iris_x_r = int(right_iris.x * w)

    right_eye_width = abs(right_x_r - left_x_r)

    if right_eye_width == 0:
        return False

    right_ratio = abs(iris_x_r - left_x_r) / right_eye_width

    # AVERAGE

    avg_ratio = (left_ratio + right_ratio) / 2

    # Looking approximately at camera
    if 0.35 <= avg_ratio <= 0.65:
        return True

    return False

























# OPTIONAL TEST RUN 
if __name__ == "__main__":
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        eye_contact = detect_eye_contact(frame)

        if eye_contact:
            text = "Eye Contact: YES"
            color = (0, 255, 0)
        else:
            text = "Eye Contact: NO"
            color = (0, 0, 255)

        cv2.putText(frame, text, (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

        cv2.imshow("Eye Contact Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


























# import cv2
# import mediapipe as mp

# mp_face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)


# def detect_eye_contact(frame):

#     rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     results = mp_face_mesh.process(rgb)

#     if results.multi_face_landmarks:
#         return True
#     else:
#         return False


# # -----------------------------
# # OPTIONAL TEST RUN (standalone mode)
# # -----------------------------
# if __name__ == "__main__":
#     cap = cv2.VideoCapture(0)

#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break

#         eye_contact = detect_eye_contact(frame)

#         if eye_contact:
#             text = "Eye Contact: YES"
#             color = (0, 255, 0)
#         else:
#             text = "Eye Contact: NO"
#             color = (0, 0, 255)

#         cv2.putText(frame, text, (30, 50),
#                     cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

#         cv2.imshow("Eye Contact Detection", frame)

#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     cap.release()
#     cv2.destroyAllWindows()

















"""
Returns True if face is detected (eye contact assumed),
otherwise False.
"""






# import cv2
# import mediapipe as mp

# mp_face_mesh = mp.solutions.face_mesh.FaceMesh(
#     refine_landmarks=True
# )

# cap = cv2.VideoCapture(0)

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break

#     rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     results = mp_face_mesh.process(rgb)

#     if results.multi_face_landmarks:
#         cv2.putText(frame,
#                     "Eye Contact: YES",
#                     (30, 50),
#                     cv2.FONT_HERSHEY_SIMPLEX,
#                     1,
#                     (0, 255, 0),
#                     2)
#     else:
#         cv2.putText(frame,
#                     "Eye Contact: NO",
#                     (30, 50),
#                     cv2.FONT_HERSHEY_SIMPLEX,
#                     1,
#                     (0, 0, 255),
#                     2)

#     cv2.imshow("Eye Contact Detection", frame)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()
