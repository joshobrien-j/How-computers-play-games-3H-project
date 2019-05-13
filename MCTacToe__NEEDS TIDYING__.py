# -*- coding: utf-8 -*-
"""
Created on Sun Jan 27 21:03:42 2019

@author: nvtz34
"""

import random
import numpy as np
import matplotlib.pyplot as plt
import ProjectFunctions as pf

#Random integer (remove int for float) number between 1 and n
def rand(n):
    a = random.random()
    r = 0
    m = 0.0
    while r==0:
        if m/n < a <= (m+1)/n:
            r = m + 1
            return int(r)
        else:
            m = m + 1
            

#MONTE CARLO
##do similar to afterstates programme
##DIFFERENCE: will need to hold states per game before updating

##write similar bestmove,mymove, his move anfd game funtion
#can use existing checkstate and is_game_finished funtions

##function will be very similar but trying to use sets instead of lists
'''problem with this function'''
def trin(grid):
#    print grid
    x = 0
    for i in range(3):
        for j in range(3):
            if grid[i][j] == -1:
                k = 2
            elif grid[i][j] == 1:
                k = 1
            else:
                k = 0
            x = x + (k)*(3**(8-3*i-j))
#    print grid, x
    return x

def bestmovemc(grid, expset, explist, expvals, eps):
    # this function evaluates the value of each possible action from a
    # state s using the MC -prediction method and chooses returns the 
    # possible next-state s' with the maximum value. We input the current
    # state, the set of states experienced (we can check quickly if the
    #  state is in the set before we search the list), a list of 
    # experienced states, their respective values, and our epsilon.
    possgrids = []
    possvals = []
    for i in range(3):  # we append each possible nect-state to list based
                        # on which grid-entried are empty
        for j in range(3):
            if grid[i][j] == 0:
                grid1 = grid.copy()
                grid1[i][j] = 1
                possgrids.append(grid1)
    for i in range(len(possgrids)):
        x = possgrids[i]
        x1 = pf.trin(x) # we store grid as number counted in base 3 to  
                        # store in set
        if x1 in expset:    # we search set of experienced states. This
                            # is a lot quicker than searching for grid in 
                            # list so searching set before list imporves
                            # efficiency
            tf = np.ndarray.tolist(explist == x)
            n = tf.index([[True, True, True],[True, True, True],
                          [True, True, True]])
            possvals.append(expvals[n]) # we extract state-value if we've 
                                        # expericned the state before
        else:
            possvals.append(0.5)    # if not we set it arbitrarily
    maxval = max(possvals)  # maximise over this value
    count = possvals.count(maxval)
    u = np.random.uniform()
    loc = []
    if u < eps or count == len(possvals): # implement epsilon-greediness;
        for i in range(len(possvals)):  # as we are exploiting, we find
                                        # the next-states which maximise 
                                        # the state-value
            if possvals[i] == maxval:
                loc.append(i)
        k = rand(count) - 1     # we choose from these maximum grid
                                # randomly (if there is more than one)
        n = loc[k]
    else:   # if we are exploring we choose randomly from the grids which
            # have value which is not equal to the maximum
        for i in range(len(possvals)):
            if possvals[i] != maxval:
                loc.append(i)
        k = rand(len(possvals) - count) - 1
        n = loc[k]
    nxtgrd = possgrids[n]
    return nxtgrd # we return the grid after we have made the 'best' move 
                  # by MC -prediction  


def mymovemc(board, expset, explist, expvals, eps):
    intgrid = board.copy()
    board = bestmovemc(board, expset, explist, expvals, eps)
    return intgrid, board

def checkstate(board):
    sums = []
#    print board, 'checkstates board'
    for i in range(3):
        sums.append(board[:,i].sum()) 
        sums.append((board[i,:].sum()))
        sums.append((board[i,i].sum()))
        sums.append((board[0,2] + board[1,1] + board[2,0]))
    if max(sums) == 3:
        return 1
    elif min(sums) == -3:
        return -1      #NOTE: changed so losses = -1
    elif 0 not in board:
        return 0
    else:
        return 0.5   ##set intermediate states to 0.5 initially
        
def is_game_finished(board):
    if checkstate(board) == 0.5:
        return False
    else:
        return True
    
