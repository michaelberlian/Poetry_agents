# the main frame work of this code is taken from class COMP3004 - Designing Intelligent Agents
import tkinter as tk
import random
from grammar import anCorrector, mistypeCorrector, determinerCorrector
from addnremove import addAdjectives,addMetaphors,removeAdjectives,removeMetaphors,closerLength
from beautiful import makeTwoLinesRhyme,alliteration

class Blackboard:

    def __init__(self, counter):
        self.counter = counter
        self.window = tk.Tk()
        self.window.resizable(False,False)
        self.canvas = tk.Canvas(self.window,width=500,height=150)
        self.canvas.pack()

        self.lines = []
        self.lines.append([50,50, \
                           "he was a good guy","l0"])
        self.lines.append([50,100, \
                           "nothing more can be asked","l1"])
        for ll in self.lines:
            self.canvas.create_text(ll[0],ll[1],text=ll[2],tags=ll[3], anchor=tk.W)
        self.agentList = [anCorrector,mistypeCorrector,determinerCorrector,addAdjectives,addMetaphors,removeAdjectives,removeMetaphors,closerLength,makeTwoLinesRhyme,alliteration]
        
    def run(self):
        print("*** in run")
        ag = random.choice(self.agentList)
        print (ag)
        self.lines = ag(self.lines)
        self.canvas.delete("all")
        for ll in self.lines:
            self.canvas.create_text(ll[0],ll[1],text=ll[2],tags=ll[3],anchor=tk.W)
        self.counter -= 1
        if self.counter > 0 :
            self.canvas.after(2000,Blackboard.run,self)
        else :
            print (self.lines[0][2])
            print (self.lines[1][2])
            self.window.quit

    def main(self):
        self.run()
        self.window.mainloop()
    

bb = Blackboard(7)
bb.main()

# close the TK window when it stop running to continue to the next part

# bb = Blackboard(12)
# bb.main()
