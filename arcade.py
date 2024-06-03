import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from moviepy.editor import VideoFileClip
import threading
import random
import time

class LibrasArcade:
    def __init__(self, root):
        self.root = root
        self.root.title("LIBRAS ARCADE")
        self.root.geometry("1920x1080")

        # Tela inicial
        self.start_frame = tk.Frame(root)
        self.start_frame.pack(fill="both", expand=True)

        self.show_start_screen()

        # Lista de perguntas para cada categoria
        self.questions_data = {
            "Viagem": [
                {"video": "WhatsApp Video 2024-06-03 at 17.03.24.mp4", "options": ["Resposta 1", "Resposta 2", "Resposta 3"], "correct_index": 0},
                {"video": "WhatsApp Video 2024-06-03 at 17.03.24.mp4", "options": ["Resposta A", "Resposta B", "Resposta C"], "correct_index": 1}
            ],
            "Escola": [
                {"video": "escola1.mp4", "options": ["Resposta 1", "Resposta 2", "Resposta 3"], "correct_index": 2},
                {"video": "escola2.mp4", "options": ["Resposta A", "Resposta B", "Resposta C"], "correct_index": 0}
            ],
            "Cotidiano": [
                {"video": "cotidiano1.mp4", "options": ["Resposta 1", "Resposta 2", "Resposta 3"], "correct_index": 1},
                {"video": "cotidiano2.mp4", "options": ["Resposta A", "Resposta B", "Resposta C"], "correct_index": 2}
            ]
        }

    def show_start_screen(self):
        for widget in self.start_frame.winfo_children():
            widget.destroy()

        # Carregar e redimensionar a imagem
        image = Image.open("libras_arcade_semfundo.png")
        image = image.resize((500, 500), Image.LANCZOS)  # Redimensiona para 400x400 pixels com método Lanczos
        photo = ImageTk.PhotoImage(image)

        # Exibir a imagem
        image_label = tk.Label(self.start_frame, image=photo)
        image_label.image = photo  # Mantém uma referência para evitar a coleta pelo garbage collector
        image_label.pack(pady=20)

        # Botão de iniciar
        start_button = tk.Button(self.start_frame, text="Começar", command=self.show_options, font=("Arial", 20), width=10, height=2)
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
            self.questions = self.questions_data[option]
            random.shuffle(self.questions)  # Embaralha as perguntas
            self.show_question()

    def show_question(self):
        for widget in self.start_frame.winfo_children():
            widget.destroy()

        question = self.questions[self.current_question]
        video_path = question["video"]
        options = question["options"]
        correct_index = question["correct_index"]

        self.video_label = tk.Label(self.start_frame)
        self.video_label.pack(pady=20)

        self.play_video(video_path)

        for idx, option in enumerate(options):
            button = tk.Button(self.start_frame, text=option, command=lambda idx=idx: self.check_answer(idx, correct_index))
            button.pack(pady=5)

    def play_video(self, video_path):
        self.video_clip = VideoFileClip(video_path)
        self.stop_event = threading.Event()  # Event to stop the video

        def stream():
            while not self.stop_event.is_set():
                for frame in self.video_clip.iter_frames(fps=self.video_clip.fps):
                    if self.stop_event.is_set():
                        break
                    image = Image.fromarray(frame)
                    photo = ImageTk.PhotoImage(image)
                    self.video_label.config(image=photo)
                    self.video_label.image = photo
                    self.root.update()

                    # Pausa para controlar a taxa de exibição
                    time.sleep(1 / self.video_clip.fps)

        threading.Thread(target=stream).start()

    def stop_video(self):
        if hasattr(self, 'stop_event'):
            self.stop_event.set()

    def check_answer(self, selected_index, correct_index):
        self.stop_video()  # Stop the video when an answer is selected

        if selected_index == correct_index:
            messagebox.showinfo("Resposta", "Correto!")
        else:
            messagebox.showerror("Resposta", "Incorreto!")

        self.current_question += 1
        if self.current_question < len(self.questions):
            threading.Thread(target=self.next_question_with_delay).start()
        else:
            self.show_start_screen()

    def next_question_with_delay(self):
        time.sleep(1)  # Pausa de 2 segundos entre as perguntas
        self.show_question()


    def show_thank_you_screen(self):
        for widget in self.start_frame.winfo_children():
            widget.destroy()

        # Carregar e redimensionar a imagem de agradecimento
        thank_you_image = Image.open("libras_arcade_semfundo.png")
        thank_you_image = thank_you_image.resize((500, 500), Image.LANCZOS)
        thank_you_photo = ImageTk.PhotoImage(thank_you_image)

        # Exibir a imagem de agradecimento
        thank_you_label_image = tk.Label(self.start_frame, image=thank_you_photo)
        thank_you_label_image.image = thank_you_photo
        thank_you_label_image.pack(pady=20)

        # Texto de agradecimento
        thank_you_label_text = tk.Label(self.start_frame, text="Obrigado por jogar o LIBRAS ARCADE!", font=("Arial", 20))
        thank_you_label_text.pack(pady=20)


if __name__ == "__main__":
    root = tk.Tk()
    app = LibrasArcade(root)
    root.mainloop()