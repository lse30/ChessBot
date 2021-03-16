"""
Just a bot to play check with, ill keep working on it for fun
might try and build an account for it and see what elo i can get it to.

v0.1.0 makes random moves, cannot see checks yet
no castles
no en passant
no pawn promotions

"""

import random

# Important to remember that you can have multiple queens!!!

WHITE_START = {
    'pawn': [(1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2), (8, 2)],
    'rook': [(1, 1), (8, 1)],
    'knight': [(2, 1), (7, 1)],
    'bishop': [(3, 1), (6, 1)],
    'queen': [(4, 1)],
    'king': (5, 1)
}
BLACK_START = {
    'pawn': [(1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7), (8, 7)],
    'rook': [(1, 8), (8, 8)],
    'knight': [(2, 8), (7, 8)],
    'bishop': [(3, 8), (6, 8)],
    'queen': [(4, 8)],
    'king': (5, 8)
}
FEN_CONVERT_DICT = {
    'r': ('black', 'rook'), 'n': ('black', 'knight'), 'b': ('black', 'bishop'),
    'q': ('black', 'queen'), 'k': ('black', 'king'), 'p': ('black', 'pawn'),
    'R': ('white', 'rook'), 'N': ('white', 'knight'), 'B': ('white', 'bishop'),
    'Q': ('white', 'queen'), 'K': ('white', 'king'), 'P': ('white', 'pawn'),
}
COORDS = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8}


class ChessBot:
    def __init__(self, colour='black', FEN_string=None):
        self.board = set_up_board(FEN_string)
        self.colour = colour
        if FEN_string is None:
            if colour == 'black':
                self.positions = BLACK_START
            else:
                self.positions = WHITE_START
        else:
            self.positions = {'pawn': [], 'rook': [], 'knight': [], 'bishop': [], 'queen': []}
            for i in range(1, 9):
                for j in range(1, 9):
                    if self.board[i][j] != 'E' and self.board[i][j][0] == self.colour:
                        position = (j, i)
                        if self.board[i][j][1] == 'king':
                            self.positions['king'] = position
                        else:
                            self.positions[self.board[i][j][1]].append(position)

    def __str__(self):
        """displays the current state of the board"""
        board = self.board
        output = ''
        i = 8
        while i >= 1:
            output += str(board[i][1:])
            output += '\n'
            i -= 1
        return output

    def make_move(self, move):
        """moves a piece from one coord to another"""
        piece = self.board[int(move[1])][COORDS[move[0]]]
        target = self.board[int(move[3])][COORDS[move[2]]]
        self.board[int(move[1])][COORDS[move[0]]] = 'E'
        self.board[int(move[3])][COORDS[move[2]]] = piece
        if piece[0] == self.colour:
            if piece[1] == 'king':
                self.positions[piece[1]] = (COORDS[move[2]], int(move[3]))
            else:
                old = (COORDS[move[0]], int(move[1]))
                self.positions[piece[1]].remove(old)
                self.positions[piece[1]].append((COORDS[move[2]], int(move[3])))
        elif target != 'E':
            if target[1] == 'king':
                print("you've just captured the king!")
            else:
                self.positions[target[1]].remove((COORDS[move[2]], int(move[3])))

    def find_moves(self):
        in_check, squares = check_for_checks(self.positions['king'], self.board, self.colour)
        king_moves = find_king_moves(self.colour, self.board, self.positions['king'])
        if in_check:
            temp = []
            for move in king_moves:
                self.make_move(move)
                illegal_move = check_for_checks(self.positions['king'], self.board, self.colour)
                if not illegal_move[0]:
                    temp.append(move)
                move_back = move[2:] + move[:2]
                self.make_move(move_back)
            king_moves = temp

        if in_check and not len(squares):
            return king_moves
        else:
            valid_moves = []
            for position in self.positions['pawn']:
                valid_moves += (find_pawn_moves(self.colour, self.board, position[1], position[0]))
            for position in self.positions['knight']:
                valid_moves += (find_knight_moves(self.colour, self.board, position[1], position[0]))
            for position in self.positions['rook']:
                valid_moves += (find_piece_moves(self.colour, self.board, position[1], position[0], 'rook'))
            for position in self.positions['bishop']:
                valid_moves += (find_piece_moves(self.colour, self.board, position[1], position[0], 'bishop'))
            for position in self.positions['queen']:
                valid_moves += (find_piece_moves(self.colour, self.board, position[1], position[0], 'queen'))
            if in_check:
                temp = []
                for move in valid_moves:
                    destination = (int(move[3]), COORDS[move[2]])
                    if destination in squares:
                        temp.append(move)
                valid_moves = temp

        if in_check:
            print("block moves!", valid_moves)
            print("king moves", king_moves)
        return valid_moves + king_moves


