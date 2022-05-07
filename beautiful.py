import random
import nltk
from nltk.corpus import wordnet as wn

# the function is inspired from class COMP3004 - Designing Intelligent Agents week 6 lab
# make the lines rhyme
def makeTwoLinesRhyme(lines):
    ll1 = lines.pop(random.randrange(len(lines)))
    ll2 = lines.pop(random.randrange(len(lines)))
    lastWord1 = nltk.word_tokenize(ll1[2])[-1]
    lastWord2 = nltk.word_tokenize(ll2[2])[-1]

    choice = random.choice([0,1])
    # choosing to rhyme which line
    if choice :
        lastWord = lastWord1
        lines.append([ll1[0],ll1[1],ll1[2],ll1[3]])
        newTokens = list(nltk.word_tokenize(ll2[2])[:-1])
        word = nltk.word_tokenize(ll2[2])[-1]
        lines.append([ll2[0],ll2[1],ll2[2],ll2[3]])
    else :
        lastWord = lastWord2
        lines.append([ll2[0],ll2[1],ll2[2],ll2[3]])
        newTokens = list(nltk.word_tokenize(ll1[2])[:-1])
        word = nltk.word_tokenize(ll1[2])[-1]
        lines.append([ll1[0],ll1[1],ll1[2],ll1[3]])

    # find the rhyming words
    entries = nltk.corpus.cmudict.entries()
    syllables = [(word, syl) for word, syl in entries if word == lastWord]
    rhymes = []
    #level = random.randrange(1,3)
    level = 2
    print (syllables)
    for (word, syllable) in syllables:
        rhymes += [word for word, pronunciation in entries \
                   if pronunciation[-level:] == syllable[-level:]]
    print("rhymes with ",lastWord)
    print(rhymes[0:10])

    # altering the words
    if rhymes:
        # newTokens = list(nltk.word_tokenize(ll2[2])[:-1])
        newToken = random.choice(rhymes)
        while (nltk.pos_tag([newToken])[0][1] != nltk.pos_tag([word])[0][1]):
            rhymes.remove(newToken)
            newToken = random.choice(rhymes)

        newTokens.append(newToken)
        newLine = " ".join(newTokens)
        lines[1][2] = newLine

    return lines

# make the line have similar first letter
def alliteration(lines): 
    # tokenizing and tagging words
    ll = lines.pop(random.randrange(len(lines)))
    tags = nltk.pos_tag(nltk.word_tokenize(ll[2]))
    words,tags = zip(*tags)
    words = list(words)
    tags = list(tags)

    # chose which word and letter to be followed
    chosen_word = random.choice(words)
    chosen_letter = chosen_word[0]

    for i in range (len(words)):
        # finding the list of synonyms 
        synonym = [syn for sets in wn.synsets(words[i]) for syn in sets.lemma_names()]

        if "NN" in tags[i]:
            word = wn.synsets(words[i], pos = wn.NOUN)
        elif "JJ" in tags[i]:
            word = wn.synsets(words[i], pos = wn.ADJ)
        elif "RB" in tags[i]:
            word = wn.synsets(words[i], pos = wn.ADJ)
        else:
            word = wn.synsets(words[i])

        if word:
            word = word[0]
            hyponym = [word for sets in word.hyponyms() for word in sets.lemma_names()]
            synonym += hyponym
        else:
            continue

        # if synonym exist find the word that has same letter at the beginning
        if synonym:
            eligibles = [word for word in synonym if word[0] == chosen_letter]
        else:
            continue
        
        # if similar word exist alter the words
        if eligibles:
            words[i] = random.choice(eligibles)
        else:
            continue    

    ll[2] = ' '.join(words)
    ll[2] = ' '.join(ll[2].split('_'))
    lines.append(ll)
    return lines

# testing purpose
# lines = []
# lines.append([50,50, \
#     "he was a good and nice person","l0"])
# lines.append([50,100, \
#     "nothing more can be asked","l1"])

# lines = makeTwoLinesRhyme(lines)
# lines = alliteration(lines)
# print (lines[0][2])
# print (lines[1][2])