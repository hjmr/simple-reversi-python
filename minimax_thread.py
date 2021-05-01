from concurrent.futures import ThreadPoolExecutor

from board import Board, Stone
from game import Game


def split_list(_list, _num):
    _result = [[] for _ in range(_num)]
    for idx, v in enumerate(_list):
        _result[idx % len(_result)].append(v)
    return list(filter(None, _result))


def get_positions_to_put_stone(_board, _stone):
    _positions = []
    for x in range(1, 9):
        for y in range(1, 9):
            if Game.possible_to_put_stone_at(_board, _stone, (x, y)):
                _positions.append((x, y))
    return _positions


def run_minimax_thread(minimax_sub, _board, _stone, _level, _pos_list):
    return minimax_sub.do_search(_board, _stone, _level, _pos_list)


class Minimax_Thread:
    def __init__(self, _evaluator, _my_stone, _num_thread=3):
        self.evaluator = _evaluator
        self.my_stone = _my_stone
        self.num_thread = _num_thread
        self.minimax_sub = None

    def search_next_move(self, _board, _max_level):
        self.minimax_sub = Minimax_Sub(self, self.evaluator, self.my_stone, _max_level)
        _pos, _eval = self._minimax(_board, self.my_stone, 0)
        return (_pos, _eval, self.minimax_sub.eval_count)

    def _minimax(self, _board, _stone, _level):
        _level += 1
        _pos_list = split_list(get_positions_to_put_stone(_board, _stone), self.num_thread)
        with ThreadPoolExecutor(max_workers=self.num_thread) as executor:
            _future = []
            for _pl in _pos_list:
                _future.append(executor.submit(run_minimax_thread, self.minimax_sub, _board, _stone, _level, _pl))
        _eval_list = [_f.result() for _f in _future]
        _eval_pos = max(_eval_list, key=lambda x: x[1])
        return _eval_pos


class Minimax_Sub:
    def __init__(self, _parent, _evaluator, _my_stone, _max_level):
        self.parent = _parent
        self.evaluator = _evaluator
        self.my_stone = _my_stone
        self.max_level = _max_level
        self.eval_count = 0

    def _minimax(self, _board, _stone, _level):
        _level += 1
        _pos_list = get_positions_to_put_stone(_board, _stone)
        return self.do_search(_board, _stone, _level, _pos_list)

    def do_search(self, _board, _stone, _level, _pos_list):
        if 0 < len(_pos_list):
            _eval_list = {}
            for _p in _pos_list:
                b = _board.copy()
                Game.put_stone_at(b, _stone, _p)
                Game.reverse_stones_from(b, _p)
                if self.max_level <= _level:
                    _eval_list[_p] = self._eval(b)
                else:
                    _eval_list[_p] = self._minimax(b, Stone.reverse(_stone), _level)[1]
            if _stone == self.my_stone:
                _eval_pos = max(_eval_list.items(), key=lambda x: x[1])
            else:
                _eval_pos = min(_eval_list.items(), key=lambda x: x[1])
        else:
            if self.max_level <= _level:
                _eval_pos = (None, self._eval(_board))
            else:
                _eval_pos = (None, self._minimax(_board, Stone.reverse(_stone), _level)[1])
        return _eval_pos

    def _eval(self, _board):
        self.eval_count += 1
        _eval = self.evaluator.eval(_board, self.my_stone)
        return _eval
