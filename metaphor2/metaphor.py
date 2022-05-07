import random

def initialiseMetaphor():
    with open ("metaphor2/resp.txt", "r") as ff:
        respLines = ff.readlines()
    resp = {}
    for rl in respLines:
        rls = rl.split(",")
        if rls[0] not in resp:
            resp[rls[0]] = rls[1]
    with open ("metaphor2/gram.txt", "r") as ff:
        gramLines = ff.readlines()
    gram = {}
    for gl in gramLines:
        gls = gl.split(",")
        gram[gls[0]] = [x.strip() for x in gls[1:]]
    return resp, gram
    
def metaphor(word,resp,gram):
    answer = None
    if word in resp.keys():
        key = resp[word].strip()
        if key in gram.keys():
            possibles = gram[key]
            answer = random.choice(possibles)
    return answer

rr, gg = initialiseMetaphor()
# print(metaphor("mysterious",rr,gg))
