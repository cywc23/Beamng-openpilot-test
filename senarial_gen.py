import numpy as np

from beamngpy import BeamNGpy, Scenario, Vehicle, setup_logging
from beamngpy.sensors import Camera
import Trajectory_generation_v3
import time

import matplotlib.pyplot as plt


import socket_service

SIZE = 1024


def main():
    global send_image
    setup_logging()

    beamng = BeamNGpy('localhost', 64256)
    bng = beamng.open(launch=True)

    scenario = Scenario('west_coast_usa', 'ai_sine')
    vehicle = Vehicle('ego_vehicle', model='etk800', licence='AI')

    cam_pos = np.array([0, 0, 5])  # placeholder values that will be recomputed later
    cam_dir = np.array([0, 180, 0])  # placeholder values that will be recomputed later
    cam_fov = 70
    cam_res = (482, 302)
    camera = Camera(cam_pos, cam_dir, cam_fov, cam_res, colour=True)
    vehicle.attach_sensor('camera', camera)


    dirction = 1 # -1 turn left

    orig = (-717.121 + 2.8 - 2.8 * dirction, 101, 118.675)




    scenario.add_vehicle(vehicle, pos=orig,rot=(0,0,225))
    
    



    vehicle1 = Vehicle('ego_vehicle1', model='etk800', licence='AI1')
    orig1 = (-769.1+4, 400.8-10, 142.8)



    scenario.make(bng)
    script = list()

    points = list()
    point_colors = list()
    spheres = list()
    sphere_colors = list()

    sim_times = 60*60

    x_loc_list,y_loc_list = Trajectory_generation_v3.generate_traj(sim_times)
    theta = 0.7850
    for i in range(sim_times):
        # -1 turn left
        x_add = x_loc_list[i]*np.cos(theta) - y_loc_list[i]*np.sin(theta)*dirction
        y_add = x_loc_list[i]*np.sin(theta) + y_loc_list[i]*np.cos(theta)*dirction
        node = {

            'x': y_add + orig[0],
            'y': x_add + orig[1],
            'z': orig[2],
            't': i/96+1,
        }

        script.append(node)
        points.append([node['x'], node['y'], node['z']])
        point_colors.append([0, np.sin(np.radians(i)), 0, 0.1])

        if i % 10 == 0:
            spheres.append([node['x'], node['y'], node['z'],
                            np.abs(np.sin(np.radians(i))) * 0.25])
            sphere_colors.append([np.sin(np.radians(i)), 0, 0, 0.8])

    try:
        bng.load_scenario(scenario)

        bng.start_scenario()
        bng.add_debug_line(points, point_colors,
                           spheres=spheres, sphere_colors=sphere_colors,
                           cling=True, offset=0.1)


        vehicle.ai_set_script(script)
        
        while True:
            beamng.poll_sensors(vehicle)
            print(vehicle.state['pos'])

            
            img_data = bng.poll_sensors(vehicle)['camera']['colour']
            send_image = np.asarray(img_data.convert('RGB'))


            # plt.imshow(np.asarray(image.convert('RGB')))
            # plt.pause(0.1)

            ss = socket_service.socket_service()
            ss.send(("start".encode('utf-8')))
            ss.send((send_image))
            # time.sleep(2)
            plt.imshow(send_image)
            plt.pause(1)
            ss.close()

            bng.step(180)

    finally:
        bng.close()


if __name__ == '__main__':
    main()
