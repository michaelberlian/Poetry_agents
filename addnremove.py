import string
import nltk
import numpy as np
import random
from metaphor2.metaphor import metaphor,initialiseMetaphor
from nltk.util import ngrams
from nltk.corpus import brown

# function to count syllables if cmudict.entries do not have the word
def sylMake(words):

    if words in string.punctuation:
        return []

    index_a = list(np.where(np.array(list(words)) == "a")[0])
    index_i = list(np.where(np.array(list(words)) == "i")[0])
    index_u = list(np.where(np.array(list(words)) == "u")[0])
    index_e = list(np.where(np.array(list(words)) == "e")[0])
    index_o = list(np.where(np.array(list(words)) == "o")[0])
    index_y = list(np.where(np.array(list(words)) == "y")[0])
    indices = index_a + index_i + index_u + index_e + index_o + index_y 

    syl = []
    pre_index = 0
    indices = sorted(indices)
    for index in indices : 
        syl.append(words[pre_index:index])
        syl.append(words[index])
        pre_index = index+1
    syl.append(words[pre_index:])

    return syl

# function to remove a metaphor from a line
def removeMetaphor(line):
    # tokenizing and tagging the words
    tags = nltk.pos_tag(nltk.word_tokenize(line))
    words,tags = zip(*tags)
    words = list(words)
    tags = list(tags)

    # finding the start of a metaphor
    index_as = list(np.where(np.array(list(words)) == "as")[0])
    index_like = list(np.where(np.array(list(words)) == "like")[0])
    indices = index_as + index_like

    # choose one of the metaphor (if multiple exist)
    if indices:
        chosen_index = random.choice(indices)
    else:
        return line

    # deleting the metaphor
    del words[chosen_index]
    del tags[chosen_index]
    del words[chosen_index]
    del tags[chosen_index]

    # if the metaphor is more than 2 words long
    if chosen_index >= len(words)-1 :
        newLine = " ".join(words)
        return newLine

    while (tags[chosen_index+1] == "NN" or tags[chosen_index+1] == "NNS"):
        del words[chosen_index]
        del tags[chosen_index]
        if (chosen_index == len(words)-1):
            break

    newLine = " ".join(words)
    return newLine

# the function is inspired from class COMP3004 - Designing Intelligent Agents week 5 lab
# function to add a metaphor from a line
def addMetaphor(line):
    # initializing the metaphor
    rr, gg = initialiseMetaphor()

    # tokenizing and tagging the words
    tags = nltk.pos_tag(nltk.word_tokenize(line))
    words,tags = zip(*tags)
    words = list(words)
    tags = list(tags)

    # finding the adjectives to be used as metaphor base
    word_index = []
    for i in range (len(tags)):
        if tags[i] == "JJ" :
            word_index.append(i)
    
    # chose the adjective if multiple adjectives are availabel
    if word_index:
        chosen_index = random.choice(word_index)
        chosen_word = words[chosen_index]
    else:
        return line

    # find the metaphor
    new_metaphor = metaphor(chosen_word,rr,gg)

    # add the metaphor to the sentence if metaphor exist
    if new_metaphor:
        words.insert(chosen_index+1,new_metaphor)
        words.insert(chosen_index+1,random.choice(['as','like']))
        newLine = " ".join(words)
        return newLine
    else:
        return line

# the function is inspired from class COMP3004 - Designing Intelligent Agents week 7 lab
# function to remove an adjective from a line
def removeAdjective(line):
    #tokenizing and tagging the words
    tagged = nltk.pos_tag(nltk.word_tokenize(line))

    # finding existing adjectives in the sentence 
    adjList = []
    for idx,val in enumerate(tagged):
        if val[1]=="JJ":
            adjList.append(idx)
    print("Adjective List is ",adjList)

    # if adjective is exist on the sentence delete it (randomize if more than 1 adjective available)
    if adjList:
        del tagged[random.choice(adjList)]
    newLine = " ".join([ x[0] for x in tagged ])
    return newLine

# the function is inspired from class COMP3004 - Designing Intelligent Agents week 7 lab
# function to add an adjective from a line
def addAdjective(line):
    ## add lines here that:

    # tokenise ll[2], and store this in a variable called tokenized
    tokenized = nltk.word_tokenize(line)

    # part-of-speech tag the tokenized list, store this in a variable called tagged
    tagged = nltk.pos_tag(tokenized)

    # find the positions of nouns in the list
    words,tags = zip(*tagged)
    words = list(words)
    tags = list(tags)
    indices = np.where(np.array(tags) == "NN")[0]

    # if there are no nouns, return originalLines
    if len(indices) > 0 :
    # choose a random noun, store this in a variable called chosenNoun
    # store the position of that noun in the list (its index) in a variable called chosenNounPosition
        chosenNounPosition = random.choice(indices)
        chosenNoun = words[chosenNounPosition]
    else :
        return line

    ##now add the adjective
    bigrams = ngrams(brown.words(), 2)
    preWords = [ bg[0] for bg in bigrams if bg[1]==chosenNoun ]
    taggedPreWords = nltk.pos_tag(preWords)
    chosenPreWords = [ pw[0] for pw in taggedPreWords if (pw[1]=="JJ" or pw[1] == "VBN") ]

    #You can also experiment with checking for VBN or NN
    if not chosenPreWords:
        return line
    chosenDescriptor = random.choice(chosenPreWords)
    tokenized.insert(chosenNounPosition, chosenDescriptor)
    newLine = " ".join(tokenized)
    return newLine

