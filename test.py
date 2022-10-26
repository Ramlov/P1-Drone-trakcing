from multiprocessing.connection import wait
import numpy as np
import random
import matplotlib 
import matplotlib.pyplot as plt
import time
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PySimpleGUI as sg
matplotlib.use("TkAgg")



def movement(xs, ys, vx, vy, t_end):
    xpos = []
    ypos = []
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
        xpos.append(xs)
        ypos.append(ys)

        if t in change:
            ax = (random.randrange(-15, 15, 1) / 10)
            ay = (random.randrange(-15, 15, 1) / 10)
    print(xpos[20], ypos[21])



movement(0, 0, 0, 0, 100)

movement(0, 0, 0, 0, 100)

movement(0, 0, 0, 0, 100)

movement(0, 0, 0, 0, 100)

movement(0, 0, 0, 0, 100)

