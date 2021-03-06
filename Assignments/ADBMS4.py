
# coding: utf-8

# In[108]:

closed_class_stop_words = ['a','the','an','and','or','but','about','above','after','along','amid','among',                           'as','at','by','for','from','in','into','like','minus','near','of','off','on',                           'onto','out','over','past','per','plus','since','till','to','under','until','up',                           'via','vs','with','that','can','cannot','could','may','might','must',                           'need','ought','shall','should','will','would','have','had','has','having','be',                           'is','am','are','was','were','being','been','get','gets','got','gotten',                           'getting','seem','seeming','seems','seemed',                           'enough', 'both', 'all', 'your' 'those', 'this', 'these',                            'their', 'the', 'that', 'some', 'our', 'no', 'neither', 'my',                           'its', 'his' 'her', 'every', 'either', 'each', 'any', 'another',                           'an', 'a', 'just', 'mere', 'such', 'merely' 'right', 'no', 'not',                           'only', 'sheer', 'even', 'especially', 'namely', 'as', 'more',                           'most', 'less' 'least', 'so', 'enough', 'too', 'pretty', 'quite',                           'rather', 'somewhat', 'sufficiently' 'same', 'different', 'such',                           'when', 'why', 'where', 'how', 'what', 'who', 'whom', 'which',                           'whether', 'why', 'whose', 'if', 'anybody', 'anyone', 'anyplace',                            'anything', 'anytime' 'anywhere', 'everybody', 'everyday',                           'everyone', 'everyplace', 'everything' 'everywhere', 'whatever',                           'whenever', 'whereever', 'whichever', 'whoever', 'whomever' 'he',                           'him', 'his', 'her', 'she', 'it', 'they', 'them', 'its', 'their','theirs',                           'you','your','yours','me','my','mine','I','we','us','much','and/or'
                           ]


# In[109]:

#!/usr/bin/env python

"""Porter Stemming Algorithm
This is the Porter stemming algorithm, ported to Python from the
version coded up in ANSI C by the author. It may be be regarded
as canonical, in that it follows the algorithm presented in

Porter, 1980, An algorithm for suffix stripping, Program, Vol. 14,
no. 3, pp 130-137,

only differing from it at the points maked --DEPARTURE-- below.

See also http://www.tartarus.org/~martin/PorterStemmer

The algorithm as described in the paper could be exactly replicated
by adjusting the points of DEPARTURE, but this is barely necessary,
because (a) the points of DEPARTURE are definitely improvements, and
(b) no encoding of the Porter stemmer I have seen is anything like
as exact as this version, even with the points of DEPARTURE!

Vivake Gupta (v@nano.com)

Release 1: January 2001

Further adjustments by Santiago Bruno (bananabruno@gmail.com)
to allow word input not restricted to one word per line, leading
to:

release 2: July 2008
"""

import sys

