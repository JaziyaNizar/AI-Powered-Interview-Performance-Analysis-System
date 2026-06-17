def analyze_speech(transcript,speaking_time):
    #convert to lowercase
    text=transcript.lower()

    #count words
    words=text.split()
    word_count=len(words)

    if speaking_time>0:
        minutes=speaking_time/60
        wpm=round(word_count/minutes)
    else:
        wpm=0

    #common filler words
    filler_words=[
        "um",
        "uh",
        "like",
        "actually",
        "basically",
        "you know"
    ]

    filler_count=0

    for filler in filler_words:
        filler_count+=text.count(filler)
    
    #confidence score
    if word_count == 0:
        confidence_score = 0

    else:
        confidence_score = 100
        if word_count<50:
            confidence_score-=20


        # Filler word penalty
        confidence_score -= filler_count * 5

        # Speaking speed penalty
        if wpm < 40:
            confidence_score -= 20

        elif wpm < 90:
            confidence_score -= 10

        confidence_score = max(0, min(confidence_score, 100))
    return{
        "word_count":word_count,
        "filler_count":filler_count,
        "confidence_score":confidence_score,
        "wpm":wpm
    }

















# OPTIONAL TEST RUN
# -----------------------------
if __name__ == "__main__":

    sample_text = """
    Um hello, my name is Jaziya.
    Actually I am interested in AI and Machine Learning.
    """

    speaking_time = 30  # seconds

    result = analyze_speech(sample_text, speaking_time)

    print("\nSpeech Analysis Result")
    print("----------------------")
    print("Word Count:", result["word_count"])
    print("Filler Count:", result["filler_count"])
    print("WPM:", result["wpm"])
    print("Confidence Score:", result["confidence_score"])