import copy
import sys
import pygame
import numpy as np

WIDTH = 600
HEIGHT = 600
ROWS = 3
COLS = 3

SQUARE_SIZE = WIDTH // COLS
GAP = SQUARE_SIZE // 4
RADIUS = SQUARE_SIZE // 3

LINE_WIDTH = 10
O_WIDTH = 13
X_WIDTH = 20

BACKGROUND_COLOR = (32, 38, 46)
LINE_COLOR = (67, 66, 66)
O_COLOR = (239, 231, 200)
X_COLOR = (34, 163, 159)

# Window Setup

pygame.init()
screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
pygame.display.set_caption('TIC TAC TOE')
screen.fill( BACKGROUND_COLOR )

# Game classes

class Board:

    def __init__(self):
        self.squares = np.zeros( (ROWS, COLS) ) # 3*3 matrix
        self.empty_squares = self.squares
        self.marked_squares = 0

    #return the state of the game (1:player1 win, 2:player2 win, 0 no winner yet)
    def game_state(self, show=False):

        # Vertical
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                player = self.squares[0][col]
                if show:
                    color = O_COLOR if player == 2 else X_COLOR
                    iPos = (col * SQUARE_SIZE + SQUARE_SIZE // 2, 20)
                    fPos = (col * SQUARE_SIZE + SQUARE_SIZE // 2, HEIGHT - 20)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                return player

        # Horizontal
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                player = self.squares[row][0] 
                if show:
                    color = O_COLOR if player == 2 else X_COLOR
                    iPos = (20, row * SQUARE_SIZE + SQUARE_SIZE // 2)
                    fPos = (WIDTH - 20, row * SQUARE_SIZE + SQUARE_SIZE // 2)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                return player

        # Diagonals
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            player = self.squares[0][0]
            if show:
                color = O_COLOR if player == 2 else X_COLOR
                iPos = (20, 20)
                fPos = (WIDTH - 20, HEIGHT - 20)
                pygame.draw.line(screen, color, iPos, fPos, X_WIDTH)
            return player

        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            player = self.squares[2][0]
            if show:
                color = O_COLOR if player == 2 else X_COLOR
                iPos = (20, HEIGHT - 20)
                fPos = (WIDTH - 20, 20)
                pygame.draw.line(screen, color, iPos, fPos, X_WIDTH)
            return player

        # NO WINNER
        return 0

    #mark a square in the matrix with 1 or 2 
    def mark_square(self, row, col, player):
        self.squares[row][col] = player
        self.marked_squares += 1

    #check if square is empty
    def empty_square(self, row, col):
        return self.squares[row][col] == 0
    
    #ckeck if board is full
    def isfull(self):
        return self.marked_squares == 9

    #check if board is empty
    def isempty(self):
        return self.marked_squares == 0

    #get all empty squares in a list of tuples (x,y)
    def get_empty_squares(self):
        empty_squares = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.empty_square(row, col):
                    empty_squares.append( (row, col) )
        
        return empty_squares


class AI:

    def __init__(self, player=2):
        self.player = player

    #the min max algorithm
    def minimax(self, board, maximizing):
        
        case = board.game_state()

        #Define the final resuls (at the leaf of the tree)
        # player wins
        if case == 1:
            return 1, None # eval, move
        # AI wins
        if case == 2:
            return -1, None
        # draw
        if board.isfull():
            return 0, None

        # put in some recusivity
        if maximizing:
            max_eval = -100         #init the min val to the max value
            best_move = None        #init best move to none
            empty_squares = board.get_empty_squares()       #get the empty squares

            #get copies of the board and test each empty square and compare the evaluation
            for (row, col) in empty_squares:
                temp_board = copy.deepcopy(board)
                temp_board.mark_square(row, col, 1)
                eval = self.minimax(temp_board, False)[0]   #call the minmax with minimizing
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)

            return max_eval, best_move

        elif not maximizing:
            min_eval = 100          #init the min val to the max value
            best_move = None        #init best move to none
            empty_squares = board.get_empty_squares()       #get the empty squares

            #get copies of the board and test each empty square and compare the evaluation
            for (row, col) in empty_squares:
                temp_board = copy.deepcopy(board)       #get a copy of the board to test on it
                temp_board.mark_square(row, col, self.player)
                eval = self.minimax(temp_board, True)[0] #call the minmax with maximizing
                if eval < min_eval:     #compare the eval
                    min_eval = eval
                    best_move = (row, col)

            return min_eval, best_move


class Game: 

    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.player = 1   #1 is X and  2 is 0
        self.running = True
        self.draw_lines()


    def draw_lines(self):
        # draw the 4 lines in the board : 

        screen.fill( BACKGROUND_COLOR )

        #screen + start(x,y) + end(x,y) + width
        # vertical lines
        pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (WIDTH - SQUARE_SIZE, 0), (WIDTH - SQUARE_SIZE, HEIGHT), LINE_WIDTH)

        # horizontal lines
        pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, HEIGHT - SQUARE_SIZE), (WIDTH, HEIGHT - SQUARE_SIZE), LINE_WIDTH)

    def draw_X_O(self, row, col):
        
        #Draw the X
        if self.player == 1:
            #line1
            line1_start = (col * SQUARE_SIZE + GAP, row * SQUARE_SIZE + GAP)
            line1_end = (col * SQUARE_SIZE + SQUARE_SIZE - GAP, row * SQUARE_SIZE + SQUARE_SIZE - GAP)
            pygame.draw.line(screen, X_COLOR, line1_start, line1_end, X_WIDTH)
            #line2
            line2_start = (col * SQUARE_SIZE + GAP, row * SQUARE_SIZE + SQUARE_SIZE - GAP)
            line2_end= (col * SQUARE_SIZE + SQUARE_SIZE - GAP, row * SQUARE_SIZE + GAP)
            pygame.draw.line(screen, X_COLOR, line2_start, line2_end, X_WIDTH)
        
        #Draw the O
        elif self.player == 2:
            # draw circle
            # center = (x,y)
            center = (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2)
            pygame.draw.circle(screen, O_COLOR, center, RADIUS, O_WIDTH)

    def switch_player(self):
        self.player = self.player % 2 + 1

    def play(self, row, col):
        self.board.mark_square(row, col, self.player)
        self.draw_X_O(row, col)
        self.switch_player()

    def isover(self):
        return self.board.game_state(show=True) != 0 or self.board.isfull()

    def reset(self):
        self.__init__()

def main():
    # create game object : 
    game = Game()
    board = game.board
    ai = game.ai

    print('Click on Space bar to restart game')
    # Game loop
    while True:

        #events
        for event in pygame.event.get():
            # quit the game
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit() 
            
            # click on a square
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // SQUARE_SIZE
                col = pos[0] // SQUARE_SIZE
                
                if board.empty_square(row, col) and game.running:
                    game.play(row, col)
                    if game.isover():
                        game.running = False

            # keydown (r for restart)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game.reset()
                    board = game.board
                    ai = game.ai

        # AI plays
        if game.player == ai.player and game.running:

            # update the screen
            pygame.display.update()

            eval, move = ai.minimax(board,False)
            row, col = move
            game.play(row, col)

            if game.isover():
                game.running = False
            
        pygame.display.update()

main()