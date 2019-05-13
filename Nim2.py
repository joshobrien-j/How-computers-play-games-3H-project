# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np

def bob(n):
    transitions = np.zeros(17)  #define empty vector to be filled
    if n < 5:   #when Bob is within one move of winning
        transitions[0] = 1.0    #wins with prob 1
    else:
        for i in range(1,4):
            transitions[n-1-i] = 1.0/3  #otherwise he plays randomly
    return transitions

def alice(n):
    transitions = np.zeros(17)  #define empty vector to be filled
    if (n-1)%4 == 0:    #when n is in the form 4j+1
        for i in range(1,4):
            transitions[n-1-i] = 1.0/3  #equal probability of making moves
    else:   #when alice is guaranteed to win
        move = (n%4)-1  #make move k (n=4j+k)
        if move == -1:  # %-division returns 0 for multiples of 4 giving
                        #error (move=-1 when should be move=3)
            move = 3    #use if loop to correct error
        transitions[n-move-1] = 1.0 #make this move with prob 1
    return transitions


def update(V, r, player1, player2, n): #function for pol eval update rule
    transitions1 = player1(n)   #trns probs for p1
    asum = 0    #a is first summation in update rule
    for i in range(1, 4):
        k = n-i     #k=number of objects reamining after our move
        a = transitions1[k-1]   #pi(a|s) for k (n-a=k)
        transitions2 = player2(k)   #Bobs trans probs from k
        bsum = 0    #b is second summation in update rule
        if k>4:
            for j in range(1, 4):
                b = transitions2[k-j-1]*(r[k-1-j]+0.9*V[k-2-j])
                bsum = bsum + b
        elif k == 1:    #if k=1 after alices move dont consider Bobs move
            bsum = 1.0
        else:
            bsum = -1.0 #certain Bob wins for this case
        asum = asum + a*bsum
    return asum


def Nim(player1, player2, n):
    V = np.zeros(n-1)   #initialise V(s)=0 fot all non-terminal states
    rewards = np.array([1]+[0]*16)  #reward of 1 for n=1, 0 otherwise
    Delta = 1
    while Delta > 0.1:  #follwoing algorithm from here
        Delta = 0
        for i in range(n-1):
            v = V[i]
            V[i] = update(V, rewards, player1, player2, i+2)
            Delta = max(Delta, abs(v-V[i]))
    return V

print (Nim(alice, bob, 17))

