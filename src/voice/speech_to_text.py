import speech_recognition as sr


recognizer = sr.Recognizer()

# Speech recognition settings
recognizer.energy_threshold = 300
recognizer.dynamic_energy_threshold = True
recognizer.pause_threshold = 1.0
recognizer.phrase_threshold = 0.3
recognizer.non_speaking_duration = 0.5


def listen():
    with sr.Microphone() as source:

        print("Listening...")

        audio = recognizer.listen(
            source,
            timeout=None,
            phrase_time_limit=None
        )

    try:
        text = recognizer.recognize_google(audio)

        print(f"You said: {text}")

        return text

    except sr.UnknownValueError:
        print("Sorry, I couldn't understand what you said.")
        return None

    except sr.RequestError as error:
        print(f"Speech recognition service error: {error}")
        return None