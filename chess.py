"""
Just a bot to play check with, ill keep working on it for fun
might try and build an account for it and see what elo i can get it to.

v0.1.0 makes random moves, cannot see checks yet
no castles
no en passant
no pawn promotions

"""
# import random


class ChessBot:
    def __init__(self, colour='black'):
        self.board = set_up_board()
        self.colour = colour
        self.coords = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8}
            self.king = 'e8'
        else:
            self.king = 'e1'

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
        if move[0:2] == self.king:
            self.king = move[2:]
        move = list(move)
        piece = self.board[int(move[1])][self.coords[move[0]]]
        self.board[int(move[1])][self.coords[move[0]]] = 'E'
        self.board[int(move[3])][self.coords[move[2]]] = piece
        return

    def find_moves(self):
        in_check = check_for_checks(int(self.king[1]), self.coords[self.king[0]], self.board, self.colour)
        print(in_check)

        valid_moves = []
        for i in range(1, 9):
            for j in range(1, 9):
                if len(self.board[i][j]) and self.board[i][j][0] == self.colour:
                    if self.board[i][j][1] == 'pawn':
                        valid_moves += (find_pawn_moves(self.colour, self.board, i, j))
                    if self.board[i][j][1] == 'rook':
                        valid_moves += (find_rook_moves(self.colour, self.board, i, j))
                    if self.board[i][j][1] == 'knight':
                        valid_moves += (find_knight_moves(self.colour, self.board, i, j))
                    if self.board[i][j][1] == 'bishop':
                        valid_moves += (find_bishop_moves(self.colour, self.board, i, j))
                    if self.board[i][j][1] == 'queen':
                        valid_moves += (find_rook_moves(self.colour, self.board, i, j))
                        valid_moves += (find_bishop_moves(self.colour, self.board, i, j))
                    if self.board[i][j][1] == 'king':
                        valid_moves += (find_king_moves(self.colour, self.board, i, j))

        return valid_moves


def check_for_checks(i, j, board, colour):
    """checks to see in the king in is check"""

    # all the squares that a piece could be moved to to block a check

    blocking_squares = []
    check = False

    # checks horizontal

    temp = set()
    jj = j - 1
    while jj >= 1:
        if board[i][jj] == 'E':
            temp.add((i, jj))
            jj -= 1
        elif board[i][jj][0] == colour:
            break
        elif board[i][jj][1] in ['pawn', 'king', 'knight', 'bishop']:
            break
        else:
            temp.add((i, jj))
            print(i, jj)
            check = True
            break
    if not check:
        temp = set()
        jj = j + 1
        while jj <= 8:
            if board[i][jj] == 'E':
                temp.add((i, jj))
                jj += 1
            elif board[i][jj][0] == colour:
                break
            elif board[i][jj][1] in ['pawn', 'king', 'knight', 'bishop']:
                break
            else:
                temp.add((i, jj))
                print(i, jj)
                check = True
                break

    # checks up and down

    if not check:
        temp = set()
        ii = i - 1
        while ii >= 1:
            if board[ii][j] == 'E':
                temp.add((ii, j))
                ii -= 1
            elif board[ii][j][0] == colour:
                break
            elif board[ii][j][1] in ['pawn', 'king', 'knight', 'bishop']:
                break
            else:
                temp.add((ii, j))
                print(ii, j)
                check = True
                break
    if not check:
        temp = set()
        ii = i + 1
        while ii <= 8:
            if board[ii][j] == 'E':
                temp.add((ii, j))
                ii += 1
            elif board[ii][j][0] == colour:
                break
            elif board[ii][j][1] in ['pawn', 'king', 'knight', 'bishop']:
                break
            else:
                temp.add((ii, j))
                print(ii, j)
                check = True
                break

    if check:
        blocking_squares.append(temp)
        check = False

    # check pawn checks

    if colour == "black" and i > 1:
        if j > 1 and board[i-1][j-1] != 'E' and board[i-1][j-1][0] == 'white' and board[i-1][j-1][1] == 'pawn':
            check = True
            print(i - 1, j - 1)
        if j < 8 and board[i-1][j+1] != 'E' and board[i-1][j+1][0] == 'white' and board[i-1][j+1][1] == 'pawn':
            check = True
            print(i - 1, j + 1)
    elif colour == "white" and i < 8:
        if j > 1 and board[i+1][j-1] != 'E' and board[i+1][j-1][0] == 'black' and board[i+1][j-1][1] == 'pawn':
            check = True
            print(i + 1, j - 1)
        if j < 8 and board[i+1][j+1] != 'E' and board[i+1][j+1][0] == 'black' and board[i+1][j+1][1] == 'pawn':
            check = True
            print(i + 1, j + 1)

    # checks diagonally

    ii = i + 1
    jj = j + 1
    while jj <= 8 and ii <= 8:
        if board[ii][jj] == 'E':
            ii += 1
            jj += 1
        elif board[ii][jj][0] == colour:
            break
        elif board[ii][jj][1] in ['king', 'rook', 'knight',  'pawn']:
            break
        else:
            print(ii, jj)
            check = True
            break
    ii = i - 1
    jj = j - 1
    while jj >= 1 and ii >= 1:
        if board[ii][jj] == 'E':
            ii -= 1
            jj -= 1
        elif board[ii][jj][0] == colour:
            break
        elif board[ii][jj][1] in ['king', 'rook', 'knight', 'pawn']:
            break
        else:
            print(ii, jj)
            check = True
            break
    ii = i + 1
    jj = j - 1
    while jj <= 8 and ii >= 1:
        if board[ii][jj] == 'E':
            ii += 1
            jj -= 1
        elif board[ii][jj][0] == colour:
            break
        elif board[ii][jj][1] in ['king', 'rook', 'knight', 'pawn']:
            break
        else:
            print(ii, jj)
            check = True
            break
    ii = i - 1
    jj = j + 1
    while jj <= 8 and ii >= 1:
        if board[ii][jj] == 'E':
            ii -= 1
            jj += 1
        elif board[ii][jj][0] == colour:
            break
        elif board[ii][jj][1] in ['king', 'rook', 'knight', 'pawn']:
            break
        else:
            print(ii, jj)
            check = True
            break

    # checks knights

    options = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
    for move in options:
        ii = i + move[0]
        jj = j + move[1]
        if (1 <= ii <= 8) and (1 <= jj <= 8):
            if board[ii][jj] != 'E' and board[ii][jj][0] != colour and board[ii][jj][1] == 'knight':
                check = True
                print(ii, jj)
    print(blocking_squares)
    return check


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


