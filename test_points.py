from points import get_points
import numpy as np


def map_to_2d(legal_1d):
    legal = np.zeros(shape=(8,8))
    for i in range(8): 
        legal[i,legal_1d[i]] = 1;
    return legal



def test_valid_board():
    #arrange
    legal_1d = [6, 4, 2, 0, 5, 7, 1, 3]
    valid_board = map_to_2d(legal_1d)

    #act
    result = get_points(valid_board, 8)

    #assert
    assert result== (262144, True, False, {'points': 262144, 'steps': 8})

def test_valid_incomplete_board():
    valid_board = np.zeros(shape=(8,8))
    valid_board[0][0]=1
    valid_board[1][3]=1
    result = get_points(valid_board, 8)
    assert result==(4, False, False, {'points': 4, 'steps':2})    

def test_smaller_board():
    valid_board = np.zeros(shape=(4,4))
    valid_board[0][1]=1
    valid_board[1][3]=1
    valid_board[2][0]=1
    valid_board[3][2]=1
    result=get_points(valid_board,4)
    assert result==(16384, True, False, {'points':16384, 'steps':4})

def test_losing_board():
    losing_board = np.zeros(shape=(4,4))
    losing_board[0][0]=1
    losing_board[1][0]=1
    losing_board[2][0]=1
    losing_board[3][0]=1
    result=get_points(losing_board,4)
    assert result==(8, False, True, {'points':8, 'steps':4})