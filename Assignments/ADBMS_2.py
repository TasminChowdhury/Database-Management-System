
# coding: utf-8

# In[62]:

import numpy as np
import random
import string
import re
def build_matrix(text, mat):
    text = re.sub("[^a-z ]+", "", text)
    #print(text)
    word_list = list(text.split())
    #print(word_list)
    print(text)
    corrupt=[]
    #corrupt_text
    for j in range(len(text)):
        letter=text[j]
        #for i in range(26):
            #if states[i]==str(first_letter):
        if letter==' ':
            corrupt.append(' ')
            continue
        else:  
            k= random.uniform(0, 1)
            if k<0.2:
                values= mat[letter]
                random_index=random.randint(0, len(values)-1)
                corrupt.append(values[random_index])
            else:
                corrupt.append(letter)
    print(str(corrupt))
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
    print(states)

    for j in range(len(word_list)):
        word=word_list[j]
        #print(word)
        first_letter=word[0]
        for i in range(26):
            if states[i]==str(first_letter):
                #print('hi')
                state_counter[i]=state_counter[i]+1
    for i in range(26):
        start_probability[i]=float(state_counter[i]/26)
    print(start_probability)
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
    #print(transition_counter)  
    transition_probability[np.isnan(transition_probability)] = 0
    #print(transition_probability)  
    
    #generation probability
    correct=list(text)
    print(correct)
    print(corrupt)
    for i in range(len(correct)):
        if (correct[i]==" "):
            continue
        else:
            r=states.index(correct[i])
            w=states.index(corrupt[i])
            generation_counter[r][w]=generation_counter[r][w]+1
            
    #print(generation_counter)
    for i in range(26):
        total=np.sum(generation_counter,axis=1)
    for i in range(26):   
        for j in range(26):
            generation_probability[i][j]=float(generation_counter[i][j]/total[i])
    #implement Viterbi
    emission_probability = np.zeros((26, 26))
    emission_state = np.zeros((26, 1))
    test=list('an ruya kove sinner lpcation')
    for i in range(26):
        #print(generation_probability[i][states.index(test[0])])
        #print(start_probability[i])
        emission_probability[i][states.index(test[0])]= generation_probability[i][states.index(test[0])]*start_probability[i]
    print(emission_probability)
    
    
    
        
    


# In[63]:

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


# In[56]:




# In[57]:




# In[ ]:




# In[ ]:




# In[ ]:



