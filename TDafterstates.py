# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 19:23:42 2019

@author: nvtz34
"""
import ProjectFunctions as pf
import numpy as np

def TD_afterstates(prev, grid, expset, explst, expvals, alpha, eps, gamma):
    
    # make move
    exp_poss_actions = []
    new_poss_actions = []
    for i in range(3):
        for j in range(3):
            if grid[i][j] == 0:
                grid1 = grid.copy()
                grid1[i][j] = 1
                if pf.trin(grid1) in expset:
                     exp_poss_actions.append(grid1)
                else:
                    new_poss_actions.append(grid1)
    poss_actions  = exp_poss_actions + new_poss_actions
                    
    if len(exp_poss_actions) == 0:
        indexes = []
        poss_action_vals1 = []
    elif len(exp_poss_actions) == 1:
        indexes = [pf.arraycheck(exp_poss_actions[0], explst)]
    else:
        indexes = pf.arraycheck2(exp_poss_actions, explst)[0]
        
    if len(indexes) > 0:
        poss_action_vals1 = [expvals[k] for k in indexes]
    poss_action_vals2 = [0.5 for k in new_poss_actions]
    poss_action_vals = poss_action_vals1 + poss_action_vals2
    action = pf.epsgreedy(poss_action_vals, eps)
    newgrid = poss_actions[action]
    vdash = pf.checkstate(newgrid)
#    print (len(poss_action_vals), len(indexes))
    if action < len(indexes):
        newindex = indexes[action]
    else:
        explst.append(newgrid)
#        print (newgrid, 'newgrid')
        expset.add(pf.trin(newgrid))
#        print (newgrid, 'grid')
        expvals.append(vdash)
        newindex = len(expvals) - 1
        
        
    #now need value of new afterstate then update previous afterstate
    # first check to see if it is our first afterstate (an so there would be no update)
    first_after = False
    for i in range(3):
        for j in range(3):
            if len(prev) == 0:
                first_after = True
                break
    
    if first_after == False:
        # find state value of current afterstate
#        print (prev,)
        v, vindex = prev
#        if pf.is_game_finished == False:
##            if pf.trin(newgrid) in expset:
##                newindex = pf.arraycheck(newgrid, explst)
##                vdash = expvals[newindex]
##            else:
##                vdash = 0.5
#        else:
#            vdash = pf.checkstate(newgrid)
        # make update
        newv = v + alpha*(gamma*vdash - v)
        expvals[vindex] = newv
        
    newprev = [vdash, newindex]
#    print (newgrid, newprev, expset, explst, expvals)
#    print (explst, expvals)
    return newgrid, newprev, expset, explst, expvals
    
#
#def afterupdate1(grid, prev, expset, explst, expvals, alpha, eps, gamma):
#    vdash = checkstate(grid)
#        
#    v, vindex = prev[0], prev[1]
#    newv = v + alpha*(gamma*vdash - v)
#    expvals[vindex] = newv   
#    return grid, expset, explst, expvals


def afterstates_game(expset, explst, expvals, alpha, eps, gamma):
    grid = np.zeros((3,3))
    prev1 = []
    prev2 = []
    move = 0
    while pf.is_game_finished(grid) == False:
        move = move + 1
        grid = -grid
        if np.sign((-1)**move) == -1:
            grid, prev1, expset, explst, expvals = TD_afterstates(prev1, grid, expset, explst, expvals, alpha, eps, gamma)
        else:
            grid, prev2, expset, explst, expvals = TD_afterstates(prev2, grid, expset, explst, expvals, alpha, eps, gamma)
    grid = -1*grid   #why
    if np.sign((-1)**move) == -1:  #player 1s move finsihes game
        grid, expset, explst, expvals = pf.afterupdate1(grid, prev2, expset, explst, expvals, alpha, eps, gamma)
    else:
        grid, expset, explst, expvals = pf.afterupdate1(grid, prev1, expset, explst, expvals, alpha, eps, gamma)
        grid = -grid
    return pf.checkresult(grid), expset, explst, expvals

#print (afterstates_game(set(), [], [], 0.5, 0.9, 0.9))
    


def testgame(expset, explst, expvals, alpha, eps, gamma):
    grid = np.zeros((3,3))
    prev = []
    move = 0
    while pf.is_game_finished(grid) == False:
        move = move + 1
        if (-1)**move == -1:
            grid = pf.randmove2(-1, grid)
        else:
            grid, prev, expset, explst, expvals = TD_afterstates(prev, grid, expset, explst, expvals, alpha, eps, gamma)
    if np.sign((-1)**move) == -1:
        grid, expset, explst, expvals = pf.afterupdate1(grid, prev, expset, explst, expvals, alpha, eps, gamma)
    return pf.checkresult(grid), expset, explst, expvals



def nrunner1(game, n, expset, explst, expvals, alpha, eps, gamma):
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
            print (i, win50*2,'%', loss50*2,'%')
            if i < n - 2500:
                learnwin.append(win50/50.0)
                learnloss.append(loss50/50.0)
            else:
                testwin.append(win50/50.0)
                testloss.append(loss50/50.0)
            win50, loss50 = 0, 0
        if i == n - 2501:
            game = testgame
            eps = 1
            np.save('expvalsafters', expvals)
            np.save('exlstafters', explst)
            np.save('expset', expset)
    np.save('learnwinTDafters', learnwin)
    np.save('learnlossTdafters', learnloss)
    np.save('testwinTDafters', testwin)
    np.save('testlossTDafters', testloss)
    return learnwin, learnloss, testwin, testloss

nrunner1(afterstates_game, 7500, set(), [], [], 0.5, 0.9, 0.9)




    
        