X = 0
Y = 1
directions = ((-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1))


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

    def possible_to_put_stone(self, _turn):
        _possible = False
        for x in range(1, 9):
            for y in range(1, 9):
                if self.possible_to_put_stone_at(_turn, (x, y)):
                    _possible = True
                    break
        return _possible

    def possible_to_put_stone_at(self, _turn, _pos):
        _possible = False
        if self._get_at(_pos) == Board.BLANK:
            for _dir in directions:
                if 0 < self._count_reversible_stones_in_direction(_turn, _pos, _dir):
                    _possible = True
                    break
        return _possible

    def count_reversible_stones(self, _turn, _pos):
        _reverse_num = 0
        for _dir in directions:
            _reverse_num += self._count_reversible_stones_in_direction(_turn, _pos, _dir)
        return _reverse_num

    def reverse_stones_from(self, _pos):
        _turn = self.board[_pos[X]][_pos[Y]]
        if _turn in (Stone.BLACK, Stone.WHITE):
            for _dir in directions:
                _last_pos = self._find_last_pos_in_direction(_turn, _pos, _dir)
                if _last_pos is not None:
                    self._reverse_stones_in_direction(_turn, _last_pos, (-_dir[X], -_dir[Y]))

    def put_stone_at(self, _turn, _pos):
        _success = False
        if self._get_at(_pos) == Board.BLANK:
            self._set_stone_at(_turn, _pos)
            _success = True
        return _success

    def _get_at(self, _pos):
        return self.board[_pos[X]][_pos[Y]]

    def _set_stone_at(self, _turn, _pos):
        self.board[_pos[X]][_pos[Y]] = _turn

    def _step(self, _pos, _dir):
        return (_pos[X] + _dir[X], _pos[Y] + _dir[Y])

    def _count_reversible_stones_in_direction(self, _turn, _pos, _dir):
        _opponent_turn = Stone.reverse(_turn)
        _reverse_num = 0
        _cur_pos = self._step(_pos, _dir)
        while self._get_at(_cur_pos) == _opponent_turn:
            _cur_pos = self._step(_cur_pos, _dir)
            _reverse_num += 1
        if self._get_at(_cur_pos) != _turn:
            _reverse_num = 0
        return _reverse_num

    def _find_last_pos_in_direction(self, _turn, _pos, _dir):
        _opponent_turn = Stone.reverse(_turn)
        _cur_pos = self._step(_pos, _dir)
        while self._get_at(_cur_pos) == _opponent_turn:
            _cur_pos = self._step(_cur_pos, _dir)
        if self._get_at(_cur_pos) != _turn:
            _cur_pos = None
        return _cur_pos

    def _reverse_stones_in_direction(self, _turn, _pos, _dir):
        _opponent_turn = Stone.reverse(_turn)
        _cur_pos = self._step(_pos, _dir)
        while self._get_at(_cur_pos) == _opponent_turn:
            self._set_stone_at(_turn, _cur_pos)
            _cur_pos = self._step(_cur_pos, _dir)

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

    b.put_stone_at(Stone.BLACK, (5, 3))
    b.reverse_stones_from((5, 3))
    print(b)
