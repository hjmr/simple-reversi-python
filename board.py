import stone

BORDER = 100
BLANK = 101
SIZE = 8


class Board:
    def __init__(self):
        self.pos_table = [[0] * (SIZE + 2) for _ in range(SIZE + 2)]
        for x in range(SIZE + 2):
            for y in range(SIZE + 2):
                self.pos_table[x][y] = y * (SIZE + 2) + x

        self.board = [BORDER] * (SIZE + 2) * (SIZE + 2)
        for x in range(1, SIZE+1):
            for y in range(1, SIZE+1):
                self.set_stone_at(BLANK, (x, y))
        self.set_stone_at(stone.BLACK, (4, 4))
        self.set_stone_at(stone.BLACK, (5, 5))
        self.set_stone_at(stone.WHITE, (4, 5))
        self.set_stone_at(stone.WHITE, (5, 4))

    def get_at(self, pos):
        _ret = BORDER
        if 1 <= pos[0] and pos[0] <= SIZE and 1 <= pos[1] and pos[1] <= SIZE:
            _ret = self.board[self.pos_table[pos[0]][pos[1]]]
        return _ret

    def set_stone_at(self, a_stone, pos):
        if 1 <= pos[0] and pos[0] <= SIZE and 1 <= pos[1] and pos[1] <= SIZE:
            self.board[self.pos_table[pos[0]][pos[1]]] = a_stone

    def is_blank_at(self, pos):
        return bool(self.get_at(pos) == BLANK)

    def count_stones(self, a_stone):
        _count = 0
        for _s in self.board:
            if _s == a_stone:
                _count += 1
        return _count

    def count_blank(self):
        _count = 0
        for _s in self.board:
            if _s == BLANK:
                _count += 1
        return _count

    def copy(self):
        b = Board()
        b.board = self.board.copy()
        return b

    def __str__(self):
        _cols = [" ", "A", "B", "C", "D", "E", "F", "G", "H"]
        _conv = {BORDER: "#", BLANK: ".", stone.BLACK: "X", stone.WHITE: "O"}
        _sep = " "
        _s = [[_conv[self.get_at((x, y))] for x in range(1, SIZE + 1)] for y in range(1, SIZE + 1)]

        _str = _sep.join(_cols[:SIZE+1]) + "\n"
        for _ln, _l in enumerate(_s):
            _str += str(_ln+1) + _sep + _sep.join(_l) + "\n"
        return _str


if __name__ == "__main__":
    b = Board()
    print(b)
