"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    empty_no = 0
    for row in board:
        for cell in row:
            if cell == EMPTY:
                empty_no += 1

    if empty_no == 9:
        return X

    if empty_no % 2:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    empty_set = set()
    for row in range(3):
        for cell in range(3):
            if board[row][cell] is EMPTY:
                empty_set.add((row, cell))
    return empty_set


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    new_board = deepcopy(board)
    if new_board[action[0]][action[1]] != EMPTY:
        raise ValueError("Move is incorrect")

    new_board[action[0]][action[1]] = player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    winner = {1: X, -1: O}
    return winner.get(utility(board))


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    result = False
    if not actions(board) or utility(board) != 0:
        result = True

    return result


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    p = {"X": 1, "O": -1}
    if v := chekc_row(board):
        return p[v]

    if v := check_col(board):
        return p[v]

    if v := check_x(board):
        return p[v]
    return 0


def check_x(board):
    if (
        board[0][0] == board[1][1] == board[2][2]
        or board[2][0] == board[1][1] == board[0][2]
        and board[0][0] is not None
    ):
        return board[1][1]


def check_col(board):
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] is not None:
            return board[0][i]


def chekc_row(board):
    for a, b, c in board:
        if a == b == c and a is not None:
            return a


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    current_action_max = (-1, -1)
    current_action_min = (-1, -1)

    def max_value(state) -> float:
        nonlocal current_action_max
        if terminal(state):
            return utility(state)
        last_v = -math.inf
        v = -math.inf
        for action in actions(state):
            v = max(v, min_value(result(state, action)))

            if last_v != v:
                last_v = v
                current_action_max = action
        return v

    def min_value(state) -> float:
        nonlocal current_action_min
        if terminal(state):
            return utility(state)
        last_v = math.inf
        v = math.inf
        for action in actions(state):
            v = min(v, max_value(result(state, action)))

            if last_v != v:
                last_v = v
                current_action_min = action
        return v

    if player(board) == O:
        print("Gram", O)
        print(min_value(board), current_action_min)
        return current_action_min
    else:
        print("Gram", X)
        print(max_value(board), current_action_max)
        return current_action_max
