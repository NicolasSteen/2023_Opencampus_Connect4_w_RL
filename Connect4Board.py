import numpy as np

class Board():

    def __init__(self, rows = 6, columns = 7):
        self.rows = rows
        self.columns = columns
        self.board = np.zeros((self.rows, self.columns), dtype=np.float32)
        self.current_player = np.random.choice((1,2))

    def reset_board(self):
        self.board = np.zeros((self.rows, self.columns), dtype=np.float32)
        self.current_player = np.random.choice((1,2))

    def update_board(self, col):
        for r in range(self.rows):
            if self.board[r][col] == 0:
                self.board[r][col] = self.current_player
                self.current_player = 2 if self.current_player == 1 else 1
                return self.board

    def full_Board(self):
        return False if any(self.board[self.rows-1][:] == 0) else True

    def valid_column(self, col):
        return True if self.board[self.rows-1][col] == 0 else False

    def winning_move(self):
        # Check horizontal locations for win
        for c in range(self.columns-3):
            for r in range(self.rows):
                if self.board[r][c] == self.board[r][c+1] == self.board[r][c+2] == self.board[r][c+3] != 0:
                    return True

        # Check vertical locations for win
        for c in range(self.columns):
            for r in range(self.rows-3):
                if self.board[r][c] == self.board[r+1][c] == self.board[r+2][c] == self.board[r+3][c] != 0:
                    return True

        # Check positively sloped diaganols
        for c in range(self.columns-3):
            for r in range(self.rows-3):
                if self.board[r][c] == self.board[r+1][c+1] == self.board[r+2][c+2] == self.board[r+3][c+3] != 0:
                    return True

        # Check negatively sloped diaganols
        for c in range(self.columns-3):
            for r in range(3, self.rows):
                if self.board[r][c] == self.board[r-1][c+1] == self.board[r-2][c+2] == self.board[r-3][c+3] != 0:
                    return True
        return False
    
    def converted_board(self):
        converter = np.vectorize(lambda x: 1 if x == 2 else 2 if x == 1 else 0)
        return np.array(converter(self.board), dtype=np.float32)

    def play(self):
        game_over = False
        while not game_over:
            print(f'Player {self.current_player}:')
            pretty_board(self.board)
            valid_actions = [col for col, value in enumerate(self.board[self.rows-1,:]) if value == 0]
            turn = int(input(f"Choose an action out of {valid_actions}: "))
            while not self.valid_column(turn):
                turn = int(input(f"Choose an action out of {valid_actions}: "))
            self.update_board(turn)

            win, remis = self.winning_move(), self.full_Board()
            if win or remis:
                game_over = True
        
        pretty_board(self.board)
        print(f'Player {1 if self.current_player == 2 else 2} wins!\n')
        print("###############################\n")
        print("########## GAME OVER ##########\n")
        print("###############################\n")
        print('- - - - - - - - - - - - - - - -')
        self.reset_board()

def pretty_board(board):
    board_flipped = np.flip(board, 0)
    row_text = "|" + " {} |"*board_flipped.shape[1]
    get_mark = lambda x: 'X' if x==1 else 'O' if x==2 else ' '
    print(("\n " + " {}  "*board_flipped.shape[1]).format(*list(range(board_flipped.shape[1]))))
    print("_____________________________")
    for row in range(board_flipped.shape[0]):
        marks = [get_mark(elem) for elem in board_flipped[row,:]]
        print(row_text.format(*marks))
    print("_____________________________\n")


if __name__ == '__main__':
    board = Board()
    board.play()
