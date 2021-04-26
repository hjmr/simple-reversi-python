from board import Board, Stone

conv_str2int = str.maketrans("abcdefgh", "12345678")
curr_turn = Stone.BLACK

board = Board()

while True:
    print("---------------------------------------")
    print(board)
    if curr_turn == Stone.BLACK:
        print("Turn: Black")
    else:
        print("Turn: White")

    if not board.possible_to_put_stone(curr_turn):
        print("Pass.")
    else:
        done = False
        while not done:
            pos_str = input("Position? ").lower().translate(conv_str2int)
            pos = (int(pos_str[0]), int(pos_str[1]))
            if board.possible_to_put_stone_at(curr_turn, pos):
                board.put_stone_at(curr_turn, pos)
                board.reverse_stones_from(pos)
                done = True

    curr_turn = Stone.reverse(curr_turn)