def hismovetdtactoe(board, expset, explist, expvals, eps):  ##does this need so many inputs
    intgrid = board.copy()
    board = randmove2(-1, board, explist, expvals, eps)
    return intgrid, board
    
def randmove2(x, board, exp, expvals, eps):
    free = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                free.append([i,j])
    k = rand(len(free))-1
    i = free[k][0]
    j = free[k][1]
    newboard = board.copy()
    newboard[i][j] = x
    return newboard

#check for multiple items in list at once, and return locations      
def arraycheck2(a, b): #where a is list of elements
    if len(b)>0:
        elindex = np.zeros(len(a))
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
    


def gamemctactoe(p1, p2, alpha, eps, expset, explist, expgames):
    expvals = []
    for i in range(len(expgames)):
        expvals.append(np.mean(expgames[i]))
    newgamestates = []
    expgamestates = []
    board = np.zeros((3, 3))
    move = 0
    while is_game_finished(board) == False:
        move = move + 1
#        print move
        x1 = trin(board)
#        for i in range(3):
#            for j in range(3):
#              x1 = x1 + board[i][j]**(9-3*i-j)  
        if x1 in expset:
            expgamestates.append(board)
        else:
            newgamestates.append(board)        
        player = (-1)**(move)
        if player == -1:
            onemove = p2(board, expset, explist, expvals, eps)
        else:
            onemove = p1(board, expset, explist, expvals, eps)
#        print onemove , 'onemove', player
        board = onemove[1]
#        print board
    result = checkstate(board)
    for i in range(len(newgamestates)):
        expset.add(trin(newgamestates[i]))
#        print expset
        explist.append(newgamestates[i])
        expgames.append([result])
    expindex = arraycheck2(expgamestates, explist)[0]
#    print (expindex)
    if len(expindex) > 0:
        for i in range(len(expindex)):
#            print (len(expindex), 'here')
            expgames[int(expindex[i])].append(result)
    return result, expset, explist, expgames
    
#print (gamemctactoe(mymovemc, hismovetdtactoe, 1, 0.9, set(), [], []))

##must be writtem after function to play game
#def rolloutbstmve(grid, p2, expset, explist, expvals, eps):
#    prob
    
        
                    
def nrunnermc(n, p1, p2, alpha, eps, expset, explist, expgames):
    win25 = 0
    loss25 = 0
    learnwin = []
    learnloss = []
    testwin = []
    testloss = []
    for i in range(n):
        result, expset, explist, expgames = gamemctactoe(p1, p2, alpha, eps, expset, explist, expgames)
        if result == 1:
            win25 = win25 + 1
        if result == -1:
            loss25 = loss25 + 1
        if (i+1)%50 == 0:
            print (i)
            if i < n - 2500:
                learnwin.append(win25/50.0)
                learnloss.append(loss25/50.0)
            else:
                testwin.append(win25/50.0)
                testloss.append(loss25/50.0)
            win25, loss25 = 0, 0
        if i == n-2501:
            eps = 1
    return learnwin, learnloss, testwin, testloss
    
