
import math
import random

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, X, EMPTY],
            [EMPTY, X, EMPTY],
            [EMPTY, X, EMPTY]]

board = initial_state()

def player(board):
    """
    Returns player who has the next turn on a board.
    """
    empty_spaces = sum(row.count(EMPTY) for row in board)
    if empty_spaces == 0:
        return "Game Finish"


    else:
        players = [X,O]
        return random.choice(players)

current_player = player(board)

print(current_player)
def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions_set = set()
   

    for i in range(len(board)):
        for j in range(len(board[i])):
            actions_set.add((i,j))
            if isinstance(board[i][j], str):
                actions_set.discard((i,j))
    return actions_set

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    raise NotImplementedError
