from djitellopy import Tello
import PySimpleGUI as sg
import time

tello = Tello()

tello.connect()

layout = [[sg.Text('Tello Drone')],         
            [sg.Button('TAKEOFF', key='-TAKEOFF-')],
            [sg.Button('LAND', key='-LAND-')],
            [
                sg.Slider(range=(20,300), default_value=20, size=(50,5), orientation='horizontal', key='-HEIGHT-'),
                sg.Button('OK', key='-OK-')
            ],
            [sg.Button('Emergency', key='-EM-')]] 

window = sg.Window('TELLO DRONE', layout)    
 
 
while True:
    event, values = window.read()    
    if event == '-TAKEOFF-':
        tello.takeoff()
    elif event == '-LAND-':
        tello.land()
    elif event == '-OK-':
        tello.go("y = int(values['-HEIGHT-'])")
        '''height = 20
        if int(values['-HEIGHT-']) > height:
            tello.move_up(int(values['-HEIGHT-']))
            height = height+int(values['-HEIGHT-'])
            print(f'FLyver op, værdien af height er {height}')
        elif int(values['-HEIGHT-']) < height:
            tello.move_down(int(values['-HEIGHT-']))
            height = height-int(values['-HEIGHT-'])
            print(f'FLyver ned, værdien af height er {height}')'''
    elif event == '-EM-':
        tello.emergency
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
 
window.close()