import customtkinter as ctk 
import openai
import time
import threading

class TeacherAssistant(ctk.CTk):
    def __init__(self):
        super().__init__()       
        self.title("Teacher Assistant") 
        ctk.set_appearance_mode("Dark")

        #Window Size
        window_width = 1000
        window_height = 700
 
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Coordinates of the upper left corner of the window to make the window appear in the center
        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))
        self.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
        self.resizable(False, False)

        optionFrame = ctk.CTkFrame(self, width=20, height=650)
        optionFrame.pack(side='left',anchor='w',fill="both", pady=5, padx=7)
 
        self.userEntryBox = ctk.CTkEntry(self, width=860, placeholder_text='Enter Text Here!')
        self.userEntryBox.pack(side='bottom')

        self.userEntryBox.bind("<Return>", self.on_enter_pressed)

        self.chatBoxFrame = ctk.CTkScrollableFrame(self, width=650, height=600)
        self.chatBoxFrame.pack(pady=5, padx=5,side='bottom',fill="both", expand=True)


        # ----------------------------------------- Option Menu Options -----------------------------------------------------
        setColorBox = ctk.CTkOptionMenu(optionFrame, values=['Dark','Light'], width=40, height=20, command=self.set_theme)
        setColorBox.set('Dark')
        setColorBox.pack(side='bottom',padx=5, pady=5)

        setColorBoxLabel = ctk.CTkLabel(optionFrame, text='Appearance Mode:')
        setColorBoxLabel.pack(side='bottom', padx=5, pady=5)

    def on_enter_pressed(self, junk):
        # Get Input from Entrybox
        userInput = self.userEntryBox.get()

        # Delete Text in Entrybox
        self.userEntryBox.delete(0, 'end')

        # Method used to place text on screen for user
        self.placeTextOnFrame(userInput)
        self.userInput = userInput
        # Automatically Scroll to keep up with text
        #Placeholder for future code

        # Method used to get AI Answer from user prompt
        
        thread = threading.Thread(target=self.getAiAnswer)
        thread.start()

    def set_theme(self, theme):
        ctk.set_appearance_mode(theme)

    def placeTextOnFrame(self, input):
        print(input)
        
        # 
        userInputFrame = ctk.CTkFrame(self.chatBoxFrame)
        userInputFrame.pack(side='top', anchor='e')
        
        userInputTextBox = ctk.CTkTextbox(userInputFrame, width=900, height=100)
        userInputTextBox.pack(anchor='center', pady=5)

        # Set the text in the Entry widget to the input variable
        userInputTextBox.insert(ctk.END, f"{input}")
        userInputTextBox.configure(state='disabled')

    def getAiAnswer(self):
        openai.api_key = "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"
        self.messages = []
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

        self.messages.append({"role": "system", "content": system_msg})
        
        print("Getting API Answer for: ", self.userInput)
        print("Teacher assistant is ready!")
        
        aiInputFrame = ctk.CTkFrame(self.chatBoxFrame)
        aiInputFrame.pack(side='top', anchor='w')
        
        aiInputTextBox = ctk.CTkTextbox(aiInputFrame, width=900, height=100)
        aiInputTextBox.pack(anchor='center', pady=5)   
        self.stop_dots = False
        previous_user_input = None 
        
        while True:
            isSame = False
            userMessage = self.userInput
            
            # Check if the current user input is the same as the previous one
            if userMessage == previous_user_input:
                isSame = True
                while isSame:
                    time.sleep(1)
                    if self.userInput != previous_user_input:
                       isSame = False 
            else:    
                if userMessage == "quit()":
                    break

                self.messages.append({"role": "user", "content": userMessage})

                thread = threading.Thread(target=lambda:self.print_thinking_dots(aiInputTextBox))
                thread.start()

                response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=self.messages)
                reply = response["choices"][0]["message"]["content"]

                self.stop_dots = True
                thread.join()

                # Print reply word by word
                print("Assistant:", end=' ')
                i = 0
                for word in reply.split():
                    i += 1
                    aiInputTextBox.insert(ctk.END, f"{word} ")
                    print(word + ' ', end='')
                    if i == 40:
                        aiInputTextBox.insert(ctk.END, "\n")
                        i = 0
                    aiInputTextBox.see("end")
                    time.sleep(0.1)  # Reducing the delay for faster output
                print("\n")
                
                self.update_textbox_height(aiInputTextBox)

                aiInputTextBox.configure(state='disabled')
                self.messages.append({"role": "assistant", "content": reply})

                # Update the previous_user_input for the next iteration
                previous_user_input = userMessage

    def print_thinking_dots(self, textbox):
        count = 1
        message = ""
        while not self.stop_dots:
            message += '. ' * count
            textbox.insert(ctk.END, f"{message}")  # Update the CTkTextbox with the message
            time.sleep(0.5)
            count = (count % 3) + 1
            textbox.delete("0.0", "end") # Insert a newline character to reset the line
            message = ""
            
    def update_textbox_height(self, aiInputTextBox):
        # Get the number of lines in the textbox
        num_lines = int(aiInputTextBox.index(ctk.END).split('.')[0])

        if num_lines > 5:
            # Calculate the new height based on the number of lines
            new_height = num_lines * 20  # Add some extra height
            
            # Update the textbox height
            aiInputTextBox.configure(height=new_height + 100)    
    
if __name__ == "__main__":
    root = TeacherAssistant()
    root.mainloop()