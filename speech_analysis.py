def analyze_speech(transcript, speaking_time):

    # BASIC TEXT PROCESSING
    text = transcript.lower().strip()

    words = text.split()

    word_count = len(words)

    # WORDS PER MINUTE
    if speaking_time > 0:

        minutes = speaking_time / 60

        wpm = round(
            word_count / minutes
        )

    else:

        wpm = 0

    # FILLER WORDS
    filler_words = [
        "um",
        "uh",
        "like",
        "actually",
        "basically",
        "you know"
    ]

    filler_count = 0

    for filler in filler_words:

        filler_count += text.count(filler)

    # FILLER RATIO
    if word_count > 0:

        filler_ratio = (
            filler_count /
            word_count
        ) * 100

    else:

        filler_ratio = 0


    # CONFIDENCE SCORE
    if word_count == 0:

        confidence_score = 0

    else:

        confidence_score = 100

 
        # SPEAKING SPEED
        if wpm < 60:

            confidence_score -= 25

        elif wpm < 90:

            confidence_score -= 10

        elif wpm <= 160:

            # Good speaking speed
            pass

        elif wpm <= 190:

            confidence_score -= 10

        else:

            confidence_score -= 20


        # FILLER WORD USAGE
        if filler_ratio <= 2:

            pass

        elif filler_ratio <= 5:

            confidence_score -= 10

        elif filler_ratio <= 10:

            confidence_score -= 20

        else:

            confidence_score -= 30

        # Keep score between 0 and 100

        confidence_score = max(
            0,
            min(confidence_score, 100)
        )

    # RETURN RESULTS
    return {
        "word_count": word_count,
        "filler_count": filler_count,
        "filler_ratio": round(filler_ratio, 2),
        "confidence_score": confidence_score,
        "wpm": wpm
    }


