import threading
import openai
import time
import sys
from docx import Document
import PyPDF2
import os

# api key to access the OpenAI API
openai.api_key = "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"

# read contents of file and return it
def read_file_content(file_path):
  
    #Detects the file type (Word, PDF, or TXT) based on its extension and extracts its content. 
    print("file path - ", file_path)
    file_extension = os.path.splitext(file_path)[1].lower()

    # Extract content from Word document
    if file_extension == '.docx':
        doc = Document(file_path)
        fullText = []
        for para in doc.paragraphs:
            fullText.append(para.text)
        return '\n'.join(fullText)

    # Extract content from PDF
    elif file_extension == '.pdf':
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text()
        return text

    # Extract content from a plain text file
    elif file_extension == '.txt':
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

    else:
        raise ValueError("Unsupported file type: {}".format(file_extension))


file_content = read_file_content("C:/Users/Aramis M. Figueroa/OneDrive/Hackathons/PlutoHacks2023/PlutoHacksProject/TestMaterial/COP_1000C_-_Intro_Cmp_Prg.pdf")

# store list of user messages, first one being the "programming" prompt
messages = []
system_msg = """
You are a specialized AI assistant for teachers, designed to support them in crafting assignments and addressing other potential educational needs based on the specific content and details found in a provided file. This file will provide key details, including subjects, grades, and curriculum standards.

Your expertise includes:
- Creating assignments of varying types: daily homework, larger projects, research tasks, essays, and multiple-choice tests.
- Tailoring the complexity of assignments based on the details found in the file or, if provided, prioritizing user's additional input.
- Adhering to curriculum standards and themes highlighted in the file content.
- If specified by the user, integrating interactive elements into the assignment.
- Generating only textual content assignments for now, fitting the category of the class as described in the file.
- When necessary, providing an answer key and grading rubric for assignments.
- Proactively inquiring for extra details when the context requires, ensuring the assignment or support is tailored to specific constraints, themes, or needs the teacher may have.
- Beyond assignment creation, you're equipped to assist with broader educational challenges, such as time management strategies, teaching methodologies, classroom management techniques, and more.

Always prioritize details from the provided file, but remain adaptable and responsive to address the holistic needs of the teacher based on user prompts and inquiries.
"""

messages.append({"role": "system", "content": system_msg})
messages.append({"role": "user", "content": f"Here's the content of my file: \n{file_content}"})

# A flag to control the display of dots
stop_dots = False  # A flag to control the display of dots

# A function to print dots as an animation while waiting for bot message
def print_thinking_dots():
    count = 1
    while not stop_dots:
        print('.' * count, end='', flush=True)
        time.sleep(0.5)
        count = (count % 3) + 1
        print('\r' + ' ' * 3, end='', flush=True)  # Reset line
        print('\r', end='', flush=True)

# display the welcome message
print("Teacher assistant is ready!")

# Start the bot
while True:
    userMessage = input("You: ") # <-- User input variable 
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

