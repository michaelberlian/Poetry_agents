the main file to be run is main.py 

addnremove.py contain several agents:
- closerLength : to make the lines have similar length (syllable)
- addAdjectives : adding adjective to the line
- addMetaphors : adding metaphor to the line, if applicable
- removeAdjectives : removing adjective from the line, if applicable
- removeMetaphors : removing metaphor from the line, if applicable

grammar.py contain several agents:
- anCorrector : correcting a/an
- determinerCorrector : adding/removing determiner to the nouns
- mistypeCorrector : correcting mistypings

beautiful.py contain several agents:
- makeTwoLinesRhyme : making lines having the same rhyme at the end, while also using the same word tag
- alliteration : altering the lines to have similar letter at start of each word

metaphor2 folder contain .txt and .py file necessary to find metaphors based on adjectives. This folder obtained from Class COMP3004 Designing Intelligent Agent lab Week 5. 
the alternative of obtaining metaphor is using link (http://bonnat.ucd.ie/jigsaw/). However, the website does not responding when creating this program. Therefore, the other alternative using metaphor2 folder was taken.

the program was tested using python3 version 3.9.7, with libraries:
- nltk version 3.6.5
- tkinter version 8.6
- numpy version 1.19.5