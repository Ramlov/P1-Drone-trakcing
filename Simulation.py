#Version 1.1 Noise Update
#import libraries
from multiprocessing.connection import wait
from re import T
from tkinter import Y
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
t = 0.5
dronelistx = []
dronelisty = []




#-----------------------------------#
            #Functions
#-----------------------------------#
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

    return xpos, ypos, ax, ay


def noise(xpos, ypos, mu, sigma):
        '''Generate Noise'''
        #Define seed and variable
        random.seed(512)
        x_list = []
        y_list = []

        #Noise Generation
        for l in range(len(xpos)):
            x_list.append(xpos[l]+(np.random.normal(mu, sigma))) # Random seed
        
        for k in range(len(ypos)):
            y_list.append(ypos[k]+(np.random.normal(mu, sigma))) #Random seed

        print(len(x_list))
        return(x_list, y_list)


def algorithm(x_mes, y_mes, t_end, t):
    #Estimated and Predicted Position, Velocity, and Acc Variable Creation
    x_est = []
    xv_est = []
    xa_est = []
    pre_x = x_mes[0]
    pre_xv = 0
    pre_xa = 0

    y_est = []
    yv_est = []
    ya_est = []
    pre_y = y_mes[0]
    pre_yv = 0
    pre_ya = 0

    #Alpha-Beta-Gamma Filter values
    a = 0.5
    b = 0.4
    g = 0.1

    #Calc Estimation
    for i in range(1,t_end):
        x_est.append(pre_x + a*(x_mes[i] - pre_x))
        xv_est.append(pre_xv + b*((x_mes[i] - pre_x)/t))
        xa_est.append(pre_xa + g*((x_mes[i] - pre_x)/0.5*t**2))
        
        pre_x = x_est[-1] + xv_est[-1]*t + 0.5*xa_est[-1]* t**2
        pre_xv = xv_est[-1] + xa_est[-1]*t 
        pre_xa = xa_est[-1]
        
        y_est.append(pre_y + a*(y_mes[i] - pre_y))
        yv_est.append(pre_yv + b*((y_mes[i] - pre_y)/t))
        ya_est.append(pre_ya + g*((y_mes[i] - pre_y)/0.5*t**2))
        
        pre_y = y_est[-1] + yv_est[-1] + 0.5*ya_est[-1]
        pre_yv = yv_est[-1] + ya_est[-1] 
        pre_ya = ya_est[-1]
    
    return(x_est, y_est)


#-----------------------------------#
        #Animation and Plotting
#-----------------------------------#

def animate(xpos, ypos, x_mes, y_mes, algox, algoy, t_end, window):
    #List to Array conversion
    npxpos = np.array(xpos)
    npypos = np.array(ypos)
    xposnew = np.array([])
    yposnew = np.array([])

    #Figure and Plot Creation
    fig, axi = plt.subplots()
    axi.set_facecolor('#324e7b')
    fig.set_facecolor('#324e7b')
    axi.set_ylabel('Y-Meters', color='white')
    axi.set_xlabel('X-Meters', color='white')
    axi.set_title('2 Dimensional Drone Flight', fontsize=20, color='white')

    for xtick in axi.get_xticklabels():         
        xtick.set_color('white')     
    for ytick in axi.get_yticklabels():        
        ytick.set_color('white')
    line1, = axi.plot(npxpos, npypos, color='white')

    #plt.title("2 Dimensional Drone Flight", fontsize=20)
    #plt.xlabel("")
    #plt.ylabel("")

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
    
    #Plot noise with graph
    axi.plot(x_mes, y_mes, 'r+', label='Noise', linewidth=0.3)
    axi.set_title("Drone movement + Noise")
    fig.canvas.draw()

    #Plot Alpha-Beta-Gamma estimate
    axi.plot(algox, algoy, label='Filter', color='green')
    axi.set_title("Drone Flight with Noise and Estimated Position")
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
sg.theme("DarkBlue12")
 
options=[
        [sg.Frame('Choose your settings', [[sg.Text('Mean (Gaussian Distribution)'), sg.Slider(orientation ='horizontal', key='mean', range=(0,10))],
                                          [sg.Text('Standard Deviation'), sg.Input('10',key='-SD-', size=(9, 1))]], border_width=3)],
        [sg.Button('Submit', font=('Times New Roman',12))],
        [sg.Text('')], [sg.Text('')], [sg.Text('')], [sg.Text('')], [sg.Text('')],
        [sg.Text('')], [sg.Text('')], [sg.Text('')], [sg.Text('')], [sg.Text('')],
        [sg.Text('')], [sg.Text('')], [sg.Text('')], [sg.Text('')], [sg.Text('')],
        [sg.Frame('Datadump',[[sg.Text(' ', key='-AX-')],
                              [sg.Text(' ', key='-AY-')],
                             [sg.Text(' ', key='-PLACE-')]])]
        ]


#Creating the choices frame
choices = [[sg.Frame('Simulation settings', layout= options, expand_y=True)]]


items_chosen = [[sg.Text('Simulering', font=('Times New Roman', 25))],
                [sg.Graph(canvas_size=(600,463),
                            graph_bottom_left=(0,0),
                            graph_top_right=(600,463),
                            key = '-graph-')]]
              
# Create layout with two columns using precreated frames
layout = [[sg.Column(choices, element_justification='c', vertical_alignment='top'), 
            sg.Column(items_chosen, element_justification='c')]]

#Window
window = sg.Window('Drone Tracking Algorithm', layout, grab_anywhere=True)


#Start GUI Loop
while True:
    event, values = window.read() #Read Events
    if event == None or event == 'Exit': #If window is closed then break
        break

    if event == 'Submit': #Make Graph
        if fig_gui != None:
            delete_fig(fig_gui)

        dronelistx, dronelisty, ax, ay = movement(0, 0, 0, 0, t_end)
        x_mes, y_mes = noise(dronelistx, dronelisty, int(values['mean']), int(values['-SD-']))


        algox, algoy = algorithm(x_mes, y_mes, t_end, t)

        #Draw Graph
        fig_gui = animate(dronelistx, dronelisty, x_mes, y_mes, algox, algoy, t_end, window)
        window['-AX-'].update(value=f'Acceleration X-value: {ax}')
        window['-AY-'].update(value=f'Acceleration Y-value: {ax}')
