"""
Just a bot to play check with, ill keep working on it for fun
might try and build an account for it and see what elo i can get it to.

v0.3.0 makes random moves, can see checks
able to  castles
completely rewrote the board and made the bot colour neutral
no en passant
no pawn promotions

"""

import random

# Important to remember that you can have multiple queens!!!

"""
FEN STRINGS
lowercase is black, UPPERCASE is WHITE
P/p = Pawn
R/r = Rook
N/n = Knight
B/b = bishop
Q/q = Queen
K/k = king
FEN strings display the board as a string reading left to right, top to bottom from whites perspective
a8, b8 ... g2, h1
"""
FEN_STRING_START = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
FEN_CONVERT_DICT = {
    'r': ('black', 'rook'), 'n': ('black', 'knight'), 'b': ('black', 'bishop'),
    'q': ('black', 'queen'), 'k': ('black', 'king'), 'p': ('black', 'pawn'),
    'R': ('white', 'rook'), 'N': ('white', 'knight'), 'B': ('white', 'bishop'),
    'Q': ('white', 'queen'), 'K': ('white', 'king'), 'P': ('white', 'pawn'),
}
"""use dict look ups to save time rather than doing the maths"""
J_COORDS = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7,
            0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
I_COORDS = {'1': 7, '2': 6, '3': 5, '4': 4, '5': 3, '6': 2, '7': 1, '8': 0,
            0: '8', 1: '7', 2: '6', 3: '5', 4: '4', 5: '3', 6: '2', 7: '1'}