#plot1y1, plot2y1, plot1y2, plot2y2 = (nrunnermc(7500, mymovemc, hismovetdtactoe, 1, 0.75, set(), [], []))
##
#print (plot1y1)
#print (plot1y2)
#print (plot2y1)
#print (plot2y2)
#
#plot1y1 = [0.3, 0.14, 0.34, 0.24, 0.3, 0.38, 0.34, 0.2, 0.34, 0.2, 0.54, 0.48, 0.18, 0.28, 0.26, 0.34, 0.36, 0.4, 0.42, 0.32, 0.24, 0.38, 0.28, 0.3, 0.3, 0.3, 0.42, 0.4, 0.38, 0.3, 0.38, 0.46, 0.34, 0.44, 0.54, 0.38, 0.44, 0.36, 0.34, 0.46, 0.44, 0.42, 0.5, 0.3, 0.54, 0.46, 0.58, 0.44, 0.34, 0.52, 0.42, 0.38, 0.36, 0.48, 0.5, 0.5, 0.52, 0.72, 0.54, 0.44, 0.42, 0.44, 0.4, 0.32, 0.54, 0.48, 0.38, 0.42, 0.6, 0.48, 0.5, 0.46, 0.52, 0.5, 0.4, 0.6, 0.5, 0.48, 0.54, 0.44, 0.56, 0.46, 0.54, 0.4, 0.6, 0.62, 0.54, 0.46, 0.4, 0.54, 0.52, 0.58, 0.64, 0.48, 0.6, 0.6, 0.56, 0.5, 0.58, 0.52]
#plot1y2 = [0.84, 0.76, 0.8, 0.84, 0.8, 0.78, 0.68, 0.78, 0.8, 0.74, 0.66, 0.7, 0.82, 0.8, 0.76, 0.78, 0.8, 0.84, 0.7, 0.7]
#plot2y1 = [0.52, 0.56, 0.48, 0.56, 0.56, 0.4, 0.52, 0.5, 0.56, 0.52, 0.28, 0.32, 0.54, 0.38, 0.56, 0.42, 0.36, 0.34, 0.38, 0.46, 0.54, 0.46, 0.48, 0.4, 0.32, 0.46, 0.34, 0.36, 0.38, 0.36, 0.34, 0.4, 0.44, 0.32, 0.28, 0.36, 0.36, 0.4, 0.36, 0.34, 0.18, 0.3, 0.3, 0.48, 0.24, 0.32, 0.18, 0.28, 0.28, 0.22, 0.3, 0.34, 0.48, 0.26, 0.34, 0.14, 0.28, 0.12, 0.24, 0.4, 0.32, 0.26, 0.36, 0.44, 0.22, 0.24, 0.28, 0.34, 0.28, 0.22, 0.22, 0.28, 0.28, 0.32, 0.28, 0.22, 0.18, 0.2, 0.24, 0.32, 0.2, 0.24, 0.2, 0.3, 0.2, 0.18, 0.24, 0.18, 0.34, 0.16, 0.18, 0.12, 0.2, 0.26, 0.26, 0.32, 0.22, 0.22, 0.16, 0.18]
#plot2y2 = [0.08, 0.04, 0.04, 0.02, 0.04, 0.06, 0.1, 0.1, 0.06, 0.04, 0.1, 0.02, 0.04, 0.02, 0.04, 0.02, 0.04, 0.02, 0.0, 0.02]
#
plot1y1 = [0.12, 0.42, 0.18, 0.22, 0.3, 0.32, 0.28, 0.3, 0.26, 0.3, 0.36, 0.34, 0.42, 0.24, 0.28, 0.28, 0.24, 0.36, 0.38, 0.46, 0.52, 0.4, 0.48, 0.46, 0.28, 0.4, 0.28, 0.5, 0.34, 0.42, 0.28, 0.5, 0.3, 0.44, 0.42, 0.38, 0.44, 0.5, 0.38, 0.34, 0.5, 0.46, 0.32, 0.36, 0.4, 0.42, 0.52, 0.36, 0.52, 0.5, 0.44, 0.46, 0.46, 0.42, 0.42, 0.56, 0.46, 0.52, 0.48, 0.4, 0.38, 0.46, 0.56, 0.46, 0.48, 0.52, 0.38, 0.48, 0.58, 0.42, 0.54, 0.6, 0.3, 0.6, 0.5, 0.44, 0.62, 0.44, 0.4, 0.44, 0.42, 0.48, 0.52, 0.52, 0.56, 0.6, 0.5, 0.56, 0.56, 0.5, 0.58, 0.46, 0.38, 0.54, 0.5, 0.48, 0.46, 0.46, 0.5, 0.36]
plot1y2 = [0.74, 0.72, 0.78, 0.76, 0.76, 0.7, 0.86, 0.78, 0.76, 0.82, 0.76, 0.82, 0.78, 0.82, 0.76, 0.72, 0.84, 0.84, 0.68, 0.8, 0.86, 0.72, 0.82, 0.74, 0.74, 0.68, 0.72, 0.7, 0.74, 0.76, 0.76, 0.66, 0.72, 0.74, 0.72, 0.76, 0.72, 0.78, 0.74, 0.8, 0.74, 0.76, 0.64, 0.82, 0.68, 0.56, 0.7, 0.76, 0.74, 0.7]
plot2y1 = [0.56, 0.4, 0.56, 0.58, 0.4, 0.46, 0.46, 0.48, 0.5, 0.54, 0.46, 0.5, 0.34, 0.52, 0.54, 0.54, 0.48, 0.36, 0.34, 0.26, 0.32, 0.3, 0.36, 0.32, 0.42, 0.4, 0.38, 0.24, 0.44, 0.44, 0.34, 0.2, 0.34, 0.26, 0.3, 0.28, 0.4, 0.36, 0.26, 0.28, 0.3, 0.3, 0.3, 0.42, 0.36, 0.26, 0.34, 0.32, 0.24, 0.26, 0.34, 0.3, 0.2, 0.32, 0.32, 0.24, 0.24, 0.4, 0.3, 0.36, 0.36, 0.3, 0.24, 0.36, 0.24, 0.3, 0.24, 0.28, 0.22, 0.32, 0.24, 0.2, 0.32, 0.16, 0.28, 0.32, 0.2, 0.36, 0.28, 0.14, 0.34, 0.24, 0.26, 0.3, 0.3, 0.22, 0.28, 0.22, 0.24, 0.34, 0.28, 0.26, 0.32, 0.2, 0.2, 0.22, 0.22, 0.26, 0.26, 0.32]
plot2y2 = [0.06, 0.08, 0.04, 0.06, 0.04, 0.06, 0.04, 0.0, 0.02, 0.06, 0.06, 0.0, 0.06, 0.0, 0.04, 0.06, 0.04, 0.02, 0.06, 0.1, 0.02, 0.04, 0.0, 0.08, 0.1, 0.1, 0.06, 0.06, 0.04, 0.08, 0.08, 0.08, 0.06, 0.04, 0.04, 0.06, 0.0, 0.0, 0.02, 0.02, 0.04, 0.08, 0.04, 0.04, 0.0, 0.14, 0.06, 0.06, 0.04, 0.0]





