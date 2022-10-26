import matplotlib.pyplot as plt

x = []
predict_x = [30000, ]
v = []
predict_vel = []
acc = []
predict_acc = []


def acceleration_track_x(alpha, beta, gamma, x_0, v_c, a, t1, t2, z):
    global x, v, acc
    # The State Extrapolation Equations
    predict_pos = x_0 + v_c*(t2-t1) + a*(((t2-t1)**2)/2)
    predict_v = v_c + a * (t2-t1)
    predict_a = a
    print(f"Prediction for next position within 5 seconds: {predict_pos}")
    for i in range(len(z1)):
        # The radar meassures the aircraft range
        print(f"Step 1: {z[i]}")

        # Calculating the current estimate using the State Update Equation
        position_a = predict_pos + alpha*(z[i]-predict_pos)
        velocity1 = predict_v + beta*((z[i]-predict_pos)/(t2-t1))
        acceleration = predict_a + gamma*((z[i]-predict_pos)/(0.5*(t2-t1)**2))
        print('Step 2: New poistion {:.1f}, new velocity: {:.1f}, new acceleration: {:.1f}'
              .format(position_a, velocity1, acceleration))

        x.append(position_a)
        v.append(velocity1)
        acc.append(acceleration)

        # calc the next state estimate using State Extrapolation Equations
        predict_pos = position_a + velocity1 * \
            (t2-t1) + acceleration*(((t2-t1)**2)/2)
        predict_v = velocity1 + acceleration*(t2-t1)
        predict_a = acceleration
        print('Step 3: {:.1f}, {:.1f}, {:.1f}'.format(
            predict_pos, predict_v, predict_a))

        predict_x.append(predict_pos)
        predict_vel.append(predict_v)
        predict_acc.append(predict_a)

        print()

    return x, v, acc


z1 = [30160, 30365, 30890, 31050, 31785, 32215, 33130, 34510, 36010, 37265]
acceleration_track_x(0.5, 0.4, 0.1, 30000, 50, 0, 0, 5, z1)


fig, ax = plt.subplots()

ax.plot(x, label='Measured position')
ax.plot(z1, label='True value of position')
ax.plot(predict_x, label='predicted position')
ax.legend()
plt.xlabel('time[s]')
plt.ylabel('position[m]')
plt.title('poistion vs time')
plt.show()

# ax.plot(v, label='velocity')
# ax.plot(predict_vel, label )
# plt.xlabel('time[s]')
# plt.ylabel('velocity[m/s]')
# plt.title('velocity vs time')

# plt.plot(acc, label=u'position x')
# plt.xlabel('time[s]')
# plt.ylabel('acceleration[m/s2]')
# plt.title('acceleration vs time')
# plt.show()
