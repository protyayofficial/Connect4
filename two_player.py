from tkinter import messagebox
import tkinter as tk

class TwoPlayerMode:
    """Class representing the Connect 4 game in two-player mode."""
    def __init__(self, rows, cols, game):
        """Initialize the TwoPlayerMode class.

        Args:
            rows (int): Number of rows in the game grid.
            cols (int): Number of columns in the game grid.
            game (Connect4Game): Instance of the Connect4Game class.
        """
        self.rows = rows
        self.cols = cols
        self.game = game
        self.turn = 1  # Player 1 starts
        self.create_game_window()

    def create_game_window(self):
        """Create the game window and initialize game variables."""
        self.canvas = self.game.canvas
        self.canvas.bind("<Motion>", self.hover_over_column)
        self.canvas.bind("<Button-1>", self.drop_piece)

        # Create circles as holes for the grid
        self.piece_radius = 40
        self.column_width = 100
        self.board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]  # Initialize empty grid

    def hover_over_column(self, event):
        """Show a hover effect over the column where the player is about to drop a piece.

        Args:
            event (tk.Event): Mouse event containing position information.
        """
        col = event.x // self.column_width
        if col >= 0 and col < self.cols:
            self.canvas.delete("hover_piece")  # Remove previous hover piece
            x = col * self.column_width + self.column_width // 2
            y = self.piece_radius
            color = "red" if self.turn == 1 else "yellow"  # Change color based on player turn
            self.canvas.create_oval(
                x - self.piece_radius,
                y - self.piece_radius,
                x + self.piece_radius,
                y + self.piece_radius,
                fill=color, outline="",
                tags="hover_piece"
            )

    def drop_piece(self, event):
        """Handle the dropping of a game piece by the player.

        Args:
            event (tk.Event): Mouse event containing position information.
        """
        col = event.x // self.column_width
        if col >= 0 and col < self.cols:
            row = self.get_next_open_row(col)
            if row is not None:  # Check if the column has free space
                x = col * self.column_width + self.column_width // 2
                y = (row + 1) * self.column_width + self.column_width // 2
                color = "red" if self.turn == 1 else "yellow"
                self.canvas.create_oval(
                    x - self.piece_radius,
                    y - self.piece_radius,
                    x + self.piece_radius,
                    y + self.piece_radius,
                    fill=color, outline=""
                )
                self.board[row][col] = self.turn  # Update the grid
                self.check_win()  # Check for win condition
                self.turn = 2 if self.turn == 1 else 1  # Switch players

    def get_next_open_row(self, col):
        """Get the next available row in a given column.

        Args:
            col (int): Column to check for available rows.

        Returns:
            int: The next available row in the column.
        """
        for r in range(self.rows - 1, -1, -1):
            if self.board[r][col] == 0:
                return r
        return None

    def check_win(self):
        """Check for a win condition in the game grid."""
        # Check for a win in rows
        for r in range(self.rows):
            for c in range(self.cols - 3):
                if self.board[r][c] == self.board[r][c + 1] == self.board[r][c + 2] == self.board[r][c + 3] != 0:
                    self.game_over(self.board[r][c])

        # Check for a win in columns
        for c in range(self.cols):
            for r in range(self.rows - 3):
                if self.board[r][c] == self.board[r + 1][c] == self.board[r + 2][c] == self.board[r + 3][c] != 0:
                    self.game_over(self.board[r][c])

        # Check for a win in diagonals (top-left to bottom-right)
        for r in range(self.rows - 3):
            for c in range(self.cols - 3):
                if self.board[r][c] == self.board[r + 1][c + 1] == self.board[r + 2][c + 2] == self.board[r + 3][c + 3] != 0:
                    self.game_over(self.board[r][c])

        # Check for a win in diagonals (bottom-left to top-right)
        for r in range(3, self.rows):
            for c in range(self.cols - 3):
                if self.board[r][c] == self.board[r - 1][c + 1] == self.board[r - 2][c + 2] == self.board[r - 3][c + 3] != 0:
                    self.game_over(self.board[r][c])

    def game_over(self, player):
        """Handle the end of the game.

        Args:
            player (int): Player who won (1 or 2).
        """
        winner = f"Player {player}"
        messagebox.showinfo("Game Over", f"{winner} wins!")
        self.game.root.destroy()  # Close the game window
