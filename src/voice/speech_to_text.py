import pyaudio
import wave
import time
import audioop

from faster_whisper import WhisperModel


# -------------------------
# Audio settings
# -------------------------

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

# How quiet the microphone must be before we consider
# the user to have stopped speaking.
SILENCE_DURATION = 0.8

# Maximum length of one command.
MAX_RECORD_SECONDS = 15

# Audio file used by Whisper
AUDIO_FILE = "temp_command.wav"


# -------------------------
# Load Whisper
# -------------------------

print("Loading Whisper model...")

model = WhisperModel(
    "small",
    device="cpu",
    compute_type="int8"
)

print("Whisper model loaded.")


# -------------------------
# Detect microphone volume
# -------------------------

def get_volume(data):
    return audioop.rms(data, 2)


# -------------------------
# Listen
# -------------------------

def listen():

    audio = pyaudio.PyAudio()

    stream = audio.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK
    )

    # -------------------------
    # Calibrate background noise
    # -------------------------

    print("\nListening...")
    print("Calibrating microphone... Please stay silent.")

    noise_levels = []

    calibration_chunks = int(RATE / CHUNK * 1.0)

    for _ in range(calibration_chunks):

        data = stream.read(
            CHUNK,
            exception_on_overflow=False
        )

        volume = get_volume(data)
        noise_levels.append(volume)

    average_noise = sum(noise_levels) / len(noise_levels)

    # Set threshold above normal background noise
    speech_threshold = max(average_noise * 3, 500)

    print(f"Background noise level: {average_noise:.0f}")
    print(f"Speech threshold: {speech_threshold:.0f}")

    # -------------------------
    # Wait for speech
    # -------------------------

    print("Waiting for speech...")

    frames = []

    while True:

        data = stream.read(
            CHUNK,
            exception_on_overflow=False
        )

        volume = get_volume(data)

        if volume > speech_threshold:

            print("Speech detected.")

            frames.append(data)

            break

    # -------------------------
    # Record speech
    # -------------------------

    start_time = time.time()
    last_speech_time = time.time()

    while True:

        data = stream.read(
            CHUNK,
            exception_on_overflow=False
        )

        frames.append(data)

        volume = get_volume(data)

        current_time = time.time()

        if volume > speech_threshold:
            last_speech_time = current_time

        # Stop after silence
        if current_time - last_speech_time >= SILENCE_DURATION:
            break

        # Safety limit
        if current_time - start_time >= MAX_RECORD_SECONDS:
            break

    print("Speech finished.")

    stream.stop_stream()
    stream.close()

    sample_width = audio.get_sample_size(FORMAT)

    audio.terminate()

    # -------------------------
    # Save audio
    # -------------------------

    with wave.open(AUDIO_FILE, "wb") as sound_file:

        sound_file.setnchannels(CHANNELS)
        sound_file.setsampwidth(sample_width)
        sound_file.setframerate(RATE)
        sound_file.writeframes(b"".join(frames))

    # -------------------------
    # Whisper
    # -------------------------

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