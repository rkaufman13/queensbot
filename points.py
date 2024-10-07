import numpy as np
import collections


def get_points(matrix, length):
    win = False
    lose = False
    board = convert_matrix(matrix)
    points = len(board)
    if len(board)==length:
        if board_is_valid(matrix, length):
            points+=10
            win = True
        else:
            points-=1
            lose = True
    points=2**points
    info = {"points": points, "steps": len(board)}
    return points, win, lose, info


def convert_matrix(matrix):
    one_dimensional_board = []
    for row in matrix:
        for idx, square in enumerate(row):
            if square == 1:
                one_dimensional_board.append(idx)
    return one_dimensional_board

def board_is_valid(matrix, length):
    legal = True
    #x duplicates
    for row in matrix:
        if collections.Counter(row).get(1,0)>1:
            legal =False
            break
    #y duplicates
    for row in np.rot90(matrix):
        if collections.Counter(row).get(1,0)>1:
            legal=False
            break
    #diagonals
    start_of_range = length-2
    end_of_range = start_of_range*-1
    for i in range(end_of_range,start_of_range):
        illegal_diagonal_moves = np.diagonal(matrix, i)
        illegal_other_diagonal_moves = np.diagonal(np.fliplr(matrix),i)
        
        if collections.Counter(illegal_diagonal_moves).get(1,0)>1:
            legal = False
            break
        elif collections.Counter(illegal_other_diagonal_moves).get(1,0)>1:
            legal = False
            break
    return legal