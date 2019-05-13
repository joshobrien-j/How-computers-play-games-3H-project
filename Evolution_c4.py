# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 17:05:01 2019

@author: nvtz34
"""

import numpy as np
from keras import initializers
from keras import models
from keras import layers
from keras.models import load_model

#import Draughts3 as d3


def create_network():
    network = models.Sequential()
    network.add(layers.Dense(25, kernel_initializer='random_uniform', activation = 'relu', input_shape=(7*6,)))
    network.add(layers.Dense(7, kernel_initializer='random_uniform', bias_initializer = initializers.RandomUniform(minval=-0.5, maxval=0.5, seed=None), activation='softmax'))
    network.compile(optimizer = 'SGD',
                    loss = 'mean_squared_error',
                    metrics=['accuracy'])
    return network

output = [1.0/256]*256

def output_choice_c4(output):
#    action = !None
    foundaction = False
    u = np.random.uniform()
    cumprob = 0
    for i in range(7):
        if i == 7:
            cumprob = 1.0 ##account for rounding error
        cumprob = cumprob + output[i]
#        print ('u is', u, 'cumprob is' )
        if u < cumprob:
            action = i
#            foundaction = True
            break
#        if action == None and i == 256:
#            print ('u is', u, 'cumprob is', cumprob )
#    if foundaction == False:
##        print (u, output)
    return action

def is_move_legal_c4(state, action):
    legal = False
    if state[action][0] == 0:
        legal = True
    return legal

def take_action_c4(grid, action):
    for j in range(7):
        if grid[action][5-j] == 0:   #changes to 5-j
            grid[action][5-j] = 1
            break
    return grid

def c4_reflect(grid):
    grid1 = np.array([grid[6]])
    for i in range(1,7):
        grid1 = np.append(grid1, [grid[6-i]], axis = 0)
    return grid1


def is_c4_finished(grid):
#    print (grid, 'checking')
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
#            print (i, j)
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
#        for j in range (1,7):
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

#grid = np.zeros((7,7))
#print (is_c4_finished(grid))

def checkstate_c4(grid):
    finished, result = is_c4_finished(grid)
    if finished == True:
        return result
    else:
        return 0.5

        
#print(output_choice(output))

def remove_choice(output, choice):
    prob = output[choice]
    scale = 1/(1.0 - prob)
    output[choice] = 0
    output = [i*scale for i in output]
    return output

#print(sum(remove_choice(output, 62)))

def nn_vs_nn(network1, network2):
    state = np.zeros((7,6))
    move = 0
    while is_c4_finished(state)[0] == False:
#        print ('playing')
        move = move + 1
        if (-1)**move == 1:
#            print (d3.board_view(state))
            output = network1.predict(state.reshape(1, 7*6))[0]   
#            print (output, 'output')
            action = output_choice_c4(output)
#            position, direction, taking = output_to_action_c4(action)
            while is_move_legal_c4(state, action) == False:
                output = remove_choice(output, action)
                action = output_choice_c4(output)
#                print (action)
#                if action == None:
##                    print (output)
##                    print(d3.board_view(state))
#                position, direction, taking = d3.output_to_action(action)
            state = take_action_c4(state, action)
            state = -state
#            print (board_view(state))
        else:
#            print (d3.board_view(state))
            output = network2.predict(state.reshape(1, 7*6))[0]  
#            print (output)
            action = output_choice_c4(output)
#            position, direction, taking = d3.output_to_action(action)
            while is_move_legal_c4(state, action) == False:
                output = remove_choice(output, action)
                action = output_choice_c4(output)
#                print (action)
#                if action == None:
#                    print (output)
#                    print(d3.board_view(state))
#                position, direction, taking = d3.output_to_action(action)
            state = take_action_c4(state, action)
            state = -state
#            print (board_view(state))
#    v = checkstate_c4(state)
    if (-1)**move == 1:
        state = -state
#    print (state)
    v = checkstate_c4(state)
    if v == 1:
            result = 'Red'
    elif v == 0:
            result = 'Yellow'
    else:
        result = 'Draw'
#    print (result)
    return result
    
    
            
def evolution(N, n, network1):  ##N pairs, n games
    improvements = 0
    for i in range(N):
        print ('N is', i, 'improvements =', improvements)
        network2 = create_network()
#        print (network2)
        count1 = 0
        count2 = 0
        for j in range(n):
            if (j+1)%10 == 0:
                print (j)
            winner = nn_vs_nn(network1, network2)
            if winner == 'Red':
                count1 = count1 + 1
            else:
                count2 = count2 + 1
#            print (winner, count1, count2)
        if count2 > count1:
            improvements = improvements + 1
#            print ('2 is better')
            network1 = network2
#        print (i,'send')
        if (i+1)%500 == 0:        
            if i == 499:
                network1.save('model500_11.h5')
                print ('savedmodel')
                np.save('improvements500_11', improvements)
                print ('savedn')
            if i == 999:
                network1.save('model1000_11.h5')
                print ('savedmodel')
                np.save('improvements1000_11', improvements)
                print ('savedn')
            if i == 1499:
                network1.save('model1500_11.h5')
                print ('savedmodel')
                np.save('improvements1500_11', improvements)
                print ('savedn')
            if i == 1999:
                network1.save('model2000_11.h5')
                print ('savedmodel')
                np.save('improvements2000_11', improvements)
                print ('savedn')
            if i == 2499:
                network1.save('model2500_11.h5')
                print ('savedmodel')
                np.save('improvements2500_11', improvements)
                print ('savedn')

    return improvements
            

start_network = create_network()
#start_network = load_model('my_model.h5')
evolution(2500, 30, start_network)   

###this seems to be working needs to be run and trained, also decide on how many games need to be played for each N (can play around with this maybe 30)
        
                
    