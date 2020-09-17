"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # Check if the input is terminal board
    if terminal(board) == True:
        return "The game is already over"

    # if the input is not terminal state
    else:
        # Keep track of sum of X and O
        sum_X = 0
        sum_O = 0

        # Iterate each cell to calculate the sum of X and O
        for row in board:
            for cell in row:
                if cell == X:
                    sum_X += 1
                if cell == O:
                    sum_O += 1

        # Access different cases in the board game
        # Initial turn
        if sum_X == 0 and sum_O == 0:
            return X
        # O turn
        elif sum_X > sum_O and sum_X != 5 and sum_O != 4:
            return O
        # X turn
        elif sum_X == sum_O and sum_X != 0 and sum_O != 0:
            return X

    raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # Check if the input is terminal board
    if terminal(board) == True:
        return "No more move"

    # if the input is not terminal state
    else:
        # initialize a set of action
        action = set()

        # for each cell in each row, check if it is possible action
        for i, row in enumerate(board):
            for j, cell in enumerate(row):
                if cell != X and cell != O:
                    action.add((i, j))
        # return a set a possible action
        return action
    raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # if action is not valid
    if action not in actions(board):
            raise Exception("Invalid move")

    # if action is valid
    else:
        # make a deepcopy from the current board
        next_board = copy.deepcopy(board)

        # update the board with user action
        next_board[action[0]][action[1]] = player(next_board)

        return next_board
    raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # conditions when X win
    if board[0][0] == board[1][0] == board[2][0] == X \
       or board[0][1] == board[1][1] == board[2][1] == X \
       or board[0][2] == board[1][2] == board[2][2] == X \
       or board[0][0] == board[0][1] == board[0][2] == X \
       or board[1][0] == board[1][1] == board[1][2] == X \
       or board[2][0] == board[2][1] == board[2][2] == X \
       or board[0][0] == board[1][1] == board[2][2] == X \
       or board[2][0] == board[1][1] == board[0][2] == X:
           return X

    # conditions when O win
    elif board[0][0] == board[1][0] == board[2][0] == O \
       or board[0][1] == board[1][1] == board[2][1] == O \
       or board[0][2] == board[1][2] == board[2][2] == O \
       or board[0][0] == board[0][1] == board[0][2] == O \
       or board[1][0] == board[1][1] == board[1][2] == O \
       or board[2][0] == board[2][1] == board[2][2] == O \
       or board[0][0] == board[1][1] == board[2][2] == O \
       or board[2][0] == board[1][1] == board[0][2] == O:
           return O

    # when no one win
    else:
        return None
    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    # keep track of empty cell
    sum_empty = 0

    # count if there is any empty cell
    for row in board:
        for cell in row:
            if cell == EMPTY:
                sum_empty += 1

    # return True if someone win the game
    if winner(board) == X or winner(board) == O:
        return True

    # return True if board is filled
    if sum_empty == 0:
        return True

    # return False if game is ongoing
    else:
        return False

    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    # when terminal board occur
    if terminal(board) == True:
        if winner(board) == X:
            utility = 1
        elif winner(board) == O:
            utility = -1
        else:
            utility = 0
        return utility
    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    # return None if it is terminal board
    if terminal(board) == True:
        return None

    # initialize a value for minimax algorithm
    if player(board) == X:
        v = -math.inf
    elif player(board) == O:
        v = math.inf

    # for every valid action
    for action in actions(board):
        # get a current score
        current_score = getscore(result(board, action), v)

        if player(board) == X:
             current_score = max(v, current_score)

        elif player(board) == O:
             current_score = min(v, current_score)

        if current_score != v:
            v = current_score
            optimal_action = action

    return optimal_action
    raise NotImplementedError

def getscore(board, best_score):
    """
    Returns the next score.
    """

    # return None if it is terminal board
    if terminal(board) == True:
        return utility(board)

    # initialize a value for minimax algorithm
    if player(board) == X:
        v = -math.inf
    elif player(board) == O:
        v = math.inf

    # for every valid action
    for action in actions(board):
        score = getscore(result(board, action), v)

        if player(board) == X:
            if score > best_score:
                return score
            v = max(v, score)

        elif player(board) == O:
            if score < best_score:
                return score
            v = min(v, score)

    return v
    raise NotImplementedError