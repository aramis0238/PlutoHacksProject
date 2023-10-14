import customtkinter as ctk 
import fastapi
import openai

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

        # Automatically Scroll to keep up with text
        #self.chatBoxFrame.

        # Method used to get AI Answer from user prompt
        self.getAiAnswer(userInput)

    def set_theme(self, theme):
        ctk.set_appearance_mode(theme)

    def placeTextOnFrame(self, input):
        print(input)
        
        # 
        userInputFrame = ctk.CTkFrame(self.chatBoxFrame)
        userInputFrame.pack(side='top', anchor='e')

        userInput = ctk.StringVar()
        userInputTextBox = ctk.CTkEntry(userInputFrame, textvariable=userInput, width=900, height=100)
        userInputTextBox.pack(anchor='center', pady=5)

        # Set the text in the Entry widget to the input variable
        userInput.set(input)
        userInputTextBox.configure(state='disabled')
    
    def split_text(self, text, chunk_size):
        return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]


    def format_text(self, text):
        chunk_size = 50
        chunks = self.split_text(text, chunk_size)
        return '\n'.join(chunks)

    def placeAiTextOnFrame(self, aiText):
        
        

        print(aiText)
        
        # 
        aiInputFrame = ctk.CTkFrame(self.chatBoxFrame)
        aiInputFrame.pack(side='top', anchor='w')

        aiInput = ctk.StringVar()
        aiInputTextBox = ctk.CTkEntry(aiInputFrame, textvariable=aiInput, width=900, height=100)
        aiInputTextBox.pack(anchor='center', pady=5)

        # Format Ai Text
        formatted_text = self.format_text(aiText)
        
        # Set the text in the Entry widget to the input variable
        aiInput.set(formatted_text)
        aiInputTextBox.configure(state='disabled')


    def getAiAnswer(self, userInput):
        print("Getting API Answer for: ", userInput)

        #---------------------------------------------------
        # Here will be the FastApi Configuration for ChatGPT
        #---------------------------------------------------

        aiAnswer = 'Hello! This is the chatbot speaking...'
        self.placeAiTextOnFrame(aiAnswer)

if __name__ == "__main__":
    root = TeacherAssistant()
    root.mainloop()