def find_rook_moves(colour, board, i, j):
    valid_moves = []
    # move left
    jj = j - 1
    while jj >= 1:
        if board[i][jj] == 'E':
            move = board[0][j] + str(i) + board[0][jj] + str(i)
            valid_moves.append(move)
        elif board[i][jj][0] == colour:
            break
        else:
            move = board[0][j] + str(i) + board[0][jj] + str(i)
            valid_moves.append(move)
            break
        jj -= 1

    jj = j + 1
    while jj <= 8:
        if board[i][jj] == 'E':
            move = board[0][j] + str(i) + board[0][jj] + str(i)
            valid_moves.append(move)
        elif board[i][jj][0] == colour:
            break
        else:
            move = board[0][j] + str(i) + board[0][jj] + str(i)
            valid_moves.append(move)
            break
        jj += 1

    ii = i - 1
    while ii >= 0:
        if board[ii][j] == 'E':
            move = board[0][j] + str(i) + board[0][j] + str(ii)
            valid_moves.append(move)
        elif board[ii][j][0] == colour:
            break
        else:
            move = board[0][j] + str(i) + board[0][j] + str(ii)
            valid_moves.append(move)
            break
        ii -= 1

    ii = i + 1
    while ii <= 8:
        if board[ii][j] == 'E':
            move = board[0][j] + str(i) + board[0][j] + str(ii)
            valid_moves.append(move)
        elif board[ii][j][0] == colour:
            break
        else:
            move = board[0][j] + str(i) + board[0][j] + str(ii)
            valid_moves.append(move)
            break
        ii += 1

    return valid_moves


def find_bishop_moves(colour, board, i, j):
    valid_moves = []
    jj = j - 1
    ii = i - 1
    while jj >= 1 and ii >= 1:
        if board[ii][jj] == 'E':
            move = board[0][j] + str(i) + board[0][jj] + str(ii)
            valid_moves.append(move)
        elif board[ii][jj][0] == colour:
            break
        else:
            move = board[0][j] + str(i) + board[0][jj] + str(ii)
            valid_moves.append(move)
            break
        jj -= 1
        ii -= 1

    jj = j - 1
    ii = i + 1
    while jj >= 1 and ii <= 8:
        if board[ii][jj] == 'E':
            move = board[0][j] + str(i) + board[0][jj] + str(ii)
            valid_moves.append(move)
        elif board[ii][jj][0] == colour:
            break
        else:
            move = board[0][j] + str(i) + board[0][jj] + str(ii)
            valid_moves.append(move)
            break
        jj -= 1
        ii += 1

    jj = j + 1
    ii = i - 1
    while jj <= 8 and ii >= 1:
        if board[ii][jj] == 'E':
            move = board[0][j] + str(i) + board[0][jj] + str(ii)
            valid_moves.append(move)
        elif board[ii][jj][0] == colour:
            break
        else:
            move = board[0][j] + str(i) + board[0][jj] + str(ii)
            valid_moves.append(move)
            break
        jj += 1
        ii -= 1

    jj = j + 1
    ii = i + 1
    while jj <= 8 and ii <= 8:
        if board[ii][jj] == 'E':
            move = board[0][j] + str(i) + board[0][jj] + str(ii)
            valid_moves.append(move)
        elif board[ii][jj][0] == colour:
            break
        else:
            move = board[0][j] + str(i) + board[0][jj] + str(ii)
            valid_moves.append(move)
            break
        jj += 1
        ii += 1

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


def find_king_moves(colour, board, i, j):
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


def set_up_board():
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

    return board


def main():
    game = ChessBot()
    game.make_move('e8f5')
    game.make_move('b1e3')
    # game.make_move('c8d4')
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
    #
    #         move = random.randint(0, len(moves) - 1)
    #         print(moves[move])
    #         game.make_move(moves[move])


if __name__ == "__main__":
    main()
