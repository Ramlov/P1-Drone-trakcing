#import libraries
from multiprocessing.connection import wait
import numpy as np
import math
from random import random
import random
import matplotlib 
import matplotlib.pyplot as plt
import time
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PySimpleGUI as sg

matplotlib.use("TkAgg")

#Variables
t_end = 100
dronelistx = []
dronelisty = []


#Functions
def movement(xs, ys, vx, vy, t_end):
    #Define Lists
    xpos = []
    ypos = []

    #How many times to change direction (4 cap)
    change = []
    rand = random.choice([2,4])
    print("rand: ", rand)
    for i in range(rand):
        change.append((t_end/rand)*i)
    
    #X and y Acceleration and velocity
    ax = 0
    ay = 0

    for t in range(t_end): #Generate Values based on the iterations of radar readings
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

        #Change acceleration based on the kinetic limits of the drone.
        if t in change:
            print("change acc", t)
            ax = (np.random.randint(-15, 15, 1) / 10)
            ay = (np.random.randint(-15, 15, 1) / 10)
            print("AX and AY: ", ax, ay)

    return xpos, ypos



def noise(xpos, ypos, spread, howmuch):
        '''Generate Noise'''
        random.seed(512)
        test = []
        test1 = []
        for m in range(howmuch):
            for l in range(len(xpos)):
                test.append(xpos[l-1]+(random.random()*spread)) # Random seed
            
            for k in range(len(ypos)):
                test1.append(ypos[k-1]+(random.random()*spread)) #Random seed

        for m in range(howmuch):
            for l in range(len(xpos)):
                test.append((xpos[l-1]+(random.random()*spread)*-1)) # Random seed
            
            for k in range(len(ypos)):
                test1.append((ypos[k-1]+(random.random()*spread)*-1)) #Random seed

        return(test, test1)



def animate(xpos, ypos, test, test1, t_end, window):
    #List to Array conversion
    npxpos = np.array(xpos)
    npypos = np.array(ypos)
    xposnew = np.array([])
    yposnew = np.array([])

    #Figure and Plot Creation
    fig, axi = plt.subplots()
    line1, = axi.plot(npxpos, npypos)

    plt.title("2 Dimensional Drone Flight", fontsize=20)
    plt.xlabel("X-Meters")
    plt.ylabel("Y-Meters")

    #Update plot on call
    plt.ion()

    #Draw Figure to window
    fig_gui = draw_figure(window['-graph-'].TKCanvas, fig)

    for _ in range(t_end):
        #Plot and Update Graph
        xposnew = np.append(xposnew, xpos[_])
        yposnew = np.append(yposnew, ypos[_])
        line1.set_xdata(xposnew)
        line1.set_ydata(yposnew)

        fig.canvas.draw() #Draw updated values
        fig.canvas.flush_events() #Run Gui events, loops until processing is finished
    
    axi.plot(test, test1, 'r+', label='Noise')
    axi.set_title("Drone movement + Noise")
    fig.canvas.draw()

    #Turn off Autodisplay
    plt.ioff()

    return(fig_gui)





#-----------------------------------#
                #GUI
#-----------------------------------#

#GUI Functions
def draw_figure(canvas, figure): #Figure on canvas
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
    return figure_canvas_agg


def delete_fig(fig): #Delete or update figure
    fig.get_tk_widget().forget()
    plt.close('all')

#Var
fig_gui = None

#Theme
sg.theme('DarkGrey4')  
layout = [
            [sg.Button('Lav graf',  key='-MAKE-')],
            [sg.Text('Hvor stor afspredelse?'), sg.Input('15', key='-SPREAD-')],
            [sg.Text('Hvor meget støj'),sg.Input('1', key='-HOWMUCH-')],
            [sg.Canvas(key = '-graph-')],
        ]


#Window
window = sg.Window('Drone Tracking Algorithm', layout, grab_anywhere=True)


#Start GUI Loop
while True:
    event, values = window.read() #Read Events

    if event == None or event == 'Exit': #If window is closed then break
        break

    if event == '-MAKE-': #Make Graph
        if fig_gui != None:
            delete_fig(fig_gui)

        dronelistx, dronelisty = movement(0, 0, 0, 0, t_end)

        test, test1 = noise(dronelistx, dronelisty, int(values['-SPREAD-']), int(values['-HOWMUCH-']))

        #Draw Graph
        fig_gui = animate(dronelistx, dronelisty, test, test1, t_end, window)