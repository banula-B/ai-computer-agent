
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

SILENCE_DURATION = 0.8
MAX_RECORD_SECONDS = 10

AUDIO_FILE = "temp_command.wav"

# Minimum volume required to detect speech.
MIN_SPEECH_THRESHOLD = 500


# -------------------------
# Load Whisper model
# -------------------------

print("Loading Whisper model...")

model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)

print("Whisper model loaded.")


# -------------------------
# Calculate audio volume
# -------------------------

def get_volume(data):
    return audioop.rms(data, 2)


# -------------------------
# Listen and transcribe
# -------------------------

def listen():

    audio = pyaudio.PyAudio()
    stream = None
    frames = []

    try:
        # Open microphone
        stream = audio.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK
        )

        print("\nListening...")
        print("Calibrating microphone... Please stay silent.")

        # -------------------------
        # Calibrate background noise
        # -------------------------

        noise_levels = []

        for _ in range(int(RATE / CHUNK)):
            data = stream.read(
                CHUNK,
                exception_on_overflow=False
            )

            noise_levels.append(get_volume(data))

        background_noise = sum(noise_levels) / len(noise_levels)

        speech_threshold = max(
            int(background_noise * 2.5),
            MIN_SPEECH_THRESHOLD
        )

        print(f"Background noise level: {background_noise:.0f}")
        print(f"Speech threshold: {speech_threshold}")
        print("Waiting for speech...")

        # -------------------------
        # Wait for speech
        # -------------------------

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
        # Record until silence
        # -------------------------

        start_time = time.time()
        last_speech_time = start_time

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

            # Stop when the user pauses long enough
            if current_time - last_speech_time >= SILENCE_DURATION:
                break

            # Prevent recordings from becoming too long
            if current_time - start_time >= MAX_RECORD_SECONDS:
                break

        print("Speech finished.")

        # -------------------------
        # Save recorded audio
        # -------------------------

        sample_width = audio.get_sample_size(FORMAT)

        with wave.open(AUDIO_FILE, "wb") as sound_file:
            sound_file.setnchannels(CHANNELS)
            sound_file.setsampwidth(sample_width)
            sound_file.setframerate(RATE)
            sound_file.writeframes(b"".join(frames))

    except OSError as error:
        print(f"Microphone error: {error}")
        return None

    finally:
        # Always release the microphone
        if stream is not None:
            try:
                if stream.is_active():
                    stream.stop_stream()
            except OSError:
                pass

            try:
                stream.close()
            except OSError:
                pass

        audio.terminate()

    # -------------------------
    # Transcribe with Whisper
    # -------------------------

    print("Transcribing...")

    try:
        segments, info = model.transcribe(
            AUDIO_FILE,
            language="en",
            beam_size=1,
            best_of=1,
            temperature=0.0,
            condition_on_previous_text=False,
            vad_filter=True,
            no_speech_threshold=0.6,
            compression_ratio_threshold=2.0,
            log_prob_threshold=-1.0,
            # initial_prompt=(
            #     "Short English computer voice commands. "
            #     "Examples: open Notepad, open Calculator, open Paint, "
            #     "write hello world, type hello world, press Enter, "
            #     "press Space, press Backspace, exit."
            # )
        )

        # Whisper generates segments lazily.
        text = " ".join(
            segment.text.strip()
            for segment in segments
        ).strip()

        words = text.lower().replace(",","").replace(".","").split()

        if len(words) >=8:
            unique_ratio = len(set(words)) / len(words)

            if unique_ratio < 0.4:
                print("Unreliable transcription discarded.")
                return None

        if not text:
            print("No speech detected.")
            return None

        print(f"You said: {text}")

        return text

    except Exception as error:
        print(f"Transcription error: {error}")
        return None
