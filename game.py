import stone
from board import Board


class Game:
    def __init__(self, players):
        self.players = players
        self.curr_stone = stone.BLACK
        self.board = Board()
        pass

    def show_board(self):
        pass

    def show_pass(self):
        pass

    def show_stat(self):
        pass

    def play(self):
        _pass_num = 0
        while _pass_num < 2:
            self.show_board()

            if not self.board.possible_to_put_stone(self.curr_stone):
                _pass_num += 1
                self.show_pass()
            else:
                _pass_num = 0
                _done = False
                while not _done:
                    _pos = self.players[self.curr_stone].next_move(self.board)
                    if self.board.possible_to_put_stone_at(self.curr_stone, _pos):
                        self.board.put_stone_at(self.curr_stone, _pos)
                        self.board.reverse_stones_from(_pos)
                        _done = True
            self.curr_stone = stone.reverse(self.curr_stone)

        self.show_stat()


class ConsoleGame(Game):
    def show_board(self):
        _str_stone = {stone.BLACK: "Black", stone.WHITE: "White"}
        print("---------------------------------------")
        print(self.board)
        print("Turn: {} ({})".format(_str_stone[self.curr_stone], self.players[self.curr_stone]))

    def show_pass(self):
        print("Pass.")

    def show_stat(self):
        black_num = self.board.count_stones(stone.BLACK)
        white_num = self.board.count_stones(stone.WHITE)
        print("Black:{} White:{}".format(black_num, white_num))
