from concurrent.futures import ThreadPoolExecutor

from board import Board, Stone
from game import Game


def split_list(a_list, num):
    _result = [[] for _ in range(num)]
    for _idx, _v in enumerate(a_list):
        _result[_idx % len(_result)].append(_v)
    return list(filter(None, _result))


def get_positions_to_put_stone(board, stone):
    _positions = []
    for x in range(1, 9):
        for y in range(1, 9):
            if Game.possible_to_put_stone_at(board, stone, (x, y)):
                _positions.append((x, y))
    return _positions


def run_minimax_thread(args):
    _ret = args[0].do_search(args[1], args[2], args[3], args[4])
    return _ret


class Minimax_Threaded:
    def __init__(self, evaluator, my_stone, num_thread=4):
        self.evaluator = evaluator
        self.my_stone = my_stone
        self.num_thread = num_thread
        self.minimax_sub = None

    def search_next_move(self, board, max_level):
        self.minimax_sub = Minimax_Sub(self, self.evaluator, self.my_stone, max_level)
        _pos, _eval = self._minimax(board, self.my_stone, 0)
        return (_pos, _eval, self.minimax_sub.eval_count)

    def _minimax(self, board, stone, level):
        level += 1
        _pos_list = split_list(get_positions_to_put_stone(board, stone), self.num_thread)
        _args = [[self.minimax_sub, board, stone, level, _pl, _n] for _n, _pl in enumerate(_pos_list)]
        with ThreadPoolExecutor(max_workers=self.num_thread) as executor:
            _eval_list = executor.map(run_minimax_thread, _args)
        _eval_pos = max(_eval_list, key=lambda x: x[1])
        return _eval_pos


class Minimax_Sub:
    def __init__(self, parent, evaluator, my_stone, max_level):
        self.parent = parent
        self.evaluator = evaluator
        self.my_stone = my_stone
        self.max_level = max_level
        self.eval_count = 0

    def _minimax(self, board, stone, level):
        level += 1
        _pos_list = get_positions_to_put_stone(board, stone)
        return self.do_search(board, stone, level, _pos_list)

    def do_search(self, board, stone, level, pos_list):
        if 0 < len(pos_list):
            _eval_list = {}
            for _p in pos_list:
                b = board.copy()
                Game.put_stone_at(b, stone, _p)
                Game.reverse_stones_from(b, _p)
                if self.max_level <= level:
                    _eval_list[_p] = self._eval(b)
                else:
                    _eval_list[_p] = self._minimax(b, Stone.reverse(stone), level)[1]
            if stone == self.my_stone:
                _eval_pos = max(_eval_list.items(), key=lambda x: x[1])
            else:
                _eval_pos = min(_eval_list.items(), key=lambda x: x[1])
        else:
            if self.max_level <= level:
                _eval_pos = (None, self._eval(board))
            else:
                _eval_pos = (None, self._minimax(board, Stone.reverse(stone), level)[1])
        return _eval_pos

    def _eval(self, _board):
        self.eval_count += 1
        _eval = self.evaluator.eval(_board, self.my_stone)
        return _eval