class PorterStemmer:

    def __init__(self):
        """The main part of the stemming algorithm starts here.
        b is a buffer holding a word to be stemmed. The letters are in b[k0],
        b[k0+1] ... ending at b[k]. In fact k0 = 0 in this demo program. k is
        readjusted downwards as the stemming progresses. Zero termination is
        not in fact used in the algorithm.

        Note that only lower case sequences are stemmed. Forcing to lower case
        should be done before stem(...) is called.
        """

        self.b = ""  # buffer for word to be stemmed
        self.k = 0
        self.k0 = 0
        self.j = 0   # j is a general offset into the string

    def cons(self, i):
        """cons(i) is TRUE <=> b[i] is a consonant."""
        if self.b[i] == 'a' or self.b[i] == 'e' or self.b[i] == 'i' or self.b[i] == 'o' or self.b[i] == 'u':
            return 0
        if self.b[i] == 'y':
            if i == self.k0:
                return 1
            else:
                return (not self.cons(i - 1))
        return 1

    def m(self):
        """m() measures the number of consonant sequences between k0 and j.
        if c is a consonant sequence and v a vowel sequence, and <..>
        indicates arbitrary presence,

           <c><v>       gives 0
           <c>vc<v>     gives 1
           <c>vcvc<v>   gives 2
           <c>vcvcvc<v> gives 3
           ....
        """
        n = 0
        i = self.k0
        while 1:
            if i > self.j:
                return n
            if not self.cons(i):
                break
            i = i + 1
        i = i + 1
        while 1:
            while 1:
                if i > self.j:
                    return n
                if self.cons(i):
                    break
                i = i + 1
            i = i + 1
            n = n + 1
            while 1:
                if i > self.j:
                    return n
                if not self.cons(i):
                    break
                i = i + 1
            i = i + 1

    def vowelinstem(self):
        """vowelinstem() is TRUE <=> k0,...j contains a vowel"""
        for i in range(self.k0, self.j + 1):
            if not self.cons(i):
                return 1
        return 0

    def doublec(self, j):
        """doublec(j) is TRUE <=> j,(j-1) contain a double consonant."""
        if j < (self.k0 + 1):
            return 0
        if (self.b[j] != self.b[j-1]):
            return 0
        return self.cons(j)

    def cvc(self, i):
        """cvc(i) is TRUE <=> i-2,i-1,i has the form consonant - vowel - consonant
        and also if the second c is not w,x or y. this is used when trying to
        restore an e at the end of a short  e.g.

           cav(e), lov(e), hop(e), crim(e), but
           snow, box, tray.
        """
        if i < (self.k0 + 2) or not self.cons(i) or self.cons(i-1) or not self.cons(i-2):
            return 0
        ch = self.b[i]
        if ch == 'w' or ch == 'x' or ch == 'y':
            return 0
        return 1

    def ends(self, s):
        """ends(s) is TRUE <=> k0,...k ends with the string s."""
        length = len(s)
        if s[length - 1] != self.b[self.k]: # tiny speed-up
            return 0
        if length > (self.k - self.k0 + 1):
            return 0
        if self.b[self.k-length+1:self.k+1] != s:
            return 0
        self.j = self.k - length
        return 1

    def setto(self, s):
        """setto(s) sets (j+1),...k to the characters in the string s, readjusting k."""
        length = len(s)
        self.b = self.b[:self.j+1] + s + self.b[self.j+length+1:]
        self.k = self.j + length

    def r(self, s):
        """r(s) is used further down."""
        if self.m() > 0:
            self.setto(s)

    def step1ab(self):
        """step1ab() gets rid of plurals and -ed or -ing. e.g.

           caresses  ->  caress
           ponies    ->  poni
           ties      ->  ti
           caress    ->  caress
           cats      ->  cat

           feed      ->  feed
           agreed    ->  agree
           disabled  ->  disable

           matting   ->  mat
           mating    ->  mate
           meeting   ->  meet
           milling   ->  mill
           messing   ->  mess

           meetings  ->  meet
        """
        if self.b[self.k] == 's':
            if self.ends("sses"):
                self.k = self.k - 2
            elif self.ends("ies"):
                self.setto("i")
            elif self.b[self.k - 1] != 's':
                self.k = self.k - 1
        if self.ends("eed"):
            if self.m() > 0:
                self.k = self.k - 1
        elif (self.ends("ed") or self.ends("ing")) and self.vowelinstem():
            self.k = self.j
            if self.ends("at"):   self.setto("ate")
            elif self.ends("bl"): self.setto("ble")
            elif self.ends("iz"): self.setto("ize")
            elif self.doublec(self.k):
                self.k = self.k - 1
                ch = self.b[self.k]
                if ch == 'l' or ch == 's' or ch == 'z':
                    self.k = self.k + 1
            elif (self.m() == 1 and self.cvc(self.k)):
                self.setto("e")

    def step1c(self):
        """step1c() turns terminal y to i when there is another vowel in the stem."""
        if (self.ends("y") and self.vowelinstem()):
            self.b = self.b[:self.k] + 'i' + self.b[self.k+1:]

    def step2(self):
        """step2() maps double suffices to single ones.
        so -ization ( = -ize plus -ation) maps to -ize etc. note that the
        string before the suffix must give m() > 0.
        """
        if self.b[self.k - 1] == 'a':
            if self.ends("ational"):   self.r("ate")
            elif self.ends("tional"):  self.r("tion")
        elif self.b[self.k - 1] == 'c':
            if self.ends("enci"):      self.r("ence")
            elif self.ends("anci"):    self.r("ance")
        elif self.b[self.k - 1] == 'e':
            if self.ends("izer"):      self.r("ize")
        elif self.b[self.k - 1] == 'l':
            if self.ends("bli"):       self.r("ble") # --DEPARTURE--
            # To match the published algorithm, replace this phrase with
            #   if self.ends("abli"):      self.r("able")
            elif self.ends("alli"):    self.r("al")
            elif self.ends("entli"):   self.r("ent")
            elif self.ends("eli"):     self.r("e")
            elif self.ends("ousli"):   self.r("ous")
        elif self.b[self.k - 1] == 'o':
            if self.ends("ization"):   self.r("ize")
            elif self.ends("ation"):   self.r("ate")
            elif self.ends("ator"):    self.r("ate")
        elif self.b[self.k - 1] == 's':
            if self.ends("alism"):     self.r("al")
            elif self.ends("iveness"): self.r("ive")
            elif self.ends("fulness"): self.r("ful")
            elif self.ends("ousness"): self.r("ous")
        elif self.b[self.k - 1] == 't':
            if self.ends("aliti"):     self.r("al")
            elif self.ends("iviti"):   self.r("ive")
            elif self.ends("biliti"):  self.r("ble")
        elif self.b[self.k - 1] == 'g': # --DEPARTURE--
            if self.ends("logi"):      self.r("log")
        # To match the published algorithm, delete this phrase

    def step3(self):
        """step3() dels with -ic-, -full, -ness etc. similar strategy to step2."""
        if self.b[self.k] == 'e':
            if self.ends("icate"):     self.r("ic")
            elif self.ends("ative"):   self.r("")
            elif self.ends("alize"):   self.r("al")
        elif self.b[self.k] == 'i':
            if self.ends("iciti"):     self.r("ic")
        elif self.b[self.k] == 'l':
            if self.ends("ical"):      self.r("ic")
            elif self.ends("ful"):     self.r("")
        elif self.b[self.k] == 's':
            if self.ends("ness"):      self.r("")

    def step4(self):
        """step4() takes off -ant, -ence etc., in context <c>vcvc<v>."""
        if self.b[self.k - 1] == 'a':
            if self.ends("al"): pass
            else: return
        elif self.b[self.k - 1] == 'c':
            if self.ends("ance"): pass
            elif self.ends("ence"): pass
            else: return
        elif self.b[self.k - 1] == 'e':
            if self.ends("er"): pass
            else: return
        elif self.b[self.k - 1] == 'i':
            if self.ends("ic"): pass
            else: return
        elif self.b[self.k - 1] == 'l':
            if self.ends("able"): pass
            elif self.ends("ible"): pass
            else: return
        elif self.b[self.k - 1] == 'n':
            if self.ends("ant"): pass
            elif self.ends("ement"): pass
            elif self.ends("ment"): pass
            elif self.ends("ent"): pass
            else: return
        elif self.b[self.k - 1] == 'o':
            if self.ends("ion") and (self.b[self.j] == 's' or self.b[self.j] == 't'): pass
            elif self.ends("ou"): pass
            # takes care of -ous
            else: return
        elif self.b[self.k - 1] == 's':
            if self.ends("ism"): pass
            else: return
        elif self.b[self.k - 1] == 't':
            if self.ends("ate"): pass
            elif self.ends("iti"): pass
            else: return
        elif self.b[self.k - 1] == 'u':
            if self.ends("ous"): pass
            else: return
        elif self.b[self.k - 1] == 'v':
            if self.ends("ive"): pass
            else: return
        elif self.b[self.k - 1] == 'z':
            if self.ends("ize"): pass
            else: return
        else:
            return
        if self.m() > 1:
            self.k = self.j

    def step5(self):
        """step5() removes a final -e if m() > 1, and changes -ll to -l if
        m() > 1.
        """
        self.j = self.k
        if self.b[self.k] == 'e':
            a = self.m()
            if a > 1 or (a == 1 and not self.cvc(self.k-1)):
                self.k = self.k - 1
        if self.b[self.k] == 'l' and self.doublec(self.k) and self.m() > 1:
            self.k = self.k -1

    def stem(self, p, i, j):
        """In stem(p,i,j), p is a char pointer, and the string to be stemmed
        is from p[i] to p[j] inclusive. Typically i is zero and j is the
        offset to the last character of a string, (p[j+1] == '\0'). The
        stemmer adjusts the characters p[i] ... p[j] and returns the new
        end-point of the string, k. Stemming never increases word length, so
        i <= k <= j. To turn the stemmer into a module, declare 'stem' as
        extern, and delete the remainder of this file.
        """
        # copy the parameters into statics
        self.b = p
        self.k = j
        self.k0 = i
        if self.k <= self.k0 + 1:
            return self.b # --DEPARTURE--

        # With this line, strings of length 1 or 2 don't go through the
        # stemming process, although no mention is made of this in the
        # published algorithm. Remove the line to match the published
        # algorithm.

        self.step1ab()
        self.step1c()
        self.step2()
        self.step3()
        self.step4()
        self.step5()
        return self.b[self.k0:self.k+1]



