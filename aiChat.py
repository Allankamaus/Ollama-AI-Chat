import requests
import json
import pyttsx3


OLLAMA_URL = "http://localhost:11434/api/chat"

engine = pyttsx3.init()

def format_ollama_response(content):
    if not content:
        return "[No response received from Ollama.]"
    return content.strip()

def send_message(messages):
    response = requests.post(OLLAMA_URL, json ={
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


def chat():
    print("Welcome to the AI Chat! Type 'exit' to quit.\n")
    messages = [{"role": "system", "content": "You are a helpful assistant"}]

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'exit':
            print("Goodbye! linga guli guli wacha linga gu linga gu")
            break

        messages.append({"role": "user", "content": user_input})
        reply = send_message(messages)
        print(f"\nAI: {reply}")  
        messages.append({"role": "assistant", "content": reply})
        engine.say(reply)
        engine.runAndWait()
        


if __name__ == "__main__":
    chat()





