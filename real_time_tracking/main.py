# Copyright (c) 2022
#  ___            _         
# | _ \__ _ _ __ | |_____ __
# |   / _` | '  \| / _ \ V /
# |_|_\__,_|_|_|_|_\___/\_/ 
#   ___ _  _ ___ ___ ___ _____ ___   _   _  _ __  __ ___  __   __   __  
#  / __| || | _ \_ _/ __|_   _|_ _| /_\ | \| |  \/  / _ \/  \ /  \ /  \ 
# | (__| __ |   /| |\__ \ | |  | | / _ \| .` | |\/| \_, / () | () | () |
#  \___|_||_|_|_\___|___/ |_| |___/_/ \_\_|\_|_|  |_|/_/ \__/ \__/ \__/ 


import acconeer.exptool as et
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('tkagg')

class Namespace:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


def main(it):
    
    #Initialize Radar and Session
    #args = et.a111.ExampleArgumentParser().parse_args()
    #et.utils.config_logging(args)
    args = Namespace(serial_port='/dev/cu.usbserial-00073', socket_addr=None, spi=False, sensors=[1], verbose=False, debug=False, quiet=False)
    
    client = et.a111.Client(**et.a111.get_client_args(args))

    client.squeeze = False

    sensor_config = et.a111.EnvelopeServiceConfig()
    sensor_config.sensor = args.sensors
    sensor_config.range_interval = [0.3,3.0]
    sensor_config.profile = sensor_config.Profile.PROFILE_2
    sensor_config.hw_accelerated_average_samples = 5
    sensor_config.downsampling_factor = 1

    session_info = client.setup_session(sensor_config)
    print("Session info:\n", session_info, "\n")

    # Figure and Plot Creation
    xlist = np.linspace(0,it/5)
    ylist = np.linspace(0.2,1)
    fig, ax = plt.subplots()
    line, = ax.plot(xlist, ylist, color="white")

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

    for g in range(it):
        #Data Collection
        info, data = client.get_next()
        index = np.argmax(data)
        dist = depths[index]
        length.append(dist)
        tlist.append(iter)
        print("Measured Position: ", length[-1])
        print("\n")

        #Calc Position
        if iter == 0:
            x.append(dist)
        x, v, acc, predict_x, predict_vel, predict_acc = acceleration_track_x(0.5, 0.1, 0.01, 0, 0.2, x, v, acc, predict_x, predict_vel, predict_acc, dist)
        if iter == 0:
            x.remove(dist)

        iter += 1/5 #Update Time/Iteration interval

        #Data Storing And Plotting
        print("Timelist: ", tlist, "Calc Pos: ", x)
        ax.plot(iter, dist, '.', color="orange", linewidth='0.1', label='Radar Points') #Plot time and data point
        ax.plot(tlist, x, label="Calculated Position", color="blue")
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

length, tlist, x = main(100)