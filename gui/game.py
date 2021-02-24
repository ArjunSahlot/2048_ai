#
#  2048 ai
#  An AI which you could use to win 2048 online. Also offers a gui in which you could play.
#  Copyright Arjun Sahlot 2021
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

import pygame
import random
import numpy as np
from constants import *


class Board:
    padding = 10
    rounding = 5
    num_starting_nums = 5
    possible_starting_nums = (2, 4)
    possiblities_probablities = (1, .1)
    anim_speed = .1
    min_text_height = 10

    colors = {
        0: (238, 228, 218, 89.25),
        2: (238, 228, 218),
        4: (237, 224, 200),
        8: (242, 177, 121),
        16: (245, 149, 99),
        32: (246, 124, 95),
        64: (246, 94, 59),
        128: (237, 207, 114),
        256: (237, 204, 97),
        512: (237, 200, 80),
        1024: (237, 197, 63),
        2048: (237, 194, 46),
        "xlarge": (60, 58, 51),
        "background": (187, 173, 160),
    }

    def __init__(self, x, y, width, height, rows=4, cols=4):
        self.x, self.y, self.width, self.height = x, y, width, height
        self.rows, self.cols = rows, cols
        self.board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.anim_speed *= FPS
        self.curr_step = 0
        self.score = 0
        self.prev = [[(None, None) for _ in range(self.cols)] for _ in range(self.rows)]
        for _ in range(self.num_starting_nums):
            self.add_tile()

    def add_tile(self):
        posibilities = [(row, col) for col in range(self.cols) for row in range(self.rows) if not self.board[row][col]]
        cell = random.choice(posibilities)
        self.board[cell[0]][cell[1]] = random.choices(self.possible_starting_nums, self.possiblities_probablities, k=1)[0]

    def move(self, dir):
        set_line, get_line, line_range = self.set_col, self.get_col, range(self.cols)
        if dir in ("left", "right"):
            set_line, get_line, line_range = self.set_row, self.get_row, range(self.rows)

        moved = False
        for ind in line_range:
            base = get_line(ind)
            line = Board.collapse_line(base, dir)
            collapsed, points = Board.merge_line(line, dir)
            new = Board.collapse_line(collapsed, dir)
            set_line(ind, new)

            if base != new:
                moved = True

            self.score += points

        if moved:
            self.add_tile()

    def get_row(self, ind):
        return self.board[ind]

    def get_col(self, ind):
        return [self.board[row][ind] for row in range(self.rows)]

    def set_col(self, ind, line):
        for row in range(self.rows):
            self.board[row][ind] = line[row]

    def set_row(self, ind, line):
        self.board[ind] = line[:]

    def update(self, window, events):
        self.draw(window)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.move("up")
                if event.key == pygame.K_LEFT:
                    self.move("left")
                if event.key == pygame.K_RIGHT:
                    self.move("right")
                if event.key == pygame.K_DOWN:
                    self.move("down")

    def draw(self, window):
        pygame.draw.rect(window, self.colors["background"], (self.x, self.y, self.width, self.height), border_radius=self.rounding)
        cell_width = (self.width - self.padding * (self.cols + 1)) / self.cols
        cell_height = (self.height - self.padding * (self.rows + 1)) / self.rows
        surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        surf.fill((0, 0, 0, 0))
        for col in range(self.cols):
            for row in range(self.rows):
                x = self.padding + col * (cell_width + self.padding)
                y = self.padding + row * (cell_height + self.padding)
                cell = self.board[row][col]

                if self.curr_step == self.anim_speed:
                    self.curr_step = 0
                    self.prev[row][col] = (None, None)
                else:
                    if self.prev[row][col][0] or self.prev[row][col][1]:
                        d_y = y - (self.padding + self.prev[row][col][0] * (cell_height + self.padding))
                        int_y = d_y / self.anim_speed
                        y -= int_y * (self.anim_speed - self.curr_step)

                        d_x = x - (self.padding + self.prev[row][col][1] * (cell_width + self.padding))
                        int_x = d_x / self.anim_speed
                        x -= int_x * (self.anim_speed - self.curr_step)

                        self.curr_step += 1

                pygame.draw.rect(surf, self.colors[cell] if cell <= 2048 else self.colors["xlarge"], (x, y, cell_width, cell_height), border_radius=self.rounding)
                if cell:
                    size_fact = 3/4 if len(str(cell)) < 4 else 1/2
                    font = pygame.font.SysFont("comicsans", int(max(self.min_text_height, cell_height*size_fact)))
                    text = font.render(str(cell), 1, BLACK if cell <= 4 else WHITE)
                    surf.blit(text, (x + cell_width/2 - text.get_width()/2, y + cell_height/2 - text.get_height()/2))

        window.blit(surf, (self.x, self.y))

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
                string += cell + " "
            string = string.strip() + "\n"

        return string.strip()

    def __len__(self):
        return self.rows * self.cols
