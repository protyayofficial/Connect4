import tkinter as tk
from tkinter import messagebox
from two_player import TwoPlayerMode
from play_with_ai import PlayWithAI
from PIL import Image, ImageTk

def start_two_player_game(rows, cols):
    """Starts a two-player Connect 4 game based on the provided rows and columns."""
    root = tk.Tk()
    root.geometry(f"{cols * 100}x{(rows + 1) * 100}")
    root.configure(bg="black")
    game = Connect4Game(root, rows, cols, "Two Player Mode")
    two_player_game = TwoPlayerMode(rows, cols, game)
    root.mainloop()

def start_play_with_ai(rows, cols):
    """Starts a Connect 4 game against AI based on the provided rows and columns."""
    root = tk.Tk()
    root.geometry(f"{cols * 100}x{(rows + 1) * 100}")
    root.configure(bg="black")
    game = Connect4Game(root, rows, cols, "Play With AI")
    play_with_ai = PlayWithAI(rows, cols, game)
    root.mainloop()

class Connect4Game:
    """Class representing the main Connect 4 game."""

    def __init__(self, root, rows, cols, game_mode):
        """Initialize the Connect4Game class.

        Args:
            root (tk.Tk): The tkinter root window.
            rows (int): Number of rows in the game.
            cols (int): Number of columns in the game.
            game_mode (str): The mode of the game ("Two Player Mode" or "Play With AI").
        """
        self.root = root
        self.rows = rows
        self.cols = cols
        self.game_mode = game_mode
        self.root.title(game_mode)
        self.canvas_width = self.cols * 100
        self.canvas_height = (self.rows + 1) * 100  # Additional row at the top
        self.create_game_window()

    def create_game_window(self):
        """Create the game window with the canvas and initial game state."""
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.pack()

        self.canvas.create_rectangle(0, 100, self.canvas_width, self.canvas_height, fill="#4169E1")  # Royal Blue background

        for i in range(1, self.rows + 1):
            for j in range(self.cols):
                x = j * 100 + 50
                y = i * 100 + 50
                self.canvas.create_oval(x - 40, y - 40, x + 40, y + 40, fill="white", outline="white")

def main_menu():
    """Main menu for the Connect 4 game."""
    root = tk.Tk()
    root.title("Connect 4 Main Menu")
    root.geometry("800x600")
    root.configure(bg="#4169E1")  # Royal Blue background

    img = Image.open("./connect4.png")  # Replace with your image file path
    img = img.resize((150, 150), resample=Image.BICUBIC)  # Resize the image as needed
    img = ImageTk.PhotoImage(img)

    image_label = tk.Label(root, image=img, bg="#4169E1")
    image_label.image = img
    image_label.place(relx=1.0, x=-10, y=10, anchor="ne")

    title_label = tk.Label(root, text="Connect 4", font=("Helvetica", 38), fg="white", bg="#4169E1")
    title_label.pack(pady=(50, 20))

    def on_entry_click(event):
        if rows.get() == "6":
            rows.delete(0, tk.END)
        if cols.get() == "7":
            cols.delete(0, tk.END)

    def on_focus_out(event):
        if not rows.get():
            rows.insert(0, "6")
        if not cols.get():
            cols.insert(0, "7")

    label_row = tk.Label(root, text="Rows:", bg="#4169E1", fg="white", font=("Helvetica", 16))
    label_row.place(relx=0.5, y=250, anchor="center")

    rows = tk.Entry(root, font=("Helvetica", 12), width=10)
    rows.place(relx=0.5, y=280, anchor="center")
    rows.insert(0, "6")  # Default placeholder value
    rows.bind("<FocusIn>", on_entry_click)
    rows.bind("<FocusOut>", on_focus_out)

    label_col = tk.Label(root, text="Columns:", bg="#4169E1", fg="white", font=("Helvetica", 16))
    label_col.place(relx=0.5, y=320, anchor="center")

    cols = tk.Entry(root, font=("Helvetica", 12), width=10)
    cols.place(relx=0.5, y=350, anchor="center")
    cols.insert(0, "7")  # Default placeholder value
    cols.bind("<FocusIn>", on_entry_click)
    cols.bind("<FocusOut>", on_focus_out)

    button_frame = tk.Frame(root, bg="#4169E1")
    button_frame.place(relx=0.5, y=400, anchor="center")

    button1 = tk.Button(button_frame, text="Two Player Mode", command=lambda: start_two_player_game(int(rows.get() or 6), int(cols.get() or 7)),
                        width=15, bg="#5cb85c", fg="white", font=("Helvetica", 12), relief=tk.GROOVE)
    button1.pack(side=tk.LEFT, padx=5)

    button2 = tk.Button(button_frame, text="Play with AI", command=lambda: start_play_with_ai(int(rows.get() or 6), int(cols.get() or 7)),
                        width=15, bg="#5bc0de", fg="white", font=("Helvetica", 12), relief=tk.GROOVE)
    button2.pack(side=tk.LEFT, padx=5)

    button4 = tk.Button(root, text="Exit", command=root.destroy, bg="#d9534f", fg="white", font=("Helvetica", 12), relief=tk.GROOVE)
    button4.place(relx=0.5, y=480, anchor="center")

    root.mainloop()

if __name__ == "__main__":
    main_menu()