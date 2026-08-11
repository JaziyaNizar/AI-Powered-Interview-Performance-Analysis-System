import speech_recognition as sr
import wave
import tempfile
import os
import numpy as np
import shutil


recognizer = sr.Recognizer()


def get_speech_text(audio_data):

    if not audio_data:
        return "",0

    chunks, sample_rate = audio_data

    if not chunks:
        return "",0

    wav_path = None

    try:

        # COMBINE AUDIO CHUNKS
        audio_array = np.concatenate(
            [
                np.asarray(chunk).reshape(-1)
                for chunk in chunks
            ]
        )

        audio_array = audio_array.astype(np.int16)

        print(
            "Combined audio shape:",
            audio_array.shape
        )

        print(
            "Sample rate:",
            sample_rate
        )

        print(
            "Maximum audio amplitude:",
            np.max(np.abs(audio_array))
        )


        # CREATE TEMP WAV
        temp_file = tempfile.NamedTemporaryFile(
            suffix=".wav",
            delete=False
        )

        temp_file.close()

        wav_path = temp_file.name

        # WRITE WAV
        with wave.open(wav_path, "wb") as wav:

            wav.setnchannels(1)

            wav.setsampwidth(2)

            wav.setframerate(16000)

            wav.writeframes(
                audio_array.tobytes()
            )


        # SAVE DEBUG RECORDING
        shutil.copy(
            wav_path,
            "debug_recording.wav"
        )

        print(
            "DEBUG AUDIO SAVED AS debug_recording.wav"
        )

        print(
            "WAV file created:",
            wav_path
        )

        # READ COMPLETE AUDIO
        with sr.AudioFile(wav_path) as source:

            audio = recognizer.record(source)


        # AUDIO DURATION
        total_duration = len(audio.frame_data) / (
            audio.sample_rate *
            audio.sample_width
        )

        print(
            "Audio duration:",
            round(total_duration, 2),
            "seconds"
        )


        # SPEECH RECOGNITION
        try:

            transcript = recognizer.recognize_google(
                audio,
                language="en-IN"
            )

            print(
                "FINAL TRANSCRIPT:"
            )

            print(
                transcript
            )

            return transcript,total_duration

        except sr.UnknownValueError:

            print(
                "Could not understand the audio"
            )

            return "",0

        except sr.RequestError as e:

            print(
                "Speech service error:",
                e
            )

            return "",0

    except Exception as e:

        print(
            "Speech recognition error:",
            e
        )

        return "",0

    finally:

        if (
            wav_path
            and os.path.exists(wav_path)
        ):

            try:

                os.remove(
                    wav_path
                )

            except:

                pass
