import math
import operator
import pandas as pd 

def viterbi(testdata,test_actual,states,start,transition,emission):
    result=[]
    temp=[]
    test_actual= test_actual.split()
    #print(test_actual)
    for i in range(len(testdata)):
        observations=testdata[i]
        true = test_actual[i]
        r= run_viterbi(observations,states,start,transition,emission)
        for i in range(len(r)):
            temp.append(states[int(r[i])])
        temp=''.join(temp)
        result.append(temp)
        print(temp,true)
        temp=[]
        
def run_viterbi(observations,states,start,transition,emission):
        nSamples = len(observations)
        nStates = transition.shape[0] # number of states
        viterbi = np.zeros((nStates,nSamples)) # initialise viterbi table
        psi = np.zeros((nStates,nSamples)) # initialise the best path table
        best_path = np.zeros(nSamples); # this will be your output
        #for t=0
        for i in range(26):
            viterbi[i][0] = start[i] * emission[i][states.index(observations[0])]
            psi[i] = 0;
        #for t>0
        for t in range(1,nSamples): # loop through time
            for s in range (0,nStates): # loop through the states @(t-1)
                trans_p = viterbi[:,t-1] * transition[:,s]
                #print(trans_p)
                psi[s,t], viterbi[s,t] = max(enumerate(trans_p), key=operator.itemgetter(1))
                #print("best path table")
                #print(psi[s,t])
                viterbi[s,t] = viterbi[s,t]*emission[s,states.index(observations[t])]
    
        #print(viterbi)
      
        #print(viterbi[:,nSamples-1].argmax())
        #D - Back-tracking
        
    
        best_path[nSamples-1] =  viterbi[:,nSamples-1].argmax() # last state
        #print(best_path)
        for t in range(nSamples-1,0,-1): # states of (last-1)th to 0th time step
            #print(best_path[t], t)
            best_path[t-1] = viterbi[:,t-1].argmax()
        #print(best_path)
        return best_path



#Author Tasmin Chowdhury

import numpy as np
import random
import string
import re
def build_matrix(text, mat):
    text = re.sub("[^a-z ]+", "", text)
    #split into training and testing
    train_states = text[:int((len(text)+1)*.80)] #Remaining 80% to training set
    test_states = text[int(len(text)*.80+1):]
    corrupt=[]
    corrupt_symbol = []
    word_list = train_states.split()
    for i in range(len(word_list)):
        word = word_list[i]
        for j in range(len(word)):
            letter=word[j]
            k= random.uniform(0, 1)
            if k<0.2:
                possible_values= mat[letter]
                random_index=random.randint(0, len(possible_values)-1)
                corrupt.append(possible_values[random_index])
            else:
                corrupt.append(letter)
        corrupt= ''.join(corrupt)
        corrupt_symbol.append(corrupt)
        #print(word, corrupt)
        corrupt=[]
    #split the corrupted data to training symbol and testing symbol
    train_corrupt_symbol = corrupt_symbol[:int((len(corrupt_symbol)+1)*.80)] #Remaining 80% to training set
    test_corrupt_symbol = corrupt_symbol[int(len(corrupt_symbol)*.80+1):]

    #Initialization of matrices
    states = []
    state_counter=[0]*26
    total=np.zeros((26, 1))
    start_probability = np.zeros((26, 1))
    transition_probability = np.zeros((26, 26))
    transition_counter = np.zeros((26, 26))
    generation_counter = np.zeros((26, 26))
    generation_probability = np.zeros((26, 26))
    
    
    for i in range(26):
        states.append(chr(ord('a') + i))
    #print(states) states = ['a', 'b','c'......'z']

    #build start_probability matrix
    for j in range(len(word_list)):
        word=word_list[j]
        first_letter=word[0]
        for i in range(26):
            if states[i]==str(first_letter):
                state_counter[i]=state_counter[i]+1
    for i in range(26):
        start_probability[i]=float(state_counter[i]/len(word_list))
        #print(state_counter[i], start_probability[i])
        
        
    #calculate transition probability
    for j in range(len(word_list)):
        word=word_list[j]
        for i in range(len(word)-1):
            prev=states.index(word[i])
            nextl=states.index(word[i+1])
            transition_counter[prev][nextl]=transition_counter[prev][nextl]+1       
    for i in range(26):
        total=np.sum(transition_counter,axis=1)
    for i in range(26):   
        for j in range(26):
            transition_probability[i][j]=float(transition_counter[i][j]/total[i])
    #print(transition_counter, transition_probability)  

    for j in range(len(word_list)):
        correct=word_list[j]
        corrupt=corrupt_symbol[j]
        for i in range(len(correct)):
            r=states.index(correct[i])
            w=states.index(corrupt[i])
            generation_counter[r][w]=generation_counter[r][w]+1
    for i in range(26):
        total=np.sum(generation_counter,axis=1)
    for i in range(26):   
        for j in range(26):
            generation_probability[i][j]=float(generation_counter[i][j]/total[i])
    #print(generation_probability) 
    
    
    #implement Viterbi
    
    viterbi(test_corrupt_symbol,test_states, states, start_probability, transition_probability, generation_probability)
    
def main():
    f=open('text.txt',encoding="utf8") 
    text= f.read()
    corrupt_matrix= {'a': ['q','w','x','z','s'],
                     'b': ['c','v','n','n','f','g','h'],
                     'c': ['x','v','s','d','f'],
                     'd': ['e','s','f','x','c'],
                     'e': ['w','s','d','f','r'],
                     'f': ['r','d','c','v','g'],
                     'g': ['t','f','b','v','h'],
                     'h': ['y','g','b','n','j'],
                     'i': ['u','o','j','k'],
                     'j': ['u','i','h','k','n','m'],
                     'k': ['i','j','l','m'],
                     'l': ['o','k','p'],
                     'm': ['n','j','k'],
                     'n': ['j','h','b','m'],
                     'o': ['i','p','k','l'],
                     'p': ['o','l'],
                     'q': ['a','s','w'],
                     'r': ['e','d','f','t'],
                     's': ['w','a','d','z','x'],
                     't': ['r','f','g','y'],
                     'u': ['y','h','j','i'],
                     'v': ['f','c','g','b'],
                     'w': ['q','a','s','e'],
                     'x': ['z','s','d','c'],
                     'y': ['t','g','h','u'],
                     'z': ['a','s','x'],
                    }
    
    build_matrix(text,corrupt_matrix)
main()