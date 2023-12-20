import numpy as np
import pygame
import math
import sys

ROW_COUNTS, COL_COUNTS = 6, 7
BOARD_COLOR = (0, 0, 255)
HOLE_COLOR = (0, 0, 0)
PLAYER1_COLOR = (255, 0, 0)
PLAYER2_COLOR = (255, 255, 0)

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


def draw_board(board):
    for r in range(ROW_COUNTS):
        for c in range(COL_COUNTS):
            pygame.draw.rect(screen, BOARD_COLOR, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, HOLE_COLOR, (c * SQUARESIZE + int(SQUARESIZE / 2), r * SQUARESIZE + SQUARESIZE + int(SQUARESIZE / 2)), RADIUS)
    
    for r in range(ROW_COUNTS):
        for c in range(COL_COUNTS):
            if board[r][c] == 1:
                pygame.draw.circle(screen, PLAYER1_COLOR, (c * SQUARESIZE + int(SQUARESIZE / 2), HEIGHT - (r * SQUARESIZE + int(SQUARESIZE / 2))), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, PLAYER2_COLOR, (c * SQUARESIZE + int(SQUARESIZE / 2), HEIGHT - (r * SQUARESIZE  + int(SQUARESIZE / 2))), RADIUS)

    pygame.display.update()    
        
    
board = create_board()
print(board)
game_over = False
turn = 0

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

while not game_over:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, HOLE_COLOR, (0, 0, WIDTH, SQUARESIZE))
            
            posx = event.pos[0]
            
            if turn == 0:
                pygame.draw.circle(screen, PLAYER1_COLOR, (posx, int(SQUARESIZE / 2)), RADIUS)
            else:
                pygame.draw.circle(screen, PLAYER2_COLOR, (posx, int(SQUARESIZE / 2)), RADIUS)
                
        pygame.display.update()
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            # print(event.pos)
            # Ask for player 1 input
            pygame.draw.rect(screen, HOLE_COLOR, (0, 0, WIDTH, SQUARESIZE))
            
            if turn == 0:
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARESIZE))
                
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)
                    
                    if winning_move(board, 1):
                        # print("Player 1 wins!")
                        label = display_font.render("Player 1 Wins!!", 1, PLAYER1_COLOR)
                        screen.blit(label, (40, 10))
                        
                        game_over = True

            # # Ask for player 2 input
            else:
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARESIZE))
                
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 2)
                    
                    if winning_move(board, 2):
                        # print("Player 2 wins!")
                        label = display_font.render("Player 2 Wins!!", 1, PLAYER2_COLOR)
                        screen.blit(label, (40, 10))
                        game_over = True
            
            
            print_board(board)        
            draw_board(board)
            turn += 1
            turn %= 2
            
            if game_over:
                
                pygame.time.wait(2000) # 2000 ms wait and then exit
                