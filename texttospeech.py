import tkinter as tk
from tkinter import ttk
from googletrans import Translator
from gtts import gTTS
import pygame
import os
import time

pygame.mixer.init()

language_codes = {
    "English": "en",
    "Hindi": "hi",
    "French": "fr"
}
file_counter = 0
generated_audio_files = []
def translate_and_speak():
    global file_counter
    text = text_input.get("1.0", tk.END).strip()
    selected_language = language_var.get()
    if selected_language not in language_codes:
        return
    lang_code = language_codes[selected_language]
    if text:
        try:
            translator = Translator()
            translated_text = translator.translate(text, dest=lang_code).text

            # Converting text to speech
            tts = gTTS(text=translated_text, lang=lang_code)

            output_file_name = f"output{file_counter}.mp3"
            output_file_path = os.path.join(os.path.dirname(__file__), output_file_name)
            pygame.mixer.music.stop()
            time.sleep(0.1)
            tts.save(output_file_path)
            generated_audio_files.append(output_file_path)
            pygame.mixer.music.load(output_file_path)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            file_counter += 1

        except Exception as e:
            print(f"Error occurred: {e}")


root = tk.Tk()
root.title("Text to Speech Converter")
root.geometry("400x400")

# Create and place the input fields and labels
label_prompt = tk.Label(root, text="Enter text:")
label_prompt.pack(pady=10)
text_input = tk.Text(root, height=5, width=50)
text_input.pack(pady=10)

language_var = tk.StringVar(value="English")
languages = list(language_codes.keys())
label_language = tk.Label(root, text="Select language:")
label_language.pack(pady=5)

for lang in languages:
    radio_button = tk.Radiobutton(root, text=lang, variable=language_var, value=lang)
    radio_button.pack()

convert_button = ttk.Button(root, text="Convert to Speech", command=translate_and_speak)
convert_button.pack(pady=10)

root.mainloop()
