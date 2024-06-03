import tkinter as tk
from PIL import Image, ImageTk
import imageio
import threading

# Create the main application window
root = tk.Tk()
root.title("Video Player")
root.geometry("800x600")

class VideoPlayer:
    def __init__(self, root, video_path):
        self.root = root
        self.video_path = video_path
        self.video = imageio.get_reader(video_path)
        self.label = tk.Label(root)
        self.label.pack()
        self.playing = False

    def start(self):
        self.playing = True
        self.display_video()

    def stop(self):
        self.playing = False

    def display_video(self):
        def stream():
            for frame in self.video.iter_data():
                if not self.playing:
                    break
                image = Image.fromarray(frame)
                photo = ImageTk.PhotoImage(image)
                self.label.config(image=photo)
                self.label.image = photo
                self.root.update()
                if not self.playing:
                    break

        threading.Thread(target=stream).start()

def start_video():
    player.start()

def stop_video():
    player.stop()

start_button = tk.Button(root, text="Start Video", command=start_video)
start_button.pack(side=tk.LEFT, padx=20)

stop_button = tk.Button(root, text="Stop Video", command=stop_video)
stop_button.pack(side=tk.RIGHT, padx=20)

video_path = "Neymar - Magic Skills, Dribles & Gols pelo Santos _ HD.mp4"  # Update this path to your video file
player = VideoPlayer(root, video_path)

# Start the Tkinter event loop
root.mainloop()