import pyaudio
import wave
import os
from faster_whisper import WhisperModel


# Audio settings
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 5

AUDIO_FILE = "temp_command.wav"


# Load Whisper model once
print("Loading Whisper model...")

model = WhisperModel(
    "small",
    device="cpu",
    compute_type="int8"
)

print("Whisper model loaded.")


def listen():
    audio = pyaudio.PyAudio()

    stream = audio.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK
    )

    print("\nListening...")

    frames = []

    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Recording finished.")

    stream.stop_stream()
    stream.close()

    sample_width = audio.get_sample_size(FORMAT)
    audio.terminate()

    # Save recorded audio
    with wave.open(AUDIO_FILE, "wb") as sound_file:
        sound_file.setnchannels(CHANNELS)
        sound_file.setsampwidth(sample_width)
        sound_file.setframerate(RATE)
        sound_file.writeframes(b"".join(frames))

    print("Transcribing...")

    segments, info = model.transcribe(
    AUDIO_FILE,
    language="en",
    beam_size=5,
    vad_filter=True,
    initial_prompt=(
        "Computer commands: open, write, type, press, "
        "click, move, close, launch, save, search."
        )
    )   

    text = " ".join(
    segment.text.strip()
    for segment in segments
    ).strip()

    if not text:
        print("No speech detected.")
        return None

    print(f"You said: {text}")

    return text

    if text:
        print(f"You said: {text}")
        return text

    print("Sorry, I couldn't understand what you said.")
    return None