plot1y1 = [i*100 for i in plot1y1]
plot1y2 = [i*100 for i in plot1y2]
plot2y1 = [i*100 for i in plot2y1]
plot2y2 = [i*100 for i in plot2y2]


#for overall percentages
overallplot1y1 = [np.mean(plot1y1[:i+1]) for i in range(len(plot1y1))]
overallplot1y2 = [np.mean(plot1y2[:i+1]) for i in range(len(plot1y2))]
overallplot2y1 = [np.mean(plot2y1[:i+1]) for i in range(len(plot2y1))]
overallplot2y2 = [np.mean(plot2y2[:i+1]) for i in range(len(plot2y2))]

axes = plt.gca()
xvals1 =  np.array(range(24, 5000, 50))
#print (xvals1)
xvals2 = np.array(range(5024, 7500, 50))
plt.title('Tic-tac-toe win rate using Monte Carlo prediction')
plt.xlabel('# games played')
plt.ylabel('percentge %')
plt.plot(xvals1, plot1y1, label = '% wins for last 50 learning games')
plt.plot(xvals2, plot1y2, label = '% wins for last 50 test games')
plt.legend()
plt.close()

axes = plt.gca()
xvals1 =  np.array(range(24, 5000, 50))
#print (xvals1)
xvals2 = np.array(range(5024, 7500, 50))
plt.title('Tic-tac-toe win rate using Monte Carlo prediction')
plt.xlabel('# games played')
plt.ylabel('percentge %')
plt.plot(xvals1, overallplot1y1, label = 'overall % wins for learning games')
plt.plot(xvals2, overallplot1y2, label = 'overall % wins for test games')
plt.legend()
plt.close()

axes = plt.gca()
xvals1 =  np.array(range(24, 5000, 50))
#print (xvals1)
xvals2 = np.array(range(5024, 7500, 50))
plt.title('Tic-tac-toe loss rate using Monte Carlo prediction')
plt.xlabel('# games played')
plt.ylabel('percentge %')
plt.plot(xvals1, plot2y1, label = '% wins for last 50 learning games')
plt.plot(xvals2, plot2y2, label = '% wins for last 50 test games')
plt.legend()
plt.close()

axes = plt.gca()
xvals1 =  np.array(range(24, 5000, 50))
#print (xvals1)
xvals2 = np.array(range(5024, 7500, 50))
plt.title('Tic-tac-toe loss rate using Monte Carlo prediction')
plt.xlabel('# games played')
plt.ylabel('percentge %')
plt.plot(xvals1, overallplot2y1, label = 'overall % losses for learning games')
plt.plot(xvals2, overallplot2y2, label = 'overall % losses for test games')
plt.legend()
#plt.close()
