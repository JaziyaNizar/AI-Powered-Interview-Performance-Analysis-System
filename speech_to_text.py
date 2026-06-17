import speech_recognition as sr

#create recognizer object
recognizer=sr.Recognizer()

def get_speech_text():
    try:
        with sr.Microphone() as source:
            print("Listening....")

            #reduce background noise
            recognizer.adjust_for_ambient_noise(source,duration=1)

            recognizer.pause_threshold=2

            #record audio
            print("Waiting for speech...")
            audio=recognizer.listen(source,timeout=10,phrase_time_limit=30)


            #convert speech to text
            text=recognizer.recognize_google(audio)

            return text
        
    except sr.WaitTimeoutError:
        return "Listening timed out"
    except sr.UnknownValueError:
        return "Could not understand"
    except sr.RequestError:
        return "Speech service unavailable"
    except Exception as e:
        return f"Error:{e}"
    




















# Test independently
if __name__ == "__main__":

    result = get_speech_text()

    print("Recognized Text:")
    print(result)   