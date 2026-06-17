import cv2
import time
import threading
from eye_contact import detect_eye_contact
from emotion_test import detect_emotion
from head_pose import get_head_pose
from speech_to_text import get_speech_text
from report_generator import generate_report
from speech_analysis import analyze_speech
from feedback_generator import generate_feedback

# SCORE TRACKING VARIABLES 

total_frames = 0
eye_contact_frames = 0

emotion_count = {
    "happy": 0,
    "neutral": 0,
    "sad": 0,
    "angry": 0,
    "fear": 0,
    "surprise": 0,
    "disgust": 0
}

head_pose_count = {
    "center":0,
    "left": 0,
    "right": 0,
    "up": 0,
    "down": 0,
    "No Face":0
}

speech_text = ""
full_transcript = ""
total_speaking_time = 0
is_recording=False
recording_status="Idle"
last_speech_time = time.time()

# EYE CONTACT SCORE 

def get_eye_contact_score():
    if total_frames == 0:
        return 0
    score= (eye_contact_frames / total_frames) * 100
    return min(score,100)


# DOMINANT EMOTION 

def get_dominant_emotion():
    total = sum(emotion_count.values())

    if total == 0:
        return "No Face Detected"
    return max(emotion_count, key=emotion_count.get)


#  DOMINANT HEAD POSE

def get_dominant_head_pose():
    return max(head_pose_count, key=head_pose_count.get)


# FINAL SCORE CALCULATION 

def calculate_final_score():
    eye_score = get_eye_contact_score()

    emotion_weights = {
        "happy": 100,
        "neutral": 80,
        "surprise": 40,
        "sad": 40,
        "angry": 30,
        "fear": 20,
        "disgust": 20
    }

    dominant_emotion = get_dominant_emotion()
    emotion_score = emotion_weights.get(dominant_emotion, 40)

    # head pose impact
    dominant_pose = get_dominant_head_pose()
    head_pose_score_map = {
        "center": 100,
        "left": 60,
        "right": 60,
        "up": 50,
        "down": 30,
        "No Face": 0
    }

    head_pose_score = head_pose_score_map.get(dominant_pose, 40)

    # FINAL WEIGHTED SCORE
    final_score = (
        0.5 * eye_score +
        0.3 * emotion_score +
        0.2 * head_pose_score
    )

    return final_score, dominant_emotion, dominant_pose

def record_speech():
    global speech_text
    global full_transcript
    global total_speaking_time
    global is_recording
    global recording_status

    is_recording = True
    recording_status="Listening...."

    print("\nSpeak your answer now...")

    speech_start = time.time()

    speech_text = get_speech_text()
    recording_status="Stopped"
    is_recording=False

    speech_end = time.time()

    total_speaking_time += (speech_end - speech_start)

    if speech_text not in [
        "Could not understand",
        "Speech service unavailable"
    ]:
        full_transcript += speech_text + " "

#  MAIN PIPELINE 

