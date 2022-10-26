import numpy as np
import random
import matplotlib.pyplot as plt

v_x = np.array([100])
v_y = np.array([70])
x   = np.array([0])
y   = np.array([0])
x_mes = np.array([])
y_mes = np.array([])
t_m = 100

def movement(x_0, y_0, v_x0, v_y0, a_x, a_y):
    global v_x, v_y, x, y, x_mes, y_mes
    v_x = np.append(v_x, [v_x0 + a_x])
    v_y = np.append(v_y, [v_y0 + a_y])
    
    x_pos = x_0 + v_x[-1] 
    y_pos = y_0 + v_y[-1]
    
    x = np.append(x, [x_pos])
    y = np.append(y, [y_pos])
    
    x_mes = np.append(x_mes, [x_pos + random.randrange(-60,60)])
    y_mes = np.append(y_mes, [y_pos + random.randrange(-60,60)])


for i in range(t_m):
    movement(x[-1], y[-1], v_x[-1], v_y[-1], -2, -1)

a = 0.5
b = 0.4
g = 0.1
x_est = []
xv_est = []
xa_est = []
pre_x = x_mes[0]
pre_xv = 0
pre_xa = 0

y_est = []
yv_est = []
ya_est = []
pre_y = x_mes[0]
pre_yv = 0
pre_ya = 0

for i in range(1,100):
    x_est.append(pre_x + a*(x_mes[i] - pre_x))
    xv_est.append(pre_xv + b*(x_mes[i] - pre_x))
    xa_est.append(pre_xa + g*(x_mes[i] - pre_x))
    
    pre_x = x_est[-1] + xv_est[-1] + 0.5*xa_est[-1]
    pre_xv = xv_est[-1] + xa_est[-1] 
    pre_xa = xa_est[-1]
    
    y_est.append(pre_y + a*(y_mes[i] - pre_y))
    yv_est.append(pre_yv + b*(y_mes[i] - pre_y))
    ya_est.append(pre_ya + g*(y_mes[i] - pre_y))
    
    pre_y = y_est[-1] + yv_est[-1] + 0.5*ya_est[-1]
    pre_yv = yv_est[-1] + ya_est[-1] 
    pre_ya = ya_est[-1]



plt.plot(x,y)
plt.plot(x_mes,y_mes,'.')
plt.plot(x_est, y_est)
plt.show()