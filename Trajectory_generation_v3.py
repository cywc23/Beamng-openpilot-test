# generate trajectory for scenario use

from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import datetime

LAND_WIDTH = 3.5


def generate_traj(sim_time):
    long_position = np.random.rand()

    long_v = np.random.rand()*20 + 13 # 13~33 m/s  46.8~118.8 km/h

    lat_v_max = np.random.rand()*3 + 0.5 # 0.5~3.5 m/s

    lat_a = np.random.rand()*6 + 3 # 3~9 m/s^2

    deviation_after = np.random.rand()*2 - 1 #lane deviation after

    deviation_before = np.random.rand()*2 - 1 #lane deviation before

    long_pos_1 = np.random.rand()*40 + 50 #where to start turnning

    delta_t = 0.01
    sim_time = int(sim_time/100)

    x_loc_list = list()
    y_loc_list = list()

    x_loc = 0
    y_loc = 0 + deviation_before
    x_loc_list.append(x_loc)
    y_loc_list.append(y_loc)

    lat_v = 0
    y_delta = 0
    stage = 0
    count = 0

    for t in range(1,int(sim_time/delta_t)):

        if stage == 0 and x_loc > long_pos_1:
            stage = 1

        if stage == 1 and 3.5 - abs(y_loc) < y_delta + deviation_after:
            stage = 2
            lat_a *= -1

        if stage == 2 and lat_v < 0:
            lat_a = 0
            lat_v = 0
            stage = 3

        if stage == 3:
            count += 1

        # if count > 20:
        #     break

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

        if lat_v == lat_v_max and y_delta == 0:
            y_delta = abs(y_loc)

    print(len(x_loc_list))

    return x_loc_list,y_loc_list
