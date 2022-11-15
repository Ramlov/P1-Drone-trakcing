# Copyright (c) 2022
#  ___            _         
# | _ \__ _ _ __ | |_____ __
# |   / _` | '  \| / _ \ V /
# |_|_\__,_|_|_|_|_\___/\_/ 

import acconeer.exptool as et
import numpy as np

def main():
    args = et.a111.ExampleArgumentParser().parse_args()
    et.utils.config_logging(args)

    client = et.a111.Client(**et.a111.get_client_args(args))

    client.squeeze = False

    sensor_config = et.a111.EnvelopeServiceConfig()
    sensor_config.sensor = args.sensors
    sensor_config.range_interval = [0.2, 5.0]
    sensor_config.profile = sensor_config.Profile.PROFILE_2
    sensor_config.hw_accelerated_average_samples = 5
    sensor_config.downsampling_factor = 2

    session_info = client.setup_session(sensor_config)
    print("Session info:\n", session_info, "\n")


    client.start_session()

    interrupt_handler = et.utils.ExampleInterruptHandler()
    print("Press Ctrl-C to end session\n")


    depths = et.a111.get_range_depths(sensor_config, session_info)

    while not interrupt_handler.got_signal:
        info, data = client.get_next()
        index = np.argmax(data)
        dist = depths[index] #Det er din data Christi <3
        #return dist
        #print(dist)

    print("Disconnecting...")
    client.disconnect()



if __name__ == "__main__":
    main()