def check_for_checks(king, board, colour):
    """
    checks to see in the king in is check
    -Check if any pawns attack the king first as it is not possible to create a double check involving a pawn.
    -Check knights, then horizontal/vertical then diagonals
    """

    # Check for checks using a pawn.
    j, i = king
    if colour == "black" and i > 1:
        if j > 1 and board[i-1][j-1] != 'E' and board[i-1][j-1] == ('white', 'pawn'):
            return True, [(i - 1, j - 1)]
        if j < 8 and board[i-1][j+1] != 'E' and board[i-1][j+1] == ('white', 'pawn'):
            return True, [(i - 1, j + 1)]
    elif colour == "white" and i < 8:
        if j > 1 and board[i+1][j-1] != 'E' and board[i+1][j-1] == ('black', 'pawn'):
            return True, [(i + 1, j - 1)]
        if j < 8 and board[i+1][j+1] != 'E' and board[i+1][j+1] == ('black', 'pawn'):
            return True, [(i + 1, j + 1)]

    # available squares that could be used to block the check
    blocking_squares = []
    # checks knights
    check_k = False
    options = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
    for move in options:
        ii = i + move[0]
        jj = j + move[1]
        if (1 <= ii <= 8) and (1 <= jj <= 8):
            if board[ii][jj] != 'E' and board[ii][jj][0] != colour and board[ii][jj][1] == 'knight':
                check_k = True
                blocking_squares = [(ii, jj)]

    check_hv = False

    # Checks Horizontal and Vertical positions
    for combination in [(0, -1),  (0, 1), (-1, 0), (1, 0)]:
        temp = []
        ii = i + combination[0]
        jj = j + combination[1]
        while 1 <= jj <= 8 and 1 <= ii <= 8:
            if board[ii][jj] == 'E':
                temp.append((ii, jj))
                ii += combination[0]
                jj += combination[1]
            elif board[ii][jj][0] == colour:
                break
            elif board[ii][jj][1] in ['pawn', 'king', 'knight', 'bishop']:
                break
            else:
                temp.append((ii, jj))
                check_hv = True
                break
        if check_hv:
            blocking_squares = temp
            break

    if check_k and check_hv:
        return True, []

    check_d = False
    # Checks Diagonals for checks
    for combination in [(-1, -1),  (-1, 1), (1, -1), (1, 1)]:
        temp = []
        ii = i + combination[0]
        jj = j + combination[1]
        while 1 <= jj <= 8 and 1 <= ii <= 8:
            if board[ii][jj] == 'E':
                temp.append((ii, jj))
                ii += combination[0]
                jj += combination[1]
            elif board[ii][jj][0] == colour:
                break
            elif board[ii][jj][1] in ['pawn', 'king', 'knight', 'rook']:
                break
            else:
                temp.append((ii, jj))
                check_d = True
                break
        if check_d:
            blocking_squares = temp
            break
    if (check_k or check_hv) and check_d:
        return True, []
    if check_k or check_hv or check_d:
        return True, blocking_squares
    else:
        return False, []


def find_pawn_moves(colour, board, i, j):
    valid_moves = []
    if colour == 'black':
        # pawn advance
        if board[i - 1][j] == 'E':
            move = board[0][j] + str(i) + board[0][j] + str(i - 1)
            valid_moves.append(move)
        if i == 7 and board[i - 2][j] == 'E' and board[i - 1][j] == 'E':
            move = board[0][j] + str(i) + board[0][j] + str(i - 2)
            valid_moves.append(move)

        # pawn take
        if j != 1:
            if len(board[i - 1][j - 1]) == 2 and board[i - 1][j - 1][0] == 'white':
                move = board[0][j] + str(i) + board[0][j - 1] + str(i - 1)
                valid_moves.append(move)
        if j != 8:
            if len(board[i - 1][j + 1]) == 2 and board[i - 1][j + 1][0] == 'white':
                move = board[0][j] + str(i) + board[0][j + 1] + str(i - 1)
                valid_moves.append(move)
    else:
        # pawn advance
        if board[i + 1][j] == 'E':
            move = board[0][j] + str(i) + board[0][j] + str(i + 1)
            valid_moves.append(move)
        if i == 2 and board[i + 2][j] == 'E' and board[i + 1][j] == 'E':
            move = board[0][j] + str(i) + board[0][j] + str(i + 2)
            valid_moves.append(move)

        # pawn take
        if j != 1:
            if len(board[i + 1][j - 1]) == 2 and board[i + 1][j - 1][0] == 'black':
                move = board[0][j] + str(i) + board[0][j - 1] + str(i + 1)
                valid_moves.append(move)
        if j != 8:
            if len(board[i + 1][j + 1]) == 2 and board[i + 1][j + 1][0] == 'black':
                move = board[0][j] + str(i) + board[0][j + 1] + str(i + 1)
                valid_moves.append(move)

    return valid_moves


