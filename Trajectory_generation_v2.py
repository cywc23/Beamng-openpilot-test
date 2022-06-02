from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import datetime

LAND_WIDTH = 3.5

long_position = np.random.rand()


long_v = np.random.rand()*20 + 13 # 13~33 m/s  46.8~118.8 km/h

lat_v_max = np.random.rand()*3 + 0.5 # 0.5~3.5 m/s

lat_a = np.random.rand()*6 + 3 # 3~9 m/s^2

deviation_after = np.random.rand()*2 - 1 #lane deviation after

deviation_before = np.random.rand()*2 - 1 #lane deviation before

long_pos_1 = np.random.rand()*40 + 10 #where to start turnning

print("long_v", long_v)

delta_t = 0.05
sim_time = 8

x_loc_list = list()
y_loc_list = list()
time_list = list()

x_loc = 0
y_loc = 0 + deviation_before
x_loc_list.append(x_loc)
y_loc_list.append(y_loc)

lat_v = 0
y_delta = 0
stage = 0
count = 0

plt.plot([-5, long_v*(sim_time+1)],[-1.75,-1.75],"-b")
plt.plot([-5, long_v*(sim_time+1)],[1.75,1.75],"-b")
plt.plot([-5, long_v*(sim_time+1)],[1.75*3,1.75*3],"-b")
for t in range(1,int(sim_time/delta_t)):
    t = t * delta_t
    time_list.append(t)

    if stage == 0 and x_loc > long_pos_1:
        stage = 1
        plt.plot(x_loc,y_loc,".b",3)

    if stage == 1 and 3.5 - abs(y_loc) < y_delta + deviation_after:
        stage = 2
        lat_a *= -1
        # print("stage 2")

    if stage == 2 and lat_v < 0:
        lat_a = 0
        lat_v = 0
        print(y_loc)
        plt.plot(x_loc,y_loc,".b",3)
        stage = 3

    if stage == 3:
        count += 1

    if count > 20:
        break

    x_loc = x_loc + long_v * delta_t
    y_loc = y_loc + lat_v * delta_t

    x_loc_list.append(x_loc)
    y_loc_list.append(y_loc)

    if stage > 0:

        lat_v += lat_a * delta_t
        lat_v = min(max(-lat_v_max,lat_v),lat_v_max)

    # time for turnning back
    if y_loc > (LAND_WIDTH + deviation_after + deviation_before)/2 and y_delta == 0:
        y_delta = abs(y_loc)
        # print("y_delta", y_delta)

    if lat_v == lat_v_max and y_delta == 0:
        # print("lat_v_max", lat_v_max)
        y_delta = abs(y_loc)
        # print("y_delta", y_delta)


    # plt.plot(x_loc_list,y_loc_list,"-b")
    plt.plot(x_loc,y_loc,".r",1)
    plt.xlim((-5,long_v*(sim_time+1)))
    plt.ylim((-8,8))
    plt.pause(delta_t)
    

plt.show()

name = ["x", "y"]
to_csv = np.array([x_loc_list,y_loc_list])

data = pd.DataFrame(columns=name,data=to_csv.T)

save_name = str(datetime.datetime.now())[:-7]

save_name = save_name.replace(" ", "_").replace(":", "")

# data.to_csv("D:\\UVA\\2022 Spring\\cs8501\\Final Project\\Generated Trajectory\\" \
    # + save_name + ".csv")