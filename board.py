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
        self.board = [Board.BLANK] * 10 * 10
        for i in range(10):
            self.set_stone_at(Board.BORDER, (0, i))
            self.set_stone_at(Board.BORDER, (9, i))
            self.set_stone_at(Board.BORDER, (i, 0))
            self.set_stone_at(Board.BORDER, (i, 9))
        self.set_stone_at(Stone.BLACK, (4, 4))
        self.set_stone_at(Stone.BLACK, (5, 5))
        self.set_stone_at(Stone.WHITE, (4, 5))
        self.set_stone_at(Stone.WHITE, (5, 4))

    def get_at(self, _pos):
        _ret = Board.BORDER
        if 1 <= _pos[X] and _pos[X] <= 8 and 1 <= _pos[Y] and _pos[Y] <= 8:
            _ret = self.board[_pos[Y] * 10 + _pos[X]]
        return _ret

    def set_stone_at(self, _stone, _pos):
        if 1 <= _pos[X] and _pos[X] <= 8 and 1 <= _pos[Y] and _pos[Y] <= 8:
            self.board[_pos[Y] * 10 + _pos[X]] = _stone

    def count_stones(self, _stone):
        _count = 0
        for _s in self.board:
            if _s == _stone:
                _count += 1
        return _count

    def copy(self):
        b = Board()
        for idx, v in enumerate(self.board):
            b.board[idx] = v
        return b

    def __str__(self):
        _cols = [" ", "A", "B", "C", "D", "E", "F", "G", "H"]
        _conv = {Board.BORDER: "#", Board.BLANK: ".", Stone.BLACK: "X", Stone.WHITE: "O"}
        _sep = " "
        _s = [[_conv[self.get_at((x, y))] for x in range(1, 9)] for y in range(1, 9)]

        _str = _sep.join(_cols) + "\n"
        for _ln, _l in enumerate(_s):
            _str += str(_ln+1) + _sep + _sep.join(_l) + "\n"
        return _str


if __name__ == "__main__":
    b = Board()
    print(b)
