import requests
import json
import pyttsx3
import whisper
import pyaudio
import wave
import os
import time



# setup text-to-speech engine
engine = pyttsx3.init()


# use to record audio from the microphone and save to a WAV file
# filename: output file name, duration: seconds to record
def record_audio(filename="audio/input.wav", duration=5):
    FORMAT = pyaudio.paInt16  # audio format (16-bit PCM)
    CHANNELS = 1              # mono audio
    RATE = 16000              # sample rate (Hz)
    CHUNK = 1024              # buffer size per read

    audio = pyaudio.PyAudio()  # create PyAudio instance

    # open a stream for recording
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

    print("Recording...")

    frames = []  # list to hold audio frames

    # record audio in chunks for the specified duration
    for _ in range(0, int(RATE / CHUNK * duration)):
        data = stream.read(CHUNK)   # read audio from the stream
        frames.append(data)         # append the audio data to the frame list

    print("Recording finished.")
    #stop stream
    stream.stop_stream()
    stream.close()
    audio.terminate()

    #save recording as a wav file
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(CHANNELS) #set number of channels
        wf.setsampwidth(audio.get_sample_size(FORMAT)) #set sample width
        wf.setframerate(RATE)  #set sample rate
        wf.writeframes(b''.join(frames)) #set audio data

    # Add a 20 second delay after recording to allow Whisper to process the audio
    print(f"Saved file: {filename}")
    print("Waiting 20 seconds to allow Whisper to process the audio...")
    time.sleep(20)

def transcribe_audio(filename="audio/input.wav"):
    print("Loading Whisper model...")
    try:
        model = whisper.load_model("base")  # or "small", "medium", "large"
        print("Model loaded. Transcribing...")
        result = model.transcribe(filename)
        print("Transcription:", result["text"])
    except Exception as e:
        print("Error during transcription:", e)


print("Current working directory:", os.getcwd())
record_audio("audio/input.wav", duration=5)
print("File exists:", os.path.isfile("audio/input.wav"))
transcribe_audio("audio/input.wav")