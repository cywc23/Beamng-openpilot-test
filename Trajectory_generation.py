from matplotlib import pyplot as plt
import numpy as np
import time

LAND_WIDTH = 3.5
JERK_LAT = 0.3

# x_loc = []
# y_loc = []

long_position = np.random.rand()


long_v = np.random.rand()*20 + 13 # 13~33 m/s  46.8~118.8 km/h

lat_a_max = np.random.rand()*10 + 8 # 1~3.5 m/s

lat_v_max = np.random.rand()*2.5 + 2 # 1~3.5 m/s

lat_j = np.random.rand()*10 + 8 # 1~3.5 m/s

delta_t = 0.05

x_loc_list = list()
y_loc_list = list()

x_loc = 0
y_loc = 0
x_loc_list.append(x_loc)
y_loc_list.append(y_loc)


lat_a = 0
lat_v = 0

y_delta = 0


# lat_j = 3
stage = 0
for t in range(1,int(5/delta_t)):
    t = t * delta_t

    if stage == 0 and x_loc > 10:
        stage = 1
        plt.plot(x_loc,y_loc,".b",3)

    if stage == 1 and 3.5 - abs(y_loc) < y_delta:
        stage = 2
        lat_j *= -1
        lat_a *= -1
        print("stage 2")

    if stage == 2 and lat_v < 0:
        lat_j = 0
        lat_a = 0
        lat_v = 0
        print(y_loc)

    x_loc = x_loc + long_v * delta_t
    y_loc = y_loc + lat_v * delta_t

    x_loc_list.append(x_loc)
    y_loc_list.append(y_loc)

    if stage > 0:
        lat_a += lat_j * delta_t
        lat_a = min(max(-lat_a_max,lat_a),lat_a_max)

        lat_v += lat_a * delta_t
        lat_v = min(max(-lat_v_max,lat_v),lat_v_max)

    if y_loc > 1.6 and y_delta == 0:
        y_delta = abs(y_loc)
        print("y_delta", y_delta)

    if lat_v == lat_v_max and y_delta == 0:
        print("lat_v_max", lat_v_max)
        y_delta = abs(y_loc)
        print("y_delta", y_delta)


    # plt.plot(x_loc_list,y_loc_list,"-b")
    plt.plot(x_loc,y_loc,".r",1)
    plt.xlim((-5,long_v*(5+1)))
    plt.ylim((-5,15))
    plt.pause(delta_t)
    
    # time.sleep(0.1)
    #print(t)
    # if y_loc > 5:
    #     break

plt.plot(x_loc_list,y_loc_list,"-b")

print(y_loc)
plt.show()


