import threading
import openai
import time
import sys
openai.api_key = "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"


messages = []
system_msg = """You are a helpful assistant to a teacher at any given school. 
                Your goal is to assist the teacher in any way possible to help that person
                do their job more effectively."""

messages.append({"role": "system", "content": system_msg})


stop_dots = False  # A flag to control the display of dots

def print_thinking_dots():
    count = 1
    while not stop_dots:
        print('.' * count, end='', flush=True)
        time.sleep(0.5)
        count = (count % 3) + 1
        print('\r' + ' ' * 3, end='', flush=True)  # Reset line
        print('\r', end='', flush=True)

print("Teacher assistant is ready!")
while True:
    userMessage = input("You: ")
    if userMessage == "quit()":
        break

    messages.append({"role": "user", "content": userMessage})
    
     # Start the dot animation on a separate thread
    stop_dots = False
    thread = threading.Thread(target=print_thinking_dots)
    thread.start()
    
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    reply = response["choices"][0]["message"]["content"]

    stop_dots = True
    thread.join()
    # Print reply word by word
    print("Assistant:", end=' ')
    for word in reply.split():
        print(word + ' ', end='')
        time.sleep(0.1)  # Reducing the delay for faster output
    print("\n")

    messages.append({"role": "assistant", "content": reply})