# In[170]:

from collections import defaultdict
import string

def parseAbsDocs(filename):
    p = PorterStemmer()
    file = open("file.txt","w")
    with open(filename,"r") as f:
        documents_index = {}
        documents = defaultdict(int)
        document_no = 0
        abstract = []
        cont = False
        for line in f:
            if ".I" in line:
                if(document_no>0):
                    cont = False
                    for key, value in documents.items() :
                        file.write(str(document_no))
                        file.write(" ")
                        file.write(str(key))
                        file.write(" ")
                        file.write(str(value))
                        file.write("\n")
                    documents = defaultdict(int)
                    abstract = []
            
                words = line.split()
                document_no = int(words[1])
                #print("document" , document_no)
            elif ".T" in line:
                continue
               
            elif ".W" in line:
                cont=True
                continue
            elif cont==True:
                exclude = set(string.punctuation)
                exclude.discard('-')
                line = ''.join(ch for ch in line if ch not in exclude)
                line = ''.join(i for i in line if not i.isdigit())
                abs_words= line.split()
                for w in abs_words:
                    
                    predicate = lambda x:x not in string.punctuation
                    filter(predicate, w)
                    w=w.lower()
                    if w in closed_class_stop_words:
                        continue
                    if w in string.punctuation:
                        continue
                    if len(w)==1:
                        continue 
                    output = p.stem(w, 0,len(w)-1)  
                    #output = output.casefold()
                    #documents_index[output]=len(documents_index)+1
                    if output not in documents_index:
                        documents_index[output] = len(documents_index)+1
                        #print(output)
                        #print(documents_index[output])
            

                        

                    #print(documents_index)
                    #abstract.append(output)
                    #print(documents_index[output])
                    documents[output] +=1 
            else:
                continue
                    
    #(documents_index)
    #print(documents)
    
    
    file.close()
              
                
            
            


