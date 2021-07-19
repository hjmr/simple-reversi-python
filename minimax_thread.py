import random
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

import stone
from board import Board

SMALL_NUMBER = -1000
LARGE_NUMBER = 1000


def split_list(a_list, num):
    _result = [[] for _ in range(num)]
    for _idx, _v in enumerate(a_list):
        _result[_idx % len(_result)].append(_v)
    return list(filter(None, _result))


def get_positions_to_put_stone(a_board, curr_stone):
    _positions = []
    for x in range(1, 9):
        for y in range(1, 9):
            if a_board.possible_to_put_stone_at(curr_stone, (x, y)):
                _positions.append((x, y))
    return _positions


def run_minimax_thread(args):
    _pos, _eval = args[0].do_search(args[1], args[2], args[3], args[4], SMALL_NUMBER, LARGE_NUMBER)
    return (_pos, _eval, args[0].eval_count)


class Minimax_Threaded:
    def __init__(self, evaluator, my_stone, num_thread=4):
        self.evaluator = evaluator
        self.my_stone = my_stone
        self.num_thread = num_thread

    def search_next_move(self, a_board, max_level):
        _pos, _eval, _eval_count = self._minimax(a_board, self.my_stone, 0, max_level)
        return (_pos, _eval, _eval_count)

    def _minimax(self, a_board, curr_stone, level, max_level):
        level += 1
        _pos_list = split_list(get_positions_to_put_stone(a_board, curr_stone), self.num_thread)
        _args = [[Minimax_Sub(self.evaluator, self.my_stone, max_level), a_board, curr_stone, level, _pl]
                 for _pl in _pos_list]

        with ProcessPoolExecutor(max_workers=self.num_thread) as executor:
            _eval_list = executor.map(run_minimax_thread, _args)

        _eval_list = [v for v in _eval_list]
        _eval_count = sum(v[2] for v in _eval_list)
        _max_list = [(v[0], v[1]) for v in _eval_list if v[1] == max(_eval_list, key=lambda x: x[1])[1]]
        _max_p, _max_v = random.choice(_max_list)
        return _max_p, _max_v, _eval_count


class Minimax_Sub:
    def __init__(self, evaluator, my_stone, max_level):
        self.evaluator = evaluator
        self.my_stone = my_stone
        self.max_level = max_level
        self.eval_count = 0

    def _minimax(self, a_board, curr_stone, level, alpha, beta):
        level += 1
        _pos_list = get_positions_to_put_stone(a_board, curr_stone)
        return self.do_search(a_board, curr_stone, level, _pos_list, alpha, beta)

    def do_search(self, a_board, curr_stone, level, pos_list, alpha, beta):
        if 0 < len(pos_list):
            _eval_list = {}
            _alpha = SMALL_NUMBER
            _beta = LARGE_NUMBER
            for _p in pos_list:
                b = a_board.copy()
                b.put_stone_at(curr_stone, _p)
                b.reverse_stones_from(_p)
                if self.max_level <= level:
                    _eval_list[_p] = self._eval(b, curr_stone)
                else:
                    _eval_list[_p] = self._minimax(b, stone.reverse(curr_stone), level, _alpha, _beta)[1]
                # alpha-beta branch cut
                if (curr_stone == self.my_stone and beta < _eval_list[_p]) or \
                   (curr_stone != self.my_stone and _eval_list[_p] < alpha):
                    break
                # update alpha-beta
                _alpha = _eval_list[_p] if _alpha < _eval_list[_p] else _alpha
                _beta = _eval_list[_p] if _eval_list[_p] < _beta else _beta

            if curr_stone == self.my_stone:
                _eval_pos = max(_eval_list.items(), key=lambda x: x[1])
            else:
                _eval_pos = min(_eval_list.items(), key=lambda x: x[1])
        else:
            if self.max_level <= level:
                _eval_pos = (None, self._eval(a_board, curr_stone))
            else:
                _eval_pos = (None, self._minimax(a_board, stone.reverse(curr_stone), level, alpha, beta)[1])
        return _eval_pos

    def _eval(self, _board, _curr_stone):
        self.eval_count += 1
        _eval = self.evaluator.eval(_board, _curr_stone, self.my_stone)
        return _eval
