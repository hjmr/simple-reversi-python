import stone

BORDER = 100
BLANK = 101
SIZE = 8

directions = ((-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1))


def _move(pos, dire):
    return (pos[0] + dire[0], pos[1] + dire[1])


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
        self.set_stone_at(stone.WHITE, (4, 4))
        self.set_stone_at(stone.WHITE, (5, 5))
        self.set_stone_at(stone.BLACK, (4, 5))
        self.set_stone_at(stone.BLACK, (5, 4))

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

    def possible_to_put_stone(self, a_stone):
        _possible = False
        for x in range(1, 9):
            for y in range(1, 9):
                if self.possible_to_put_stone_at(a_stone, (x, y)):
                    _possible = True
                    break
        return _possible

    def possible_to_put_stone_at(self, a_stone, pos):
        _possible = False
        if self.is_blank_at(pos):
            for _dir in directions:
                if 0 < self._count_reversible_stones_in_direction(a_stone, pos, _dir):
                    _possible = True
                    break
        return _possible

    def count_reversible_stones(self, a_stone, pos):
        _reverse_num = 0
        for _dir in directions:
            _reverse_num += self._count_reversible_stones_in_direction(a_stone, pos, _dir)
        return _reverse_num

    def reverse_stones_from(self, pos):
        _stone = self.get_at(pos)
        if _stone in (stone.BLACK, stone.WHITE):
            for _dir in directions:
                _last_pos = self._find_last_pos_in_direction(_stone, pos, _dir)
                if _last_pos is not None:
                    self._reverse_stones_in_direction(_stone, _last_pos, (-_dir[0], -_dir[1]))

    def put_stone_at(self, a_stone, pos):
        _success = False
        if self.is_blank_at(pos):
            self.set_stone_at(a_stone, pos)
            _success = True
        return _success

    def _count_reversible_stones_in_direction(self, a_stone, pos, dire):
        _opponent_turn = stone.reverse(a_stone)
        _reverse_num = 0
        _cur_pos = _move(pos, dire)
        while self.get_at(_cur_pos) == _opponent_turn:
            _cur_pos = _move(_cur_pos, dire)
            _reverse_num += 1
        if self.get_at(_cur_pos) != a_stone:
            _reverse_num = 0
        return _reverse_num

    def _find_last_pos_in_direction(self, a_stone, pos, dire):
        _opponent_turn = stone.reverse(a_stone)
        _cur_pos = _move(pos, dire)
        while self.get_at(_cur_pos) == _opponent_turn:
            _cur_pos = _move(_cur_pos, dire)
        if self.get_at(_cur_pos) != a_stone:
            _cur_pos = None
        return _cur_pos

    def _reverse_stones_in_direction(self, a_stone, pos, dire):
        _opponent_turn = stone.reverse(a_stone)
        _cur_pos = _move(pos, dire)
        while self.get_at(_cur_pos) == _opponent_turn:
            self.set_stone_at(a_stone, _cur_pos)
            _cur_pos = _move(_cur_pos, dire)

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
