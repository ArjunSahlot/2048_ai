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
