from random import random
import numpy as np
import math
import matplotlib.pyplot as plt
import random

'''
def algo(nb):
    xpos = []
    ypos = []
    for n in range(nb):
        y = math.sin(1) + 0.5*n
        if y < 0:
            y = -1*y
        xpos.append(n)
        ypos.append(y)
    
    print(xpos, "\n\n", ypos)
    plt.plot(xpos, ypos)
    plt.show()
'''

def movement(xs, ys, vx, vy, t_end):
    #Define Lists
    xpos = []
    ypos = []
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
        xpos.append(xs)
        ypos.append(ys)

        if t in change:
            print("change acc", t)
            ax = (random.randrange(-15, 15, 1) / 10)
            ay = (random.randrange(-15, 15, 1) / 10)
            print(ax, ay)

    plt.plot(xpos, ypos)
    plt.show()

movement(0, 0, 0, 0, 100)