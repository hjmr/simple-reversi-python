from board import Stone, Board

X = 0
Y = 1
directions = ((-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1))


class Game:
    def __init__(self):
        self.board = Board()

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
        if self.board.get_at(_pos) == Board.BLANK:
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
        _turn = self.board.get_at(_pos)
        if _turn in (Stone.BLACK, Stone.WHITE):
            for _dir in directions:
                _last_pos = self._find_last_pos_in_direction(_turn, _pos, _dir)
                if _last_pos is not None:
                    self._reverse_stones_in_direction(_turn, _last_pos, (-_dir[X], -_dir[Y]))

    def put_stone_at(self, _turn, _pos):
        _success = False
        if self.board.get_at(_pos) == Board.BLANK:
            self.board.set_stone_at(_turn, _pos)
            _success = True
        return _success

    def _move(self, _pos, _dir):
        return (_pos[X] + _dir[X], _pos[Y] + _dir[Y])

    def _count_reversible_stones_in_direction(self, _turn, _pos, _dir):
        _opponent_turn = Stone.reverse(_turn)
        _reverse_num = 0
        _cur_pos = self._move(_pos, _dir)
        while self.board.get_at(_cur_pos) == _opponent_turn:
            _cur_pos = self._move(_cur_pos, _dir)
            _reverse_num += 1
        if self.board.get_at(_cur_pos) != _turn:
            _reverse_num = 0
        return _reverse_num

    def _find_last_pos_in_direction(self, _turn, _pos, _dir):
        _opponent_turn = Stone.reverse(_turn)
        _cur_pos = self._move(_pos, _dir)
        while self.board.get_at(_cur_pos) == _opponent_turn:
            _cur_pos = self._move(_cur_pos, _dir)
        if self.board.get_at(_cur_pos) != _turn:
            _cur_pos = None
        return _cur_pos

    def _reverse_stones_in_direction(self, _turn, _pos, _dir):
        _opponent_turn = Stone.reverse(_turn)
        _cur_pos = self._move(_pos, _dir)
        while self.board.get_at(_cur_pos) == _opponent_turn:
            self.board.set_stone_at(_turn, _cur_pos)
            _cur_pos = self._move(_cur_pos, _dir)

    def __str__(self):
        return str(self.board)
