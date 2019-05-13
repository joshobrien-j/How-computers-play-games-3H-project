# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 14:43:43 2019

@author: nvtz34
"""
import numpy as np

#Random integer (remove int for float) number between 1 and n
def rand(n):
    a = np.random.uniform()
    r = 0
    m = 0.0
    while r==0:
        if m/n < a <= (m+1)/n:
            r = m + 1
            return int(r)
        else:
            m = m + 1
            

##Funtion to find location of max val in matrix
def maxmatloc(a):
    MaxVal = 0
    for i in range(len(a)):
        for j in range(len(a[0])):
            if a[i][j] > MaxVal:
                MaxVal = a[i][j]
                i1 = i
                j1 = j
            else:
                i1 = np.random.randint(len(a))
                j1 = np.random.randint(len(a[0]))
    return i1, j1


## Check if a is an element of b
def arraycheck(a, b):
    for i in range(len(b)):
        x = np.array_equal(a, b[i])
        if x == True:
            return i
        

## Fucntion to check any of a list of elements a are in the list b
def arraycheck2(a, b): #where a is list of elements
    if len(b)>0:
        elindex = [0]*len(a)
        tf = np.array([False]*len(a))
        for i in range(len(b)):
            for j in range(len(a)):
                x = np.array_equal(a[j], b[i])
                if x == True:
                    tf[j] = True
                    elindex[j] = i
        return elindex, tf
    else:
        return [], np.array([False]*len(a))


## function to count in base 3 (when you can have white, black or none)
def trin(grid):
#    print grid
    x = 0
    r = len(grid[0])
    for i in range(r):
        for j in range(r):
            k = grid[i][j] + 1

            x = x + (k)*(3**((((r**2)-1)-r*i-j)))
    return x

## function to check state values of tictacotoe (see if game is finsihed)
def checkstate(board):
    sums = []
#    print board, 'checkstates board'
    for i in range(3):
        sums.append(board[:,i].sum())
        sums.append(board[i,:].sum())
        sums.append(board[i,i].sum())
        sums.append(board[0,2] + board[1,1] + board[2,0])
    if max(sums) == 3:
        return 1
    elif min(sums) == -3:
        return 0   #'''NOTE:: changed so loss = -1 not 0'''
    elif 0 not in board:
        return 0.75 #draw
    else:
        return 0.5   ##set intermediate states to 0.5 initially
    
def checkresult(board):
    sums = []
#    print board, 'checkstates board'
    for i in range(3):
        sums.append(board[:,i].sum()) 
        sums.append(board[i,:].sum())
        sums.append(board[i,i].sum())
        sums.append(board[0,2] + board[1,1] + board[2,0])
    if max(sums) == 3:
        return 1
    elif min(sums) == -3:
        return -1   #'''NOTE:: changed so loss = -1 not 0'''
    elif 0 not in board:
        return 0 #draw
    

## check is tictacotoe is finished
def is_game_finished(board):
    zero = False
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                zero = True
    if checkstate(board) == 0.5 and zero == True:
        return False
    else:
        return True
    

## random tictactoe player (makes one move)
def randmove2(x, board):
    free = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                free.append([i,j])
    k = rand(len(free))-1
    i = free[k][0]
    j = free[k][1]
    newboard = board.copy()
#    print newboard
    newboard[i][j] = x
    return newboard


def rand_finisher(x, board):
    free = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                free.append([i,j])
                newboard = board.copy()
                if is_game_finished(newboard) == True:
                    return newboard
    k = rand(len(free))-1
    i = free[k][0]
    j = free[k][1]
    newboard = board.copy()
#    print newboard
    newboard[i][j] = x
    return newboard



### board in square matrix to array [row1, row2, ..., rown]
#def mat_to_array(matrix):
#    l = len(matrix[0])
#    array = np.zeros((l)**2)
#    for i in range(l):
#        for j in range(l):
#            array[i*l+j] = matrix[i][j]
#    return array
#
##array to square matrix
#def array_to_mat(array):
#    l = len(array)**0.5
#    mat = np.zeros((l,l))
#    for i in range(l):
#        for j in range(l):
#            mat[i][j] = array[i*l+j]
#    return mat
#    
### function to swap board perspective (from player to player)
#def swap_player(board):
#    board1 = np.zeros(len(board))
    

# function to choose epsilon greedy action
def epsgreedy(poss_action_vals, eps):
    u = np.random.uniform()
    maxval = np.max(poss_action_vals)
    maxmoves = []
    exploremoves = []
    for i in range(len(poss_action_vals)):
#        print (poss_action_vals, maxval, 'cunt')
        if poss_action_vals[i] == maxval:
             maxmoves.append(i)
        else:
            exploremoves.append(i)
#    print (len(exploremoves), len(maxmoves), 'lengths')
    if u < eps or len(exploremoves) == 0:
        k = rand(len(maxmoves)) - 1
        action = maxmoves[k]
    else:
        k = rand(len(exploremoves)) - 1
        action = exploremoves[k]
    return action
    

def nrunner(game, n, expset, explst, expvals, alpha, eps, gamma):
    win50 = 0
    loss50 = 0
    learnwin = []
    learnloss = []
    testwin = []
    testloss = []
    for i in range(n):
        result, expset, explst, expvals = game(expset, explst, expvals, 
                                               alpha, eps, gamma)
        if result == 1:
            win50 = win50 + 1
        if result == -1:
            loss50 = loss50 + 1
        if (i+1)%50 == 0:
#            print (i, win50*2,'%', loss50,'%')
            if i < n - 2500:
                learnwin.append(win50/50.0)
                learnloss.append(loss50/50.0)
            else:
                testwin.append(win50/50.0)
                testloss.append(loss50/50.0)
            win50, loss50 = 0, 0
        if i == n - 2501:
            eps = 1
    return learnwin, learnloss, testwin, testloss


def afterupdate1(grid, prev, expset, explst, expvals, alpha, eps, gamma):
    vdash = checkstate(grid)

    v, vindex = prev[0], prev[1]
    newv = v + alpha*(gamma*vdash - v)
    expvals[vindex] = newv   
    return grid, expset, explst, expvals
    
    
    