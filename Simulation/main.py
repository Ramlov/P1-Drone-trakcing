from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PySimpleGUI as sg
import matplotlib 
import matplotlib.pyplot as plt
import numpy as np
import Simulation

matplotlib.use("TkAgg")

t_end = 100
t = 0.5


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
    axi.set_ylabel('Longitude', color='white')
    axi.set_xlabel('Latitude', color='white')
    #axi.set_title('2 Dimensional Drone Flight', fontsize=20, color='white')

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
    axi.plot(x_mes, y_mes, 'r+', label='Noise', linewidth=0.2)
    axi.set_title("Drone movement + Noise")
    fig.canvas.draw()

    #Plot Alpha-Beta-Gamma estimate
    axi.plot(algox, algoy, label='Filter', color='yellow')
    #axi.set_title("Drone Flight with Noise and Estimated Position")
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
sg.theme("DarkBlue11")
 
options=[
        [sg.Frame('Choose your settings', [[sg.Text('Mean (Gaussian Distribution)'), sg.Slider(orientation ='horizontal', key='mean', default_value=0, range=(-10,10))],
                                          [sg.Text('Bird Flocks'), sg.Checkbox(' ')]], border_width=3)],
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


items_chosen = [[sg.Text('2 Dimensional Drone Flight', font=('Times New Roman', 25))],
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

        dronelistx, dronelisty, ax, ay = Simulation.movement(0, 0, 0, 0, t_end)
        x_mes, y_mes = Simulation.noise(dronelistx, dronelisty, int(values['mean']))


        algox, algoy = Simulation.algorithm(x_mes, y_mes, t_end, t)

        #Draw Graph
        fig_gui = animate(dronelistx, dronelisty, x_mes, y_mes, algox, algoy, t_end, window)
        window['-AX-'].update(value=f'Acceleration X-value: {ax}')
        window['-AY-'].update(value=f'Acceleration Y-value: {ax}')
