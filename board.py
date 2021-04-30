X = 0
Y = 1


class Stone:
    BLACK = 1
    WHITE = 2

    @classmethod
    def reverse(cls, _stone):
        _rev_stone = cls.BLACK if _stone == cls.WHITE else cls.WHITE
        return _rev_stone


class Board:
    BORDER = 100
    BLANK = 101

    def __init__(self):
        self.board = [[Board.BLANK] * 10 for i in range(10)]
        for i in range(10):
            self.board[0][i] = self.board[9][i] = self.board[i][0] = self.board[i][9] = Board.BORDER
        self.board[4][4] = self.board[5][5] = Stone.BLACK
        self.board[4][5] = self.board[5][4] = Stone.WHITE

    def get_at(self, _pos):
        _ret = Board.BORDER
        if 1 <= _pos[X] and _pos[X] <= 8 and 1 <= _pos[Y] and _pos[Y] <= 8:
            _ret = self.board[_pos[X]][_pos[Y]]
        return _ret

    def set_stone_at(self, _stone, _pos):
        if 1 <= _pos[X] and _pos[X] <= 8 and 1 <= _pos[Y] and _pos[Y] <= 8:
            self.board[_pos[X]][_pos[Y]] = _stone

    def __str__(self):
        _cols = [" ", "A", "B", "C", "D", "E", "F", "G", "H"]
        _conv = {Board.BORDER: "#", Board.BLANK: ".", Stone.BLACK: "X", Stone.WHITE: "O"}
        _sep = " "
        _s = [[_conv[self.board[x][y]] for x in range(1, 9)] for y in range(1, 9)]

        _str = _sep.join(_cols) + "\n"
        for _ln, _l in enumerate(_s):
            _str += str(_ln+1) + _sep + _sep.join(_l) + "\n"
        return _str


if __name__ == "__main__":
    b = Board()
    print(b)