def find_piece_moves(colour, board, i, j, piece):
    if piece == "rook":
        directions = [(0, -1),  (0, 1), (-1, 0), (1, 0)]
    elif piece == "bishop":
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    else:
        directions = [(0, -1),  (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]

    valid_moves = []
    for direction in directions:
        ii = i + direction[0]
        jj = j + direction[1]
        while 1 <= ii <= 8 and 1 <= jj <= 8:
            if board[ii][jj] == 'E':
                move = board[0][j] + str(i) + board[0][jj] + str(ii)
                valid_moves.append(move)
            elif board[ii][jj][0] == colour:
                break
            else:
                move = board[0][j] + str(i) + board[0][jj] + str(ii)
                valid_moves.append(move)
                break
            ii += direction[0]
            jj += direction[1]
    return valid_moves


def find_knight_moves(colour, board, i, j):
    valid_moves = []
    options = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
    for move in options:
        ii = i + move[0]
        jj = j + move[1]
        if (1 <= ii <= 8) and (1 <= jj <= 8):
            if board[ii][jj] == 'E' or board[ii][jj][0] != colour:
                valid_moves.append(board[0][j] + str(i) + board[0][jj] + str(ii))

    return valid_moves


def find_king_moves(colour, board, position):
    j, i = position
    valid_moves = []
    for ii in [-1, 0, 1]:
        for jj in [-1, 0, 1]:
            if ii == 0 and jj == 0:
                pass
            else:
                if (1 <= (i + ii) <= 8) and (1 <= (j + jj) <= 8):
                    if board[i+ii][j+jj] == 'E' or board[i+ii][j+jj][0] != colour:
                        valid_moves.append(board[0][j] + str(i) + board[0][j+jj] + str(i+ii))

    return valid_moves


def set_up_board(FEN_string):
    board = []
    if FEN_string is None:
        board = [[0, 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']]
        colour = 'white'
        order = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']
        rank = 1
        while rank <= 8:
            line = [rank]
            for i in range(1, 9):
                if rank == 1 or rank == 8:
                    line.append((colour, order[i-1]))
                elif rank == 2 or rank == 7:
                    line.append((colour, 'pawn'))
                else:
                    line.append('E')
            board.append(line)
            if rank == 2:
                colour = 'black'
            rank += 1
    else:
        rank = 8
        line = [rank]
        for item in FEN_string:
            if item == ' ':
                board.append(line)
                board.append([0, 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'])
                board.reverse()
                return board
            elif item == '/':
                board.append(line)
                rank -= 1
                line = [rank]
            elif item in '12345678':
                for i in range(int(item)):
                    line.append('E')
            else:
                line.append(FEN_CONVERT_DICT[item])
    return board


def main():
    FEN = "rnb1kbnr/p1qpp1pp/1p6/7Q/5p2/4P3/PPPP1PPP/R1B1KBNR b KQkq - 1 5"
    # FEN = None
    game = ChessBot(FEN_string=FEN)
    # print(game)
    # game.make_move('e8e4')
    # game.make_move('d1c4')
    # game.make_move('d8d6')
    # game.make_move('c1b4')
    # game.make_move('e8c3')
    game.find_moves()
    # while True:
    #     player_move = input("Enter your move: ")
    #     if player_move == 'p':
    #         print(game)
    #     else:
    #         game.make_move(player_move)
    #         moves = game.find_moves()
    #         print(len(moves))
    #         move = random.randint(0, len(moves) - 1)
    #         print(moves[move])
    #         game.make_move(moves[move])


if __name__ == "__main__":
    main()
