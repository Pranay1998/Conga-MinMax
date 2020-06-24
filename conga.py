import numpy as np
import random as rand
import math
import copy
import time

EMPTY = 'E'
BLACK = 'B'
WHITE = 'W'

MAX = 10000
MIN = -10000

smart = WHITE 
random = BLACK

gameboard = []
for i in range(4):
    gameboard.append([EMPTY, EMPTY, EMPTY, EMPTY])
stone_numbers = np.zeros((4,4), dtype=int)
gameboard[0][0] = WHITE
stone_numbers[0][0] = 10
gameboard[3][3] = BLACK
stone_numbers[3][3] = 10

num_nodes = 0
num_moves = 0

branching_sum = 0
num_times = 0



def play():
    turn = WHITE #Player who starts first

    global gameboard
    global stone_numbers
    global num_moves

    while(True):
        winner = None
        num_moves += 1

        if turn == smart:
            m = minmax(gameboard, stone_numbers)
            if m[1] is None:
                winner = opposite(turn) 
                break
        
            res = move(gameboard, stone_numbers, m[1])

            gameboard = res[0]
            stone_numbers = res[1]

        elif turn == random:
            m = randomLegalMove(gameboard, turn)
            if m is None:  
                winner = opposite(turn)
                break
            
            res = move(gameboard, stone_numbers, m)
            gameboard = res[0]
            stone_numbers = res[1]


        turn = opposite(turn)

    print(winner + " Wins!")

    print("Total moves " + str(num_moves))
    print("Total nodes explored " + str(num_nodes))
    print("Nodes exmplored per move " + str(num_nodes/num_moves))
    print("Depth = " + str(3))
    print()

    branching_factor = branching_sum/num_times

    print("Avg. branching - ", str(branching_factor))

    print_game_board()


def minmax(board, stones, isMax = True, limit = 3, alpha = MIN , beta = MAX):
    global num_nodes

    num_nodes += 1

    if limit == 0:
        return (evaluate(board, stones), None) #Depth limit reached

    if isMax:
        moves = legalMoves(board, smart if isMax else random)
        if len(moves) == 0:
            return (evaluate(board, stones), None) #Leaf Node
        else:
            bestVal = (MIN, None)
            for m in moves:
                ret = move(board, stones, m)
                value = (minmax(ret[0], ret[1], False, limit-1, alpha, beta))[0]
                if (value > bestVal[0]):
                    bestVal = (value, m)
                alpha = max(alpha, bestVal[0])
                if beta <= alpha:
                    break
            return bestVal
    else:
        moves = legalMoves(board, smart if isMax else random)
        if len(moves) == 0:
            return (evaluate(board, stones), None) #Leaf Node
        else:
            bestVal = (MAX, None)
            for m in moves:
                ret = move(board, stones, m)
                value = (minmax(ret[0], ret[1], True, limit-1, alpha, beta))[0]
                if (value < bestVal[0]):
                    bestVal = (value, m)
                beta = min(alpha, bestVal[0])
                if beta <= alpha:
                    break
            return bestVal

def evaluate2(board, stones):
    smart_positions = 0
    random_positions = 0

    for i in range(4):
        for j in range(4):
            if gameboard[i][j] == smart:
                smart_positions += 1
            else:
                random_positions += 1

    return smart_positions-random_positions


#Works based off of smart and random variables
def evaluate(board, stones):
    return len(legalMoves(board, smart)) - len(legalMoves(board, random))


def randomLegalMove(board, turn):
    moves = legalMoves(board, turn)
    return rand.choice(moves) if len(moves) > 0 else None

#Gets legal moves based on $turn
def legalMoves(board, turn):

    global branching_sum
    global num_times

    directions = [N, E, S, W, NE, NW, SE, SW]
    moves = []
    for i in range(4):
        for j in range(4):
            if board[i][j] == turn:
                for d in directions:
                    m = Move(i, j, d)
                    if isLegalMove(board, m):
                        moves.append(m)
    
    branching_sum += len(moves)
    num_times += 1
    
    return moves
    
def print_game_board():
    for i in range(4):
        for j in range(4):
            if (gameboard[i][j] == EMPTY):
                print(gameboard[i][j], end = '    ')
            else:
                print(gameboard[i][j] + '-' + str(stone_numbers[i][j]), end = '  ')
        print()
    print()

def E(i, j): return (i, j+1)
def W(i, j): return (i, j-1)
def N(i, j): return (i-1, j)
def S(i, j): return (i+1, j)
def SW(i, j): return (i+1, j-1)
def SE(i, j): return (i+1, j+1)
def NW(i, j): return (i-1, j-1)
def NE(i, j): return (i-1, j+1)

def opposite(color):
    return WHITE if (color == BLACK) else BLACK

class Move:
    def __init__(self, i, j, direction):
        self.i = i
        self.j = j
        self.d = direction

def isLegalMove(board, m):
    color = board[m.i][m.j]
    if color == EMPTY: return False
    next_tile = m.d(m.i,m.j)
    return next_tile[0] in range(4) and next_tile[1] in range(4) and board[next_tile[0]][next_tile[1]] != opposite(color)

#Returns a new board after performing move
def move(board, stones, m):
    board = copy.deepcopy(board)
    stones = copy.deepcopy(stones)

    color = gameboard[m.i][m.j]
    value = stones[m.i][m.j]

    next_tile = m.d(m.i,m.j)

    board[m.i][m.j] = EMPTY
    stones[m.i][m.j] = 0

    board[next_tile[0]][next_tile[1]] = color
    stones[next_tile[0]][next_tile[1]] += 1
    value -= 1

    next_next_tile = m.d(next_tile[0], next_tile[1])

    if value != 0 and next_next_tile[0] in range(4) and next_next_tile[1] in range(4) and board[next_next_tile[0]][next_next_tile[1]] != opposite(color):
        board[next_next_tile[0]][next_next_tile[1]] = color
        stones[next_next_tile[0]][next_next_tile[1]] += min(2, value)
        value -= min(2, value)

        next_next_next_tile = m.d(next_next_tile[0], next_next_tile[1])

        if value != 0 and next_next_next_tile[0] in range(4) and next_next_next_tile[1] in range(4) and board[next_next_next_tile[0]][next_next_next_tile[1]] != opposite(color):
            board[next_next_next_tile[0]][next_next_next_tile[1]] = color
            stones[next_next_next_tile[0]][next_next_next_tile[1]] += value
        else:
            stones[next_next_tile[0]][next_next_tile[1]] += value
    else:
        stones[next_tile[0]][next_tile[1]] += value
    
    return (board, stones)


if __name__ == "__main__":
    start = time.time()
    play()
    end = time.time()
    print("Time Elapsed: " + str(end-start))

    