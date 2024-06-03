import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import imageio
import threading

class LibrasArcade:
    def __init__(self, root):
        self.root = root
        self.root.title("LIBRAS ARCADE")
        self.root.geometry("800x600")

        # Tela inicial
        self.start_frame = tk.Frame(root)
        self.start_frame.pack(fill="both", expand=True)

        self.show_start_screen()

    def show_start_screen(self):
        for widget in self.start_frame.winfo_children():
            widget.destroy()

        # Imagem e título
        image = Image.open("path/to/your/image.jpg")
        photo = ImageTk.PhotoImage(image)

        image_label = tk.Label(self.start_frame, image=photo)
        image_label.image = photo  # Keep a reference to avoid garbage collection
        image_label.pack(pady=20)

        title_label = tk.Label(self.start_frame, text="LIBRAS ARCADE", font=("Arial", 30))
        title_label.pack(pady=20)

        start_button = tk.Button(self.start_frame, text="Start", command=self.show_options)
        start_button.pack(pady=20)

    def show_options(self):
        for widget in self.start_frame.winfo_children():
            widget.destroy()

        options = ["Viagem", "Escola", "Cotidiano", "Parar"]
        for option in options:
            button = tk.Button(self.start_frame, text=option, command=lambda opt=option: self.handle_option(opt))
            button.pack(pady=10)

    def handle_option(self, option):
        if option == "Parar":
            self.show_thank_you_screen()
        else:
            self.current_question = 0
            self.questions = [
                {"video": "path/to/video1.mp4", "options": ["Resposta 1", "Resposta 2", "Resposta 3"]},
                {"video": "path/to/video2.mp4", "options": ["Resposta A", "Resposta B", "Resposta C"]}
            ]
            self.show_question()

    def show_question(self):
        for widget in self.start_frame.winfo_children():
            widget.destroy()

        question = self.questions[self.current_question]
        video_path = question["video"]
        options = question["options"]

        self.video_label = tk.Label(self.start_frame)
        self.video_label.pack(pady=20)

        self.play_video(video_path)

        for option in options:
            button = tk.Button(self.start_frame, text=option, command=self.next_question)
            button.pack(pady=5)

    def play_video(self, video_path):
        self.video = imageio.get_reader(video_path)

        def stream():
            for frame in self.video.iter_data():
                image = Image.fromarray(frame)
                photo = ImageTk.PhotoImage(image)
                self.video_label.config(image=photo)
                self.video_label.image = photo
                self.root.update()

        threading.Thread(target=stream).start()

    def next_question(self):
        self.current_question += 1
        if self.current_question < len(self.questions):
            self.show_question()
        else:
            self.show_start_screen()

    def show_thank_you_screen(self):
        for widget in self.start_frame.winfo_children():
            widget.destroy()

        video_path = "path/to/thank_you_video.mp4"
        self.play_video(video_path)

        thank_you_label = tk.Label(self.start_frame, text="Obrigado por jogar o LIBRAS ARCADE!", font=("Arial", 20))
        thank_you_label.pack(pady=20)


if __name__ == "__main__":
    root = tk.Tk()
    app = LibrasArcade(root)
    root.mainloop()