from random import random
import numpy as np
import math
import random
import matplotlib 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PySimpleGUI as sg
matplotlib.use("TkAgg")
Debug = True

class graph():
    def __init__(self):
        xpos = []
        ypos = []
        self.xpos = xpos
        self.ypos = ypos

    def reset(self):
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
                
                ax = (random.randrange(-15, 15, 1) / 10)
                ay = (random.randrange(-15, 15, 1) / 10)
                if Debug == True:
                    print("change acc", t)
                    print(ax, ay)
        #plt.plot(self.xpos, self.ypos)

    def show_graph(self):
        '''Generate Graph'''
        #plt.show()

    def noise(self, spread, howmuch):
        '''Generate Noise'''
        random.seed(42)
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
        if Debug == True:
            print("Figuren er: ", fig)
        return(fig)
        #plt.show()

graf = graph()

#graf.movement(0, 0, 0, 0, 100)
#graf.noise()
#plt.show()



def draw_figure(canvas, figure): #Figure on canvas
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
    return figure_canvas_agg

def delete_fig(fig): #Delete or update figure
    fig.get_tk_widget().forget()
    plt.close('all')

sg.theme('DarkGrey4')  
layout = [
            [sg.Button('Lav graf',  key='-MAKE-')],
            [sg.Text('Hvor stor afspredelse?'), sg.Input('15', key='-SPREAD-')],
            [sg.Text('Hvor meget støj'),sg.Input('1', key='-HOWMUCH-')],
            [sg.Canvas(key = '-graph-')],
        ]

window = sg.Window('Drone Tracking Algorithm', layout, grab_anywhere=True)

fig_gui = None


while True:
    if Debug == True:
        print(fig_gui)
    event, values = window.read()
    if event == None or event == 'Exit':
        break
    if event == '-MAKE-':
        if fig_gui != None:
            delete_fig(fig_gui)
            if Debug == True:
                print(fig_gui)
        graf.reset()
        graf.movement(0, 0, 0, 0, 100)
        fig = graf.noise(int(values['-SPREAD-']), int(values['-HOWMUCH-']))
        fig_gui = draw_figure(window['-graph-'].TKCanvas, fig)