# the syllable calculation is inspired from class COMP3004 - Designing Intelligent Agents week 5 lab
# an agent make the lines length (syllables) closer to each other, utilizing other function
def closerLength(lines):
    ll1 = lines.pop(0)
    ll2 = lines.pop(0)
    words1 = nltk.word_tokenize(ll1[2])
    words2 = nltk.word_tokenize(ll2[2])

    entries = nltk.corpus.cmudict.entries()
    syllables1 = []
    syllables2 = []

    # calculating the length of the line (syllables)
    for c_word in words1 : 
        syllables = [(word, syl) for word, syl in entries if word == c_word]
        if not syllables :
            syllables = [(c_word, sylMake(c_word))]
        # print (syllables)
        syllables1 += syllables[0]

    for c_word in words2 : 
        syllables = [(word, syl) for word, syl in entries if word == c_word]
        if not syllables :
            syllables = [(c_word, sylMake(c_word))]
        # print (syllables)
        syllables2 += syllables[0]

    # if the lines is equal the skipped
    if len(syllables1) == len(syllables2):
        lines.append(ll1)
        lines.append(ll2)
        return lines
    else :

        # deciding which line shorter or longer
        if len(syllables1) > len(syllables2): 
            longer = ll1
            shorter = ll2
            diff = len(syllables1) - len(syllables2)
        elif len(syllables1) < len(syllables2):
            longer = ll2 
            shorter = ll1 
            diff = len(syllables2) - len(syllables1)
        
        # if there are no adjective on longer word, shortening the line is unavailable
        enableReduce = False
        longer_words = nltk.word_tokenize(longer[2])
        longer_tags = nltk.pos_tag(longer_words)

        words,tags = zip(*longer_tags)
        longer_words = list(words)
        longer_tags = list(tags)

        if "JJ" in longer_tags:
            enableReduce = True

        # randomize between adding words to shorter lines or removing word to longer lines
        if enableReduce:
            choice = random.choice([0,1])
        else :
            choice = 0 

        if choice :
            lines.append(shorter)

            # shortening the longer line
            # if metaphor is available, removeing metaphor as the method to shortening the line, else remove available adjectives
            metaphor = False 
            if "as" in longer_words or "like" in longer_words:
                metaphor = True
            
            if metaphor :
                longer[2] = removeMetaphor(longer[2])
                lines.append(longer)
            else :
                longer[2] = removeAdjective(longer[2])
                lines.append(longer)
            print ('make it shorter')

        else :
            lines.append(longer)

            # longer the shorter line
            shorter_words = nltk.word_tokenize(shorter[2])
            shorter_tags = nltk.pos_tag(shorter_words)

            words,tags = zip(*shorter_tags)
            shorter_words = list(words)
            shorter_tags = list(tags)

            # if adjective available, create a metaphor, else add sensible adjectives
            if "JJ" in shorter_tags :
                shorter[2] = addMetaphor(shorter[2])
                lines.append(shorter)
            else:
                shorter[2] = addAdjective(shorter[2])
                lines.append(shorter)

            print ('make it longer')

        return lines

# an agent to remove a methaphor
def removeMetaphors(lines):
    ll = lines.pop(random.randrange(len(lines)))
    ll[2] = removeMetaphor(ll[2])
    lines.append(ll)
    return lines

# an agent to add a methaphor
def addMetaphors(lines):
    ll = lines.pop(random.randrange(len(lines)))
    ll[2] = addMetaphor(ll[2])
    lines.append(ll)
    return lines

# an agent to remove an adjective
def removeAdjectives(lines):
    ll = lines.pop(random.randrange(len(lines)))
    ll[2] = removeAdjective(ll[2])
    lines.append(ll)
    return lines
    
# an agent to add an adjective
def addAdjectives(lines):
    ll = lines.pop(random.randrange(len(lines)))
    ll[2] = addAdjective(ll[2])
    lines.append(ll)
    return lines

# testing purpose
# lines = []
# lines.append([50,50, \
#     "he was a good and nice person","l0"])
# lines.append([50,50, \
#     "he was a good person","l0"])
# lines.append([50,50, \
#     "he was a good and nice like a pin prick person","l0"])
# lines.append([50,100, \
#     "nothing more can be asked","l1"])

# lines = closerLength(lines)
# lines = addAdjectives(lines)
# lines = addMetaphors(lines)
# lines = removeAdjectives(lines)
# lines = removeMetaphors(lines)
# print (lines[0][2])
# print (lines[1][2])