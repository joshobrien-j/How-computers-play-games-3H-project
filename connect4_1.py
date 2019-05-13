# -*- coding: utf-8 -*-
"""
Created on Sat Apr 27 14:20:36 2019

@author: nvtz34
"""

##connect 4
import numpy as np
import ProjectFunctions as pf

grid = np.zeros((7,6))

def c4_reflect(grid):
    grid1 = np.array([grid[6]])
    for i in range(1,7):
        grid1 = np.append(grid1, [grid[6-i]], axis = 0)
    return grid1


def is_c4_finished(grid):
    finished = False
    result = None
    empty = 0
    
    for i in range(7):
        col_count = 0
        row_count = 0
        diag_count, diag_count1 = 0, 0
        reflection = c4_reflect(grid)
        for j in range(1,6):
#            col_count = 0
            if grid[i][j] == grid[i][j-1] and grid[i][j] != 0:
                col_count = col_count + 1
                if col_count > 2:
                    finished = True
#                    print ('col')
                    result = int(grid[i][j])
                    break
            else:
                col_count = 0
            if i < 6:
                if grid[j][i] == grid[j-1][i] and grid[j][i] != 0:
                    row_count = row_count + 1
                    if row_count > 2:
                        finished = True
    #                    print ('row')
                        result = int(grid[j][i])
                        break
            else:
                row_count = 0
        
            if i + j < 7:
                if grid[i+j][j] == grid[i+j-1][j -1] and grid[i+j][j] != 0:
                    diag_count = diag_count + 1
                    if diag_count > 2:
                        finished = True
#                        print ('diag1')
#                        print (grid, 'errorcheck')
                        result = int(grid[i+j][j])
                else:
                    diag_count = 0
                    
                if reflection[i+j][j] == reflection[i+j-1][j-1] and reflection[i+j][j]:
                    diag_count1 = diag_count1 + 1
                    if diag_count1 > 2:
                        finished = True
#                        print ('diag2')
                        result = int(reflection[i+j][j])
                else:
                    diag_count1 = 0
                    
                if grid[i][j] == 0:
                    empty = empty + 1
    
    if finished == False and empty == 0:
        finished = True
        result = 0.6
    
    if finished == True:
        if abs(result) == 1:
            result = (1+result)/2.0
    return finished, result
##pretty sure this can be imporoved a lot, dont need so many indicies
    

#grid[1][1] = 1
#grid[1][2] = 1
#grid[1][3] = 1
#grid[1][4] = 1


def update10(seenvals, last10vals, last10index, alpha, gamma):
    v = last10vals[0]
    if v > -1:
        vdash = last10vals[10]
        rewards = np.full(9, 0)
        for i in range(1, 9):
            if int(last10vals[i]) == last10vals[i]:
                rewards[i - 1] = last10vals[i]
        rewards = [(rewards[i - 1])*(gamma)**(i) for i in range(1,10)]  #took out i-1 from power of gamma
        vnew = v + alpha*(np.sum(rewards) + (gamma**10)*vdash - v)
        index  = last10index[0]
        seenvals[index] = vnew
    return seenvals


def checkstate_c4(grid):
    finished, result = is_c4_finished(grid)
    if finished == True:
        return result
    else:
        return 0.5

def td10step(grid, expset, explst, expvals, last10states, last10vals, last10index, alpha, eps, gamma):
    
    can_move = []
    poss_afters = []
    exp_poss_moves = []
    exp_poss_afters = []
    poss_vals = np.zeros(7)
    
    for i in range(7):
        newgrid = grid.copy()
        if grid[i][0] == 0:
#            print ('can make this move', i)
            can_move.append(i)
            for j in range(7):
#                print (j)
                if grid[i][5-j] == 0:
#                    print (j)
                    newgrid[i][5-j] = 1
#                    print (newgrid, 'NEWGRID')
                    poss_afters.append(newgrid)
                    break
#            poss_afters.append(newgrid)
            if tuple(np.asarray(grid).ravel()) in expset:
                exp_poss_moves.append(i)
                exp_poss_afters.append(newgrid)
            else:
                poss_vals[i] = 0.5
#        else:
#            poss_vals[i] = -1
    
    if len(exp_poss_moves) > 0:
        exp_poss_indexes = pf.arraycheck2(exp_poss_afters, explst)[0]
        for i in range(len(exp_poss_indexes)):
            poss_vals[exp_poss_moves[i]] = expvals[exp_poss_indexes[i]]
            
    poss_vals = [poss_vals[i] for i in can_move]
    action = pf.epsgreedy(poss_vals, eps)
    grid = poss_afters[action]
