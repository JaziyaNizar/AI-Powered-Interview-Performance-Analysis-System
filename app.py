import streamlit as st
import base64
import matplotlib.pyplot as plt

from camera_analysis import ( 
        start_camera,
        get_analysis_result,
        reset_analysis,
        get_audio_frames,
        reset_audio,
        get_audio_status
)

from speech_to_text import get_speech_text
from speech_analysis import analyze_speech
from feedback_generator import generate_feedback
from report_generator import generate_report

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

if "interview_started" not in st.session_state:
    st.session_state.interview_started = False



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
    /* =========================================
       TEXT VISIBILITY FIX
       ========================================= */

    h1, h2, h3, h4, h5, h6 {
        color: #FFFFFF !important;
    }

    p, span, label {
        color: #FFFFFF !important;
    }

    [data-testid="stMarkdownContainer"] {
        color: #FFFFFF !important;
    }

    [data-testid="stMarkdownContainer"] p {
        color: #FFFFFF !important;
    }

    [data-testid="stMetricLabel"] {
        color: #FFFFFF !important;
    }

    [data-testid="stMetricValue"] {
        color: #FFFFFF !important;
    }

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

                # Reset camera analysis for the new interview
                reset_analysis()
                reset_audio()

                # Reset interview status
                st.session_state.interview_started = False


                st.session_state.page = "interview"

                st.rerun()



# PAGE 3 : INTERVIEW PAGE 

elif st.session_state.page == "interview":

    st.title("AI Interview Performance Assessment")

    st.success(
        f"Candidate: {st.session_state.candidate_name}"
    )

    st.markdown("---")

    st.markdown("### Interview Instructions")

    st.write("""
    This assessment evaluates selected visual and speech-based communication indicators during your interview session.

    **During the assessment, the system will analyze:**

    - 👁️ **Eye Contact**
    - 🙂 **Facial Expression** 
    - 🧑 **Head Posture** 
    - 🎤 **Speech Performance**
    - 📝 **Speech Transcript**

    For the best results, sit in a well-lit environment, keep your face clearly visible, position yourself directly in front of the camera, and speak clearly at a natural pace.
    """)

    st.info(
        "When you are ready, click START in the camera window below and allow camera and microphone access."
    )

    st.markdown("### Interview Session")

    ctx = start_camera()


    if ctx.state.playing:

        st.session_state.interview_started = True

        st.success(
            "● Interview session in progress — camera and microphone are active."
        )

        audio_count = get_audio_status()

        if audio_count > 0:

            st.caption(
                "🎤 Microphone connected and audio is being captured."
            )

        else:

            st.caption(
                "🎤 Waiting for microphone audio..."
            )

    else:

        if st.session_state.interview_started:

            st.success(
                "Interview session stopped. Click FINISH INTERVIEW to generate your assessment report."
            )

        else:

            st.info(
                "The interview has not started. Click START in the camera window when you are ready."
            )


    if st.button(
        "FINISH INTERVIEW",
        use_container_width=True
    ):

        if ctx.state.playing:

            st.warning(
                "Please click STOP in the camera window before selecting FINISH INTERVIEW."
            )

        else:

            result = get_analysis_result()

            # Get recorded browser microphone audio
            audio = get_audio_frames()

            # Convert speech to text
            transcript, speaking_time = get_speech_text(audio)

            result["transcript"] = transcript

            print(
                "Actual interview duration:",
                round(speaking_time, 2),
                "seconds"
            )

            # Analyze speech using actual duration
            speech_result = analyze_speech(
                transcript,
                speaking_time
            )

            result["word_count"] = speech_result["word_count"]
            result["filler_count"] = speech_result["filler_count"]
            result["confidence_score"] = speech_result["confidence_score"]
            result["wpm"] = speech_result["wpm"]

            
            # SPEAKING PACE SCORE

            wpm = result["wpm"]

            if wpm == 0:
                pace_score = 0

            elif 90 <= wpm <= 160:
                pace_score = 100

            elif 75 <= wpm < 90:
                pace_score = 80

            elif 60 <= wpm < 75:
                pace_score = 60

            elif 160 < wpm <= 180:
                pace_score = 80

            elif 180 < wpm <= 200:
                pace_score = 60

            else:
                pace_score = 40

            result["pace_score"] = pace_score

           
            # FACIAL EXPRESSION SCORE

            emotion_score_map = {
                "happy": 100,
                "neutral": 90,
                "surprise": 70,
                "sad": 50,
                "fear": 50,
                "angry": 40,
                "disgust": 40
            }

            emotion_score = emotion_score_map.get(
                result["dominant_emotion"],
                50
            )

            result["emotion_score"] = emotion_score


            
            # HEAD POSTURE SCORE
            head_pose_score_map = {
                "center": 100,
                "left": 70,
                "right": 70,
                "up": 60,
                "down": 50,
                "No Face": 0
            }

            head_pose_score = head_pose_score_map.get(
                result["dominant_pose"],
                50
            )

            result["head_pose_score"] = head_pose_score

            # FINAL INTERVIEW SCORE
            final_score = (
                0.30 * result["eye_score"]
                + 0.15 * result["emotion_score"]
                + 0.15 * result["head_pose_score"]
                + 0.25 * result["confidence_score"]
                + 0.15 * result["pace_score"]
            )

            result["final_score"] = round(
                final_score,
                2
            )


            feedback = generate_feedback(
                result["eye_score"],
                result["dominant_emotion"],
                result["dominant_pose"],
                result["confidence_score"],
                result["wpm"]
            )

            result["feedback"] = feedback

            if result["final_score"] >= 80:
                result["rating"] = "Excellent"

            elif result["final_score"] >= 60:
                result["rating"] = "Good"

            elif result["final_score"] >= 40:
                result["rating"] = "Average"

            else:
                result["rating"] = "Needs Improvement"

           
            # GENERATE UPDATED REPORT FILE
            generate_report(
                st.session_state.candidate_name,
                result["eye_score"],
                result["dominant_emotion"],
                result["dominant_pose"],
                result["final_score"],
                result["transcript"],
                result["word_count"],
                result["filler_count"],
                result["confidence_score"],
                result["wpm"],
                result["feedback"],
                result["rating"]
            )

            st.session_state.report_data = result

            st.session_state.transcript = ""

            st.session_state.page = "report"

            st.rerun()

elif st.session_state.page == "report":

    st.title("INTERVIEW REPORT")

    report = st.session_state.report_data

    st.success("Interview Completed Successfully")

    st.markdown("---")

    st.write(f"### Candidate Name")
    st.write(st.session_state.candidate_name)


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

    st.write(f"### Speech Fluency Score")
    st.write(f"{report['confidence_score']}%")

    st.write("### Words Per Minute")
    st.write(report['wpm'])

    st.markdown("---")


    # TRANSCRIPT
    st.write("### Transcript")

    st.text_area(
        "Speech Transcript",
        value=report["transcript"],
        height=200
    )

   
    # AI FEEDBACK
    st.write("### AI Feedback")

    for item in report["feedback"]:
        st.write(item)


    # FINAL SCORE
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

