# In[171]:

print("Process Abstract Docs")
parseAbsDocs("cran.all.1400")
#print(absDocs)

 


# In[ ]:




# In[173]:

# returns document number which contains the query
def find(filename, query):
    result = []
    with open(filename,"r") as f:
        for line in f:
            words= line.split()
            if query == words[1]:
                result.append(int(words[0]))
    return result


# In[238]:

def evaluate_postfix(formula):
    OPERATORS = set(['AND', 'OR', 'NOT', '(', ')'])
    stack = []
    p = PorterStemmer()
    alln = set()
    for i in range(1,1401):
        alln.add(i)
    print(formula)
    for i in range(len(formula)):
        if formula[i] not in OPERATORS:
            k=formula[i]
            m = p.stem(k, 0,len(k)-1) 
            stack.append(m)
            #print(stack)
            if len(formula)==1:
                b = stack.pop()
                r = set(find("file.txt",b))
                stack.append(r)
                
        else:
            if formula[i] == 'NOT':
                b = stack.pop()
                c = alln.difference(b)
                stack.append(c)
                #print(stack)
                continue    
            o1 = stack.pop()
            #print(o1)
            if isinstance(o1, str):
                o1 = set(find("file.txt",o1))
            #print(o1)
            o2 = stack.pop()
            #print(o2)
            if isinstance(o2, str):
                o2 = set(find("file.txt",o2))
            #print(o2)
            if formula[i] == 'AND':
                c=o1.intersection(o2)
            else:
                c=o1.union(o2)
            stack.append(c)
            #print(stack)
    #print (stack[-1])
    return stack[-1]


# In[239]:

def findQuery(query):
    stack = []
    output = []
    OPERATORS = set(['AND', 'OR', 'NOT', '(', ')'])
    PRIORITY = {'AND':1, 'OR':1, 'NOT':2}
    Q = query.split()
    queryword=[]
    #print(Q)
    for i in range(len(Q)):
        predicate = lambda x:x not in string.punctuation
        filter(predicate, Q[i])
        if Q[i] in closed_class_stop_words:
            continue
        else:
            queryword.append(Q[i])
            
    #print(queryword)   
    for i in range(len(queryword)):
         
        if queryword[i] not in OPERATORS:
            word = queryword[i].lower()
            output.append(word)
        elif queryword[i] == '(':
            stack.append('(')
        elif queryword[i] == ")" :
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop() # pop '('
        else:
            while stack and stack[-1] != '(' and PRIORITY[queryword[i]] <= PRIORITY[stack[-1]]:
                output.append(stack.pop())
            stack.append(queryword[i])
            #while stack and stack[-1] != '(' :
             #   output.append(stack.pop())
            #stack.append(queryword[i])
            
    # leftover
    while stack: output.append(stack.pop())
    #print (output)
    return output


# In[245]:

res = findQuery(" VARY ")
result = evaluate_postfix(res)
print(sorted(result))




# In[ ]:




# In[ ]:




# In[ ]:



