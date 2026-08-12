import cv2
import av
import threading
import numpy as np
import streamlit as st

from twilio.rest import Client
from av.audio.resampler import AudioResampler
from streamlit_webrtc import webrtc_streamer
from speech_to_text import get_speech_text

from eye_contact import detect_eye_contact
from emotion_test import detect_emotion
from head_pose import get_head_pose



# SHARED ANALYSIS DATA
lock = threading.Lock()

audio_lock = threading.Lock()

audio_chunks = []

audio_sample_rate = 16000

audio_frame_count = 0

audio_resampler = AudioResampler(
    format="s16",
    layout="mono",
    rate=16000
)

audio_frames= []

analysis_data = {
    "total_frames": 0,
    "eye_contact_frames": 0,

    "emotion_count": {
        "happy": 0,
        "neutral": 0,
        "sad": 0,
        "angry": 0,
        "fear": 0,
        "surprise": 0,
        "disgust": 0,
    },

    "head_pose_count": {
        "center": 0,
        "left": 0,
        "right": 0,
        "up": 0,
        "down": 0,
        "No Face": 0,
    },
}



# RESET ANALYSIS
def reset_analysis():

    with lock:

        analysis_data["total_frames"] = 0
        analysis_data["eye_contact_frames"] = 0

        analysis_data["emotion_count"] = {
            "happy": 0,
            "neutral": 0,
            "sad": 0,
            "angry": 0,
            "fear": 0,
            "surprise": 0,
            "disgust": 0,
        }

        analysis_data["head_pose_count"] = {
            "center": 0,
            "left": 0,
            "right": 0,
            "up": 0,
            "down": 0,
            "No Face": 0,
        }



# VIDEO FRAME CALLBACK
def video_frame_callback(frame):

    # Convert WebRTC frame to OpenCV image
    img = frame.to_ndarray(format="bgr24")

    # Mirror webcam
    img = cv2.flip(img, 1)

 
    # EYE CONTACT
    try:
        eye_contact = detect_eye_contact(img)
    except Exception:
        eye_contact = False

   
    # EMOTION
    try:
        emotion = detect_emotion(img)
    except Exception:
        emotion = "No Face Detected"

  
    # HEAD POSE
    if emotion == "No Face Detected":

        head_pose = "No Face"
        eye_contact = False

    else:

        try:
            head_pose = get_head_pose(img)
        except Exception:
            head_pose = "No Face"

   
    # UPDATE ANALYSIS COUNTERS
    with lock:

        analysis_data["total_frames"] += 1

        if eye_contact:
            analysis_data["eye_contact_frames"] += 1

        if emotion in analysis_data["emotion_count"]:
            analysis_data["emotion_count"][emotion] += 1

        if head_pose in analysis_data["head_pose_count"]:
            analysis_data["head_pose_count"][head_pose] += 1


    # DISPLAY ON CAMERA
    cv2.putText(
        img,
        f"Eye Contact: {eye_contact}",
        (30, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2,
    )

    cv2.putText(
        img,
        f"Emotion: {emotion}",
        (30, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 0, 0),
        2,
    )

    cv2.putText(
        img,
        f"Head Pose: {head_pose}",
        (30, 120),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 200, 255),
        2,
    )

    # Return processed frame
    return av.VideoFrame.from_ndarray(
        img,
        format="bgr24"
    )

def audio_frame_callback(frame):

    global audio_frame_count

    try:

        # Convert incoming browser audio
        # to mono, 16-bit, 16 kHz
        resampled_frames = audio_resampler.resample(frame)

        with audio_lock:

            for resampled_frame in resampled_frames:

                samples = resampled_frame.to_ndarray()

                samples = samples.reshape(-1)

                audio_chunks.append(
                    samples.copy()
                )

                audio_frame_count += 1

        # DO NOT PLAY MICROPHONE AUDIO BACK TO USER
        original_samples = frame.to_ndarray()

        silent_samples = np.zeros_like(
            original_samples
        )

        silent_frame = av.AudioFrame.from_ndarray(
            silent_samples,
            format=frame.format.name,
            layout=frame.layout.name
        )

        silent_frame.sample_rate = frame.sample_rate

        return silent_frame

    except Exception as e:

        print("AUDIO ERROR:", e)

        return frame

