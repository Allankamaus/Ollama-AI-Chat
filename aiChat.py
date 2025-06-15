import requests

OLLAMA_URL = "http://localhost:11434/api/chat"

def send_message(messages):
    response = requests.post(OLLAMA_URL, json ={
        "model": "llama2",
        "messages": messages
    })
    data = response.json()
   
    if "message" not in data:
        print("Unexpected response:", data)
        return "Error: Unexpected response from Ollama."
    return data["message"]["content"]


def chat():
    print("Welcome to the AI Chat! Type 'exit' to quit.\n")
    messages = [{"role": "system", "content": "You are a helpful assistant"}]

    while True:
        user_input = input("You:")
        if user_input.lower() == 'exit':
            print("Goodbye! linga guli guli wacha linga gu linga gu")
            break

        messages.append({"role": "user", "content": user_input})
        reply =  send_message(messages)
        messages.append({"role": "assistant", "content" : reply})


chat()