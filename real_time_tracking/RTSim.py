# Copyright (c) 2022
#  ___            _         
# | _ \__ _ _ __ | |_____ __
# |   / _` | '  \| / _ \ V /
# |_|_\__,_|_|_|_|_\___/\_/ 
#   ___ _  _ ___ ___ ___ _____ ___   _   _  _ __  __ ___  __   __   __  
#  / __| || | _ \_ _/ __|_   _|_ _| /_\ | \| |  \/  / _ \/  \ /  \ /  \ 
# | (__| __ |   /| |\__ \ | |  | | / _ \| .` | |\/| \_, / () | () | () |    -AKA Farmand
#  \___|_||_|_|_\___|___/ |_| |___/_/ \_\_|\_|_|  |_|/_/ \__/ \__/ \__/ 

import acconeer.exptool as et
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import timeit
matplotlib.use('tkagg')

class Namespace:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

def getbackground(client):
    background = []
    for i in range(5):
        info, data = client.get_next()
        background.append(data[0].tolist())
    res_lt = [] # declaration of the list  
    for x in range (0, len (background[0])):  
        res_lt.append( background[0][x] + background[1][x] + background[2][x] + background[3][x] + background[4][x])  

    newList = [x / 5 for x in res_lt]
    return newList

def main():
    
    #Initialize Radar and Session
    #args = et.a111.ExampleArgumentParser().parse_args()
    #et.utils.config_logging(args)
    args = Namespace(serial_port='COM3', socket_addr=None, spi=False, sensors=[1], verbose=False, debug=False, quiet=False)
    
    client = et.a111.Client(**et.a111.get_client_args(args))

    client.squeeze = False

    sensor_config = et.a111.EnvelopeServiceConfig()
    sensor_config.sensor = args.sensors
    sensor_config.range_interval = [0.2,4.0]
    sensor_config.profile = sensor_config.Profile.PROFILE_2
    sensor_config.hw_accelerated_average_samples = 5
    sensor_config.downsampling_factor = 1

    session_info = client.setup_session(sensor_config)
    print("Session info:\n", session_info, "\n")

    # Figure and Plot Creation
    fig, ax = plt.subplots()
    ax.set_xlim(0,10, auto=False)
    ax.set_ylim(-0.5, 4, auto=False)

    ax.legend()
    plt.xlabel('time[s]')
    plt.ylabel('position[m]')
    plt.title('poistion vs time')
    plt.ion()
    plt.show()


    #Draw Figure to window
    #fig_gui = draw_figure(window['-graph-'].TKCanvas, fig)

    #First Time Variable Creation
    iter = 0 #iterations
    frq = 0.2 #Frequency If we use time
    length = [] #Measured Length to Drone
    tlist = [] #Time History

    #Noise Filter
    x = []
    v = [0]
    acc = [0]
    predict_x = []
    predict_vel = []
    predict_acc = []

    #Session Start
    client.start_session()

    interrupt_handler = et.utils.ExampleInterruptHandler()
    print("Press Ctrl-C to end session\n")


    depths = et.a111.get_range_depths(sensor_config, session_info)
    background_data = getbackground(client)

    while not interrupt_handler.got_signal:
        #Data Collection
        info, data = client.get_next() #Get radar info
        starttime = timeit.default_timer()
        #Here we subtract the background noise
        array1 = np.array(data)
        array2 = np.array(background_data)
        subarray = np.subtract(array1, array2)

        #Plot Greatest noise point only if it exists
        max1 = np.amax(subarray) #Find highest dB reading and set it as out reading
        min1 = np.amin(subarray)

        #Find Length/Distance
        index = np.argmax(data)        
        dist = depths[index] #Find the corresponding distance with noise reading

        if max1 - min1 < 120:
            dist = -0.6*dist
        length.append(dist) #Add to Tracking History
        tlist.append(iter) #5hz. Add time point ever data read

        #Calc Position
        if iter == 0:
            x.append(dist) #Throw first data point as calculated. Gives us the option of a measured start point instead of chosen
        x, v, acc, predict_x, predict_vel, predict_acc = acceleration_track_x(0.5, 0.1, 0.01, 0, 0.2, x, v, acc, predict_x, predict_vel, predict_acc, dist) #Calc Movement
        if iter == 0:
            x.remove(dist) #Remove First measured point and replace with calculated

        iter += 1/5 #Update Time/Iteration interval

        #Data Storing And Plotting
        ax.plot(iter, dist, '.', color="orange", linewidth='0.1', label='Radar Points') #Plot time and data point
        if len(tlist) > 1:
            ax.plot(tlist[-2:], x[-2:], label="Calculated Position", color="blue") #Plot Last 2 points connected instead of whole plot. Optimizes the run
            if len(tlist) > 39:
                ax.set_xlim(tlist[-40], tlist[-1]) #Move the x axis in correspondance with time

        else:
            ax.plot(tlist, x, label="Calculated Position", color="blue") #Plot enitre list as only one point has been generated

        fig.canvas.draw() #Draw Data
        fig.canvas.flush_events() #Wait until Drawn

    print("Disconnecting...")
    client.disconnect()

    #When Done Collecting Data
    plt.ioff()
    ax.plot(iter, dist, '.', color="orange", linewidth='0.1', label='Radar Points') #Plot time and data point
    ax.plot(tlist, x, label="Calculated Position", color="blue")
    ax.set_title("Drone movement + Noise")
    fig.canvas.draw()
    plt.show()
    return(length, tlist, x)


#Alpha Beta Gamma Filter
def acceleration_track_x(alpha, beta, gamma, t1, t2, position, velocity, acceleration, predict_x, predict_vel, predict_acc, distance):
    # calc the next state estimate using State Extrapolation Equations
    predict_pos = position[-1] + velocity[-1] * (t2-t1) + acceleration[-1]*(((t2-t1)**2)/2)
    predict_v = velocity[-1] + acceleration[-1]*(t2-t1)
    predict_a = acceleration[-1]

    # Calculating the current estimate using the State Update Equation
    positionEst = predict_pos + alpha*(distance-predict_pos)
    velocityEst = predict_v + beta*((distance-predict_pos)/(t2-t1))
    AccEst = predict_a + gamma*((distance-predict_pos)/(0.5*(t2-t1)**2))

    position.append(positionEst)
    velocity.append(velocityEst)
    acceleration.append(AccEst)

    predict_x.append(predict_pos)
    predict_vel.append(predict_v)
    predict_acc.append(predict_a)

    return position, velocity, acceleration, predict_x, predict_vel, predict_acc

length, tlist, x = main()