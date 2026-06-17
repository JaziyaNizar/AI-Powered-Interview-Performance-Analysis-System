import streamlit as st
import base64
import matplotlib.pyplot as plt

# PAGE CONFIG 

st.set_page_config(
    page_title="AI Interview Analysis System",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# SESSION STATE 

if "page" not in st.session_state:
    st.session_state.page = "home"

if "candidate_name" not in st.session_state:
    st.session_state.candidate_name = ""

if "roll_number" not in st.session_state:
    st.session_state.roll_number = ""

if "report_data" not in st.session_state:
    st.session_state.report_data = None

if "transcript" not in st.session_state:
    st.session_state.transcript = ""



#  LOAD IMAGE 

def get_base64(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

img = get_base64("intervw_img.png")


#  COMMON BACKGROUND

st.markdown(
    f"""
    <style>

    .stApp {{
        background-image: url("data:image/png;base64,{img}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}

    #MainMenu {{
        visibility: hidden;
    }}

    footer {{
        visibility: hidden;
    }}

    header {{
        visibility: hidden;
    }}

    .main-title {{
        text-align: center;
        color: white;
        font-size: 52px;
        font-weight: bold;
        margin-top: 40px;
        text-shadow: 3px 3px 12px black;
    }}

    .sub-title {{
        text-align: center;
        color: white;
        font-size: 40px;
        font-weight: bold;
        margin-top: 30px;
        text-shadow: 3px 3px 12px black;
    }}

    </style>
    """,
    unsafe_allow_html=True
)

# PAGE 1 : HOME PAGE

if st.session_state.page == "home":

    st.markdown(
        """
        <div class="main-title">
            AI INTERVIEW ANALYSIS SYSTEM
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br><br><br>", unsafe_allow_html=True)
    # ✅ Centered image
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.image(
            "interview_img3.png",
            width=600
        )


    st.markdown("<br><br><br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([3,1,3])

    with col2:
        if st.button("PROCEED", use_container_width=True):
            st.session_state.page = "candidate"
            st.rerun()


# PAGE 2 : CANDIDATE DETAILS

elif st.session_state.page == "candidate":

    st.markdown(
        """
        <div class="sub-title">
            Candidate Details
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br><br><br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])

    with col2:

        candidate_name = st.text_input(
            "Enter Candidate Name"
        )

        roll_number = st.text_input(
            "Enter Roll Number"
        )

        st.markdown("<br>", unsafe_allow_html=True)
        
        

        if st.button(
            "START INTERVIEW",
            use_container_width=True
        ):
            if not candidate_name.strip() or not roll_number.strip():
                st.error("⚠️ Please fill in both Candidate Name and Roll Number before proceeding.")
            else:
                st.session_state.candidate_name = candidate_name
                st.session_state.roll_number = roll_number
                st.session_state.report_data = None  
                st.session_state.transcript = ""      
                st.session_state.page = "interview"
                st.rerun()



# PAGE 3 : INTERVIEW PAGE 

elif st.session_state.page == "interview":

    st.title("AI Interview Analysis")

    st.success(
        f"Candidate : {st.session_state.candidate_name}"
    )

    st.markdown("---")

    st.write("""
    Click the button below to start the interview.

    During the interview:
    - Eye Contact Detection runs
    - Emotion Detection runs
    - Head Pose Detection runs
    - Speech-to-Text runs
    - Speech Analysis runs
    
    Press 'S' to speak something...
    
    Press 'Q' in the OpenCV window to finish the interview.
    """)

    if st.button("START INTERVIEW", use_container_width=True):

        from camera_analysis import run_analysis

        result = run_analysis(
            st.session_state.candidate_name
        )

        st.session_state.report_data = result
        st.session_state.transcript=result.get("transcript", "")

        st.session_state.page = "report"

        st.rerun()

elif st.session_state.page == "report":

    st.title("INTERVIEW REPORT")

    report = st.session_state.report_data

    st.success("Interview Completed Successfully")

    st.markdown("---")

    st.write(f"### Candidate Name")
    st.write(st.session_state.candidate_name)

    # st.write(f"### Roll Number")
    # st.write(st.session_state.roll_number)

    st.markdown("---")

    st.write(f"### Eye Contact Score")
    st.write(f"{report['eye_score']:.2f}%")

    st.write(f"### Dominant Emotion")
    st.write(report['dominant_emotion'])

    st.write("### Emotion Distribution")
    emotion_data = report["emotion_count"]
    fig, ax = plt.subplots(figsize=(4,3))
    ax.bar(
        emotion_data.keys(),
        emotion_data.values()
    )
    ax.set_ylabel("Count")
    ax.set_title("Emotion Detection Summary")
    ax.tick_params(axis='x', rotation=45)

    plt.tight_layout()
    col1, col2, col3 = st.columns([1,2,1])

    with col1:
        st.pyplot(fig)

    st.write(f"### Dominant Head Pose")
    st.write(report['dominant_pose'])

    st.markdown("---")

    st.write("### Head Pose Distribution")
    head_data = report["head_pose_count"]
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.bar(
        head_data.keys(),
        head_data.values()
    )
    ax.set_ylabel("Count")
    ax.set_title("Head Pose Summary")
    plt.xticks(rotation=30)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        st.pyplot(fig)


    st.write(f"### Final Interview Score")
    st.write(f"{report['final_score']:.2f}")

    st.markdown("---")

    st.write(f"### Word Count")
    st.write(report['word_count'])

    st.write(f"### Filler Words")
    st.write(report['filler_count'])

    st.write(f"### Confidence Score")
    st.write(f"{report['confidence_score']}%")

    st.write("### Words Per Minute")
    st.write(report['wpm'])

    st.markdown("---")

    st.write("### Transcript")

    st.write("### AI Feedback")
    for item in report['feedback']:
        st.write(item)
    
    st.text_area(
    "Speech Transcript",
    value=st.session_state.transcript,
    height=200,
    key="transcript_box")

    score = report["final_score"]

    st.markdown("## Final Interview Score")

    st.progress(int(score))

    if score >= 80:
        st.success(f"🏆 {score:.2f}/100  |  Excellent Performance")
    elif score >= 60:
        st.info(f"👍 {score:.2f}/100  |  Good Performance")
    elif score >= 40:
        st.warning(f"⚠️ {score:.2f}/100  |  Average Performance")
    else:
        st.error(f"❌ {score:.2f}/100  |  Needs Improvement")

    st.markdown("---")

    try:

        with open(
            "interview_report.txt",
            "r",
            encoding="utf-8"
        ) as file:

            report_content = file.read()

        st.download_button(
            label="Download Report",
            data=report_content,
            file_name="interview_report.txt",
            mime="text/plain"
        )

    except:
        st.warning("Report file not found.")

    if st.button("BACK TO HOME"):

        st.session_state.page = "home"

        st.rerun()

































# # import cv2
# # import time
# # from eye_contact import detect_eye_contact
# # from emotion_test import detect_emotion
# # from head_pose import get_head_pose
# # from speech_to_text import get_speech_text
# # from report_generator import generate_report
# # from speech_analysis import analyze_speech

# # # ---------------- SCORE TRACKING VARIABLES ----------------

# # total_frames = 0
# # eye_contact_frames = 0

# # emotion_count = {
# #     "happy": 0,
# #     "neutral": 0,
# #     "sad": 0,
# #     "angry": 0,
# #     "fear": 0,
# #     "surprise": 0,
# #     "disgust": 0
# # }

# # head_pose_count = {
# #     "forward": 0,
# #     "left": 0,
# #     "right": 0,
# #     "down": 0
# # }

# # speech_text = ""
# # full_transcript = ""
# # last_speech_time = time.time()

# # # ---------------- EYE CONTACT SCORE ----------------

# # def get_eye_contact_score():
# #     if total_frames == 0:
# #         return 0
# #     return (eye_contact_frames / total_frames) * 100


# # # ---------------- DOMINANT EMOTION ----------------

# # def get_dominant_emotion():
# #     return max(emotion_count, key=emotion_count.get)


# # # ---------------- DOMINANT HEAD POSE ----------------

# # def get_dominant_head_pose():
# #     return max(head_pose_count, key=head_pose_count.get)


# # # ---------------- FINAL SCORE CALCULATION ----------------

# # def calculate_final_score():
# #     eye_score = get_eye_contact_score()

# #     emotion_weights = {
# #         "happy": 100,
# #         "neutral": 60,
# #         "surprise": 70,
# #         "sad": 40,
# #         "angry": 30,
# #         "fear": 20,
# #         "disgust": 20
# #     }

# #     dominant_emotion = get_dominant_emotion()
# #     emotion_score = emotion_weights.get(dominant_emotion, 60)

# #     # head pose impact
# #     dominant_pose = get_dominant_head_pose()
# #     head_pose_score_map = {
# #         "forward": 100,
# #         "left": 60,
# #         "right": 60,
# #         "down": 30
# #     }

# #     head_pose_score = head_pose_score_map.get(dominant_pose, 60)

# #     # FINAL WEIGHTED SCORE
# #     final_score = (
# #         0.5 * eye_score +
# #         0.3 * emotion_score +
# #         0.2 * head_pose_score
# #     )

# #     return final_score, dominant_emotion, dominant_pose


# # # ---------------- MAIN PIPELINE ----------------

# # def run_analysis():
# #     global total_frames, eye_contact_frames
# #     global speech_text,full_transcript,last_speech_time

# #     cap = cv2.VideoCapture(0)

# #     while True:
# #         ret, frame = cap.read()
# #         if not ret:
# #             break

# #         frame = cv2.flip(frame, 1)

# #         # ---------------- EYE CONTACT ----------------
# #         eye_contact = detect_eye_contact(frame)

# #         total_frames += 1
# #         if eye_contact:
# #             eye_contact_frames += 1

# #         # ---------------- EMOTION ----------------
# #         emotion = detect_emotion(frame)

# #         if emotion in emotion_count:
# #             emotion_count[emotion] += 1

# #         # ---------------- HEAD POSE ----------------
# #         head_pose = get_head_pose(frame)

# #         if head_pose in head_pose_count:
# #             head_pose_count[head_pose] += 1
        
# #         # ---------------- SPEECH TO TEXT ----------------
# #         current_time = time.time()

# #         if current_time - last_speech_time > 10:

# #             speech_text = get_speech_text()

# #             if speech_text not in [
# #                 "Could not understand",
# #                 "Speech service unavailable"
# #             ]:
# #                 full_transcript += speech_text + " "

# #             last_speech_time = current_time

# #         # ---------------- FINAL SCORE ----------------
# #         final_score, dominant_emotion, dominant_pose = calculate_final_score()

# #         # ---------------- DISPLAY ----------------
# #         cv2.putText(frame, f"Eye Contact: {eye_contact}",
# #                     (30, 50), cv2.FONT_HERSHEY_SIMPLEX,
# #                     0.8, (0, 255, 0), 2)

# #         cv2.putText(frame, f"Emotion: {emotion}",
# #                     (30, 90), cv2.FONT_HERSHEY_SIMPLEX,
# #                     0.8, (255, 0, 0), 2)

# #         cv2.putText(frame, f"Head Pose: {head_pose}",
# #                     (30, 130), cv2.FONT_HERSHEY_SIMPLEX,
# #                     0.8, (0, 200, 255), 2)

# #         cv2.putText(frame, f"Final Score: {int(final_score)}",
# #                     (30, 170), cv2.FONT_HERSHEY_SIMPLEX,
# #                     0.8, (0, 255, 255), 2)
        
# #         cv2.putText(frame,
# #                     f"Speech: {speech_text[:40]}",
# #                     (30, 210),
# #                     cv2.FONT_HERSHEY_SIMPLEX,
# #                     0.6,
# #                     (255, 255, 255),
# #                     2)

# #         cv2.imshow("AI Interview Analysis", frame)

# #         if cv2.waitKey(1) & 0xFF == ord('q'):
# #             break

# #     cap.release()
# #     cv2.destroyAllWindows()

# #     # ---------------- FINAL REPORT ----------------
# #     final_score, dominant_emotion, dominant_pose = calculate_final_score()

# #     #analyze speech transcript
# #     speech_result=analyze_speech(full_transcript)

# #     word_count=speech_result['word_count']
# #     filler_count=speech_result['filler_count']
# #     confidence_score=speech_result['confidence_score']


# #     generate_report(
# #         get_eye_contact_score(),
# #         dominant_emotion,
# #         dominant_pose,
# #         final_score,
# #         full_transcript,
# #         word_count,
# #         filler_count,
# #         confidence_score
# #     )

# #     print("\n================ FINAL REPORT ================")
# #     print(f"Eye Contact Score: {get_eye_contact_score():.2f}")
# #     print(f"Dominant Emotion: {dominant_emotion}")
# #     print(f"Dominant Head Pose: {dominant_pose}")
# #     print(f"Final Interview Score: {final_score:.2f}")

# #     print(f"Word Count: {word_count}")
# #     print(f"Filler Words: {filler_count}")
# #     print(f"Confidence Score: {confidence_score}%")
    

# #     print("\nSpeech Transcript:")
# #     print(full_transcript)

# #     print("=============================================")

# # # ---------------- RUN PROGRAM ----------------

# # if __name__ == "__main__":
# #     run_analysis()...this is my code in camera analysis.py