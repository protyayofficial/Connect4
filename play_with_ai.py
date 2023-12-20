from tkinter import messagebox
import tkinter as tk

class PlayWithAI:
    """Class representing the Connect 4 game against AI."""
    def __init__(self, rows, cols, game):
        """Initialize the PlayWithAI class.

        Args:
            rows (int): Number of rows in the game.
            cols (int): Number of columns in the game.
            game (Connect4Game): Instance of the Connect4Game class.
        """
        self.rows = rows
        self.cols = cols
        self.game = game
        self.turn = 1  # Human player starts
        self.create_game_window()

    def create_game_window(self):
        """Create the game window and initialize game variables."""
        self.canvas = self.game.canvas
        self.canvas.bind("<Motion>", self.hover_over_column)
        self.canvas.bind("<Button-1>", self.drop_piece)

        self.piece_radius = 40
        self.column_width = 100
        self.board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

    def evaluate_position(self, board):
        """Evaluate the position of the game board for AI strategy.

        Args:
            board (list): Current state of the game board.

        Returns:
            int: The score of the current board position.
        """
        score = 0
        # Check for potential winning moves for the AI (2 in a row/column)
        for r in range(self.rows):
            for c in range(self.cols - 3):
                window = board[r][c:c + 4]
                score += self.evaluate_window(window)

        for c in range(self.cols):
            for r in range(self.rows - 3):
                window = [board[i][c] for i in range(r, r + 4)]
                score += self.evaluate_window(window)

        for r in range(self.rows - 3):
            for c in range(self.cols - 3):
                window = [board[r + i][c + i] for i in range(4)]
                score += self.evaluate_window(window)

        for r in range(3, self.rows):
            for c in range(self.cols - 3):
                window = [board[r - i][c + i] for i in range(4)]
                score += self.evaluate_window(window)

        return score

    def evaluate_window(self, window):
        """Evaluate the score of a specific window of the game board.

        Args:
            window (list): A window of the game board.

        Returns:
            int: The score of the given window.
        """
        ai_piece = 2
        human_piece = 1
        score = 0

        if window.count(ai_piece) == 4:
            score += 10000
        elif window.count(ai_piece) == 3 and window.count(0) == 1:
            score += 100
        elif window.count(ai_piece) == 2 and window.count(0) == 2:
            score += 10

        if window.count(human_piece) == 3 and window.count(0) == 1:
            score -= 100
        elif window.count(human_piece) == 2 and window.count(0) == 2:
            score -= 10

        return score


    def hover_over_column(self, event):
        """Display the hover effect when the mouse is over a column.

        Args:
            event (tk.Event): Mouse event containing position information.
        """
        col = event.x // self.column_width
        if col >= 0 and col < self.cols:
            self.canvas.delete("hover_piece")
            x = col * self.column_width + self.column_width // 2
            y = self.piece_radius
            color = "red" if self.turn == 1 else "yellow"
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
                self.human_move(col)
                if not self.check_winner():
                    self.ai_move()

    def ai_move(self):
        """Perform the AI's move on the game board."""
        best_score = float('-inf')
        best_col = 0

        for col in range(self.cols):
            if self.get_next_open_row(col) is not None:
                row = self.get_next_open_row(col)
                self.board[row][col] = 2  # Simulate AI move
                score = self.minimax(self.board, 5, False, float('-inf'), float('inf'))
                self.board[row][col] = 0  # Undo move

                if score > best_score:
                    best_score = score
                    best_col = col

        self.drop_piece_with_ai(best_col)

        
    def minimax(self, board, depth, maximizing_player, alpha, beta):
        """Implement the minimax algorithm for AI decision-making.

        Args:
            board (list): Current state of the game board.
            depth (int): Depth of the search tree.
            maximizing_player (bool): Indicates if the AI is maximizing.
            alpha (int): Alpha value for alpha-beta pruning.
            beta (int): Beta value for alpha-beta pruning.

        Returns:
            int: The evaluated score of the board.
        """
        result = self.check_winner()
        if result != 0:
            if result == 2:
                return 10000 - depth
            elif result == 1:
                return -10000 + depth
            else:
                return 0

        if depth >= 6:  # Limiting depth for performance
            return 0

        if maximizing_player:
            max_eval = float('-inf')
            for col in range(self.cols):
                if self.get_next_open_row(col) is not None:
                    row = self.get_next_open_row(col)
                    board[row][col] = 2  # Simulate AI move
                    eval = self.evaluate_position(board)
                    board[row][col] = 0  # Undo move
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
            return max_eval
        else:
            min_eval = float('inf')
            for col in range(self.cols):
                if self.get_next_open_row(col) is not None:
                    row = self.get_next_open_row(col)
                    board[row][col] = 1  # Simulate human move
                    eval = self.evaluate_position(board)
                    board[row][col] = 0  # Undo move
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
            return min_eval

    def drop_piece_with_ai(self, col):
        """Drop the game piece for the AI.

        Args:
            col (int): Column where the AI wants to drop the piece.
        """
        row = self.get_next_open_row(col)
        if row is not None:
            x = col * self.column_width + self.column_width // 2
            y = (row + 1) * self.column_width + self.column_width // 2
            
            color = "yellow"  # AI color
            self.canvas.create_oval(
                x - self.piece_radius,
                y - self.piece_radius,
                x + self.piece_radius,
                y + self.piece_radius,
                fill=color, outline=""
            )
            self.board[row][col] = 2  # Update the grid for AI
            winner = self.check_winner()
            if winner:
                self.game_over(winner)
            else:
                self.turn = 1  # Switch back to human player's turn
                
    def human_move(self, col):
        """Drop the game piece for the human player.

        Args:
            col (int): Column where the human player wants to drop the piece.
        """
        row = self.get_next_open_row(col)
        if row is not None:
            x = col * self.column_width + self.column_width // 2
            y = (row + 1) * self.column_width + self.column_width // 2
            color = "red"  # Human player color
            self.canvas.create_oval(
                x - self.piece_radius,
                y - self.piece_radius,
                x + self.piece_radius,
                y + self.piece_radius,
                fill=color, outline=""
            )
            self.board[row][col] = 1  # Update the grid for the human player
            winner = self.check_winner()
            if winner:
                self.game_over(winner)
            else:
                self.turn = 2  # Switch to AI player's turn


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

    
    def check_winner(self):
        """Check for a winner on the game board.

        Returns:
            int: 0 if no winner, 1 if human player wins, 2 if AI wins.
        """
        for r in range(self.rows):
            for c in range(self.cols - 3):
                if (
                    self.board[r][c]
                    == self.board[r][c + 1]
                    == self.board[r][c + 2]
                    == self.board[r][c + 3]
                    != 0
                ):
                    return self.board[r][c]

        for c in range(self.cols):
            for r in range(self.rows - 3):
                if (
                    self.board[r][c]
                    == self.board[r + 1][c]
                    == self.board[r + 2][c]
                    == self.board[r + 3][c]
                    != 0
                ):
                    return self.board[r][c]

        for r in range(self.rows - 3):
            for c in range(self.cols - 3):
                if (
                    self.board[r][c]
                    == self.board[r + 1][c + 1]
                    == self.board[r + 2][c + 2]
                    == self.board[r + 3][c + 3]
                    != 0
                ):
                    return self.board[r][c]

                if (
                    self.board[self.rows - 1 - r][c]
                    == self.board[self.rows - 2 - r][c + 1]
                    == self.board[self.rows - 3 - r][c + 2]
                    == self.board[self.rows - 4 - r][c + 3]
                    != 0
                ):
                    return self.board[self.rows - 1 - r][c]

        return 0


    def game_over(self, player):
        """Handle the end of the game.

        Args:
            player (int): Player who won (1 for human, 2 for AI).
        """
        winner = f"Player {player}"
        
        ai_score = self.evaluate_position(self.board) if player == 2 else 0
        human_score = self.evaluate_position(self.board) if player == 1 else 0
        
        message = f"{winner} wins!\nAI Score: {ai_score}\nHuman Score: {human_score}"
        messagebox.showinfo("Game Over", message)
        self.game.root.destroy()  # Close the game window