def run_analysis(candidate_name):
    global total_frames, eye_contact_frames
    global speech_text,full_transcript,last_speech_time
    global emotion_count, head_pose_count
    global total_speaking_time
    global is_recording
    global recording_status

    
    total_frames = 0
    eye_contact_frames = 0
    speech_text = ""
    full_transcript = ""
    last_speech_time = time.time()
    total_speaking_time=0
    is_recording=False

    emotion_count = {
        "happy": 0, "neutral": 0, "sad": 0,
        "angry": 0, "fear": 0, "surprise": 0, "disgust": 0
    }

    head_pose_count = {
        "center": 0, "left": 0, "right": 0, "up": 0, "down": 0,"No Face":0
    }

    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)

        #  EYE CONTACT 
        eye_contact = detect_eye_contact(frame)
        total_frames += 1


        # EMOTION 
        emotion = detect_emotion(frame)
        if emotion != "No Face Detected":
            emotion_count[emotion] += 1

        if emotion == "No Face Detected":

            eye_contact = False
            head_pose = "No Face"
        else:
            eye_contact = detect_eye_contact(frame)
            if eye_contact:
                eye_contact_frames += 1

            head_pose = get_head_pose(frame)

        # Count head pose
        if head_pose in head_pose_count:
            head_pose_count[head_pose] += 1


        # FINAL SCORE 
        final_score, dominant_emotion, dominant_pose = calculate_final_score()

        #  DISPLAY 

        cv2.putText(frame, f"Eye Contact: {eye_contact}",
                    (30, 50), cv2.FONT_HERSHEY_SIMPLEX,
                    0.8, (0, 255, 0), 2)

        if emotion == "No Face Detected":
            emotion_color = (0, 0, 255)
        else:
            emotion_color = (255, 0, 0)

        cv2.putText(
            frame,
            f"Emotion: {emotion}",
            (30, 90),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            emotion_color,
            2
        )

        cv2.putText(frame, f"Head Pose: {head_pose}",
                    (30, 130), cv2.FONT_HERSHEY_SIMPLEX,
                    0.8, (0, 200, 255), 2)
    
        cv2.putText(frame,
                    f"Mic: {recording_status}",
                    (30, 170),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (255, 255, 0),
                    2)

        
        cv2.putText(frame,
                    f"Speech: {speech_text[:40]}",
                    (30, 210),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (255, 255, 255),
                    2)

        cv2.imshow("AI Interview Analysis", frame)

        key = cv2.waitKey(1) & 0xFF

        # Press S to capture speech

        if key == ord('s') and not is_recording:

            speech_thread = threading.Thread(
                target=record_speech
            )

            speech_thread.start()

        # Press Q to end interview
        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    # FINAL REPORT 
    final_score, dominant_emotion, dominant_pose = calculate_final_score()

    #analyze speech transcript
    speech_result=analyze_speech(full_transcript,total_speaking_time)

    word_count=speech_result['word_count']
    filler_count=speech_result['filler_count']
    confidence_score=speech_result['confidence_score']
    wpm=speech_result["wpm"]

    if final_score >= 80:
        rating = "Excellent"
    elif final_score >= 60:
        rating = "Good"
    elif final_score >= 40:
        rating = "Average"
    else:
        rating = "Needs Improvement"

    feedback=generate_feedback(
        get_eye_contact_score(),
        dominant_emotion,
        dominant_pose,
        confidence_score,
        wpm
    )


    generate_report(
        candidate_name,
        get_eye_contact_score(),
        dominant_emotion,
        dominant_pose,
        final_score,
        full_transcript,
        word_count,
        filler_count,
        confidence_score,
        wpm,
        feedback,
        rating
    )

    print("\n================ FINAL REPORT ================")
    print(f"Eye Contact Score: {get_eye_contact_score():.2f}")
    print(f"Dominant Emotion: {dominant_emotion}")
    print(f"Dominant Head Pose: {dominant_pose}")
    print(f"Final Interview Score: {final_score:.2f}")

    print(f"Word Count: {word_count}")
    print(f"Filler Words: {filler_count}")
    print(f"Confidence Score: {confidence_score}%")
    print(f"Words per minute:{wpm}")
    

    print("\nSpeech Transcript:")
    print(full_transcript)

    print("\nAI FEEDBACK")
    print(feedback)

    print("\nOverall Rating")
    print(rating)

    print("=============================================")

    return {
    "eye_score": get_eye_contact_score(),
    "dominant_emotion": dominant_emotion,
    "dominant_pose": dominant_pose,
    "final_score": final_score,
    "transcript": full_transcript,
    "word_count": word_count,
    "filler_count": filler_count,
    "confidence_score": confidence_score,
    "wpm": wpm,
    "feedback": feedback,
    "rating": rating,
    "emotion_count": emotion_count,
    "head_pose_count": head_pose_count
}


















# ---------------- RUN PROGRAM ----------------

if __name__ == "__main__":
    run_analysis("test candidate")