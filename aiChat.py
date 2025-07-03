import requests
import json
import pyttsx3
import pyaudio
import wave 
from tts import *
import io
import sys
import os

OLLAMA_URL = "http://localhost:11434/api/chat"



# format Ollama's response for readability
# returns a cleaned-up string
def format_ollama_response(content):
    if not content:
        return "[No response received from Ollama.]"
    return content.strip()




# send a message list to Ollama and return the AI's response as text
# handles streaming JSON lines from the API
# returns the assistant's reply as a string
def send_message(messages):
    response = requests.post(OLLAMA_URL, json={
        "model": "llama2",
        "messages": messages
    }, stream=True)
    content = ""
    for line in response.iter_lines():
        if line:
            try:
                line_str = line.decode('utf-8') if isinstance(line, bytes) else line
                data = json.loads(line_str)
                if "message" in data and "content" in data["message"]:
                    content += data["message"]["content"]
            except Exception as e:
                print("Line decode error:", e, line)
    if not content:
        print("No content received or unexpected response.")
        return "Error: No content received from Ollama."
    return format_ollama_response(content)




# main chat loop: gets user input, sends to Ollama, prints and speaks the response
# continues until user types 'exit'
def chat():
    print("Welcome to the AI Chat! Type 'exit' to quit.\nType 'audio' to use your microphone for input.\n")
    messages = [{"role": "system", "content": "You are a helpful assistant"}]

    while True:
        user_input = input("\nYou: ")  # get user input
        if user_input.lower() == 'exit':
            print("Goodbye! linga guli guli wacha linga gu linga gu")
            break
        if user_input.lower() == 'audio':
            # Record audio and transcribe using tts.py functions
            record_audio("audio/input.wav", duration=5)
            print("Transcribing your audio...")
            try:
                # Use the transcribe_audio function from tts.py
                if os.path.isfile("audio/input.wav"):
                    # Capture the transcription output
                    old_stdout = sys.stdout
                    sys.stdout = mystdout = io.StringIO()
                    transcribe_audio("audio/input.wav")
                    sys.stdout = old_stdout
                    transcription = mystdout.getvalue().split("Transcription:")[-1].strip()
                    if not transcription:
                        print("No speech detected.")
                        continue
                    user_input = transcription
                    print(f"You (from audio): {user_input}")
                else:
                    print("Audio file not found.")
                    continue
            except Exception as e:
                print("Error during audio transcription:", e)
                continue
        messages.append({"role": "user", "content": user_input})  # add user message
        reply = send_message(messages)  # get AI response
        print(f"\nAI: {reply}")  # print AI response
        messages.append({"role": "assistant", "content": reply})  # add AI response to history
        engine.say(reply)  # speak the AI response
        engine.runAndWait()  # wait for speech to finish




#start
if __name__ == "__main__":
    chat()





