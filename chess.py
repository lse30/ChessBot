"""
Just a bot to play check with, ill keep working on it for fun
might try and build an account for it and see what elo i can get it to.

v0.2.0 makes random moves, can see checks
able to  castles
no en passant
no pawn promotions

"""

import random

# Important to remember that you can have multiple queens!!!


FEN_STRING_START = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
FEN_CONVERT_DICT = {
    'r': ('black', 'rook'), 'n': ('black', 'knight'), 'b': ('black', 'bishop'),
    'q': ('black', 'queen'), 'k': ('black', 'king'), 'p': ('black', 'pawn'),
    'R': ('white', 'rook'), 'N': ('white', 'knight'), 'B': ('white', 'bishop'),
    'Q': ('white', 'queen'), 'K': ('white', 'king'), 'P': ('white', 'pawn'),
}
COORDS = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8}


class ChessBot:
    def __init__(self, colour='black', fen_string=FEN_STRING_START):
        fen_string = fen_string.split(' ')
        self.board = set_up_board(fen_string[0])
        self.colour = colour
        self.active_colour = fen_string[1]
        self.castling_availability = [] if fen_string[2] == '-' else list(fen_string[2])
        self.en_passant = fen_string[3]
        # TODO - add half-move clock and full-move number
        # These are fen_string[4 & 5]

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

        # If king is moved make sure castling is also removed
        if piece[1] == 'king':
            if piece[0] == 'white':
                if 'K' in self.castling_availability:
                    self.castling_availability.remove('K')
                if 'Q' in self.castling_availability:
                    self.castling_availability.remove('Q')
            else:
                if 'k' in self.castling_availability:
                    self.castling_availability.remove('k')
                if 'q' in self.castling_availability:
                    self.castling_availability.remove('q')
            if move == "e1g1":
                self.make_move("h1f1")
            elif move == "e1c1":
                self.make_move("a1d1")
            elif move == "e8cg8":
                self.make_move("h8f8")
            elif move == "e8c8":
                self.make_move("a8d8")

        if piece[1] == 'rook' and move[:2] == 'a1' and 'Q' in self.castling_availability:
            self.castling_availability.remove('Q')
        elif piece[1] == 'rook' and move[:2] == 'h1' and 'K' in self.castling_availability:
            self.castling_availability.remove('K')
        elif piece[1] == 'rook' and move[:2] == 'a8' and 'q' in self.castling_availability:
            self.castling_availability.remove('q')
        elif piece[1] == 'rook' and move[:2] == 'h8' and 'k' in self.castling_availability:
            self.castling_availability.remove('k')

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

    def make_pseudo_move(self, move):
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
        in_check, squares = self.check_for_checks()
        king_moves = self.find_king_moves()
        if in_check:
            temp = []
            for move in king_moves:
                self.make_pseudo_move(move)
                if not self.quick_check_for_checks():
                    temp.append(move)
                move_back = move[2:] + move[:2]
                self.make_pseudo_move(move_back)
            king_moves = temp
        else:
            castling = self.check_castling()
            king_moves += castling

        if in_check and not len(squares):
            return king_moves
        else:
            valid_moves = []
            for position in self.positions['pawn']:
                valid_moves += (self.find_pawn_moves(position))
            for position in self.positions['knight']:
                valid_moves += (self.find_knight_moves(position))
            for position in self.positions['rook']:
                valid_moves += (self.find_piece_moves(position, 'rook'))
            for position in self.positions['bishop']:
                valid_moves += (self.find_piece_moves(position, 'bishop'))
            for position in self.positions['queen']:
                valid_moves += (self.find_piece_moves(position, 'queen'))
            if in_check:
                temp = []
                for move in valid_moves:
                    destination = (int(move[3]), COORDS[move[2]])
                    if destination in squares:
                        temp.append(move)
                valid_moves = temp

        # if in_check:
        #     print("block moves!", valid_moves)
        #     print("king moves", king_moves)
        output = []
        for option in valid_moves:
            if self.in_line_with_king(option[0], option[1]):
                self.make_pseudo_move(option)
                in_check, squares = self.check_for_checks()
                if not in_check:
                    output.append(option)
                move_back = option[2:] + option[:2]
                self.make_pseudo_move(move_back)
            else:
                output.append(option)

        for option in king_moves:
            self.make_pseudo_move(option)
            if not self.quick_check_for_checks():
                output.append(option)
            move_back = option[2:] + option[:2]
            self.make_pseudo_move(move_back)
        return output

    def in_check(self):
        return self.quick_check_for_checks()

    def check_castling(self):
        """
        check if the pieces haven't moved
        check there is no pieces blocking the castle
        check the 2 other squares for checks
        """
        output = []
        if self.colour == 'white':
            if 'K' in self.castling_availability:
                if self.squares_empty([(1, 6), (1, 7)]):
                    if self.castling_king_safety(['e1f1', 'e1g1']):
                        output.append('e1g1')

            if 'Q' in self.castling_availability:
                if self.squares_empty([(1, 4), (1, 3), (1, 2)]):
                    if self.castling_king_safety(['e1d1', 'e1c1']):
                        output.append('e1c1')
        else:
            if 'k' in self.castling_availability:
                if self.squares_empty([(8, 6), (8, 7)]):
                    if self.castling_king_safety(['e8f8', 'e8g8']):
                        output.append('e8g8')
            if 'q' in self.castling_availability:
                if self.squares_empty([(8, 4), (8, 3), (8, 2)]):
                    if self.castling_king_safety(['e8d8', 'e8c8']):
                        output.append('e8c8')
        return output

    def squares_empty(self, location_list):
        for location in location_list:
            if self.board[location[0]][location[1]] != 'E':
                return False
        return True

    def castling_king_safety(self, moves):
        for move in moves:
            self.make_pseudo_move(move)
            if self.in_check():
                return False
            move_back = move[2:] + move[:2]
            self.make_pseudo_move(move_back)
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

    def find_pawn_moves(self, position):
        j, i = position
        valid_moves = []
        if self.colour == 'black':
            # pawn advance
            if self.board[i - 1][j] == 'E':
                move = self.board[0][j] + str(i) + self.board[0][j] + str(i - 1)
                valid_moves.append(move)
            if i == 7 and self.board[i - 2][j] == 'E' and self.board[i - 1][j] == 'E':
                move = self.board[0][j] + str(i) + self.board[0][j] + str(i - 2)
                valid_moves.append(move)

            # pawn take
            if j != 1:
                if len(self.board[i - 1][j - 1]) == 2 and self.board[i - 1][j - 1][0] == 'white':
                    move = self.board[0][j] + str(i) + self.board[0][j - 1] + str(i - 1)
                    valid_moves.append(move)
            if j != 8:
                if len(self.board[i - 1][j + 1]) == 2 and self.board[i - 1][j + 1][0] == 'white':
                    move = self.board[0][j] + str(i) + self.board[0][j + 1] + str(i - 1)
                    valid_moves.append(move)
        else:
            # pawn advance
            if self.board[i + 1][j] == 'E':
                move = self.board[0][j] + str(i) + self.board[0][j] + str(i + 1)
                valid_moves.append(move)
            if i == 2 and self.board[i + 2][j] == 'E' and self.board[i + 1][j] == 'E':
                move = self.board[0][j] + str(i) + self.board[0][j] + str(i + 2)
                valid_moves.append(move)

            # pawn take
            if j != 1:
                if len(self.board[i + 1][j - 1]) == 2 and self.board[i + 1][j - 1][0] == 'black':
                    move = self.board[0][j] + str(i) + self.board[0][j - 1] + str(i + 1)
                    valid_moves.append(move)
            if j != 8:
                if len(self.board[i + 1][j + 1]) == 2 and self.board[i + 1][j + 1][0] == 'black':
                    move = self.board[0][j] + str(i) + self.board[0][j + 1] + str(i + 1)
                    valid_moves.append(move)

        return valid_moves

    def find_piece_moves(self, position, piece):
        j, i = position
        if piece == "rook":
            directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        elif piece == "bishop":
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        else:
            directions = [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]

        valid_moves = []
        for direction in directions:
            ii = i + direction[0]
            jj = j + direction[1]
            while 1 <= ii <= 8 and 1 <= jj <= 8:
                if self.board[ii][jj] == 'E':
                    # free square to move to
                    move = self.board[0][j] + str(i) + self.board[0][jj] + str(ii)
                    valid_moves.append(move)
                elif self.board[ii][jj][0] == self.colour:
                    # hit a piece of the same colour
                    break
                else:
                    # capture a piece
                    move = self.board[0][j] + str(i) + self.board[0][jj] + str(ii)
                    valid_moves.append(move)
                    break
                ii += direction[0]
                jj += direction[1]
        return valid_moves

    def find_knight_moves(self, position):
        j, i = position
        valid_moves = []
        options = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        for move in options:
            ii = i + move[0]
            jj = j + move[1]
            if (1 <= ii <= 8) and (1 <= jj <= 8):
                if self.board[ii][jj] == 'E' or self.board[ii][jj][0] != self.colour:
                    valid_moves.append(self.board[0][j] + str(i) + self.board[0][jj] + str(ii))

        return valid_moves

    def find_king_moves(self):
        j, i = self.positions['king']
        valid_moves = []
        for ii in [-1, 0, 1]:
            for jj in [-1, 0, 1]:
                if ii == 0 and jj == 0:
                    pass
                else:
                    if (1 <= (i + ii) <= 8) and (1 <= (j + jj) <= 8):
                        if self.board[i+ii][j+jj] == 'E' or self.board[i+ii][j+jj][0] != self.colour:
                            valid_moves.append(self.board[0][j] + str(i) + self.board[0][j+jj] + str(i+ii))

        return valid_moves

    def check_for_checks(self):
        """
        checks to see in the king in is check
        -Check if any pawns attack the king first as it is not possible to create a double check involving a pawn.
        -Check knights, then horizontal/vertical then diagonals
        """

        # Check for checks using a pawn.
        j, i = self.positions['king']
        if self.colour == "black" and i > 1:
            if j > 1 and self.board[i - 1][j - 1] != 'E' and self.board[i - 1][j - 1] == ('white', 'pawn'):
                return True, [(i - 1, j - 1)]
            if j < 8 and self.board[i - 1][j + 1] != 'E' and self.board[i - 1][j + 1] == ('white', 'pawn'):
                return True, [(i - 1, j + 1)]
        elif self.colour == "white" and i < 8:
            if j > 1 and self.board[i + 1][j - 1] != 'E' and self.board[i + 1][j - 1] == ('black', 'pawn'):
                return True, [(i + 1, j - 1)]
            if j < 8 and self.board[i + 1][j + 1] != 'E' and self.board[i + 1][j + 1] == ('black', 'pawn'):
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
                if self.board[ii][jj] != 'E' and self.board[ii][jj][0] != self.colour and self.board[ii][jj][1] == 'knight':
                    check_k = True
                    blocking_squares = [(ii, jj)]

        check_hv = False

        # Checks Horizontal and Vertical positions
        for combination in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            temp = []
            ii = i + combination[0]
            jj = j + combination[1]
            while 1 <= jj <= 8 and 1 <= ii <= 8:
                if self.board[ii][jj] == 'E':
                    temp.append((ii, jj))
                    ii += combination[0]
                    jj += combination[1]
                elif self.board[ii][jj][0] == self.colour:
                    break
                elif self.board[ii][jj][1] in ['pawn', 'king', 'knight', 'bishop']:
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
        for combination in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            temp = []
            ii = i + combination[0]
            jj = j + combination[1]
            while 1 <= jj <= 8 and 1 <= ii <= 8:
                if self.board[ii][jj] == 'E':
                    temp.append((ii, jj))
                    ii += combination[0]
                    jj += combination[1]
                elif self.board[ii][jj][0] == self.colour:
                    break
                elif self.board[ii][jj][1] in ['pawn', 'king', 'knight', 'rook']:
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

    def quick_check_for_checks(self):
        """
        checks to see in the king in is check
        faster than other check for check because it doesnt care about
        double checks or blocking squares
        """
        j, i = self.positions['king']
        # Check for checks using a pawn.

        if self.colour == "black" and i > 1:
            if j > 1 and self.board[i - 1][j - 1] != 'E' and self.board[i - 1][j - 1] == ('white', 'pawn'):
                return True
            if j < 8 and self.board[i - 1][j + 1] != 'E' and self.board[i - 1][j + 1] == ('white', 'pawn'):
                return True
        elif self.colour == "white" and i < 8:
            if j > 1 and self.board[i + 1][j - 1] != 'E' and self.board[i + 1][j - 1] == ('black', 'pawn'):
                return True
            if j < 8 and self.board[i + 1][j + 1] != 'E' and self.board[i + 1][j + 1] == ('black', 'pawn'):
                return True
        # checks knights
        options = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        for move in options:
            ii = i + move[0]
            jj = j + move[1]
            if (1 <= ii <= 8) and (1 <= jj <= 8):
                if self.board[ii][jj] != 'E' and self.board[ii][jj][0] != self.colour and self.board[ii][jj][1] == 'knight':
                    return True

        # Checks Horizontal and Vertical positions
        for combination in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            ii = i + combination[0]
            jj = j + combination[1]
            while 1 <= jj <= 8 and 1 <= ii <= 8:
                if self.board[ii][jj] == 'E':
                    ii += combination[0]
                    jj += combination[1]
                elif self.board[ii][jj][0] == self.colour:
                    break
                elif self.board[ii][jj][1] in ['pawn', 'king', 'knight', 'bishop']:
                    break
                else:
                    return True

        # Checks Diagonals for checks
        for combination in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            ii = i + combination[0]
            jj = j + combination[1]
            while 1 <= jj <= 8 and 1 <= ii <= 8:
                if self.board[ii][jj] == 'E':
                    ii += combination[0]
                    jj += combination[1]
                elif self.board[ii][jj][0] == self.colour:
                    break
                elif self.board[ii][jj][1] in ['pawn', 'king', 'knight', 'rook']:
                    break
                else:
                    return True
        return False

    def in_line_with_king(self, i, j):
        i = COORDS[i]
        j = int(j)
        king_i, king_j = self.positions['king']
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
    rank = 8
    line = [rank]
    for item in fen_string:
        if item == '/':
            board.append(line)
            rank -= 1
            line = [rank]
        elif item in '12345678':
            for i in range(int(item)):
                line.append('E')
        else:
            line.append(FEN_CONVERT_DICT[item])
    board.append(line)
    board.append([0, 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'])
    board.reverse()
    return board


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
    #
    # for depth in range(0, max_depth + 1):
    #     for move in moves:
    #         pass
    #     print("Depth: {}, Nodes = {}, Captures = {}, E.p. = {}, Castles = {}, Checks = {}, Checkmates = {}"
    #           .format(depth, len(moves), captures, en_passant, castles, checks, check_mates))

    white_bot = ChessBot(colour='white')
    moves = white_bot.find_moves()
    move_combinations = []
    for move in moves:
        move_combinations.append([move])

    print(len(move_combinations))
    start = move_combinations
    for depth in range(1, max_depth):
        move_combinations = start
        checks = 0
        while depth > 0:
            temp = []

            for move_set in move_combinations:

                if len(move_set) % 2 == 1:
                    black_bot = ChessBot()
                    for move in move_set:
                        black_bot.make_move(move)
                    if black_bot.in_check():
                        checks += 1
                    next_move = black_bot.find_moves()
                else:
                    white_bot = ChessBot(colour='white')
                    for move in move_set:
                        white_bot.make_move(move)
                    next_move = white_bot.find_moves()
                    if white_bot.in_check():
                        checks += 1
                for item in next_move:
                    temp.append(move_set + [item])

            move_combinations = temp
            depth -= 1
        print(len(move_combinations), checks)


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
    # game.make_move('f1e4')
    # game.make_move('g1g4')
    # game.make_move('e1g1')
    # print(game.find_moves())
    # print(game.produce_fen_string())
    # # game.make_move('d8d6')
    # # game.make_move('c1b4')
    # # game.make_move('e8c3')
    # # game.find_moves()


if __name__ == "__main__":
    main()
