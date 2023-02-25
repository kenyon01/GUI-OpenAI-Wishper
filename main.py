import customtkinter
from tkinter import filedialog
import tkinter.messagebox as mb
import whisper
import threading
import pyperclip

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.selected_file = None

        self.geometry("1280x720")
        self.title("Audio Transcriber")
        self.minsize(1280,720)
        self.maxsize(3840,2160)
        customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
        customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green

        self.iconbitmap("./logo.ico")


        # create 2x2 grid system
        self.grid_rowconfigure(0, weight=0)
        self.grid_columnconfigure((0, 2), weight=1)


        self.audiolabel = customtkinter.CTkLabel(master=self, text="Audio File")
        self.audiolabel.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

        self.audiopathlabel = customtkinter.CTkLabel(master=self, text="")
        self.audiopathlabel.grid(row=0, column=2, padx=20, pady=20, sticky="ew")

        self.audiopathbutton = customtkinter.CTkButton(master=self, command=self.browseFiles, text="Choise Audio")
        self.audiopathbutton.grid(row=0, column=1, padx=20, pady=20, sticky="ew")

        self.langlabel = customtkinter.CTkLabel(master=self, text="Language")
        self.langlabel.grid(row=1, column=0, padx=20, pady=20, sticky="ew")

        self.langcombobox = customtkinter.CTkComboBox(master=self, values=["English"], border_color="blue", button_color="blue", button_hover_color="blue")
        self.langcombobox.grid(row=1, column=1, padx=20, pady=20, sticky="ew")
        self.langcombobox.configure(state="disabled")

        self.modellabel = customtkinter.CTkLabel(master=self, text="Model")
        self.modellabel.grid(row=2, column=0, padx=20, pady=20, sticky="ew")

        self.modelcombobox = customtkinter.CTkComboBox(master=self, values=["Tiny", "Base", "Small", "Medium"], border_color="blue", button_color="blue", button_hover_color="blue")
        self.modelcombobox.grid(row=2, column=1, padx=20, pady=20, sticky="ew")

        self.textboxlabel = customtkinter.CTkLabel(master=self, text="Output")
        self.textboxlabel.grid(row=3, column=0, padx=20, pady=20, sticky="ew")

        self.textbox = customtkinter.CTkTextbox(master=self)
        self.textbox.grid(row=3, column=1, columnspan=2, padx=20, pady=20, sticky="nsew")
        self.textbox.insert("0.0","Press Transcribe button to trancribe a audio file.")
        self.textbox.configure(state="disabled", wrap="word")

        self.trancribebutton = customtkinter.CTkButton(master=self, command=self.trancribebutton_callback, text="Transcribe")
        self.trancribebutton.grid(row=4, column=1, padx=20, pady=20, sticky="ew")

        self.checkaudiolabel = customtkinter.CTkLabel(master=self, text="")
        self.checkaudiolabel.grid(row=4, column=2, padx=20, pady=20, sticky="ew")

        self.savebutton = customtkinter.CTkButton(master=self, command=self.savebutton_callback, text="Save")
        self.savebutton.grid(row=5, column=1, padx=20, pady=20, sticky="ew")

        self.copybutton = customtkinter.CTkButton(master=self, command=self.copybutton_callback, text="Copy Text")
        self.copybutton.grid(row=6, column=1, padx=20, pady=20, sticky="ew")

    def browseFiles(self):
        self.selected_file = filedialog.askopenfilename(initialdir="/", title="Select a File",
                                                        filetypes=(("audio files", "*.mp3"), ("all files", "*.*")))
        self.audiopathlabel.configure(text="File Opened: " + self.selected_file)
        return self.selected_file

    def trancribebutton_callback(self):
        audio = self.selected_file
        if audio is None:
            self.checkaudiolabel.configure(text="No file selected.")
            return
        else:
            self.checkaudiolabel.configure(text="")

            audio_extensions = ['.mp3', '.wav', '.flac']

            if any(audio.lower().endswith(ext) for ext in audio_extensions):

                def run_transcribe():
                    get_module = self.modelcombobox.get()

                    model = get_module.lower() + ".en"

                    self.checkaudiolabel.configure(text="")
                    self.checkaudiolabel.configure(text='Transcribing started please wait :)')
                    self.textbox.configure(state="normal")
                    self.textbox.delete("1.0", "end")  # Clear the text box
                    self.textbox.configure(state="disabled")

                    model = whisper.load_model(model)
                    text = model.transcribe(audio, language="en")
                    self.output_text = text["text"][1:]

                    self.checkaudiolabel.configure(text='Transcribing finished.')

                    # Update the text box with the new output text
                    self.textbox.configure(state="normal")
                    self.textbox.delete("1.0", "end")  # Clear the text box
                    self.textbox.insert("1.0", self.output_text)  # Insert the new output text
                    self.textbox.configure(state="disabled")

                    return self.output_text
                thread = threading.Thread(target=run_transcribe)
                thread.start()

            else:
                self.checkaudiolabel.configure(text=f'Error: {audio} is not an audio file.')

    def savebutton_callback(self):
        text_to_save = self.textbox.get("1.0", "end-1c")  # get the text from the textbox

        # ask the user for a filename to save the text to
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", initialfile="output.txt")

        if not file_path:
            return

        try:
            with open(file_path, "w") as f:
                f.write(text_to_save)
            mb.showinfo("Save Successful", f"File saved as {file_path}")
        except Exception as e:
            mb.showerror("Save Failed", str(e))

    def copybutton_callback(self):
        text = self.textbox.get("1.0", "end-1c")  # get the text from the textbox
        pyperclip.copy(text)
        mb.showinfo("Copy Successful", "Text copied to clipboard!")


if __name__ == "__main__":
    app = App()
    app.mainloop()