#import libraries
from multiprocessing.connection import wait
import numpy as np
import random
import matplotlib 
import matplotlib.pyplot as plt
import time
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PySimpleGUI as sg
matplotlib.use("TkAgg")

#Variables
t_end = 100

#GUI Functions
def draw_figure(canvas, figure): #Figure on canvas
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
    return figure_canvas_agg

def delete_fig(fig): #Delete or update figure
    fig.get_tk_widget().forget()
    plt.close('all')


#Create Graph Class
class graph():
    def __init__(self):
        #Coordinate Lists
        xpos = []
        ypos = []
        self.xpos = xpos
        self.ypos = ypos

    def reset(self):
        xpos = []
        ypos = []
        self.xpos = xpos
        self.ypos = ypos
        print(self.xpos, self.ypos)


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
            print(xs, ys)


            if t in change:
                ax = (np.random.randint(-15, 15, 1) / 10)
                ay = (np.random.randint(-15, 15, 1) / 10)

    def animate(self, t_end, window):
        #List to Array conversion
        npxpos = np.array(self.xpos)
        npypos = np.array(self.ypos)
        xposnew = np.array([])
        yposnew = np.array([])

        #Figure Creation
        fig = plt.figure()
        axi = fig.add_subplot(111)
        line1, = axi.plot(npxpos, npypos)

        plt.title("2 Dimensional Drone Flight", fontsize=20)
        plt.xlabel("X-Meters")
        plt.ylabel("Y-Meters")

        #Draw Figure to window
        fig_gui = draw_figure(window['-graph-'].TKCanvas, fig)

        #Update plot on call
        plt.ion()

        for _ in range(t_end):
            #Plot and Update Graph
            xposnew = np.append(xposnew, self.xpos[_])
            yposnew = np.append(yposnew, self.ypos[_])
            line1.set_xdata(xposnew)
            line1.set_ydata(yposnew)

            window.refresh()
        
        #Turn off plot on fig creation
        plt.ioff()

        return(fig_gui)


    def noise(self, spread, howmuch):
        '''Generate Noise'''
        random.seed(31212)
        test = []
        test1 = []
        for m in range(howmuch):
            for l in range(len(self.xpos)):
                test.append(self.xpos[l-1]+(random.random()*spread)) # Random seed
            
            for k in range(len(self.ypos)):
                test1.append(self.ypos[k-1]+(random.random()*spread)) #Random seed
        for m in range(howmuch):
            for l in range(len(self.xpos)):
                test.append((self.xpos[l-1]+(random.random()*spread)*-1)) # Random seed
            
            for k in range(len(self.ypos)):
                test1.append((self.ypos[k-1]+(random.random()*spread)*-1)) #Random seed
        
        
        fig, ax = plt.subplots()
        ax.plot(self.xpos, self.ypos, label='Movement')
        ax.plot(test, test1, 'r+', label='Noise')
        ax.set_title("Drone movement + Noise")
        ax.legend()
        return(fig)

graf = graph()


#----------GUI----------
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
        graf.reset()
        if fig_gui != None:
            delete_fig(fig_gui)
        graf.movement(0, 0, 0, 0, 100)

        #Draw Graph
        fig_gui = graf.animate(t_end, window)

        if fig_gui != None:
            delete_fig(fig_gui)

        #Draw Noise
        fig = graf.noise(int(values['-SPREAD-']), int(values['-HOWMUCH-']))
        fig_gui = draw_figure(window['-graph-'].TKCanvas, fig)