class ChessBot:
    def __init__(self, fen_string=FEN_STRING_START):
        fen_string = fen_string.split(' ')
        self.board = set_up_board(fen_string[0])
        self.active_colour = fen_string[1]
        self.castling_availability = [] if fen_string[2] == '-' else list(fen_string[2])
        self.en_passant = fen_string[3]
        # TODO - add half-move clock and full-move number
        # These are fen_string[4 & 5]

        self.positions = {'P': [], 'R': [], 'N': [], 'B': [], 'Q': [], 'p': [], 'r': [], 'n': [], 'b': [], 'q': []}
        for i in range(8):
            for j in range(8):
                if self.board[i][j] != '_':
                    if self.board[i][j] == 'K':
                        self.positions['K'] = (i, j)
                    elif self.board[i][j] == 'k':
                        self.positions['k'] = (i, j)
                    else:
                        self.positions[self.board[i][j]].append((i, j))

    def __str__(self):
        """displays the current state of the board"""
        output = ''
        for line in self.board:
            for position in line:
                output += position + ' '
            output += '\n'
        return output

    def make_move(self, move):
        """moves a piece from one coord to another"""
        i_1, j_1 = convert_to_i_j(move[:2])
        i_2, j_2 = convert_to_i_j(move[2:])
        piece = self.board[i_1][j_1]
        target = self.board[i_2][j_2]

        # Make the move on self.board
        self.board[i_1][j_1] = '_'
        self.board[i_2][j_2] = piece

        # Special Cases of if the king is moved/castled

        if piece == 'K':
            if 'K' in self.castling_availability:
                self.castling_availability.remove('K')
            if 'Q' in self.castling_availability:
                self.castling_availability.remove('Q')
            if move == "e1g1":
                self.make_move("h1f1")
            elif move == "e1c1":
                self.make_move("a1d1")
        elif piece == 'k':
            if 'k' in self.castling_availability:
                self.castling_availability.remove('k')
            if 'q' in self.castling_availability:
                self.castling_availability.remove('q')
            if move == "e8cg8":
                self.make_move("h8f8")
            elif move == "e8c8":
                self.make_move("a8d8")

        # Stop castling if the rook is moved or captured
        if piece in 'Rr' or target in 'Rr':
            if piece == 'R' and move[:2] == 'a1' and 'Q' in self.castling_availability:
                self.castling_availability.remove('Q')
            elif piece == 'R' and move[:2] == 'h1' and 'K' in self.castling_availability:
                self.castling_availability.remove('K')
            elif piece == 'r' and move[:2] == 'a8' and 'q' in self.castling_availability:
                self.castling_availability.remove('q')
            elif piece == 'r' and move[:2] == 'h8' and 'k' in self.castling_availability:
                self.castling_availability.remove('k')
            # if the rook gets captured
            elif target == 'R' and move[2:] == 'a1' and 'Q' in self.castling_availability:
                self.castling_availability.remove('Q')
            elif target == 'R' and move[2:] == 'h1' and 'K' in self.castling_availability:
                self.castling_availability.remove('K')
            elif target == 'r' and move[2:] == 'a8' and 'q' in self.castling_availability:
                self.castling_availability.remove('q')
            elif target == 'r' and move[2:] == 'h8' and 'k' in self.castling_availability:
                self.castling_availability.remove('k')

        # move the piece in self.positions
        if piece in 'Kk':
            self.positions[piece] = convert_to_i_j(move[2:])
        else:
            self.positions[piece].remove(convert_to_i_j(move[:2]))
            self.positions[piece].append(convert_to_i_j(move[2:]))
            if target != '_':
                self.positions[target].remove(convert_to_i_j(move[2:]))

    def hide_piece(self, position):
        i, j = convert_to_i_j(position)
        self.board[i][j] = '_'

    def return_piece(self, position, piece):
        i, j = convert_to_i_j(position)
        self.board[i][j] = piece

    def find_moves(self, colour):
        if colour == 'w':
            pieces = ['P', 'N', 'R', 'B', 'Q', 'K']
        else:
            pieces = ['p', 'n', 'r', 'b', 'q', 'k']

        in_check, squares = self.check_for_checks(pieces)

        king_moves = self.find_king_moves(pieces)
        if in_check:
            temp = []
            for move in king_moves:
                self.hide_piece(move[:2])
                if not self.quick_check_for_checks(pieces, convert_to_i_j(move[2:])):
                    temp.append(move)
                self.return_piece(move[:2], pieces[5])
            king_moves = temp
        else:
            castling = self.check_castling(pieces)
            king_moves += castling

        if in_check and not len(squares):
            return king_moves
        else:
            move_options = []
            for position in self.positions[pieces[0]]:
                move_options += self.find_pawn_moves(position, colour)
            for position in self.positions[pieces[1]]:
                move_options += self.find_knight_moves(position, pieces)
            for piece in pieces[2:5]:
                for position in self.positions[piece]:
                    move_options += self.find_piece_moves(position, piece, pieces)
            if in_check:
                temp = []
                for move in move_options:
                    if move[2:] in squares:
                        temp.append(move)
                return king_moves + temp
            else:
                output = []
                for option in move_options:
                    if in_line_with_king(self.positions[pieces[5]], option[:2]):
                        i, j = convert_to_i_j(option[:2])
                        target = self.board[i][j]
                        self.hide_piece(option[:2])
                        if not self.quick_check_for_checks(pieces, self.positions[pieces[5]]):
                            output.append(option)
                        self.return_piece(option[:2], target)
                    else:
                        output.append(option)
                for option in king_moves:
                    self.hide_piece(option[:2])
                    if not self.quick_check_for_checks(pieces, convert_to_i_j(option[2:])):
                        output.append(option)
                    self.return_piece(option[:2], self.positions[pieces[5]])
                return output

    def check_castling(self, pieces):
        """
        check if the pieces haven't moved
        check there is no pieces blocking the castle
        check the 2 other squares for checks
        """
        output = []
        if pieces[5] == 'K':
            if 'K' in self.castling_availability:
                if self.squares_empty([(0, 5), (0, 6)]):
                    if self.castling_king_safety(['f1', 'g1'], pieces):
                        output.append('e1g1')

            if 'Q' in self.castling_availability:
                if self.squares_empty([(0, 3), (0, 2), (0, 1)]):
                    if self.castling_king_safety(['d1', 'c1'], pieces):
                        output.append('e1c1')
        else:
            if 'k' in self.castling_availability:
                if self.squares_empty([(7, 5), (7, 6)]):
                    if self.castling_king_safety(['f8', 'g8'], pieces):
                        output.append('e8g8')
            if 'q' in self.castling_availability:
                if self.squares_empty([(7, 3), (7, 2), (7, 1)]):
                    if self.castling_king_safety(['d8', 'c8'], pieces):
                        output.append('e8c8')
        return output

    def squares_empty(self, location_list):
        for location in location_list:
            if self.board[location[0]][location[1]] != '_':
                return False
        return True

    def castling_king_safety(self, moves, pieces):
        for move in moves:
            if self.quick_check_for_checks(pieces, move):
                return False
        return True

    def produce_fen_string(self):
        """makes a fen string for the current game"""
        output = ""
        rank = 8
        while rank > 0:
            count = 0
            for i in range(1, 9):
                if self.board[rank][i] == 'E':
                    count += 1
                else:
                    if count != 0:
                        output += str(count)
                        count = 0
                    piece = self.board[rank][i]
                    if piece[0] == 'white':
                        if piece[1] == 'pawn':
                            output += 'P'
                        elif piece[1] == 'rook':
                            output += 'R'
                        elif piece[1] == 'knight':
                            output += 'N'
                        elif piece[1] == 'bishop':
                            output += 'B'
                        elif piece[1] == 'queen':
                            output += 'Q'
                        else:
                            output += 'K'
                    else:
                        if piece[1] == 'pawn':
                            output += 'p'
                        elif piece[1] == 'rook':
                            output += 'r'
                        elif piece[1] == 'knight':
                            output += 'n'
                        elif piece[1] == 'bishop':
                            output += 'b'
                        elif piece[1] == 'queen':
                            output += 'q'
                        else:
                            output += 'k'

            if count != 0:
                output += str(count)
            output += '/'
            rank -= 1
        output = output[:-1]
        output += ' ' + self.active_colour + ' '
        if self.castling_availability:
            for item in self.castling_availability:
                output += item
        else:
            output += '-'
        output += ' ' + self.en_passant
        return output

    def find_pawn_moves(self, position, colour):
        i, j = position
        possible_moves = []
        # TODO pawn promotions
        if colour == 'w':
            # Pawn advance 1 square
            if i > 0 and self.board[i - 1][j] == '_':
                possible_moves.append(convert_to_chess_coords(i, j) + convert_to_chess_coords(i - 1, j))
            # Pawn advance 2 squares
            if i == 6 and self.board[i - 1][j] == '_' and self.board[i - 2][j] == '_':
                possible_moves.append(convert_to_chess_coords(i, j) + convert_to_chess_coords(i - 2, j))
            # Pawn take left
            if j > 0 and i > 0 and self.board[i - 1][j - 1] in 'prnbq':
                possible_moves.append(convert_to_chess_coords(i, j) + convert_to_chess_coords(i - 1, j - 1))
            # Pawn take right
            if j < 7 and i > 0 and self.board[i - 1][j + 1] in 'prnbq':
                possible_moves.append(convert_to_chess_coords(i, j) + convert_to_chess_coords(i - 1, j + 1))
        else:
            # Pawn advance 1 square
            if i < 7 and self.board[i + 1][j] == '_':
                possible_moves.append(convert_to_chess_coords(i, j) + convert_to_chess_coords(i + 1, j))
            # Pawn advance 2 squares
            if i == 1 and self.board[i + 1][j] == '_' and self.board[i + 2][j] == '_':
                possible_moves.append(convert_to_chess_coords(i, j) + convert_to_chess_coords(i + 2, j))
            # Pawn take left
            if j > 0 and i < 7 and self.board[i + 1][j - 1] in 'PRNBQ':
                possible_moves.append(convert_to_chess_coords(i, j) + convert_to_chess_coords(i + 1, j - 1))
            # Pawn take right
            if j < 7 and i < 7 and self.board[i + 1][j + 1] in 'PRNBQ':
                possible_moves.append(convert_to_chess_coords(i, j) + convert_to_chess_coords(i + 1, j + 1))
        return possible_moves

    def find_piece_moves(self, position, piece, pieces):
        i, j = position

        if piece in "Rr":
            directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        elif piece in "Bb":
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        else:
            directions = [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]

        possible_moves = []
        for direction in directions:
            ii = i + direction[0]
            jj = j + direction[1]
            while 0 <= ii <= 7 and 0 <= jj <= 7:
                if self.board[ii][jj] == '_':
                    # free square to move to
                    possible_moves.append(convert_to_chess_coords(i, j) + convert_to_chess_coords(ii, jj))
                elif self.board[ii][jj] in pieces:
                    # hit a piece of the same colour
                    break
                else:
                    # capture a piece
                    possible_moves.append(convert_to_chess_coords(i, j) + convert_to_chess_coords(ii, jj))
                    break
                ii += direction[0]
                jj += direction[1]
        return possible_moves

    def find_knight_moves(self, position, pieces):
        i, j = position
        possible_moves = []
        options = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        for move in options:
            ii = i + move[0]
            jj = j + move[1]
            if (0 <= ii <= 7) and (0 <= jj <= 7):
                if self.board[ii][jj] == '_' or self.board[ii][jj] not in pieces:
                    possible_moves.append(convert_to_chess_coords(i, j) + convert_to_chess_coords(ii, jj))
        return possible_moves

    def find_king_moves(self, pieces):
        i, j = self.positions[pieces[5]]
        valid_moves = []
        for ii in [-1, 0, 1]:
            for jj in [-1, 0, 1]:
                if ii == 0 and jj == 0:
                    pass
                else:
                    if (0 <= (i + ii) <= 7) and (0 <= (j + jj) <= 7):
                        if self.board[i + ii][j + jj] == '_' or self.board[i + ii][j + jj] not in pieces:
                            valid_moves.append(convert_to_chess_coords(i, j) + convert_to_chess_coords(i + ii, j + jj))
        return valid_moves

    def check_for_checks(self, pieces):
        """
        checks to see in the king in is check
        -Check if any pawns attack the king first as it is not possible to create a double check involving a pawn.
        -Check knights, then horizontal/vertical then diagonals
        """

        i, j = self.positions[pieces[5]]
        if pieces[5] == 'K':
            opponent_knight = 'n'
        else:
            opponent_knight = 'N'

        # Check for checks using a pawn.
        if pieces[5] == 'K' and i > 1:
            if j > 0 and self.board[i - 1][j - 1] == 'p':
                return True, [convert_to_chess_coords(i - 1, j - 1)]
            elif j < 7 and self.board[i - 1][j + 1] == 'p':
                return True, [convert_to_chess_coords(i - 1, j + 1)]
        elif pieces[5] == 'k' and i < 6:
            if j > 0 and self.board[i + 1][j - 1] == 'P':
                return True, [convert_to_chess_coords(i + 1, j - 1)]
            elif j < 7 and self.board[i + 1][j + 1] == 'P':
                return True, [convert_to_chess_coords(i + 1, j + 1)]

        # available squares that could be used to block the check
        blocking_squares = []

        # checks knights
        check_k = False
        options = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        for move in options:
            ii = i + move[0]
            jj = j + move[1]
            if (0 <= ii <= 7) and (0 <= jj <= 7):
                if self.board[ii][jj] == opponent_knight:
                    check_k = True
                    blocking_squares = [convert_to_chess_coords(ii, jj)]

        check_hv = False

        # Checks Horizontal and Vertical positions
        for combination in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            temp = []
            ii = i + combination[0]
            jj = j + combination[1]
            while 0 <= jj <= 7 and 0 <= ii <= 7:
                if self.board[ii][jj] == '_':
                    temp.append(convert_to_chess_coords(ii, jj))
                    ii += combination[0]
                    jj += combination[1]
                elif self.board[ii][jj] in pieces:
                    break
                elif self.board[ii][jj] in 'PpKkNnBb':
                    break
                else:
                    temp.append(convert_to_chess_coords(ii, jj))
                    check_hv = True
                    break
            if check_hv:
                blocking_squares = temp
                break

        if check_k and check_hv:
            return True, []

        check_d = False
        # Checks Diagonals for checks
        for combination in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            temp = []
            ii = i + combination[0]
            jj = j + combination[1]
            while 0 <= jj <= 7 and 0 <= ii <= 7:
                if self.board[ii][jj] == '_':
                    temp.append(convert_to_chess_coords(ii, jj))
                    ii += combination[0]
                    jj += combination[1]
                elif self.board[ii][jj] in pieces:
                    break
                elif self.board[ii][jj] in 'PpKkNnRr':
                    break
                else:
                    temp.append(convert_to_chess_coords(ii, jj))
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

    def quick_check_for_checks(self, pieces, position):
        """
        checks to see in the king in is check
        faster than other check for check because it doesnt care about
        double checks or blocking squares
        """
        i, j = position
        if pieces[5] == 'K':
            opponent_knight = 'n'
        else:
            opponent_knight = 'N'
        # Check for checks using a pawn.
        if pieces[5] == 'K' and i > 1:
            if j > 0 and self.board[i - 1][j - 1] == 'p':
                return True
            elif j < 7 and self.board[i - 1][j + 1] == 'p':
                return True
        elif pieces[5] == 'k' and i < 6:
            if j > 0 and self.board[i + 1][j - 1] == 'P':
                return True
            elif j < 7 and self.board[i + 1][j + 1] == 'P':
                return True

        # checks knights
        options = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        for move in options:
            ii = i + move[0]
            jj = j + move[1]
            if (0 <= ii <= 7) and (0 <= jj <= 7):
                if self.board[ii][jj] == opponent_knight:
                    return True

        # Checks Horizontal and Vertical positions
        for combination in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            temp = []
            ii = i + combination[0]
            jj = j + combination[1]
            while 0 <= jj <= 7 and 0 <= ii <= 7:
                if self.board[ii][jj] == '_':
                    temp.append(convert_to_chess_coords(ii, jj))
                    ii += combination[0]
                    jj += combination[1]
                elif self.board[ii][jj] in pieces:
                    break
                elif self.board[ii][jj] in 'PpKkNnBb':
                    break
                else:
                    return True

        # Checks Diagonals for checks
        for combination in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            ii = i + combination[0]
            jj = j + combination[1]
            while 0 <= jj <= 7 and 0 <= ii <= 7:
                if self.board[ii][jj] == '_':
                    ii += combination[0]
                    jj += combination[1]
                elif self.board[ii][jj] in pieces:
                    break
                elif self.board[ii][jj] in 'PpKkNnRr':
                    break
                else:
                    return True
        return False


