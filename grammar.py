import nltk
import numpy as np
import random
from nltk.metrics.distance  import edit_distance
from nltk.metrics.distance import jaccard_distance
from nltk.util import ngrams
from nltk.corpus import words as c_words

# the function is inspired from class COMP3004 - Designing Intelligent Agents week 5 lab
# a/an corrector
def anCorrector(lines):
    lls = []
    for line in lines:
        lls.append(lines.pop(0))
    for ll in lls:
        newLine = ll[2]

        words = nltk.word_tokenize(newLine)
        
        # find the a and check it 
        indices = np.where(np.array(words) == "a")[0]
        for index in indices:
            if words[index+1][0] in 'aiueo':
                words[index] = 'an'

        # find the an and check it
        indices = np.where(np.array(words) == "an")[0]
        for index in indices:
            if not (words[index+1][0] in 'aiueo'):
                words[index] = 'a'

        newLine = ' '.join(words)
        lines.append([ll[0],ll[1],newLine,ll[3]])
    return lines

# a/an/the remover/adder
def determinerCorrector(lines):
    lls = []
    for line in lines:
        lls.append(lines.pop(0))
    for ll in lls:
        newLine = ll[2]
        words = nltk.word_tokenize(newLine)
        words_tag = nltk.pos_tag(words)
        words,tags = zip(*words_tag)
        words = list(words)
        tags = list(tags)
        
        # finding the noun
        indices = np.where(np.array(tags) == "NN")[0]
        for i in range (len(indices)):
            index = indices[i]
            # skip if determiner already exist
            if "DT" in tags[index-1] or "DT" in tags[index-2] or "PRP" in tags[index-1] or "PRP" in tags[index-2] or "IN" in tags[index-1]:
                continue
            else : 
                # adding the determiner
                if "JJ" in tags[index-1] or "VBN" in tags[index-1]:
                    add_index = index-1
                else :
                    add_index = index
                choice = random.choice([0,1])
                if choice :
                    words.insert(add_index, "a")
                else :
                    words.insert(add_index, "the")
                indices = [i+1 for i in indices]
        
        # finding the plural noun
        indices = np.where(np.array(tags) == "NNS")[0]
        for i in range (len(indices)):
            index = indices[i]

            # remove the wrong determinr 
            if ("JJ" in tags[index-1] or "VBN" in tags[index-1]) and (words[index-2] == 'a' or words[index-2] == 'an'):
                del words[index-2]
            elif  (words[index-1] == 'a' or words[index-1] == 'an'):
                del words[index-1]

        newLine = ' '.join(words)
        lines.append([ll[0],ll[1],newLine,ll[3]])
    return lines

# ref: https://www.geeksforgeeks.org/correcting-words-using-nltk-in-python/
# a function to fix mis typing 
def mistypeCorrector(lines):
    lls = []
    for line in lines:
        lls.append(lines.pop(0))
    for ll in lls:
        newLine = ll[2]
        words = nltk.word_tokenize(newLine.lower())
        correct_words = c_words.words()
        
        for i in range (len(words)):
            # check if the word exist in correct word dictionary
            if not (words[i] in correct_words):
                choice = random.choice([0,1])
                # find the closest word
                if choice :
                    temp = [(edit_distance(words[i], w),w) for w in correct_words if w[0]==words[i][0]]
                else :
                    temp = [(jaccard_distance(set(ngrams(words[i], 2)),
                                            set(ngrams(w, 2))),w)
                            for w in correct_words if w[0]==words[i][0]]
                if temp:
                    words[i] = sorted(temp, key = lambda val:val[0])[0][1]
    
        newLine = ' '.join(words)
        lines.append([ll[0],ll[1],newLine,ll[3]])
    
    return lines


# testing purpose
# lines = []
# lines.append([50,50, \
#     "he was an nice person","l0"])
# lines.append([50,50, \
#     "he was nice person","l0"])
# lines.append([50,50, \
#     "he was a nice persson","l0"])

# lines = anCorrector(lines)
# lines = determinerCorrector(lines)
# lines = mistypeCorrector(lines)
# print (lines[0][2])
# print (lines[1][2])