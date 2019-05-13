# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 13:24:24 2019

@author: nvtz34
"""

import numpy as np
import ProjectFunctions as pf


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


def checkstate_c4(grid):
    finished, result = is_c4_finished(grid)
    if finished == True:
        return result
    else:
        return 0.5
    
    

def connect4_tdlam(grid, expset, explst, expvals, alpha, eps, gamma, eligibility_player, eligibility_opponent, elig_player_index, elig_opponent_index, lam):
    
    #make move
    can_move = []
    poss_afters = []
    exp_poss_afters = []
    exp_poss_actions = []
    poss_vals = np.zeros(7)
    for i in range(7):
        newgrid = grid.copy()
        if grid[i][0] == 0:
            can_move.append(i)
            for j in range(6):
                if grid[i][5-j] == 0:
                    newgrid[i][5-j] = 1
                    poss_afters.append(newgrid)
                    break
            if tuple(np.asarray(grid).ravel()) in expset:
                exp_poss_actions.append(i)
                exp_poss_afters.append(newgrid)
            else:
                poss_vals[i] = 0.5
                    
    if len(exp_poss_actions) > 0:
        exp_poss_indexes = pf.arraycheck2(exp_poss_afters, explst)[0]
        for i in range(len(exp_poss_indexes)):
            poss_vals[exp_poss_actions[i]] = expvals[exp_poss_indexes[i]]
            
    poss_vals = [poss_vals[i] for i in can_move]
    action = pf.epsgreedy(poss_vals, eps)
    grid = poss_afters[action]
    
    #eligibilities decay
#    print (6eligibility_player, lam*gamma)
    eligibility_player = [lam*gamma*i for i in eligibility_player]
    
    if tuple(np.asarray(grid).ravel()) in expset:
        vdash_index = pf.arraycheck(grid, explst)
        vdash = expvals[vdash_index]
    else:
        vdash = checkstate_c4(grid)
#        print (vdash, is_c4_finished(grid))
        expset.add(tuple(np.asarray(grid).ravel()))
        explst.append(grid)
        expvals.append(vdash)
        vdash_index = len(expvals) - 1
    eligibility_player.append(1.0)
    elig_player_index.append(vdash_index)
    elig_opponent_index.append(vdash_index)
    eligibility_opponent.append(0.0)
#    print (vdash, 'vdash')
#    print(len(eligibility_player), len(expvals), 'the lengths')
    
    for i in range(len(eligibility_player)-1):
        k = elig_player_index[i]
        newv = expvals[k] + alpha*(gamma*vdash - expvals[k])*eligibility_player[i]  ##require elig_index
        expvals[k] = newv
    for i in range(vdash_index+1, len(eligibility_player)):
        newv = expvals[i] + alpha*(gamma*vdash - expvals[i])*eligibility_player[i]
        expvals[i] = newv        
    return grid, expset, explst, expvals, eligibility_player, eligibility_opponent



def afterupdate_lam(grid, expset, explst, expvals, alpha, eps, gamma, eligibility, lam):
    vdash = checkstate_c4(grid)
    if tuple(np.asarray(grid).ravel()) in expset:
        vindex = pf.arraycheck(grid, explst)
        eligibility[vindex] = vdash
    
    # eligibility decay
    eligibility = [gamma*lam*i for i in eligibility]
    
    for i in range(len(eligibility)):
        newv = expvals[i] + alpha*(gamma*vdash - expvals[i])*eligibility[i]
        expvals[i] = newv
    return grid, expset, explst, expvals

def c4_game_tdlam(expset, explst, expvals, alpha, eps, gamma, lam):
    eligibility1, eligibility2 = [], []
    elig_index1, elig_index2 = [], []
    grid = np.zeros((7,6))
    move = 0
    while is_c4_finished(grid)[0] == False:
#        print (move, 'move')
        move = move + 1
        if (-1)**move == -1:
            grid, expset, explst, expvals, eligibility1, eligibility2 = connect4_tdlam(grid, expset, explst, expvals, alpha, eps, gamma, eligibility1, eligibility2, elig_index1, elig_index2, lam)
        else:
            grid, expset, explst, expvals, eligibility2, eligibility1 = connect4_tdlam(grid, expset, explst, expvals, alpha, eps, gamma, eligibility2, eligibility1, elig_index2, elig_index1, lam)
        grid = -grid
    
#    print (eligibility1, eligibility2, len(eligibility1))
#    print (expvals, 'expvals', len(expvals))
#    print ('finsished')
    if np.sign((-1)**move) != -1:  # if player 1s move finsihes game
        grid, expset, explst, expvals = afterupdate_lam(grid, expset, explst, expvals, alpha, eps, gamma, eligibility1, lam)
    else:
        grid, expset, explst, expvals = afterupdate_lam(grid, expset, explst, expvals, alpha, eps, gamma, eligibility2, lam)
        grid = -grid
#    print (grid, checkstate_c4(grid))
    return checkstate_c4(grid), expset, explst, expvals, move
    
c4_game_tdlam(set(), [], [], 0.5, 0.9, 0.9, 0.5)

def n_trainer(n, expset, explst, expvals, alpha, epsilon, gamma, lam):
    red50 = 0
    yel50 = 0
    lengths = []
    learnred = []
    learnyel = []
    testred = []
    testyel = []
    for i in range(n):
#        print (i)
        result, expset, explst, expvals, length = c4_game_tdlam(expset, explst, expvals, alpha, epsilon, gamma, lam)
        if result == 0:
            red50 = red50 + 1
        elif result == 1:
            yel50 = yel50 + 1
        lengths.append(length)
        if (i+1)%50 == 0:
            print (i, yel50*2,'%', red50*2,'%')
            if i < n - 2500:
                learnred.append(red50/50.0)
                learnyel.append(yel50/50.0)
                red50, yel50 = 0, 0
            else:
                testred.append(red50/50.0)
                testyel.append(yel50/50.0)
            if i == n-2501:
                epsilon = 1
    np.save('lenghts_elig', lengths)
    np.save('expvalsc4_elig', expvals)
    np.save('exlstc4_elig', explst)
    np.save('expsetc4_elig', expset)
    np.save('learnredc4_elig', learnred)
    np.save('learnyelc4_elig', learnyel)
    return learnyel, learnred, lengths    

n_trainer(7500, set(), [], [], 0.5, 0.9, 0.9, 0.5)    



