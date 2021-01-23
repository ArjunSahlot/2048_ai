import random


class Board:
    def __init__(self, board=[[0 for _ in range(4)] for _ in range(4)], score=0):
        self.board = board
        self.rows = len(board)
        self.cols = len(board[0])
        self.score = score
        self.prev_move = None
        if board == [[0 for _ in range(4)] for _ in range(4)]:
            for _ in range(2):
                self.add_tile()

    def move(self, dir, on_self=True):
        set_line, get_line, line_range = self.set_col, self.get_col, range(self.cols)
        if dir in ("left", "right"):
            set_line, get_line, line_range = self.set_row, self.get_row, range(self.rows)

        moved = False

        for ind in line_range:
            base = get_line(ind)
            line = Board.collapse_line(base, dir)
            collapsed, points = Board.merge_line(line, dir)
            new = Board.collapse_line(collapsed, dir)
            if on_self:
                set_line(ind, new)

            if base != new:
                if not on_self:
                    return True
                moved = True

            self.score += points

        if not on_self and moved:
            self.add_tile()
            self.prev_move = dir

        if not on_self:
            return False

    def add_tile(self, choices=(2, 4), weights=(1, .1)):
        if self.get_empty_cells():
            val = random.choices(choices, weights, k=1)[0]
            pos = random.choice(self.get_empty_cells())
            self.board[pos[0]][pos[1]] = val

    def possible_moves(self):
        moves = ["left", "right", "up", "down"]
        rem = []
        for move in moves:
            if not self.move(move, False):
                rem.append(move)
        for r in rem:
            moves.remove(r)

        return moves

    def get_empty_cells(self):
        return [(row, col) for col in range(self.cols) for row in range(self.cols) if not self.board[row][col]]

    def get_row(self, ind):
        return self.board[ind]

    def get_col(self, ind):
        return [self.board[row][ind] for row in range(self.rows)]

    def set_col(self, ind, line):
        for row in range(self.rows):
            self.board[row][ind] = line[row]

    def set_row(self, ind, line):
        self.board[ind] = line[:]

    def evaluate(self):
        return len(self.get_empty_cells())

    def is_full(self):
        return len(self.possible_moves()) == 0

    @staticmethod
    def merge_line(line, dir):
        inc = -1
        line_range = range(len(line)-1, 0, -1)
        if dir in ("left", "up"):
            inc = 1
            line_range = range(len(line)-1)

        points = 0
        for i in line_range:
            if line[i]:
                if line[i] == line[i+inc]:
                    new_cell = 2 * line[i]
                    line[i] = new_cell
                    line[i+inc] = 0
                    points += new_cell

        return line, points

    @staticmethod
    def collapse_line(line, dir):
        full_line = [cell for cell in line if cell]

        if dir in ("left", "up"):
            return full_line + [0] * (len(line) - len(full_line))

        return [0] * (len(line) - len(full_line)) + full_line

    def __repr__(self):
        string = ""
        for row in self.board:
            for cell in row:
                string += str(cell) + " "

            string = string.strip() + "\n"

        return string.strip()


def get_all_moves(board: Board):
    moves = []
    for move in board.possible_moves():
        b = Board(board.board)
        b.move(move)
        moves.append((b, move))

    return moves


def expectiminimax(board: Board, depth, max_player=True):
    if depth == 0 or board.is_full():
        return board.evaluate(), board.prev_move

    if max_player:
        max_eval = float("-inf")
        best_move = None
        for board_pos, move in get_all_moves(board):
            evaluation = expectiminimax(board_pos, depth-1, False)[0]
            if evaluation > max_eval:
                max_eval = evaluation
                best_move = move
        return max_eval, best_move
    else:
        min_eval = float("inf")
        best_move = None
        for board_pos, move in get_all_moves(board):
            evaluation = expectiminimax(board_pos, depth-1)[0]
            if evaluation < min_eval:
                min_eval = evaluation
                best_move = move

        return min_eval, best_move
