import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel, Text
from tkinter import ttk
from moviepy.editor import VideoFileClip
import speech_recognition as sr
import threading
import time

def convert_to_wav():
    video_path = filedialog.askopenfilename(title="Ouvrir une vidéo", filetypes=[("Video files", "*.mp4;*.mkv;*.avi")])
    if not video_path:
      return

    video_clip = VideoFileClip(video_path)
    audio_path = video_path.rsplit('.', 1)[0] + ".wav"
    video_clip.audio.write_audiofile(audio_path)
    messagebox.showinfo("Succès", f"La vidéo a été convertie en WAV: {audio_path}")

def transcribe_audio():
    filepath = filedialog.askopenfilename(title="Ouvrir un fichier WAV", filetypes=[("WAV files", "*.wav")])
    if not filepath:
        return

    top = Toplevel()
    top.title("Transcription")
    top.geometry("600x600")

    progress = ttk.Progressbar(top, orient="horizontal", length=400, mode="determinate", style="red.Horizontal.TProgressbar")
    progress.pack(pady=20)

    def transcription_thread():
        recognizer = sr.Recognizer()
        with sr.AudioFile(filepath) as source:
            audio_data = recognizer.record(source)
            audio_duration = source.DURATION  # Get the duration of the audio file
            increment = audio_duration / 100  # Divide the duration into 100 steps
            try:
                for i in range(100):
                    time.sleep(increment)  # Simulate transcription progress
                    progress['value'] += 1
                    top.update_idletasks()
                text = recognizer.recognize_google(audio_data, language='en-US')
                show_transcription(text, top)
            except sr.UnknownValueError:
                messagebox.showerror("Erreur", "Google Speech Recognition n'a pas pu comprendre l'audio")
            except sr.RequestError as e:
                messagebox.showerror("Erreur", f"Impossible d'obtenir les résultats de Google Speech Recognition; {e}")

    threading.Thread(target=transcription_thread).start()

def show_transcription(text, top):
    text_widget = Text(top, wrap="word")
    text_widget.insert("1.0", text)
    text_widget.pack(expand=True, fill="both")

root = tk.Tk()
root.title("Transcripteur Audio et Convertisseur Vidéo")
root.geometry("300x200")

convert_button = tk.Button(root, text="Convertir Vidéo en WAV", command=convert_to_wav)
convert_button.pack(pady=10)

transcribe_button = tk.Button(root, text="Transcrire Audio", command=transcribe_audio)
transcribe_button.pack(pady=10)

style = ttk.Style()
style.theme_use('default')
style.configure("red.Horizontal.TProgressbar", foreground='red', background='red')

root.mainloop()