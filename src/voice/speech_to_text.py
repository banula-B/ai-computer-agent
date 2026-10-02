import speech_recognition as sr


def listen():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")

        recognizer.adjust_for_ambient_noise(source, duration=1)

        audio = recognizer.listen(source)

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