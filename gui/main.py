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
from constants import *
from game import Board


# Window Management
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048")


def main(window):
    pygame.init()
    clock = pygame.time.Clock()
    board = Board(0, 0, 1000, 1000)

    while True:
        clock.tick(FPS)
        window.fill(WHITE)
        events = pygame.event.get()
        board.update(window, events)
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        pygame.display.update()


main(WINDOW)
