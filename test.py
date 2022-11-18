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


length = [] #Estimated Length to Drone

def main():
    
    #Initialize Radar and Session
    #args = et.a111.ExampleArgumentParser().parse_args()
    #et.utils.config_logging(args)
    args = Namespace(serial_port='/dev/cu.usbserial-00073', socket_addr=None, spi=False, sensors=[1], verbose=False, debug=False, quiet=False) # Mac
    #args = Namespace(serial_port='COM3', socket_addr=None, spi=False, sensors=[1], verbose=False, debug=False, quiet=False) #Windows
    
    client = et.a111.Client(**et.a111.get_client_args(args))

    client.squeeze = False

    sensor_config = et.a111.EnvelopeServiceConfig()
    sensor_config.sensor = args.sensors
    sensor_config.range_interval = [0.2,3.0]
    sensor_config.profile = sensor_config.Profile.PROFILE_2
    sensor_config.hw_accelerated_average_samples = 5
    sensor_config.downsampling_factor = 2

    session_info = client.setup_session(sensor_config)
    print("Session info:\n", session_info, "\n")

    #Figure and Plot Creation
    xlist = np.linspace(0,100)
    ylist = np.linspace(0.2,3.0)
    fig, ax = plt.subplots()
    line, = ax.plot(xlist, ylist, color="white")

    plt.title("1 Dimensional Drone Flight", fontsize=20)
    plt.xlabel("Time (s)")
    plt.ylabel("Distance (m)")
    plt.ion()
    plt.show()


    #Draw Figure to window
    #fig_gui = draw_figure(window['-graph-'].TKCanvas, fig)

    #First Time Variable Creation
    iter = 0 #iterations
    frq = 0.2 #Frequency If we use time
    tlist = [] #Time History

    #Session Start
    client.start_session()

    interrupt_handler = et.utils.ExampleInterruptHandler()
    print("Press Ctrl-C to end session\n")


    depths = et.a111.get_range_depths(sensor_config, session_info)

    while not interrupt_handler.got_signal:
        #Data Collection
        info, data = client.get_next()
        index = np.argmax(data)
        dist = depths[index]

        print(f'The distance from the radar to the target is: {round(dist, 3)} m')
        #Data Storing And Plotting
        ax.plot(iter, dist, '.', color="orange", linewidth='0.1', label='Radar Points') #Plot time and data point
        fig.canvas.draw() #Draw Data
        fig.canvas.flush_events() #Wait until Drawn
        length.append(dist)
        tlist.append(iter)
        iter += 1 #Update Time/Iteration interval

    print("Disconnecting...")
    client.disconnect()

    #When Done Collecting Data
    ax.clear()
    ax.plot(tlist, length, 'r+', label='Noise', linewidth=0.2)
    ax.set_title("Drone movement + Noise")
    fig.canvas.draw()


if __name__ == "__main__":
    main()