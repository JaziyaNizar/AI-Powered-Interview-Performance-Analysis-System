def generate_feedback(
    eye_score,
    emotion,
    head_pose,
    confidence_score,
    wpm
):

    feedback = []

    # EYE CONTACT
    if eye_score >= 80:

        feedback.append(
            "✅ Excellent eye contact was maintained throughout the interview."
        )

    elif eye_score >= 60:

        feedback.append(
            "⚠️ Eye contact was acceptable, but try to maintain more consistent focus toward the interviewer."
        )

    else:

        feedback.append(
            "❌ Eye contact needs improvement. Try to look toward the interviewer more consistently."
        )

    # EMOTION / FACIAL EXPRESSION
    if emotion == "happy":

        feedback.append(
            "✅ You displayed a positive and friendly facial expression."
        )

    elif emotion == "neutral":

        feedback.append(
            "✅ You maintained a calm and professional facial expression."
        )

    elif emotion == "surprise":

        feedback.append(
            "⚠️ Your facial expression varied noticeably during the interview."
        )

    elif emotion in ["fear", "sad"]:

        feedback.append(
            "⚠️ Your facial expression indicated some nervousness or discomfort."
        )

    elif emotion == "angry":

        feedback.append(
            "⚠️ Try to maintain a calmer and more relaxed facial expression."
        )

    elif emotion == "disgust":

        feedback.append(
            "⚠️ Try to maintain a more neutral and professional facial expression."
        )


    # HEAD POSE
    if head_pose == "center":

        feedback.append(
            "✅ You maintained good head posture and faced the interviewer properly."
        )

    elif head_pose in ["left", "right"]:

        feedback.append(
            "⚠️ Your head was frequently turned away. Try to keep your face directed toward the interviewer."
        )

    elif head_pose == "down":

        feedback.append(
            "⚠️ You frequently looked downward. Try to keep your head upright while answering."
        )

    elif head_pose == "up":

        feedback.append(
            "⚠️ Try to maintain a more natural forward-facing head position."
        )

    # SPEECH FLUENCY
    if confidence_score >= 85:

        feedback.append(
            "✅ Speech fluency was strong with good control of filler words and speaking pace."
        )

    elif confidence_score >= 70:

        feedback.append(
            "⚠️ Speech fluency was good, but there is still room to improve pace and reduce hesitation."
        )

    elif confidence_score >= 50:

        feedback.append(
            "⚠️ Speech fluency was moderate. Try to reduce filler words and maintain a steadier speaking pace."
        )

    else:

        feedback.append(
            "❌ Speech fluency needs improvement. Practice speaking continuously with fewer pauses and filler words."
        )

    # SPEAKING SPEED
    if wpm == 0:

        feedback.append(
            "❌ No measurable speech was detected."
        )

    elif wpm < 60:

        feedback.append(
            "❌ Your speaking pace was too slow. Try to speak more continuously."
        )

    elif wpm < 90:

        feedback.append(
            "⚠️ Your speaking pace was slightly slow. Aim for a more natural conversational pace."
        )

    elif wpm <= 160:

        feedback.append(
            "✅ Your speaking pace was appropriate for an interview."
        )

    elif wpm <= 190:

        feedback.append(
            "⚠️ Your speaking pace was slightly fast. Try slowing down for better clarity."
        )

    else:

        feedback.append(
            "❌ Your speaking pace was too fast. Slow down to improve clarity."
        )

    return feedback
