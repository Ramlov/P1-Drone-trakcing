import numpy as np 


def test(n):
    l =  np.random.rand()
    return l


def x_y(nb):
    x_pos = []
    y_pos = []
    for n in range(nb):
        y = 1+np.random.rand()
        x_pos.append(n)
        y_pos.append(y)

    return y_pos, y_pos
        


print(x_y(100))






# x = np.random.uniform(a, b, antal_punkter)  # generér tilfældige x-koordinater
# y = np.random.uniform(0, m, antal_punkter)  # generér tilfældige y-koordinater





