import numpy as np
import pygame
import math
import sys
import random

ROW_COUNTS, COL_COUNTS = 6, 7
BOARD_COLOR = (0, 0, 255)
HOLE_COLOR = (0, 0, 0)
PLAYER1_COLOR = (255, 0, 0)
PLAYER2_COLOR = (255, 255, 0)

PLAYER = 0
AI = 1

EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2

DEPTH = 7

ALPHA, BETA = -math.inf, math.inf

WINDOW_LENGTH = 4

def create_board():
    board = np.zeros((6, 7))
    
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[5][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNTS):
        if board[r][col] == 0:
            return r

def print_board(board):
    print(np.flip(board, axis = 0))    
    
def winning_move(board, piece):
    # Check all horizontal locations for win
    
    for c in range(COL_COUNTS - 3):
        for r in range(ROW_COUNTS):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
                return True
    
    # Check all vertical locations for win    
    for r in range(ROW_COUNTS - 3):
        for c in range(COL_COUNTS):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
                return True
    
    # Check for positive slope diagonals
    for r in range(ROW_COUNTS - 3):
        for c in range(COL_COUNTS - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
                return True
    
    #Check for negative slope diagonals
    for r in range(3, ROW_COUNTS):
        for c in range(COL_COUNTS - 3):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                return True

def evaluate_window(window, piece):
    score = 0
    OPPONENT_PIECE = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opponent_piece = AI_PIECE
    
    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2
        
    if window.count(OPPONENT_PIECE) == 3 and window.count(EMPTY) == 1:
        score -= 4
        
    return score

def score_position(board, piece):
    score = 0
    
    # Center Piece Score
    center_array = [int(i) for i in list(board[:, COL_COUNTS // 2])]
    center_count = center_array.count(piece)
    
    score += center_count * 3

    # Horizontal Score    
    for r in range(ROW_COUNTS):
        row_array = [int(i) for i in list(board[r, :])]
        
        for c in range(COL_COUNTS - 3):
            window = row_array[c: c + WINDOW_LENGTH]
            score += evaluate_window(window, piece)
                
    # Vertical Score
    for r in range(COL_COUNTS):
        col_array = [int(i) for i in list(board[: ,c])]
        
        for r in range(ROW_COUNTS - 3):
            window = col_array[r: r + WINDOW_LENGTH] 
            score += evaluate_window(window, piece)

            
    # Positive Slope Diagonals Score
    for r in range(ROW_COUNTS - 3):
        for c in range(COL_COUNTS - 3):
            window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)] 
            score += evaluate_window(window, piece)
            
    # Negative Slope Diagonals Score
    for r in range(ROW_COUNTS - 3):
        for c in range(COL_COUNTS - 3):
            window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score

def is_terminal_node(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0

def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, 100000000000000)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -100000000000000)
            else: # Game is over, no more valid moves
                return (None, 0)
        else: # Depth is 0
            return (None, score_position(board, AI_PIECE))
            
    if maximizingPlayer: 
        value = -math.inf
        column = random.choice(valid_locations)
        
        for col in valid_locations:
            row = get_next_open_row(board, col)
            board_copy = board.copy()
            drop_piece(board_copy, row, col, AI_PIECE)
            new_score = minimax(board_copy, depth - 1, alpha, beta, False)[1]
            
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
            row = get_next_open_row(board, col)
            board_copy = board.copy()
            drop_piece(board_copy, row, col, PLAYER_PIECE)
            new_score = minimax(board_copy, depth - 1, alpha, beta, True)[1]
            
            if value > new_score:
                value = new_score
                column = col
                
            beta = min(value, beta)
            
            if alpha >= beta:
                break
    
        return column, value
    

def get_valid_locations(board):
    valid_locations = []
    
    for c in range(COL_COUNTS):
        if is_valid_location(board, c):
            valid_locations.append(c)
            
    return valid_locations
    
    
def pick_best_move(board, piece):
    best_score = -1000000    
    valid_locations = get_valid_locations(board)
    best_col = random.choice(valid_locations)
    
    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, piece)
        score = score_position(temp_board, piece)
        
        if best_score < score:
            best_score = score
            best_col = col
            
    return best_col

def draw_board(board):
    for r in range(ROW_COUNTS):
        for c in range(COL_COUNTS):
            pygame.draw.rect(screen, BOARD_COLOR, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, HOLE_COLOR, (c * SQUARESIZE + int(SQUARESIZE / 2), r * SQUARESIZE + SQUARESIZE + int(SQUARESIZE / 2)), RADIUS)
    
    for r in range(ROW_COUNTS):
        for c in range(COL_COUNTS):
            if board[r][c] == PLAYER_PIECE:
                pygame.draw.circle(screen, PLAYER1_COLOR, (c * SQUARESIZE + int(SQUARESIZE / 2), HEIGHT - (r * SQUARESIZE + int(SQUARESIZE / 2))), RADIUS)
            elif board[r][c] == AI_PIECE:
                pygame.draw.circle(screen, PLAYER2_COLOR, (c * SQUARESIZE + int(SQUARESIZE / 2), HEIGHT - (r * SQUARESIZE  + int(SQUARESIZE / 2))), RADIUS)

    pygame.display.update() 
           
    
board = create_board()
print(board)
game_over = False

pygame.init()

SQUARESIZE = 100
WIDTH = COL_COUNTS * SQUARESIZE
HEIGHT = (ROW_COUNTS + 1) * SQUARESIZE
RADIUS = int(SQUARESIZE / 2 - 5)


SIZE = (WIDTH, HEIGHT)

screen = pygame.display.set_mode(SIZE)
draw_board(board)

display_font = pygame.font.SysFont("monospace", 75)

pygame.display.update()

turn = random.randint(PLAYER, AI)

while not game_over:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, HOLE_COLOR, (0, 0, WIDTH, SQUARESIZE))
            
            posx = event.pos[0]
            
            if turn == PLAYER:
                pygame.draw.circle(screen, PLAYER1_COLOR, (posx, int(SQUARESIZE / 2)), RADIUS)
            # else:
            #     pygame.draw.circle(screen, PLAYER2_COLOR, (posx, int(SQUARESIZE / 2)), RADIUS)
                
        pygame.display.update()
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            # print(event.pos)
            # Ask for player 1 input
            pygame.draw.rect(screen, HOLE_COLOR, (0, 0, WIDTH, SQUARESIZE))
            
            if turn == PLAYER:
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARESIZE))
                
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)
                    
                    if winning_move(board, PLAYER_PIECE):
                        # print("Player 1 wins!")
                        label = display_font.render("Player 1 Wins!!", 1, PLAYER1_COLOR)
                        screen.blit(label, (40, 10))
                        
                        game_over = True
                        
                    turn += 1
                    turn %= 2
                    print_board(board)        
                    draw_board(board)

            # # Ask for player 2 input
    if turn == AI and not game_over:
        
        # col = pick_best_move(board, AI_PIECE)
        col, score = minimax(board, DEPTH, ALPHA, BETA, True)
        
        if is_valid_location(board, col):
            # pygame.time.wait(700)
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, 2)
            
            if winning_move(board, AI_PIECE):
                # print("Player 2 wins!")
                label = display_font.render("Player 2 Wins!!", 1, PLAYER2_COLOR)
                screen.blit(label, (40, 10))
                game_over = True
            
            print_board(board)        
            draw_board(board)
            
    
            turn += 1
            turn %= 2
    
    if game_over:
        pygame.time.wait(3000) # 2000 ms wait and then exit
                