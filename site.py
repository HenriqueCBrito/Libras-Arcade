import tkinter as tk
from tkinter import messagebox

# Create the main application window
root = tk.Tk()
root.title("Calculator")

# Set the window to full screen
root.attributes('-fullscreen', True)

# Create and place the entry widget
entry = tk.Entry(root, width=16, font=('Arial', 24), borderwidth=2, relief='solid')
entry.grid(row=0, column=0, columnspan=4, pady=20)

# Define the button click function
def button_click(value):
    current_text = entry.get()
    entry.delete(0, tk.END)
    entry.insert(0, current_text + value)

# Define the clear function
def clear():
    entry.delete(0, tk.END)

# Define the calculate function
def calculate():
    try:
        result = eval(entry.get())
        entry.delete(0, tk.END)
        entry.insert(0, str(result))
    except:
        messagebox.showerror("Error", "Invalid Input")

# Create buttons and center them
buttons = [
    '7', '8', '9', '/',
    '4', '5', '6', '*',
    '1', '2', '3', '-',
    '0', '.', '=', '+'
]

# Create a frame to hold the buttons and center it
button_frame = tk.Frame(root)
button_frame.grid(row=1, column=0, padx=50, pady=50)

row = 0
col = 0

for button in buttons:
    if button == "=":
        tk.Button(button_frame, text=button, width=10, height=4, command=calculate).grid(row=row, column=col, columnspan=2, padx=5, pady=5)
        col += 1
    else:
        tk.Button(button_frame, text=button, width=10, height=4, command=lambda b=button: button_click(b)).grid(row=row, column=col, padx=5, pady=5)
    col += 1
    if col > 3:
        col = 0
        row += 1

tk.Button(button_frame, text="C", width=10, height=4, command=clear).grid(row=row, column=col, columnspan=2, padx=5, pady=5)

# Start the Tkinter event loop
root.mainloop()