def in_line_with_king(king, piece):
    i, j = convert_to_i_j(piece)
    king_i, king_j = king
    if i == king_i or j == king_j or abs(i - king_i) == abs(j - king_j):
        return True
    else:
        return False


def set_up_board(fen_string):
    """
    sets up the board based on a given fen_record
    Note the pieces can be referenced by board[rank][file]
    where file is a number a = 1, b = 2 etc...
    """
    board = []
    rank = []
    for item in fen_string:
        if item == '/':
            board.append(rank)
            rank = []
        elif item in '12345678':
            for i in range(int(item)):
                rank.append('_')
        else:
            rank.append(item)
    board.append(rank)
    return board


def convert_to_chess_coords(i, j):
    return J_COORDS[j] + I_COORDS[i]


def convert_to_i_j(chess_coords):
    return I_COORDS[chess_coords[1]], J_COORDS[chess_coords[0]]


def perft(max_depth):
    """
    Perft is a performance test, move path enumeration
    """
    # moves = []
    # nodes = len(moves)
    # captures = 0
    # en_passant = 0
    # castles = 0
    # promotions = 0
    # checks = 0
    # check_mates = 0
    bot = ChessBot()
    moves = bot.find_moves('w')
    move_combinations = []
    for move in moves:
        move_combinations.append([move])

    print(len(move_combinations))
    start = move_combinations
    for depth in range(1, max_depth):
        move_combinations = start
        while depth > 0:
            temp = []
            for move_set in move_combinations:
                bot = ChessBot()
                for move in move_set:
                    bot.make_move(move)
                if len(move_set) % 2 == 1:
                    next_move = bot.find_moves('b')
                else:
                    next_move = bot.find_moves('w')
                for item in next_move:
                    temp.append(move_set + [item])

            move_combinations = temp
            depth -= 1
        print(len(move_combinations))


def play_game(colour='black'):
    game = ChessBot(colour)
    if colour == 'white':
        moves = game.find_moves()
        move = random.randint(0, len(moves) - 1)
        print(moves[move])
        game.make_move(moves[move])
    while True:
        player_move = input("Enter your move: ")
        if player_move == 'p':
            print(game)
        elif player_move == 'fen':
            print(game.produce_fen_string())
            print(game.castling_availability)
        else:
            game.make_move(player_move)
            moves = game.find_moves()
            print(len(moves))
            move = random.randint(0, len(moves) - 1)
            print(moves[move])
            game.make_move(moves[move])


def main():
    perft(5)
    # play_game("white")
    # game = ChessBot()

    # game.make_move('b7b5')
    # game.make_move('a2a4')
    # game.make_move('b1d6')
    # print(game)
    # game.make_move('e1g1')
    # print(game.find_moves('w'))
    # print(game.produce_fen_string())
    # # game.make_move('d8d6')
    # # game.make_move('c1b4')
    # # game.make_move('e8c3')
    # # game.find_moves()


if __name__ == "__main__":
    main()
