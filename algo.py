from random import random
import numpy as np
import math
import matplotlib.pyplot as plt
import random


class graph():
    def __init__(self):
        xpos = []
        ypos = []
        self.xpos = xpos
        self.ypos = ypos


    def movement(self, xs, ys, vx, vy, t_end):
        #Define Lists
        change = []
        for i in range(4):
            change.append((t_end/4)*i)


        
        #X and y Acceleration and velocity
        ax = 0
        ay = 0

        for t in range(t_end):
            #Calculate X Velocity
            vx = vx + (ax)
            if vx > 8: #Speed Threshold for X
                vx = 8
            else:
                if vx < -8:
                    vx = -8

            #Calculate Y Velocity
            vy = vy + (ay)
            if vy > 8: #Speed Threshold for Y
                vy = 8
            else:
                if vy < -8:
                    vy = -8

            #Calculate new position for x and y placement
            xs = xs + vx
            ys = ys + vy
            #Append Location
            self.xpos.append(xs)
            self.ypos.append(ys)

            if t in change:
                print("change acc", t)
                ax = (random.randrange(-15, 15, 1) / 10)
                ay = (random.randrange(-15, 15, 1) / 10)
                print(ax, ay)
        #plt.plot(self.xpos, self.ypos)
        #plt.show()

    def show_graph(self):
        '''Generate Graph'''
        #plt.show()

    def noise(self):
        '''Generate Noise'''
        random.seed(42)
        N = len(self.xpos)
        rang = range(N)
        new_xpos = [random.random() for i in rang]

        B = len(self.ypos)
        rangg = range(B)
        new_ypos = [random.random() for I in rangg]
        #print(new_xpos, new_ypos)
        for l in range(B):
            test = []
            test.append(self.ypos+random.random())
        
        for k in range(N):
            test1 = []
            test1.append(self.xpos+random.random())


        fig = plt.figure()
        fig, ax = plt.subplots()
        ax.plot(self.xpos, self.ypos, label='Movement')
        ax.plot(test, test1, 'r+', label='Noise')
        ax.set_title("My Plot")
        ax.legend()
        #plt.plot(new_xpos, new_ypos, 'r+')
        #plt.plot(self.xpos, self.ypos)
        plt.show()

graf = graph()

graf.movement(0, 0, 0, 0, 100)
graf.noise()
#plt.show()