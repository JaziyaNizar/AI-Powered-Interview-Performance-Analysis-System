def generate_feedback(
    eye_score,
    emotion,
    head_pose,
    confidence_score,
    wpm
):

    feedback = []

    # Eye Contact
    if eye_score >= 80:
        feedback.append(
            "✅Maintained excellent eye contact."
        )
    elif eye_score >= 60:
        feedback.append(
            "⚠️Eye contact was acceptable but can be improved."
        )
    else:
        feedback.append(
            "❌Needs improvement in maintaining eye contact."
        )

    # Emotion
    if emotion == "happy":
        feedback.append(
            "✅Displayed a positive and friendly expression."
        )

    elif emotion == "neutral":
        feedback.append(
            "✅Maintained a professional expression."
        )

    elif emotion in ["fear", "sad"]:
        feedback.append(
            "❌Appeared nervous during the interview."
        )

    # Head Pose
    if head_pose == "center":
        feedback.append(
            "✅Maintained good head posture."
        )
    else:
        feedback.append(
            "⚠️Try keeping your face directed toward the interviewer."
        )

    # Confidence Score
    if confidence_score >= 80:
        feedback.append(
            "✅Spoke confidently and clearly."
        )
    elif confidence_score >= 60:
        feedback.append(
            "⚠️Confidence level was moderate."
        )
    else:
        feedback.append(
            "❌Work on reducing filler words and improving fluency."
        )

    # WPM
    if wpm < 80:
        feedback.append(
            "❌Speaking pace was too slow."
        )
    elif wpm > 180:
        feedback.append(
            "⚠️Speaking pace was too fast."
        )
    else:
        feedback.append(
            "✅Speaking pace was appropriate."
        )

    return feedback