def get_audio_frames():

    with audio_lock:

        chunks = audio_chunks.copy()

    print("TOTAL AUDIO CHUNKS:", len(chunks))
    print("SAMPLE RATE: 16000")

    return chunks, 16000

def reset_audio():

    global audio_chunks
    global audio_frame_count

    with audio_lock:

        audio_chunks = []
        audio_frame_count = 0

def get_audio_status():

    with audio_lock:
        return audio_frame_count

# GET ANALYSIS RESULT
def get_analysis_result():

    with lock:

        total_frames = analysis_data["total_frames"]

        eye_contact_frames = analysis_data["eye_contact_frames"]

        emotion_count = analysis_data["emotion_count"].copy()

        head_pose_count = analysis_data["head_pose_count"].copy()


    # EYE CONTACT SCORE
    if total_frames == 0:

        eye_score = 0

    else:

        eye_score = (
            eye_contact_frames / total_frames
        ) * 100

   
    # DOMINANT EMOTION
    emotion_total = sum(emotion_count.values())

    if emotion_total == 0:

        dominant_emotion = "No Face Detected"

    else:

        dominant_emotion = max(
            emotion_count,
            key=emotion_count.get
        )

  
    # DOMINANT HEAD POSE
    pose_total = sum(head_pose_count.values())

    if pose_total == 0:

        dominant_pose = "No Face"

    else:

        dominant_pose = max(
            head_pose_count,
            key=head_pose_count.get
        )


    # EMOTION SCORE
    emotion_weights = {

        "happy": 100,
        "neutral": 80,
        "surprise": 40,
        "sad": 40,
        "angry": 30,
        "fear": 20,
        "disgust": 20,
    }

    emotion_score = emotion_weights.get(
        dominant_emotion,
        40
    )


    # HEAD POSE SCORE
    head_pose_score_map = {

        "center": 100,
        "left": 60,
        "right": 60,
        "up": 50,
        "down": 30,
        "No Face": 0,
    }

    head_pose_score = head_pose_score_map.get(
        dominant_pose,
        40
    )

    # FINAL SCORE
    final_score = (
        0.5 * eye_score
        + 0.3 * emotion_score
        + 0.2 * head_pose_score
    )


    # RETURN RESULT
    return {
        "eye_score": eye_score,
        "dominant_emotion": dominant_emotion,
        "dominant_pose": dominant_pose,
        "visual_score": final_score,
        "emotion_count": emotion_count,
        "head_pose_count": head_pose_count,
    }

# START CAMERA
def start_camera():

    try:
       
        # TWILIO STUN / TURN CONFIGURATION
        account_sid = st.secrets["TWILIO_ACCOUNT_SID"]
        auth_token = st.secrets["TWILIO_AUTH_TOKEN"]

        client = Client(
            account_sid,
            auth_token
        )

        token = client.tokens.create(
            ttl=3600
        )

        rtc_configuration = {
            "iceServers": token.ice_servers
        }

        print(
            "Twilio TURN configuration loaded successfully"
        )

    except Exception as e:

        print(
            "Twilio TURN configuration error:",
            e
        )

        # FALLBACK GOOGLE STUN
        rtc_configuration = {
            "iceServers": [
                {
                    "urls": [
                        "stun:stun.l.google.com:19302"
                    ]
                }
            ]
        }


    # START WEBRTC CAMERA + MICROPHONE
    
    ctx = webrtc_streamer(

        key="interview-camera",

        video_frame_callback=video_frame_callback,

        audio_frame_callback=audio_frame_callback,

        media_stream_constraints={
            "video": True,
            "audio": True,
        },

        rtc_configuration=rtc_configuration,

    )

    return ctx

















