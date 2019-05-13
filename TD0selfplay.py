# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 15:19:07 2019

@author: nvtz34
"""

import numpy as np
import ProjectFunctions as pf
import matplotlib.pyplot as plt

def tdtactoeselfplayer(prev, grid, expset, explst, expvals, alpha, eps, gamma):

   
    if pf.trin(grid) in expset:  #change this to other tuple thing, probs willl have to runn examples again, actually u wont
        index = pf.arraycheck(grid, explst)
        vdash = expvals[index]
    else:
#        print (grid, 'this board')
#        if pf.is_game_finished(grid) == False:
#            vdash = pf.checkstate(grid)
#        else:
#            print ('finsihed')
#            vdash = pf.checkresult(grid)
        vdash = pf.checkstate(grid)
#        print (vdash)
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
#        print (v, vdash)
        newv = v + alpha*(gamma*vdash - v)
#        print (newv, 'newv')
        expvals[vindex] = newv            
    if pf.is_game_finished(grid) == False:
#        print ('moving')
        ## now we make our next move
        if vdash!= 0:  
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
                            
#                            print (exp_poss_grids, new_poss_grids, 'here')
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
                            poss_state_vals = (poss_state_vals1 + 
                                               poss_state_vals2)
                            action_val = np.mean(poss_state_vals)
                        else:
                            action_val = pf.checkstate(grid1)
                        poss_action_vals.append(action_val)
            action = pf.epsgreedy(poss_action_vals, eps)
            newgrid = poss_actions[action]  
    else:
        newgrid = grid
    return newgrid, newprev, expset, explst, expvals


def afterupdate(grid, prev, expset, explst, expvals, alpha, eps, gamma):
    if pf.trin(grid) in expset:
        index = pf.arraycheck(grid, explst)
        vdash = expvals[index]
    else:
        vdash = pf.checkstate(grid)
        expset.add(pf.trin(grid))
        explst.append(grid)
        expvals.append(vdash)
        index = len(expvals) - 1
        
    v, vindex = prev[0], prev[1]
    newv = v + alpha*(gamma*vdash - v)
    expvals[vindex] = newv   
    return grid, expset, explst, expvals
    
    
    
#def TDtactoeselftraining(expset, explst, expvals, alpha, eps, gamma):
#    grid = np.zeros((3,3))
#    prev1 = np.zeros((3,3))
#    prev2 = np.zeros((3,3))
##    finished = False
##    finished_by_1 = False
#    while pf.is_game_finished(grid) == False:
##        print (grid, prev1, expset, explst, expvals)
##        print (tdtactoeselfplayer(prev1, grid, expset, explst, expvals, alpha, eps, gamma))
#        grid, prev1, expset, explst, expvals = tdtactoeselfplayer(prev1, grid, expset, explst, expvals, alpha, eps, gamma)
#        print (grid, 'player1', expvals)
#        grid = -grid
#        grid, prev2, expset, explst, expvals = tdtactoeselfplayer(
#                prev2, grid, expset, explst, expvals, alpha, eps, gamma)
##        grid = -grid
##        if finished == False and pf.is_game_finished(grid) == True:
##            print ('that if')
##            finished = True
#        grid = -grid
#        print (grid, 'player2', expvals)
#    grid, expset, explst, expvals = afterupdate(grid, prev1, expset, explst, expvals, alpha, eps, gamma)
#    grid = -grid
#    grid, expset, explst, expvals = afterupdate(grid, prev2, expset, explst, expvals, alpha, eps, gamma)
#    grid = -grid
#    return pf.checkresult(grid), expset, explst, expvals


def TDtactoeselftraining1(expset, explst, expvals, alpha, eps, gamma):
    grid = np.zeros((3,3))
    prev1 = np.zeros((3,3))
    prev2 = np.zeros((3,3))
    move = 0
    while pf.is_game_finished(grid) == False:
#        print (grid, move)
#        print (move)
        move = move + 1
        grid = -grid
#        print (grid)
        if np.sign((-1)**move) == -1:
            grid, prev1, expset, explst, expvals = tdtactoeselfplayer(prev1, grid, expset, explst, expvals, alpha, eps, gamma)
#            print (grid, 'player1', expvals)
        else:
            grid, prev2, expset, explst, expvals = tdtactoeselfplayer(
                    prev2, grid, expset, explst, expvals, alpha, eps, gamma)
#        print (grid, move)

#        grid = -grid
#        if finished == False and pf.is_game_finished(grid) == True:
#            print ('that if')
#            finished = True
#        grid = -grid
#        print (grid, 'player2', expvals)
#    print (move, (-1)**move)
    if np.sign((-1)**move) == -1:     #player1s move ended game
#        print ('player1s move ended game')
        grid = -1*grid
    grid, expset, explst, expvals = pf.afterupdate1(grid, prev1, expset, explst, expvals, alpha, eps, gamma)
    grid = -grid
    grid, expset, explst, expvals = pf.afterupdate1(grid, prev2, expset, explst, expvals, alpha, eps, gamma)
    grid = -grid
    ## our check result is from player 2s persepective
    return pf.checkresult(grid), expset, explst, expvals

def testgame(expset, explst, expvals, alpha, eps, gamma):
    grid = np.zeros((3,3))
    prev = np.zeros((3,3))
    move = 0
    while pf.is_game_finished(grid) == False:
        move = move + 1
        if (-1)**move == -1:
            grid = pf.randmove2(-1, grid)
        else:
            grid, prev, expset, explst, expvals = tdtactoeselfplayer(prev, grid, expset, explst, expvals, alpha, eps, gamma)
    grid, expset, explst, expvals = afterupdate(grid, prev, expset, explst, expvals, alpha, eps, gamma)
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
    np.save('learnwinTDseld', learnwin)
    np.save('learnlossTdself', learnloss)
    np.save('testwinTDself', testwin)
    np.save('testlossTDself', testloss)
    return learnwin, learnloss, testwin, testloss
    

#(TDtactoeselftraining1(set(), [], [], 0.5, 0.5, 0.9))
    
print (nrunner1(TDtactoeselftraining1, 7500, set(), [], [], 0.5, 0.9, 0.9))

#([0.24, 0.22, 0.34, 0.2, 0.22, 0.16, 0.34, 0.16, 0.32, 0.28, 0.34, 0.14, 0.16, 0.28, 0.22, 0.18, 0.14, 0.06, 0.14, 0.14, 0.14, 0.18, 0.16, 0.16, 0.12, 0.12, 0.12, 0.14, 0.1, 0.06, 0.12, 0.26, 0.14, 0.2, 0.2, 0.16, 0.66, 0.18, 0.18, 0.16, 0.16, 0.18, 0.08, 0.22, 0.2, 0.04, 0.2, 0.06, 0.26, 0.14, 0.16, 0.16, 0.1, 0.12, 0.18, 0.1, 0.3, 0.42, 0.1, 0.2, 0.2, 0.22, 0.58, 0.12, 0.16, 0.18, 0.14, 0.18, 0.04, 0.16, 0.44, 0.18, 0.1, 0.16, 0.26, 0.32, 0.1, 0.1, 0.14, 0.24, 0.04, 0.18, 0.8, 0.54, 0.56, 0.5, 0.4, 0.3, 0.32, 0.6, 0.22, 0.16, 0.18, 0.16, 0.08, 0.22, 0.08, 0.08, 0.14, 0.24], [0.72, 0.64, 0.44, 0.58, 0.52, 0.5, 0.52, 0.6, 0.42, 0.52, 0.46, 0.66, 0.66, 0.5, 0.58, 0.68, 0.64, 0.7, 0.64, 0.66, 0.64, 0.72, 0.74, 0.66, 0.82, 0.74, 0.74, 0.74, 0.7, 0.72, 0.8, 0.46, 0.8, 0.64, 0.72, 0.64, 0.3, 0.76, 0.76, 0.7, 0.74, 0.48, 0.66, 0.72, 0.74, 0.8, 0.74, 0.88, 0.62, 0.72, 0.8, 0.82, 0.86, 0.82, 0.72, 0.86, 0.54, 0.26, 0.48, 0.6, 0.74, 0.68, 0.34, 0.74, 0.68, 0.66, 0.8, 0.78, 0.8, 0.78, 0.44, 0.54, 0.78, 0.78, 0.6, 0.46, 0.72, 0.82, 0.68, 0.54, 0.86, 0.78, 0.18, 0.3, 0.24, 0.32, 0.48, 0.54, 0.52, 0.32, 0.62, 0.84, 0.68, 0.62, 0.86, 0.6, 0.82, 0.88, 0.68, 0.68], [0.2, 0.36, 0.26, 0.42, 0.34, 0.52, 0.38, 0.74, 0.62, 0.48, 0.56, 0.76, 0.72, 0.68, 0.86, 0.72, 0.8, 0.74, 0.84, 0.78, 0.74, 0.82, 0.92, 0.72, 0.84, 0.9, 0.84, 0.7, 0.82, 0.72, 0.8, 0.86, 0.8, 0.9, 0.8, 0.8, 0.86, 0.74, 0.8, 0.82, 0.76, 0.82, 0.82, 0.9, 0.9, 0.76, 0.74, 0.78, 0.88, 0.86], [0.72, 0.48, 0.62, 0.4, 0.36, 0.34, 0.42, 0.18, 0.24, 0.32, 0.34, 0.24, 0.2, 0.28, 0.08, 0.18, 0.14, 0.22, 0.14, 0.12, 0.14, 0.14, 0.06, 0.26, 0.14, 0.1, 0.14, 0.2, 0.14, 0.22, 0.18, 0.1, 0.12, 0.08, 0.18, 0.16, 0.1, 0.2, 0.18, 0.1, 0.18, 0.14, 0.14, 0.1, 0.04, 0.18, 0.18, 0.18, 0.06, 0.12])

#plot1y1 = [0.36, 0.24, 0.32, 0.12, 0.34, 0.2, 0.22, 0.06, 0.14, 0.14, 0.16, 0.18, 0.14, 0.2, 0.1, 0.1, 0.08, 0.18, 0.18, 0.3, 0.04, 0.2, 0.06, 0.14, 0.3, 0.14, 0.08, 0.16, 0.14, 0.12, 0.06, 0.14, 0.1, 0.08, 0.16, 0.1, 0.08, 0.12, 0.06, 0.22, 0.06, 0.14, 0.12, 0.08, 0.02, 0.14, 0.1, 0.0, 0.08, 0.18, 0.14, 0.08, 0.08, 0.08, 0.16, 0.42, 0.46, 0.06, 0.06, 0.08, 0.12, 0.12, 0.06, 0.08, 0.5, 0.54, 0.14, 0.24, 0.64, 0.02, 0.16, 0.0, 0.1, 0.04, 0.1, 0.02, 0.26, 0.58, 0.28, 0.22, 0.54, 0.4, 0.06, 0.16, 0.1, 0.02, 0.14, 0.08, 0.1, 0.04, 0.12, 0.06, 0.06, 0.12, 0.06, 0.2, 0.28, 0.1, 0.14, 0.18]
#plot2y1 = [0.6, 0.68, 0.54, 0.38, 0.38, 0.32, 0.26, 0.3, 0.24, 0.36, 0.16, 0.16, 0.24, 0.22, 0.14, 0.26, 0.24, 0.34, 0.2, 0.16, 0.14, 0.18, 0.24, 0.2, 0.24, 0.18, 0.18, 0.36, 0.4, 0.28, 0.16, 0.16, 0.16, 0.26, 0.2, 0.28, 0.18, 0.28, 0.14, 0.16, 0.26, 0.26, 0.18, 0.2, 0.22, 0.1, 0.2, 0.28, 0.12, 0.16, 0.18, 0.14, 0.28, 0.26, 0.26, 0.24, 0.2, 0.22, 0.18, 0.2, 0.12, 0.06, 0.3, 0.14, 0.14, 0.12, 0.12, 0.26, 0.16, 0.22, 0.16, 0.26, 0.16, 0.12, 0.22, 0.16, 0.18, 0.12, 0.2, 0.2, 0.12, 0.14, 0.24, 0.16, 0.16, 0.3, 0.2, 0.1, 0.18, 0.14, 0.1, 0.24, 0.18, 0.14, 0.18, 0.2, 0.14, 0.16, 0.18, 0.12]
#plot1y2 = [0.18, 0.24, 0.38, 0.34, 0.4, 0.38, 0.36, 0.42, 0.62, 0.52, 0.56, 0.64, 0.74, 0.74, 0.78, 0.74, 0.74, 0.84, 0.68, 0.78, 0.84, 0.8, 0.88, 0.86, 0.74, 0.76, 0.84, 0.78, 0.78, 0.78, 0.78, 0.8, 0.88, 0.86, 0.86, 0.72, 0.86, 0.78, 0.66, 0.66, 0.82, 0.82, 0.82, 0.78, 0.78, 0.88, 0.76, 0.8, 0.8, 0.84]
#plot2y2 = [0.36, 0.42, 0.18, 0.24, 0.22, 0.22, 0.22, 0.26, 0.22, 0.1, 0.14, 0.06, 0.1, 0.08, 0.06, 0.06, 0.02, 0.04, 0.1, 0.14, 0.04, 0.08, 0.06, 0.06, 0.08, 0.0, 0.02, 0.08, 0.06, 0.02, 0.06, 0.1, 0.02, 0.02, 0.04, 0.2, 0.04, 0.08, 0.14, 0.1, 0.06, 0.04, 0.06, 0.14, 0.06, 0.04, 0.06, 0.04, 0.04, 0.02]
#
#
#overallplot1y1 = [np.mean(plot1y1[:i+1]) for i in range(len(plot1y1))]
#overallplot1y2 = [np.mean(plot1y2[:i+1]) for i in range(len(plot1y2))]
#overallplot2y1 = [np.mean(plot2y1[:i+1]) for i in range(len(plot2y1))]
#overallplot2y2 = [np.mean(plot2y2[:i+1]) for i in range(len(plot2y2))]
#
##plt.subplot(2,2,1)
#axes = plt.gca()
#xvals1 =  np.array(range(24, 5000, 50))
##print (xvals1)
#xvals2 = np.array(range(5024, 7500, 50))
#plt.title('Tic-tac-toe P2 win rate using TD(0) prediction (self-trained agent)')
#plt.xlabel('# games played')
#plt.ylabel('percentge %')
#plt.plot(xvals1, plot1y1, label = '% wins for last 50 learning games')
#plt.plot(xvals2, plot1y2, label = '% wins for last 50 test games')
#plt.legend()
##plt.close()
#plt.show()
#
##plt.subplot(2,2,2)
#axes = plt.gca()
#xvals1 =  np.array(range(24, 5000, 50))
##print (xvals1)
#xvals2 = np.array(range(5024, 7500, 50))
#plt.title('Tic-tac-toe P2 win rate using TD(0) prediction (self-trained agent)')
#plt.xlabel('# games played')
#plt.ylabel('percentge %')
#plt.plot(xvals1, overallplot1y1, label = 'overall % wins for learning games')
#plt.plot(xvals2, overallplot1y2, label = 'overall % wins for test games')
#plt.legend()
##plt.close()
#plt.show()
#
##plt.subplot(2,2,3)
#axes = plt.gca()
#xvals1 =  np.array(range(24, 5000, 50))
##print (xvals1)
#xvals2 = np.array(range(5024, 7500, 50))
#plt.title('Tic-tac-toe P1 win rate using TD(0) prediction (self-trained agent)')
#plt.xlabel('# games played')
#plt.ylabel('percentge %')
#plt.plot(xvals1, plot2y1, label = 'overall % P2 wins for last 50 learning games')
#plt.plot(xvals2, plot2y2, label = 'overall % P2 wins for last 50 test games')
#plt.legend()
##plt.close()
#plt.show()
#
##plt.subplot(2,2,4)
#axes = plt.gca()
#xvals1 =  np.array(range(24, 5000, 50))
##print (xvals1)
#xvals2 = np.array(range(5024, 7500, 50))
#plt.title('Tic-tac-toe P1 win rate using TD(0) prediction (self-trained agent)')
#plt.xlabel('# games played')
#plt.ylabel('percentge %')
#plt.plot(xvals1, overallplot2y1, label = 'overall % P1 wins for learning games')
#plt.plot(xvals2, overallplot2y2, label = 'overall % P1 wins for test games')
#plt.legend()
##plt.close()
#plt.show()
