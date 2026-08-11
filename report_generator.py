def generate_report(
    candidate_name,
    eye_score,
    dominant_emotion,
    dominant_pose,
    final_score,
    transcript,
    word_count,
    filler_count,
    confidence_score,
    wpm,
    feedback,
    rating
):

    report = f"""
================ AI INTERVIEW REPORT ================

Candidate Name    : {candidate_name}

Eye Contact Score : {eye_score:.2f}%

Dominant Emotion  : {dominant_emotion}

Dominant Head Pose: {dominant_pose}

Final Score       : {final_score:.2f}

Word count        : {word_count}

Filler Words      : {filler_count}

Speech Fluency Score : {confidence_score}%

Words Per Minute  : {wpm}

Speech Transcript : {transcript}

AI Feedback       : {feedback}

Overall Rating    : {rating}

=====================================================
"""

    # Save report
    with open("interview_report.txt", "w", encoding="utf-8") as file:
        file.write(report)

    print(report)
    print("Report saved as interview_report.txt")
