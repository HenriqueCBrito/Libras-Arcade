import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from moviepy.editor import VideoFileClip
import threading
import random
import time
import serial

class LibrasArcade:
    def __init__(self, root):
        self.root = root
        self.root.title("LIBRAS ARCADE")
        self.root.geometry("1920x1080")

        self.arduino = serial.Serial('COM4', 9600)  # Configure para a porta correta
        time.sleep(2)  # Aguarde a inicialização do Arduino

        self.start_frame = tk.Frame(root)
        self.start_frame.pack(fill="both", expand=True)

        self.lives = 4  # Inicializa as vidas
        self.current_menu_option = 0
        self.menu_options = ["Viagem", "Escola", "Cotidiano", "Parar"]

        self.questions_data = {
            "Viagem": [
                {"video": "videos/viagem1.mp4", "options": ["A) 'Você último viajar?'", "B) 'Você último lugar viajar?'", "C) 'Qual foi o último lugar que você visitou?'"], "correct_index": 2},
                {"video": "videos/viagem2.mp4", "options": ["A) 'Sonho seu viajar?'", "B) 'Qual viagem dos seus sonhos?'", "C) 'Você sonho lugar viajar?'"], "correct_index": 1},
                {"video": "videos/viagem3.mp4", "options": ["A) 'Meu país preferido é o Brasil.'", "B) 'Meu país Brasil preferir.'", "C) 'Eu Brasil preferir.'"], "correct_index": 0},
                {"video": "videos/viagem4.mp4", "options": ["A) 'Qual é sua cidade favorita?'", "B) 'Você cidade favorita ser?'", "C) 'Cidade favorita ser?'"], "correct_index": 0},
                {"video": "videos/viagem5.mp4", "options": ["A) 'Eu praia amar viajar!'", "B) 'Amo viajar para a praia!' ", "C) 'Praia amar viajar!'" ], "correct_index": 1}
            ],
            "Escola": [
                {"video": "videos/escola1.mp4", "options": ["A) 'Qual preferida é sua matéria?'", "B) 'Qual matéria preferida?'", "C) 'Qual é a sua matéria preferida?'"], "correct_index": 2},
                {"video": "videos/escola2.mp4", "options": ["A) 'Você estudou para a prova?'", "B) 'Você estudou prova?'", "C) 'Você prova estudou?' "], "correct_index": 0},
                {"video": "videos/escola3.mp4", "options": ["A) 'Eu amo estudar matemática!'", "B) 'Eu matemática!'", "C) 'Estudar eu matemática!'"], "correct_index": 0},
                {"video": "videos/escola4.mp4", "options": ["A) 'Qual ser o nome da sua professora?'", "B) 'Qual é o nome da sua professora?'", "C) 'Qual nome sua professora?'"], "correct_index": 1},
                {"video": "videos/escola5.mp4", "options": ["A) 'Eu quero ser professor de matemática!'", "B) 'Eu ser professor de matemática!'", "C) 'Eu professor de matemática quero ser!'"], "correct_index": 0}
            ],
            "Cotidiano": [
                {"video": "videos/cotidiano5.mp4", "options": ["A) 'Como foi seu dia hoje?'", "B) 'Foi hoje dia?'", "C) 'Como foi hoje dia?'"], "correct_index": 0},
                {"video": "videos/cotidiano4.mp4", "options": ["A) 'Acordei hoje eu.'", "B) 'Acordei eu hoje.'", "C) 'Hoje eu acordei.'"], "correct_index": 2},
                {"video": "videos/cotidiano3.mp4", "options": ["A) 'Acordar ou você até mais tarde?'", "B) 'Você prefere acordar cedo ou dormir até mais tarde?'", "C) 'Preferir acordar você cedo ou dormir até mais tarde?'"], "correct_index": 1},
                {"video": "videos/cotidiano2.mp4", "options": ["A) 'Eu gostar de jogar futebol!'", "B) 'Eu gosto de jogar futebol!'", "C) 'Mim gosta de jogar futebol!'"], "correct_index": 1},
                {"video": "videos/cotidiano1.mp4", "options": ["A) 'Atividade livre no tempo preferidas quais são?'", "B) 'Quais ser as suas atividades preferidas no tempo livre ?'", "C) 'Quais são as suas atividades preferidas no tempo livre?'"], "correct_index": 2}
            ]
        }

        self.update_menu()
        self.listen_to_arduino()

    def update_menu(self):
        for widget in self.start_frame.winfo_children():
            widget.destroy()

        current_option = self.menu_options[self.current_menu_option]
        label = tk.Label(self.start_frame, text=f"Opção: {current_option}", font=("Arial", 24))
        label.pack(pady=20)

        instruction = tk.Label(self.start_frame, text="Use os botões para navegar e confirmar", font=("Arial", 16))
        instruction.pack(pady=10)

    def listen_to_arduino(self):
        def listen():
            while True:
                if self.arduino.in_waiting > 0:
                    command = self.arduino.readline().decode().strip()
                    if command == "left":
                        self.current_menu_option = (self.current_menu_option - 1) % len(self.menu_options)
                        self.update_menu()
                    elif command == "right":
                        self.current_menu_option = (self.current_menu_option + 1) % len(self.menu_options)
                        self.update_menu()
                    elif command == "confirm":
                        self.handle_option(self.menu_options[self.current_menu_option])

        threading.Thread(target=listen, daemon=True).start()

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

        self.current_option_index = 0
        self.correct_index = correct_index
        self.options = options
        self.update_question_options()

    def update_question_options(self):
        for widget in self.start_frame.winfo_children():
            widget.destroy()

        question = self.questions[self.current_question]
        video_path = question["video"]
        options = question["options"]

        self.video_label = tk.Label(self.start_frame)
        self.video_label.pack(pady=20)

        self.play_video(video_path)

        for idx, option in enumerate(options):
            prefix = "-> " if idx == self.current_option_index else "   "
            option_label = tk.Label(self.start_frame, text=prefix + option, font=("Arial", 16))
            option_label.pack(pady=5)

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

                    time.sleep(1 / self.video_clip.fps)

        threading.Thread(target=stream).start()

    def stop_video(self):
        if hasattr(self, 'stop_event'):
            self.stop_event.set()

    def check_answer(self, selected_index):
        self.stop_video()

        if selected_index == self.correct_index:
            self.arduino.write(b'correct\n')
            messagebox.showinfo("Resposta", "Correto!")
        else:
            self.lives -= 1
            self.arduino.write(b'incorrect\n')
            if self.lives == 0:
                messagebox.showerror("Resposta", "Você perdeu todas as vidas!")
                self.show_thank_you_screen()
                return
            else:
                messagebox.showerror("Resposta", f"Incorreto! Vidas restantes: {self.lives}")

        self.current_question += 1
        if self.current_question < len(self.questions):
            threading.Thread(target=self.next_question_with_delay).start()
        else:
            self.show_options()

    def next_question_with_delay(self):
        time.sleep(1)
        self.show_question()

    def show_thank_you_screen(self):
        self.arduino.write(b'stop\n')
        for widget in self.start_frame.winfo_children():
            widget.destroy()

        thank_you_image = Image.open("libras-arcade.png")
        thank_you_image = thank_you_image.resize((500, 500), Image.LANCZOS)
        thank_you_photo = ImageTk.PhotoImage(thank_you_image)

        thank_you_label_image = tk.Label(self.start_frame, image=thank_you_photo)
        thank_you_label_image.image = thank_you_photo
        thank_you_label_image.pack(pady=20)
        
        thank_you_label_text = tk.Label(self.start_frame, text="Obrigado por jogar o LIBRAS ARCADE!", font=("Arial", 20))
        thank_you_label_text.pack(pady=20)

        restart_button = tk.Button(self.start_frame, text="Jogar Novamente", command=self.show_start_screen, font=("Arial", 20), width=15, height=2)
        restart_button.pack(pady=20)

# Inicialização da aplicação
root = tk.Tk()
app = LibrasArcade(root)
root.mainloop()