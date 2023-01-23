#Version 1.1 Noise Update
#import libraries
import numpy as np
from random import random
import random


#Variables

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
        xs = xs + vx + 0.5* ax
        ys = ys + vy + 0.5* ay
    
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


def noise(xpos, ypos, mu):
    '''Generate Noise'''
    #Define seed and variable
    x_list = []
    y_list = []

    #Noise Generation
    for l in range(len(xpos)):
        #Calculate Distance to drone, and the relative deviation
        dist = np.sqrt((xpos[l])**2 + (ypos[l])**2)
        sigma = (dist/8) * 0.08 #Increment the deviance by 8cm for every 8 meter

        #Generate Noise
        x_list.append(xpos[l]+(np.random.normal(mu, sigma))) #Append Noise on x
        y_list.append(ypos[l]+(np.random.normal(mu, sigma))) #Append Noise on y

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
        xa_est.append(pre_xa + g*((x_mes[i] - pre_x)/(0.5*t**2)))
        
        pre_x = x_est[-1] + xv_est[-1]*t + 0.5*xa_est[-1]* t**2
        pre_xv = xv_est[-1] + xa_est[-1]*t 
        pre_xa = xa_est[-1]
        
        y_est.append(pre_y + a*(y_mes[i] - pre_y))
        yv_est.append(pre_yv + b*((y_mes[i] - pre_y)/t))
        ya_est.append(pre_ya + g*((y_mes[i] - pre_y)/(0.5*t**2)))
        
        pre_y = y_est[-1] + yv_est[-1] + 0.5*ya_est[-1]
        pre_yv = yv_est[-1] + ya_est[-1] 
        pre_ya = ya_est[-1]
    
    return(x_est, y_est)


