# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 17:05:01 2019

@author: nvtz34
"""

import numpy as np
from keras import models
from keras import layers
from keras.models import load_model

import Draughts3 as d3


def create_network():
    network = models.Sequential()
    network.add(layers.Dense(145, activation = 'relu', input_shape=(34,)))
    network.add(layers.Dense(256, activation='softmax'))
    network.compile(optimizer = 'SGD',
                    loss = 'mean_squared_error',
                    metrics=['accuracy'])
    return network

output = [1.0/256]*256

def output_choice(output):
#    action = !None
    foundaction = False
    u = np.random.uniform()
    cumprob = 0
    for i in range(256):
        if i == 255:
            cumprob = 1.0 ##account for rounding error
        cumprob = cumprob + output[i]
#        print ('u is', u, 'cumprob is' )
        if u < cumprob:
            action = i
            foundaction = True
            break
#        if action == None and i == 256:
#            print ('u is', u, 'cumprob is', cumprob )
#    if foundaction == False:
##        print (u, output)
    return action
        
#print(output_choice(output))

def remove_choice(output, choice):
    prob = output[choice]
    scale = 1/(1.0 - prob)
    output[choice] = 0
    output = [i*scale for i in output]
    return output

#print(sum(remove_choice(output, 62)))

def nn_vs_nn(network1, network2):
    state = np.array([-1]*12 + [0]*8 + [1]*12 + [1, 0])
    while d3.is_game_finished(state) == False:
        if state[32] == 1:
#            print (d3.board_view(state))
            output = network1.predict(state.reshape(1, 34))[0]   
            action = output_choice(output)
            position, direction, taking = d3.output_to_action(action)
            while d3.is_move_legal(state, position, direction, taking) == False:
                output = remove_choice(output, action)
                action = output_choice(output)
#                print (action)
#                if action == None:
##                    print (output)
##                    print(d3.board_view(state))
                position, direction, taking = d3.output_to_action(action)
            state = d3.take_action(state, position, direction, taking)
            state = d3.swap_player(state)
#            print (board_view(state))
        else:
#            print (d3.board_view(state))
            output = network2.predict(state.reshape(1, 34))[0]   
            action = output_choice(output)
            position, direction, taking = d3.output_to_action(action)
            while d3.is_move_legal(state, position, direction, taking) == False:
                output = remove_choice(output, action)
                action = output_choice(output)
#                print (action)
#                if action == None:
#                    print (output)
#                    print(d3.board_view(state))
                position, direction, taking = d3.output_to_action(action)
            state = d3.take_action(state, position, direction, taking)
            state = d3.swap_player(state)
#            print (board_view(state))
    v = d3.checkstate(state)
#    print (state, v)
    if v == 1:
#        print ('v is 1')
        if state[32] == 1:
            return 'Black'
        else:
            return 'White'
    else:
        if state[32] == 1:
            return 'White'
        else:
            return 'Black'
            
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
                print (i)
            winner = nn_vs_nn(network1, network2)
            if winner == 'White':
                count1 = count1 + 1
            else:
                count2 = count2 + 1
#            print (winner, count1, count2)
        if count2 > count1:
            improvements = improvements + 1
#            print ('2 is better')
            network1 = network2
        print (i,'send')
        if (i+1)%500 == 0:        
            if i == 499:
                network1.save('model500_1.h5')
                print ('savedmodel')
                np.save('improvements500_1', improvements)
                print ('savedn')
            if i == 999:
                network1.save('model1000_1.h5')
                print ('savedmodel')
                np.save('improvements1000_1', improvements)
                print ('savedn')
            if i == 1499:
                network1.save('model1500_1.h5')
                print ('savedmodel')
                np.save('improvements1500_1', improvements)
                print ('savedn')
            if i == 2999:
                network1.save('model2000_1.h5')
                print ('savedmodel')
                np.save('improvements2000_1', improvements)
                print ('savedn')
            if i == 2499:
                network1.save('model2500_1.h5')
                print ('savedmodel')
                np.save('improvements2500_1', improvements)
                print ('savedn')

    return improvements
            

start_network = create_network()
#start_network = load_model('my_model.h5')
evolution(2500, 30, start_network)   

###this seems to be working needs to be run and trained, also decide on how many games need to be played for each N (can play around with this maybe 30)
        
                
    