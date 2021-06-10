import stone

BORDER = 100
BLANK = 101
SIZE = 8

directions = ((-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1))


cdef (int, int) _move((int, int) pos, (int, int) dire):
    return (pos[0] + dire[0], pos[1] + dire[1])


cdef class Board:
    cdef public list pos_table
    cdef public list board

    def __init__(self):
        cdef int x, y
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

    cpdef int get_at(self, (int, int) pos):
        cdef int _ret = BORDER
        if 1 <= pos[0] and pos[0] <= SIZE and 1 <= pos[1] and pos[1] <= SIZE:
            _ret = self.board[self.pos_table[pos[0]][pos[1]]]
        return _ret

    cpdef set_stone_at(self, int a_stone, (int, int) pos):
        if 1 <= pos[0] and pos[0] <= SIZE and 1 <= pos[1] and pos[1] <= SIZE:
            self.board[self.pos_table[pos[0]][pos[1]]] = a_stone

    cpdef bint is_blank_at(self, (int, int) pos):
        return bool(self.get_at(pos) == BLANK)

    cpdef int count_stones(self, int a_stone):
        cdef int _count = 0
        cdef int _s = 0
        for _s in self.board:
            if _s == a_stone:
                _count += 1
        return _count

    cpdef int count_blank(self):
        cdef int _count = 0
        cdef int _s = 0
        for _s in self.board:
            if _s == BLANK:
                _count += 1
        return _count

    cpdef object copy(self):
        cdef object b = Board()
        b.board = self.board.copy()
        return b

    cpdef bint possible_to_put_stone(self, int a_stone):
        cdef bint _possible = False
        cdef int x, y
        for x in range(1, 9):
            for y in range(1, 9):
                if self.possible_to_put_stone_at(a_stone, (x, y)):
                    _possible = True
                    break
        return _possible

    cpdef bint possible_to_put_stone_at(self, int a_stone, (int, int) pos):
        cdef bint _possible = False
        if self.is_blank_at(pos):
            for _dir in directions:
                if 0 < self._count_reversible_stones_in_direction(a_stone, pos, _dir):
                    _possible = True
                    break
        return _possible

    cpdef int count_reversible_stones(self, int a_stone, (int, int) pos):
        cdef int _reverse_num = 0
        for _dir in directions:
            _reverse_num += self._count_reversible_stones_in_direction(a_stone, pos, _dir)
        return _reverse_num

    cpdef void reverse_stones_from(self, (int, int) pos):
        cdef int _stone = self.get_at(pos)
        cdef (int, int) _last_pos
        if _stone in (stone.BLACK, stone.WHITE):
            for _dir in directions:
                _last_pos = self._find_last_pos_in_direction(_stone, pos, _dir)
                if 0 <= _last_pos[0] and 0 <= _last_pos[1]:
                    self._reverse_stones_in_direction(_stone, _last_pos, (-_dir[0], -_dir[1]))

    cpdef bint put_stone_at(self, int a_stone, (int, int) pos):
        cdef bint _success = False
        if self.is_blank_at(pos):
            self.set_stone_at(a_stone, pos)
            _success = True
        return _success

    cdef int _count_reversible_stones_in_direction(self, int a_stone, (int, int) pos, (int, int) dire):
        cdef int _opponent_turn = stone.reverse(a_stone)
        cdef int _reverse_num = 0
        cdef (int, int) _cur_pos = _move(pos, dire)
        while self.get_at(_cur_pos) == _opponent_turn:
            _cur_pos = _move(_cur_pos, dire)
            _reverse_num += 1
        if self.get_at(_cur_pos) != a_stone:
            _reverse_num = 0
        return _reverse_num

    cdef (int, int) _find_last_pos_in_direction(self, int a_stone, (int, int) pos, (int, int) dire):
        cdef int _opponent_turn = stone.reverse(a_stone)
        cdef (int, int) _cur_pos = _move(pos, dire)
        while self.get_at(_cur_pos) == _opponent_turn:
            _cur_pos = _move(_cur_pos, dire)
        if self.get_at(_cur_pos) != a_stone:
            _cur_pos = (-1, -1)
        return _cur_pos

    cdef void _reverse_stones_in_direction(self, int a_stone, (int, int) pos, (int, int) dire):
        cdef int _opponent_turn = stone.reverse(a_stone)
        cdef (int, int) _cur_pos = _move(pos, dire)
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
