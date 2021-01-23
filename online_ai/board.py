import random
from copy import deepcopy


class Board:
    def __init__(self, board=[[0 for _ in range(4)] for _ in range(4)], score=0):
        self.board = board
        self.rows = len(board)
        self.cols = len(board[0])
        self.score = score
        self.player_move = True

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

        self.player_move = not moved

        if not on_self:
            return False

    def add_tile(self):
        if self.get_empty_cells():
            pos = random.choice(self.get_empty_cells())
            self.rand_tile(pos)
            self.player_move = True

    def rand_tile(self, pos, choices=(2, 4), weights=(.9, .1)):
        val = random.choices(choices, weights, k=1)[0]
        self.board[pos[0]][pos[1]] = val
        return weights[choices.index(val)]

    def possible_moves(self):
        moves = ["left", "right", "up", "down"]
        rem = []
        for move in moves:
            if not self.move(move, False):
                rem.append(move)
        for r in rem:
            moves.remove(r)

        return moves

    def generate_children(self):
        children = []
        if self.player_move:
            for move in self.possible_moves():
                tmp = deepcopy(self)
                tmp.move(move)
                children.append(tmp)
        else:
            for pos in self.get_empty_cells():
                tmp = deepcopy(self)
                prob = tmp.rand_tile(pos)
                children.append((tmp, prob))

        return children

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


def expectiminimax(node: Board, depth):
    if depth == 0 or node.is_full():
        return node.evaluate()

    if node.player_move:
        a = float("inf")
        for child in node.generate_children():
            a = min(a, expectiminimax(child, depth-1))
    else:
        a = 0
        for child, prob in node.generate_children():
            a += prob * expectiminimax(child, depth-1)

    return a
