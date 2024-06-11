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
        
        self.start_frame = tk.Frame(root)
        self.start_frame.pack(fill="both", expand=True)
        
        self.arduino = None  # Inicializa a variável arduino
        self.start_serial_thread()

        self.lives = 4  # Inicializa as vidas
        self.show_start_screen()

        # Lista de perguntas para cada categoria
        self.questions_data = {
            "Viagem": [
                {"video": "videos/viagem1.mp4", "options": ["A) 'Você último viajar?'", "B) 'Você último lugar viajar?'", "C) 'Qual foi o último lugar que você viajou?'"], "correct_index": 2},
                {"video": "videos/viagem2.mp4", "options": ["A) 'Sonho seu viajar?'", "B) 'Qual viagem dos seus sonhos?'", "C) 'Você sonho lugar viajar?'"], "correct_index": 1},
                {"video": "videos/viagem3.mp4", "options": ["A) 'Meu país preferido é o Brasil.'", "B) 'Meu país Brasil preferir.'", "C) 'Eu Brasil preferir.'"], "correct_index": 0},
                {"video": "videos/viagem4.mp4", "options": ["A) 'Qual é sua cidade favorita?'", "B) 'Você cidade favorita ser?'", "C) 'Cidade favorita ser?'"], "correct_index": 0},
                {"video": "videos/viagem5.mp4", "options": ["A) 'Eu praia amar viajar!'", "B) 'Amo viajar para a praia!' ", "C) 'Praia amar viajar!'" ], "correct_index": 1}
            ],
            "Escola": [
                {"video": "videos/escola1.mp4", "options": ["A) 'Qual preferida é sua matéria?'", "B) 'Qual ser a sua matéria preferida?'", "C) 'Qual é a sua matéria preferida?'"], "correct_index": 2},
                {"video": "videos/escola2.mp4", "options": ["A) 'Você estudou para a prova?'", "B) 'Você estudar prova?'", "C) 'Você prova estudou?' "], "correct_index": 0},
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
    def start_serial_thread(self):
        try:
            self.arduino = serial.Serial('COM4', 9600, timeout=1)  # Ajuste 'COM3' para a porta correta
            self.serial_thread = threading.Thread(target=self.read_from_serial)
            self.serial_thread.daemon = True
            self.serial_thread.start()
        except serial.SerialException as e:
            messagebox.showerror("Erro de Conexão", f"Não foi possível conectar ao Arduino: {e}")

        
    def show_start_screen(self):
        for widget in self.start_frame.winfo_children():
            widget.destroy()

        # Carregar e redimensionar a imagem
        image = Image.open("libras-arcade.png")
        image = image.resize((500, 500), Image.LANCZOS)  # Redimensiona para 400x400 pixels com método Lanczos
        photo = ImageTk.PhotoImage(image)

        # Exibir a imagem
        image_label = tk.Label(self.start_frame, image=photo)
        image_label.image = photo  # Mantideém uma referência para evitar a coleta pelo garbage collector
        image_label.pack(pady=20)

        # Botão de iniciar
        start_button = tk.Button(self.start_frame,command = self.show_options, text="Começar", font=("Arial", 20), width=10, height=2)
        start_button.pack(pady=20)
        
    def read_from_serial(self):
        while True:
            if self.arduino and self.arduino.in_waiting > 0:
                line = self.arduino.readline().decode('utf-8').strip()
                
                print('aaaaaaaaa: ')
                print(line)
                
                if line == "COMEÇAR":
                    self.show_options()
                elif line == "Viagem":
                    self.handle_option(line)
                elif line == "Escola":
                    self.handle_option(line)
                elif line == "Cotidiano":
                    self.handle_option(line)
                elif line == "A0":
                    selected_Opt = 0
                    correct_Opt = int(line[1])
                    self.check_answer(selected_Opt,correct_Opt)
                elif line == "A1":
                    selected_Opt = 0
                    correct_Opt = int(line[1])
                    self.check_answer(selected_Opt,correct_Opt)
                elif line == "A2":
                    selected_Opt = 0
                    correct_Opt = int(line[1])
                    self.check_answer(selected_Opt,correct_Opt)
                elif line == "B0":
                    selected_Opt = 0
                    correct_Opt = int(line[1])
                    self.check_answer(selected_Opt,correct_Opt)
                elif line == "B1":
                    selected_Opt = 1
                    correct_Opt = int(line[1])
                    self.check_answer(selected_Opt,correct_Opt)
                elif line == "B2":
                    selected_Opt = 1
                    correct_Opt = int(line[1])
                    self.check_answer(selected_Opt,correct_Opt)
                elif line == "C0":
                    selected_Opt = 2
                    correct_Opt = int(line[1])
                    self.check_answer(selected_Opt,correct_Opt)
                elif line == "C1":
                    selected_Opt = 2
                    correct_Opt = int(line[1])
                    self.check_answer(selected_Opt,correct_Opt)
                elif line == "C2":
                    selected_Opt = 2
                    correct_Opt = int(line[1])
                    self.check_answer(selected_Opt,correct_Opt)
                elif line == "GAMEOVER":
                    self.lives-=1
                    self.show_thank_you_screen()
                elif line == "Parar":
                    self.show_thank_you_screen()
            time.sleep(0.1)  
        
    def show_options(self):
        for widget in self.start_frame.winfo_children():
            widget.destroy()

        options = ["Viagem", "Escola", "Cotidiano", "Parar"]
        for option in options:
            button = tk.Button(self.start_frame, text=option, command=lambda opt=option: self.handle_option(opt), font=("Arial",30), width=10, height=2)
            button.pack(pady=10)

    def handle_option(self, option):
        if option == "Parar":
            self.show_thank_you_screen()
        else:
            self.current_question = 0
            self.questions = self.questions_data[option]
  
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
            button = tk.Button(self.start_frame, text=option, command=lambda idx=idx: self.check_answer(idx, correct_index), font=("Arial",13))
            print(idx, correct_index)
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
        
        if selected_index != correct_index:
            self.lives -= 1
            if self.lives == 0:
                self.show_thank_you_screen()
                return
            
                

        self.current_question += 1
        if self.current_question < len(self.questions):
            threading.Thread(target=self.next_question_with_delay).start()
        else:
            self.show_options()

    def next_question_with_delay(self):
        time.sleep(1)  # Pausa de 2 segundos entre as perguntas
        self.show_question()

    def show_thank_you_screen(self):
        for widget in self.start_frame.winfo_children():
            widget.destroy()

        # Carregar e redimensionar a imagem de agradecimento
        thank_you_image = Image.open("libras-arcade.png")
        thank_you_image = thank_you_image.resize((500, 500), Image.LANCZOS)
        thank_you_photo = ImageTk.PhotoImage(thank_you_image)

        # Exibir a imagem de agradecimento
        thank_you_label_image = tk.Label(self.start_frame, image=thank_you_photo)
        thank_you_label_image.image = thank_you_photo  # Mantém uma referência para evitar a coleta pelo garbage collector
        thank_you_label_image.pack(pady=20)
        
        thank_you_label_text = tk.Label(self.start_frame, text="Obrigado por jogar o LIBRAS ARCADE!", font=("Arial", 20))
        thank_you_label_text.pack(pady=20)

        # Botão para retornar à tela inicial
        restart_button = tk.Button(self.start_frame, text="Jogar Novamente", command=self.show_start_screen, font=("Arial", 20), width=15, height=2)
        restart_button.pack(pady=20)
        self.lives = 4

# Inicialização da aplicação
root = tk.Tk()
app = LibrasArcade(root)
root.mainloop()