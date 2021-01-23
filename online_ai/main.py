import pyautogui
import cv2
import numpy as np
import os
from board import expectiminimax, Board
from pynput.keyboard import Listener
import threading
from random_utils.funcs import crash


resolution = int(input("Resolution of board: "))
input("Move your mouse to top left of game and press enter.")
tl = pyautogui.position()
input("Move your mouse to the bottom right of the game and press enter.")
br = pyautogui.position()

game_rect = (*tl, br[0] - tl[0], br[1] - tl[1])
go = False


def monitor_keys():
    with Listener(on_press=check_key) as l:
        l.join()


def move():
    move = get_best_move(get_board())
    if move is not None:
        pyautogui.press(move)


def check_key(key):
    global go
    if hasattr(key, "char"):
        if key.char == "q":
            crash()
        elif key.char == "n":
            move()
    elif hasattr(key, "_name_"):
        if key._name_ == "enter":
            go = not go
            threading.Thread(target=many_moves).start()


def many_moves():
    while go:
        move()


def get_board():
    tiles = {}
    board = [[0 for _ in range(resolution)] for _ in range(resolution)]
    screen = cv2.cvtColor(np.array(pyautogui.screenshot(region=game_rect)), cv2.COLOR_BGR2GRAY)
    for tile in [0, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]:
        template = cv2.imread(os.path.join(os.path.dirname("__file__"), "tiles", str(tile) + ".png"), cv2.IMREAD_GRAYSCALE)
        res = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
        locations = np.where(res >= .85)[::-1]
        for location in zip(*locations):
            tiles[round(location[1] / 100), round(location[0] / 100)] = tile
    tiles = [v for _, v in sorted(tiles.items())]
    for i, tile in enumerate(tiles):
        try:
            board[i // resolution][i % resolution] = tile
        except IndexError:
            return [[0 for _ in range(resolution)] for _ in range(resolution)]

    return board


def get_best_move(board):
    return expectiminimax(Board(board), 6)[1]


threading.Thread(target=monitor_keys).start()
