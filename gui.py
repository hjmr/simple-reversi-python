from os import environ
import sys
import pygame
from pygame.locals import *

import stone
from game import Game
from player import Player
from board import SIZE

WIN_SIZE = (WIN_W, WIN_H) = (600, 600)
CELL_W, CELL_H = (WIN_W / SIZE, WIN_H / SIZE)
STONE_SIZE = (CELL_W / 2) * 0.9

COL_GREEN = (50, 150, 50)
COL_BLACK = (0, 0, 0)
COL_WHITE = (255, 255, 255)

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'


class HumanGUIPlayer(Player):
    def __init__(self, my_stone):
        super().__init__(my_stone)

    def next_move(self, board):
        _done = False
        _pos = None
        while not _done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    _pos = (int(event.pos[0] / CELL_W) + 1, int(event.pos[1] / CELL_H) + 1)
                    _done = True
        return _pos

    def __str__(self):
        return "Human"


class GUIGame(Game):
    def __init__(self, players):
        super().__init__(players)
        pygame.init()
        pygame.display.set_caption("Reversi")
        self.screen = pygame.display.set_mode(WIN_SIZE)

    def show_board(self):
        self.screen.fill(COL_GREEN)
        for x in range(SIZE):
            pygame.draw.line(self.screen, COL_BLACK, (x * CELL_W, 0),  (x * CELL_W, WIN_H))
        for y in range(SIZE):
            pygame.draw.line(self.screen, COL_BLACK, (0, y * CELL_H), (WIN_W, y * CELL_H))
        for x in range(SIZE):
            for y in range(SIZE):
                _s = self.board.get_at((x+1, y+1))
                _center_x = x * CELL_W + CELL_W / 2
                _center_y = y * CELL_H + CELL_H / 2
                if _s == stone.BLACK:
                    pygame.draw.circle(self.screen, COL_BLACK, (_center_x, _center_y), STONE_SIZE)
                elif _s == stone.WHITE:
                    pygame.draw.circle(self.screen, COL_WHITE, (_center_x, _center_y), STONE_SIZE)
        pygame.display.flip()
        _str_stone = {stone.BLACK: "Black", stone.WHITE: "White"}
        print("Turn: {} ({})".format(_str_stone[self.curr_stone], self.players[self.curr_stone]))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()


    def show_pass(self):
        pass

    def show_result(self):
        black_num = self.board.count_stones(stone.BLACK)
        white_num = self.board.count_stones(stone.WHITE)
        win_str = "Draw."
        if black_num < white_num:
            win_str = "White Win."
        else:
            win_str = "Black Win."
        print("{} (Black:{} White:{})".format(win_str, black_num, white_num))
