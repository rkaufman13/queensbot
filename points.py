import collections
import numpy as np


def get_points(matrix):
    win = False
    points=0
    board = convert_matrix(matrix)
    #base points for the number of queens on the board.
    base_points= (8- abs(8-len(board))) 
    if base_points>0:
        points+=2**base_points
    else:
        points-=2**(base_points*-1)
    #remove points for illegally placed queens
    duplicates_in_y_column = [y for y, value in collections.Counter(board).items() if value >1 and y >0]
    points -= 10*len(duplicates_in_y_column)

    duplicates_in_x_column = []
    for row in matrix:
        dupes= len([x for x in row if x >0])
        if dupes>1:
            duplicates_in_x_column.append(dupes-1)
    points -= 10*len(duplicates_in_x_column)
    for i in range(-6,6):
        illegal_diagonal_moves = np.diagonal(matrix, i)
        illegal_other_diagonal_moves = np.diagonal(np.fliplr(matrix),i)
        
        if collections.Counter(illegal_diagonal_moves).get(1,0)>1:
            points -=10*collections.Counter(illegal_diagonal_moves).get(1,0)
        if collections.Counter(illegal_other_diagonal_moves).get(1,0)>1:
            points -=10*collections.Counter(illegal_diagonal_moves).get(1,0)
    if len(board)==8 and not len(duplicates_in_x_column) and not len(duplicates_in_y_column) and not collections.Counter(illegal_diagonal_moves).get(1,0)>1 and not collections.Counter(illegal_other_diagonal_moves).get(1,0)>1:
        win = True
    return points, win


def convert_matrix(matrix):
    one_dimensional_board = []
    for row in matrix:
        for idx, square in enumerate(row):
            if square == 1:
                one_dimensional_board.append(idx)
    return one_dimensional_board