#    print (grid, 'newgrid')
#    vdash = checkstate_c4(grid)
    
#    print (expset, 'ttttt', pf.trin(grid))
    if tuple(np.asarray(grid).ravel()) in expset:
        vdash_index = pf.arraycheck(grid, explst)
        if vdash_index == None:
            print (grid, pf.trin(grid), expset)
        vdash = expvals[vdash_index]
    else:
        vdash = checkstate_c4(grid)
        expset.add(tuple(np.asarray(grid).ravel()))
        explst.append(grid)
        expvals.append(vdash)
        vdash_index = len(expvals) - 1
        
    # now we have moved we update our previoius afterstates
    for i in range(10):
        last10states[i] = last10states[i + 1]
        last10vals[i] = last10vals[i + 1]
        last10index[i] = last10index[i + 1]
    last10states[10] = grid
    last10vals[10] = vdash
    last10index[10] = vdash_index
    expvals = update10(expvals, last10vals, last10index, alpha, gamma)
#    print (last10vals)
    return grid, expset, explst, expvals, last10states, last10vals, last10index
    

def after_learner(result, seenvals, last10vals, last10index, alpha, gamma):
    if last10vals[10] == 0.5:
        for i in range(10):
            last10vals[i] = last10vals[i + 1]
            last10index[i] = last10index[i + 1]
        last10vals[10], last10index[10] = result, 0
    for i in range(9):
        for j in range(10 - i):
            last10vals[j] = last10vals[j + 1]
            last10index[j] = last10index[j + 1]
        last10vals[10 - i], last10index[10] = 0, 0
        seenvals = update10(seenvals, last10vals, last10index,
                            alpha, gamma)  
    return seenvals
        

def c4_game(expset, explst, expvals, alpha, eps, gamma):
    grid = np.zeros((7,6))
    red10vals = np.full(11, -1.0)
    red10states = [np.zeros((7,6))]*11
    red10index = np.zeros(11, dtype = np.int)
    yel10vals = np.full(11, -1.0)
    yel10states = [np.zeros((7,6))]*11
    yel10index = np.zeros(11, dtype = np.int)
    move = 0
    while is_c4_finished(grid)[0] == False:
        move = move + 1
        if (-1)**move == -1:
            grid, expset, explst, expvals, red10states, red10vals, red10index = td10step(grid, expset, explst, expvals, red10states, red10vals, red10index, alpha, eps, gamma)
        else:
            grid, expset, explst, expvals, yel10states, yel10vals, yel10index = td10step(grid, expset, explst, expvals, yel10states, yel10vals, yel10index, alpha, eps, gamma) 
        grid = -grid
    
    if (-1)**move == -1:
        grid = -grid
    result = checkstate_c4(grid)
    expvals = after_learner(result, expvals, red10vals, red10index, alpha, gamma)
    grid = -grid
    if result != 0.6:
        result = 0**result
    expvals = after_learner(result, expvals, yel10vals, yel10index, alpha, gamma)
    return result, expset, explst, expvals, move

c4_game(set(), [], [], 0.5, 0.9, 0.9)



def n_trainer(n, expset, explst, expvals, alpha, epsilon, gamma):
    red50 = 0
    yel50 = 0
    lengths = []
    learnred = []
    learnyel = []
    testred = []
    testyel = []
    for i in range(n):
#        print (i)
        result, expset, explst, expvals, length = c4_game(expset, explst, expvals, alpha, epsilon, gamma)
        if result == 0:
            red50 = red50 + 1
        elif result == 1:
            yel50 = yel50 + 1
        lengths.append(length)
        if (i+1)%50 == 0:
#            print (i, yel50*2,'%', red50*2,'%')
            if i < n - 2500:
                learnred.append(red50/50.0)
                learnyel.append(yel50/50.0)
                red50, yel50 = 0, 0
            else:
                testred.append(red50/50.0)
                testyel.append(yel50/50.0)
            if i == n-2501:
                epsilon = 1
    np.save('expvalsc4', expvals)
    np.save('exlstc4', explst)
    np.save('expsetc4', expset)
    np.save('learnredc4', learnred)
    np.save('learnyelc4', learnyel)
    return learnyel, learnred, lengths    

n_trainer(7500, set(), [], [], 0.5, 0.9, 0.9)