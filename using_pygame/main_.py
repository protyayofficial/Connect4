import numpy as np
import pygame
import math
import sys
import random

class Connect4:
    def __init__(self):
        
        self.ROW_COUNTS, self.COL_COUNTS = 6, 7
        self.BOARD_COLOR = (0, 0, 255)
        self.HOLE_COLOR = (0, 0, 0)
        self.PLAYER1_COLOR = (255, 0, 0)
        self.PLAYER2_COLOR = (255, 255, 0)

        self.PLAYER = 0
        self.AI = 1

        self.EMPTY = 0
        self.PLAYER_PIECE = 1
        self.AI_PIECE = 2

        self.DEPTH = 5

        self.ALPHA, self.BETA = -math.inf, math.inf

        self.WINDOW_LENGTH = 4
        
        self.turn = random.randint(self.PLAYER, self.AI)
        
    def create_board(self):
        
        board = np.zeros((self.ROW_COUNTS, self.COL_COUNTS))
        return board
    

    def drop_piece(self, board, row, col, piece):
        board[row][col] = piece

    def is_valid_location(self, board, col):
        return board[5][col] == 0

    def get_next_open_row(self, board, col):
        for r in range(self.ROW_COUNTS):
            if board[r][col] == 0:
                return r

    def print_board(self, board):
        print(np.flip(board, axis = 0))    
        
    def winning_move(self, board, piece):
        # Check all horizontal locations for win
        
        for c in range(self.COL_COUNTS - 3):
            for r in range(self.ROW_COUNTS):
                if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
                    return True
        
        # Check all vertical locations for win    
        for r in range(self.ROW_COUNTS - 3):
            for c in range(self.COL_COUNTS):
                if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
                    return True
        
        # Check for positive slope diagonals
        for r in range(self.ROW_COUNTS - 3):
            for c in range(self.COL_COUNTS - 3):
                if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
                    return True
        
        #Check for negative slope diagonals
        for r in range(3, self.ROW_COUNTS):
            for c in range(self.COL_COUNTS - 3):
                if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                    return True

    def evaluate_window(self, window, piece):
        score = 0
        OPPONENT_PIECE = self.PLAYER_PIECE
        if piece == self.PLAYER_PIECE:
            opponent_piece = self.AI_PIECE
        
        if window.count(piece) == 4:
            score += 100
        elif window.count(piece) == 3 and window.count(self.EMPTY) == 1:
            score += 5
        elif window.count(piece) == 2 and window.count(self.EMPTY) == 2:
            score += 2
            
        if window.count(OPPONENT_PIECE) == 3 and window.count(self.EMPTY) == 1:
            score -= 4
            
        return score

    def score_position(self, board, piece):
        score = 0
        
        # Center Piece Score
        center_array = [int(i) for i in list(board[:, self.COL_COUNTS // 2])]
        center_count = center_array.count(piece)
        
        score += center_count * 3

        # Horizontal Score    
        for r in range(self.ROW_COUNTS):
            row_array = [int(i) for i in list(board[r, :])]
            
            for c in range(self.COL_COUNTS - 3):
                window = row_array[c: c + self.WINDOW_LENGTH]
                score += self.evaluate_window(window, piece)
                    
        # Vertical Score
        for r in range(self.COL_COUNTS):
            col_array = [int(i) for i in list(board[: ,c])]
            
            for r in range(self.ROW_COUNTS - 3):
                window = col_array[r: r + self.WINDOW_LENGTH] 
                score += self.evaluate_window(window, piece)

                
        # Positive Slope Diagonals Score
        for r in range(self.ROW_COUNTS - 3):
            for c in range(self.COL_COUNTS - 3):
                window = [board[r + i][c + i] for i in range(self.WINDOW_LENGTH)] 
                score += self.evaluate_window(window, piece)
                
        # Negative Slope Diagonals Score
        for r in range(self.ROW_COUNTS - 3):
            for c in range(self.COL_COUNTS - 3):
                window = [board[r + 3 - i][c + i] for i in range(self.WINDOW_LENGTH)]
                score += self.evaluate_window(window, piece)

        return score

    def is_terminal_node(self, board):
        return self.winning_move(board, self.PLAYER_PIECE) or self.winning_move(board, self.AI_PIECE) or len(self.get_valid_locations(board)) == 0

    def minimax(self, board, depth, alpha, beta, maximizingPlayer):
        valid_locations = self.get_valid_locations(board)
        is_terminal = self.is_terminal_node(board)
        if depth == 0 or is_terminal:
            if is_terminal:
                if self.winning_move(board, self.AI_PIECE):
                    return (None, 100000000000000)
                elif self.winning_move(board, self.PLAYER_PIECE):
                    return (None, -100000000000000)
                else: # Game is over, no more valid moves
                    return (None, 0)
            else: # Depth is 0
                return (None, self.score_position(board, self.AI_PIECE))
                
        if maximizingPlayer: 
            value = -math.inf
            column = random.choice(valid_locations)
            
            for col in valid_locations:
                row = self.get_next_open_row(board, col)
                board_copy = board.copy()
                self.drop_piece(board_copy, row, col, self.AI_PIECE)
                new_score = self.minimax(board_copy, depth - 1, alpha, beta, False)[1]
                
                if value < new_score:
                    value = new_score
                    column = col
                    
                alpha = max(value, alpha)
                
                if alpha >= beta:
                    break

            return column, value

        else:
            value = math.inf
            column = random.choice(valid_locations)
            
            for col in valid_locations:
                row = self.get_next_open_row(board, col)
                board_copy = board.copy()
                self.drop_piece(board_copy, row, col, self.PLAYER_PIECE)
                new_score = self.minimax(board_copy, depth - 1, alpha, beta, True)[1]
                
                if value > new_score:
                    value = new_score
                    column = col
                    
                beta = min(value, beta)
                
                if alpha >= beta:
                    break
        
            return column, value
        

    def get_valid_locations(self, board):
        valid_locations = []
        
        for c in range(self.COL_COUNTS):
            if self.is_valid_location(board, c):
                valid_locations.append(c)
                
        return valid_locations
        
        
    def pick_best_move(self, board, piece):
        best_score = -1000000    
        valid_locations = self.get_valid_locations(board)
        best_col = random.choice(valid_locations)
        
        for col in valid_locations:
            row = self.get_next_open_row(board, col)
            temp_board = board.copy()
            self.drop_piece(temp_board, row, col, piece)
            score = self.score_position(temp_board, piece)
            
            if best_score < score:
                best_score = score
                best_col = col
                
        return best_col
    
class GAMEUI:
    def __init__(self, connect4_game):
        self.connect4 = connect4_game
        self.SQUARESIZE = 100
        self.WIDTH = self.connect4.COL_COUNTS * self.SQUARESIZE
        self.HEIGHT = (self.connect4.ROW_COUNTS + 1) * self.SQUARESIZE
        self.RADIUS = int(self.SQUARESIZE / 2 - 5)
        self.play_again = False

    def initialize_pygame(self):
        pygame.init()
        SIZE = (self.WIDTH, self.HEIGHT)
        self.screen = pygame.display.set_mode(SIZE)
        # self.draw_board(self.connect4.board)
        board = self.connect4.create_board()
        self.draw_board(board)
        
        return board
        
    def draw_board(self, board):
        for r in range(self.connect4.ROW_COUNTS):
            for c in range(self.connect4.COL_COUNTS):
                pygame.draw.rect(self.screen, self.connect4.BOARD_COLOR, (c * self.SQUARESIZE, r * self.SQUARESIZE + self.SQUARESIZE, self.SQUARESIZE, self.SQUARESIZE))
                pygame.draw.circle(self.screen, self.connect4.HOLE_COLOR, (c * self.SQUARESIZE + int(self.SQUARESIZE / 2), r * self.SQUARESIZE + self.SQUARESIZE + int(self.SQUARESIZE / 2)), self.RADIUS)
        
        for r in range(self.connect4.ROW_COUNTS):
            for c in range(self.connect4.COL_COUNTS):
                if board[r][c] == self.connect4.PLAYER_PIECE:
                    pygame.draw.circle(self.screen, self.connect4.PLAYER1_COLOR, (c * self.SQUARESIZE + int(self.SQUARESIZE / 2), self.HEIGHT - (r * self.SQUARESIZE + int(self.SQUARESIZE / 2))), self.RADIUS)
                elif board[r][c] == self.connect4.AI_PIECE:
                    pygame.draw.circle(self.screen, self.connect4.PLAYER2_COLOR, (c * self.SQUARESIZE + int(self.SQUARESIZE / 2), self.HEIGHT - (r * self.SQUARESIZE  + int(self.SQUARESIZE / 2))), self.RADIUS)

        pygame.display.update() 
        
    def draw_play_again_prompt(self):
        pygame.draw.rect(self.screen, self.connect4.HOLE_COLOR, (0, 0, self.WIDTH, self.SQUARESIZE))
        font = pygame.font.SysFont("monospace", 30)
        text = font.render("Press 1 to play again or 2 to exit", True, (255, 255, 255))
        self.screen.blit(text, (20, self.HEIGHT - 50))

    def handle_play_again_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            self.play_again = True
        elif keys[pygame.K_2]:
            self.play_again = False
            sys.exit()
            
    def reset_game(self):
        self.play_again = False
        
if __name__ == "__main__":
    connect4_game = Connect4()
    game_ui = GAMEUI(connect4_game)
    
    board = game_ui.initialize_pygame()
    
    game_over = False
    
    display_font = pygame.font.SysFont("monospace", 50)

    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                
            if not game_over:
                
                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(game_ui.screen, game_ui.connect4.HOLE_COLOR, (0, 0, game_ui.WIDTH, game_ui.SQUARESIZE))
                    
                    posx = event.pos[0]
                    
                    if game_ui.connect4.turn == game_ui.connect4.PLAYER:
                        pygame.draw.circle(game_ui.screen, game_ui.connect4.PLAYER1_COLOR, (posx, int(game_ui.SQUARESIZE / 2)), game_ui.RADIUS)
                    # else:
                    #     pygame.draw.circle(screen, PLAYER2_COLOR, (posx, int(SQUARESIZE / 2)), RADIUS)
                        
                pygame.display.update()
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # print(event.pos)
                    # Ask for player 1 input
                    pygame.draw.rect(game_ui.screen, game_ui.connect4.HOLE_COLOR, (0, 0, game_ui.WIDTH, game_ui.SQUARESIZE))
                    
                    if game_ui.connect4.turn == game_ui.connect4.PLAYER:
                        posx = event.pos[0]
                        col = int(math.floor(posx / game_ui.SQUARESIZE))
                        
                        if game_ui.connect4.is_valid_location(board, col):
                            row = game_ui.connect4.get_next_open_row(board, col)
                            game_ui.connect4.drop_piece(board, row, col, 1)
                            
                            if game_ui.connect4.winning_move(board, game_ui.connect4.PLAYER_PIECE):
                                # print("Player 1 wins!")
                                label = display_font.render("Player 1 Wins!!", 1, game_ui.connect4.PLAYER1_COLOR)
                                game_ui.screen.blit(label, (40, 10))
                                
                                game_over = True
                                
                            game_ui.connect4.turn += 1
                            game_ui.connect4.turn %= 2
                            # game_ui.connect4.print_board(board)        
                            game_ui.draw_board(board)

                    # # Ask for player 2 input
                if game_ui.connect4.turn == game_ui.connect4.AI and not game_over:
                    
                    # col = pick_best_move(board, AI_PIECE)
                    label = display_font.render("AI is thinking...", 1, (255, 255, 255))
                    game_ui.screen.blit(label, (40, 10))
                    
                    pygame.display.update()  
                    col, score = game_ui.connect4.minimax(board, game_ui.connect4.DEPTH, game_ui.connect4.ALPHA, game_ui.connect4.BETA, True)
                    
                    if game_ui.connect4.is_valid_location(board, col):
                        # pygame.time.wait(700)
                        row = game_ui.connect4.get_next_open_row(board, col)
                        game_ui.connect4.drop_piece(board, row, col, 2)
                        
                        if game_ui.connect4.winning_move(board, game_ui.connect4.AI_PIECE):
                            # print("Player 2 wins!")
                            label = display_font.render("Player 2 Wins!!", 1, game_ui.connect4.PLAYER2_COLOR)
                            game_ui.screen.blit(label, (40, 10))
                            game_over = True
                        
                        # print_board(board)   
                        game_ui.draw_board(board)
      
                        pygame.display.update()   
                
                        game_ui.connect4.turn += 1
                        game_ui.connect4.turn %= 2
                        
                        game_ui.draw_board(board)
                        
            else:
                game_ui.draw_play_again_prompt()
                pygame.display.update()
                
                game_ui.handle_play_again_input()
                pygame.display.update()
                

                if game_ui.play_again:
                    # Reset necessary game elements for a new game
                    board = game_ui.connect4.create_board()
                    game_ui.connect4.turn = game_ui.connect4.PLAYER
                    game_ui.draw_board(board)
                    game_over = False
                    game_ui.reset_game()  # Reset the play_again flag
                
                    pygame.display.update()
                else:
                    break
                
        pygame.display.flip()
    pygame.quit()
    sys.exit()
        