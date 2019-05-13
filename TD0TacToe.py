# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 14:10:00 2019

@author: nvtz34
"""

import numpy as np
import ProjectFunctions as pf
import matplotlib.pyplot as plt

def tdtactoeplayer(prev, grid, expset, explst, expvals, alpha, eps, gamma):
    
    if pf.trin(grid) in expset:
        index = pf.arraycheck(grid, explst)
        vdash = expvals[index]
    else:
        vdash = pf.checkstate(grid)
        expset.add(pf.trin(grid))
        explst.append(grid)
        expvals.append(vdash)
        index = len(expvals) - 1
    newprev = [vdash, index]
                
    count = 0
    for i in range(3):
        for j in range(3):
            if grid[i][j] != 0:
                count = count + 1
    if count > 1:
        v, vindex = prev[0], prev[1]
        newv = v + alpha*(gamma*vdash - v)
        expvals[vindex] = newv            
    
    poss_actions = []
    poss_action_vals = []
    for i in range(3):
        for j in range(3):
            if grid[i][j] == 0:
                grid1 = grid.copy()
                grid1[i][j] = 1
                poss_actions.append(grid1)
                if pf.is_game_finished(grid1) == False:
                    exp_poss_grids = []
                    new_poss_grids = []
                    for r in range(3):
                        for s in range(3):
                            if grid1[r][s] == 0:
                                grid2 = grid1.copy()  
                                grid2[r][s] = -1
                                if pf.trin(grid2) in expset:
                                    exp_poss_grids.append(grid2)
                                else:
                                    new_poss_grids.append(grid2)
                    
                    indexes = []
                    if len(exp_poss_grids) == 0:
                        poss_state_vals1 = []
                    elif len(exp_poss_grids) == 1:
                        indexes = [pf.arraycheck(exp_poss_grids[0],
                                                 explst)]
                    else:
                        indexes = pf.arraycheck2(exp_poss_grids,
                                                 explst)[0]
                    if len(indexes) > 0:
                        poss_state_vals1 = [expvals[i] for i in 
                                            indexes]
                    else:
                        poss_state_vals1 = []
                    poss_state_vals2 = [0.5 for i in 
                                        new_poss_grids]
#                    print (poss_state_vals1, poss_state_vals2, '1and2')
                    poss_state_vals = (poss_state_vals1 + 
                                       poss_state_vals2)
                    action_val = np.mean(poss_state_vals)
                else:
                    action_val = pf.checkstate(grid1)
                poss_action_vals.append(action_val)
    ## choosing action
    u = np.random.uniform()
#    print (poss_action_vals)
    maxval = np.max(poss_action_vals)
#    print (maxval, 'maxval')
    maxmoves = []
    exploremoves = []
    for i in range(len(poss_action_vals)):
        if poss_action_vals[i] == maxval:
             maxmoves.append(i)
        else:
            exploremoves.append(i)
#    print (maxmoves, exploremoves, 'max, explore')
    if u < eps or len(exploremoves) == 0:
        k = pf.rand(len(maxmoves)) - 1
        action = maxmoves[k]
    else:
        k = pf.rand(len(exploremoves)) - 1
        action = exploremoves[k]
#    print (action)
    newgrid = poss_actions[action]
    return newgrid, newprev, expset, explst, expvals
    


#def afterupdate(grid, prev, expset, explst, expvals, alpha, eps, gamma):
#    if pf.trin(grid) in expset:
#        index = pf.arraycheck(grid, explst)
#        vdash = expvals[index]
#    else:
#        vdash = pf.checkstate(grid)
#        expset.add(pf.trin(grid))
#        explst.append(grid)
#        expvals.append(vdash)
#        index = len(expvals) - 1
#        
#    v, vindex = prev[0], prev[1]
#    newv = v + alpha*(gamma*vdash - v)
#    expvals[vindex] = newv   
#    return grid, expset, explst, expvals


def afterupdate1(grid, prev, expset, explst, expvals, alpha, eps, gamma):
    vdash = pf.checkstate(grid)
    
    v, vindex = prev[0], prev[1]
    newv = v + alpha*(gamma*vdash - v)
    expvals[vindex] = newv   
    return grid, expset, explst, expvals
    
    
    


def TDtactoegame(expset, explst, expvals, alpha, eps, gamma):
    grid = np.zeros((3,3))
    prev = np.zeros((3,3))
    move = 0
    while pf.is_game_finished(grid) == False:
        move = move + 1
        if (-1)**move == -1:
            grid = pf.randmove2(-1, grid)
        else:
            grid, prev, expset, explst, expvals = tdtactoeplayer(
                    prev, grid, expset, explst, expvals, alpha, eps, gamma)
    grid, expset, explst, expvals = afterupdate1(grid, prev, expset, explst, expvals, alpha, eps, gamma)
    return pf.checkresult(grid), expset, explst, expvals

print (TDtactoegame(set(), [], [], 0.5, 0.9, 0.9))


def nrunner(game, n, expset, explst, expvals, alpha, eps, gamma):
    win50 = 0
    loss50 = 0
    learnwin = []
    learnloss = []
    testwin = []
    testloss = []
    for i in range(n):
#        print ('NEW GAME')
        result, expset, explst, expvals = game(expset, explst, expvals, 
                                               alpha, eps, gamma)
        if result == 1:
            win50 = win50 + 1
        if result == -1:
            loss50 = loss50 + 1
        if (i+1)%50 == 0:
            print (i, win50*2,'%')
#            print (expvals)
            if i < n - 2500:
                learnwin.append(win50/50.0)
                learnloss.append(loss50/50.0)
            else:
                testwin.append(win50/50.0)
                testloss.append(loss50/50.0)
            win50, loss50 = 0, 0
        if i == n - 2501:
            eps = 1
#    print (expvals)
    return learnwin, learnloss, testwin, testloss



#print (nrunner(TDtactoegame, 7500, set(), [], [], 0.5, 0.9, 1))
    
#    
##([0.6, 0.54, 0.58, 0.6, 0.5, 0.66, 0.7, 0.68, 0.78, 0.76, 0.68, 0.54, 0.74, 0.78, 0.76, 0.72, 0.64, 0.82, 0.74, 0.68, 0.74, 0.76, 0.76, 0.8, 0.76, 0.68, 0.72, 0.68, 0.78, 0.74, 0.74, 0.72, 0.72, 0.76, 0.74, 0.82, 0.88, 0.76, 0.7, 0.68, 0.74, 0.7, 0.78, 0.8, 0.66, 0.72, 0.74, 0.7, 0.76, 0.84, 0.72, 0.7, 0.82, 0.78, 0.8, 0.76, 0.8, 0.7, 0.76, 0.7, 0.66, 0.72, 0.8, 0.84, 0.82, 0.66, 0.76, 0.72, 0.7, 0.76, 0.64, 0.78, 0.76, 0.64, 0.7, 0.68, 0.78, 0.72, 0.76, 0.82, 0.78, 0.66, 0.56, 0.72, 0.7, 0.74, 0.66, 0.74, 0.8, 0.74, 0.78, 0.78, 0.78, 0.76, 0.74, 0.7, 0.64, 0.68, 0.66, 0.66, 0.84, 0.76, 0.78, 0.8, 0.66, 0.7, 0.62, 0.7, 0.68, 0.82, 0.76, 0.68, 0.76, 0.78, 0.64, 0.64, 0.74, 0.76, 0.74, 0.74, 0.76, 0.68, 0.82, 0.7, 0.8, 0.72, 0.8, 0.78, 0.8, 0.74, 0.72, 0.74, 0.7, 0.78, 0.68, 0.78, 0.68, 0.74, 0.74, 0.72], [0.34, 0.24, 0.38, 0.3, 0.38, 0.32, 0.24, 0.26, 0.12, 0.14, 0.26, 0.34, 0.1, 0.22, 0.2, 0.24, 0.34, 0.12, 0.2, 0.22, 0.22, 0.22, 0.18, 0.12, 0.2, 0.24, 0.16, 0.26, 0.16, 0.24, 0.22, 0.18, 0.28, 0.22, 0.2, 0.14, 0.06, 0.14, 0.22, 0.26, 0.22, 0.22, 0.16, 0.14, 0.2, 0.26, 0.16, 0.2, 0.2, 0.16, 0.2, 0.26, 0.12, 0.18, 0.18, 0.22, 0.16, 0.18, 0.18, 0.24, 0.26, 0.24, 0.16, 0.16, 0.14, 0.34, 0.2, 0.22, 0.22, 0.24, 0.28, 0.16, 0.16, 0.22, 0.26, 0.32, 0.2, 0.28, 0.22, 0.16, 0.18, 0.26, 0.32, 0.24, 0.26, 0.24, 0.32, 0.18, 0.14, 0.24, 0.2, 0.16, 0.16, 0.18, 0.22, 0.18, 0.26, 0.26, 0.28, 0.26, 0.16, 0.16, 0.16, 0.16, 0.22, 0.24, 0.3, 0.28, 0.28, 0.16, 0.2, 0.2, 0.22, 0.18, 0.28, 0.3, 0.18, 0.2, 0.16, 0.22, 0.18, 0.3, 0.18, 0.26, 0.16, 0.2, 0.18, 0.18, 0.18, 0.24, 0.18, 0.2, 0.3, 0.2, 0.24, 0.16, 0.24, 0.2, 0.24, 0.2], [0.88, 0.76, 0.8, 0.88, 0.8, 0.74, 0.86, 0.84, 0.86, 0.9], [0.1, 0.24, 0.16, 0.06, 0.16, 0.18, 0.12, 0.12, 0.14, 0.08])
#
#results11 = [0.36, 0.34, 0.22, 0.34, 0.34, 0.32, 0.34, 0.34, 0.24, 0.36, 0.3, 0.32, 0.34, 0.3, 0.3, 0.26, 0.34, 0.26, 0.24, 0.24, 0.28, 0.34, 0.36, 0.28, 0.32, 0.26, 0.36, 0.4, 0.3, 0.44, 0.22, 0.3, 0.22, 0.36, 0.28, 0.4, 0.48, 0.36, 0.3, 0.4, 0.34, 0.36, 0.36, 0.28, 0.32, 0.46, 0.36, 0.32, 0.36, 0.16, 0.24, 0.44, 0.32, 0.34, 0.28, 0.26, 0.34, 0.28, 0.2, 0.42, 0.44, 0.32, 0.38, 0.32, 0.28, 0.4, 0.34, 0.26, 0.4, 0.28, 0.4, 0.36, 0.28, 0.38, 0.3, 0.34, 0.28, 0.38, 0.26, 0.5, 0.42, 0.38, 0.28, 0.28, 0.28, 0.34, 0.26, 0.36, 0.36, 0.34, 0.22, 0.2, 0.16, 0.28, 0.3, 0.3, 0.4, 0.22, 0.12, 0.28, 0.18, 0.3, 0.32, 0.4, 0.34, 0.48, 0.4, 0.4, 0.42, 0.38, 0.24, 0.3, 0.3, 0.34, 0.4, 0.26, 0.38, 0.26, 0.36, 0.26, 0.38, 0.34, 0.32, 0.5, 0.44, 0.42, 0.44, 0.54, 0.46, 0.24, 0.4, 0.34, 0.42, 0.48, 0.28, 0.3, 0.36, 0.34, 0.32, 0.28, 0.38, 0.3, 0.34, 0.22, 0.28, 0.32, 0.22, 0.32, 0.3, 0.3]
#results1 =  [0.64, 0.66, 0.78, 0.66, 0.66, 0.68, 0.66, 0.66, 0.76, 0.64, 0.7, 0.68, 0.66, 0.7, 0.7, 0.74, 0.66, 0.74, 0.76, 0.76, 0.72, 0.66, 0.64, 0.72, 0.68, 0.74, 0.64, 0.6, 0.7, 0.56, 0.78, 0.7, 0.78, 0.64, 0.72, 0.6, 0.52, 0.64, 0.7, 0.6, 0.66, 0.64, 0.64, 0.72, 0.68, 0.54, 0.64, 0.68, 0.64, 0.84, 0.76, 0.56, 0.68, 0.66, 0.72, 0.74, 0.66, 0.72, 0.8, 0.58, 0.56, 0.68, 0.62, 0.68, 0.72, 0.6, 0.66, 0.74, 0.6, 0.72, 0.6, 0.64, 0.72, 0.62, 0.7, 0.66, 0.72, 0.62, 0.74, 0.5, 0.58, 0.62, 0.72, 0.72, 0.72, 0.66, 0.74, 0.64, 0.64, 0.66, 0.78, 0.8, 0.84, 0.72, 0.7, 0.7, 0.6, 0.78, 0.88, 0.72, 0.82, 0.7, 0.68, 0.6, 0.66, 0.52, 0.6, 0.6, 0.58, 0.62, 0.76, 0.7, 0.7, 0.66, 0.6, 0.74, 0.62, 0.74, 0.64, 0.74, 0.62, 0.66, 0.68, 0.5, 0.56, 0.58, 0.56, 0.46, 0.54, 0.76, 0.6, 0.66, 0.58, 0.52, 0.72, 0.7, 0.64, 0.66, 0.68, 0.72, 0.62, 0.7, 0.66, 0.78, 0.72, 0.68, 0.78, 0.68, 0.7, 0.7]
#print (len(results))
                        
                        
                                        
#2nd latest
#([0.44, 0.5, 0.62, 0.58, 0.72, 0.74, 0.72, 0.66, 0.7, 0.62, 0.64, 0.68, 0.68, 0.66, 0.7, 0.7, 0.62, 0.64, 0.7, 0.64, 0.56, 0.72, 0.68, 0.6, 0.56, 0.66, 0.72, 0.68, 0.7, 0.64, 0.7, 0.7, 0.62, 0.82, 0.64, 0.62, 0.74, 0.64, 0.64, 0.68, 0.66, 0.68, 0.8, 0.6, 0.66, 0.76, 0.64, 0.7, 0.64, 0.66, 0.6, 0.66, 0.66, 0.64, 0.64, 0.72, 0.78, 0.62, 0.74, 0.7, 0.7, 0.68, 0.68, 0.64, 0.76, 0.82, 0.68, 0.7, 0.78, 0.8, 0.76, 0.68, 0.86, 0.7, 0.68, 0.78, 0.82, 0.74, 0.76, 0.8, 0.78, 0.78, 0.72, 0.66, 0.58, 0.78, 0.76, 0.8, 0.78, 0.72, 0.76, 0.72, 0.64, 0.84, 0.7, 0.78, 0.76, 0.78, 0.7, 0.8, 0.78, 0.84, 0.6, 0.64, 0.7, 0.74, 0.64, 0.76, 0.68, 0.78, 0.7, 0.74, 0.76, 0.64, 0.86, 0.72, 0.78, 0.82, 0.78, 0.74, 0.82, 0.74, 0.74, 0.74, 0.74, 0.78, 0.74, 0.7, 0.84, 0.72, 0.64, 0.82, 0.9, 0.74, 0.7, 0.68, 0.8, 0.86, 0.74, 0.76], [0.38, 0.38, 0.3, 0.24, 0.22, 0.18, 0.2, 0.28, 0.22, 0.28, 0.28, 0.28, 0.24, 0.3, 0.3, 0.26, 0.3, 0.28, 0.18, 0.28, 0.38, 0.28, 0.22, 0.26, 0.32, 0.32, 0.22, 0.26, 0.26, 0.32, 0.28, 0.18, 0.3, 0.14, 0.28, 0.36, 0.18, 0.32, 0.28, 0.32, 0.28, 0.32, 0.16, 0.34, 0.28, 0.22, 0.32, 0.3, 0.28, 0.3, 0.34, 0.28, 0.22, 0.24, 0.3, 0.18, 0.16, 0.38, 0.22, 0.26, 0.26, 0.32, 0.26, 0.26, 0.2, 0.12, 0.26, 0.2, 0.16, 0.16, 0.18, 0.22, 0.1, 0.28, 0.28, 0.18, 0.16, 0.2, 0.18, 0.14, 0.2, 0.18, 0.2, 0.24, 0.28, 0.14, 0.22, 0.2, 0.16, 0.22, 0.2, 0.24, 0.28, 0.1, 0.26, 0.14, 0.18, 0.2, 0.2, 0.14, 0.18, 0.12, 0.32, 0.28, 0.24, 0.24, 0.32, 0.18, 0.2, 0.16, 0.24, 0.22, 0.22, 0.28, 0.1, 0.26, 0.16, 0.12, 0.2, 0.2, 0.14, 0.22, 0.18, 0.2, 0.18, 0.18, 0.16, 0.14, 0.16, 0.22, 0.24, 0.12, 0.06, 0.24, 0.26, 0.3, 0.16, 0.1, 0.14, 0.2], [0.76, 0.84, 0.82, 0.78, 0.7, 0.7, 0.7, 0.84, 0.86, 0.88], [0.12, 0.12, 0.18, 0.18, 0.26, 0.28, 0.26, 0.12, 0.14, 0.12])

#latest
plot1y1 = [0.46, 0.68, 0.56, 0.76, 0.72, 0.64, 0.78, 0.8, 0.7, 0.76, 0.7, 0.76, 0.76, 0.76, 0.74, 0.72, 0.7, 0.74, 0.7, 0.72, 0.78, 0.76, 0.74, 0.78, 0.8, 0.82, 0.64, 0.8, 0.74, 0.76, 0.8, 0.68, 0.68, 0.76, 0.68, 0.78, 0.68, 0.74, 0.78, 0.76, 0.7, 0.72, 0.78, 0.74, 0.78, 0.84, 0.68, 0.76, 0.8, 0.78, 0.72, 0.7, 0.76, 0.8, 0.7, 0.84, 0.64, 0.82, 0.82, 0.8, 0.92, 0.8, 0.66, 0.78, 0.68, 0.72, 0.7, 0.76, 0.84, 0.72, 0.84, 0.86, 0.76, 0.78, 0.74, 0.84, 0.72, 0.9, 0.66, 0.84, 0.74, 0.72, 0.72, 0.7, 0.72, 0.82, 0.72, 0.78, 0.72, 0.86, 0.68, 0.86, 0.74, 0.82, 0.66, 0.7, 0.74, 0.72, 0.78, 0.58]
plot2y1 = [0.38, 0.22, 0.22, 0.16, 0.22, 0.32, 0.14, 0.16, 0.2, 0.16, 0.2, 0.12, 0.22, 0.14, 0.2, 0.22, 0.2, 0.2, 0.24, 0.16, 0.2, 0.22, 0.24, 0.2, 0.16, 0.14, 0.22, 0.12, 0.2, 0.16, 0.16, 0.22, 0.22, 0.12, 0.2, 0.14, 0.24, 0.18, 0.14, 0.18, 0.24, 0.22, 0.16, 0.18, 0.1, 0.12, 0.18, 0.2, 0.12, 0.18, 0.18, 0.26, 0.1, 0.2, 0.22, 0.06, 0.3, 0.18, 0.12, 0.18, 0.04, 0.16, 0.24, 0.16, 0.16, 0.22, 0.2, 0.22, 0.12, 0.2, 0.12, 0.08, 0.22, 0.14, 0.18, 0.12, 0.2, 0.06, 0.28, 0.12, 0.14, 0.22, 0.18, 0.26, 0.26, 0.14, 0.2, 0.16, 0.16, 0.1, 0.26, 0.08, 0.16, 0.14, 0.22, 0.24, 0.16, 0.18, 0.2, 0.36]
plot1y2 = [0.76, 0.88, 0.94, 0.9, 0.64, 0.88, 0.82, 0.82, 0.78, 0.84, 0.8, 0.84, 0.9, 0.78, 0.86, 0.78, 0.78, 0.86, 0.82, 0.9, 0.82, 0.9, 0.76, 0.96, 0.78, 0.86, 0.82, 0.88, 0.9, 0.86, 0.82, 0.78, 0.84, 0.84, 0.82, 0.82, 0.92, 0.86, 0.78, 0.8, 0.8, 0.84, 0.76, 0.7, 0.82, 0.84, 0.82, 0.82, 0.82, 0.88]
plot2y2 = [0.2, 0.04, 0.04, 0.1, 0.18, 0.06, 0.16, 0.14, 0.08, 0.1, 0.18, 0.1, 0.08, 0.2, 0.1, 0.2, 0.14, 0.1, 0.16, 0.08, 0.14, 0.06, 0.22, 0.04, 0.16, 0.1, 0.16, 0.1, 0.08, 0.12, 0.08, 0.18, 0.12, 0.12, 0.14, 0.12, 0.04, 0.1, 0.16, 0.12, 0.18, 0.12, 0.16, 0.22, 0.14, 0.12, 0.14, 0.16, 0.1, 0.08]

overallplot1y1 = [np.mean(plot1y1[:i+1]) for i in range(len(plot1y1))]
overallplot1y2 = [np.mean(plot1y2[:i+1]) for i in range(len(plot1y2))]
overallplot2y1 = [np.mean(plot2y1[:i+1]) for i in range(len(plot2y1))]
overallplot2y2 = [np.mean(plot2y2[:i+1]) for i in range(len(plot2y2))]

print (overallplot2y2)
print (xvals2)

axes = plt.gca()
xvals1 =  np.array(range(24, 5000, 50))
#print (xvals1)
xvals2 = np.array(range(5024, 7500, 50))
plt.title('Tic-tac-toe win rate using TD(0) prediction')
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
plt.title('Tic-tac-toe win rate using TD(0) prediction')
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
plt.title('Tic-tac-toe loss rate using TD(0) prediction')
plt.xlabel('# games played')
plt.ylabel('percentge %')
plt.plot(xvals1, plot2y1, label = '% losses for last 50 learning games')
plt.plot(xvals2, plot2y2, label = '% losses for last 50 test games')
plt.legend()
plt.close()

axes = plt.gca()
xvals1 =  np.array(range(24, 5000, 50))
#print (xvals1)
xvals2 = np.array(range(5024, 7500, 50))
plt.title('Tic-tac-toe loss rate using TD(0) prediction')
plt.xlabel('# games played')
plt.ylabel('percentge %')
plt.plot(xvals1, overallplot2y1, label = 'overall % losses for learning games')
plt.plot(xvals2, overallplot2y2, label = 'overall % losses for test games')
plt.legend()
plt.close()

            