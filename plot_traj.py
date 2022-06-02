from matplotlib import pyplot as plt
import pandas as pd
import sys

PATH = "D:\\UVA\\2022 Spring\\cs8501\\Final Project\\Generated Trajectory\\"
print(sys.argv[1])

data = pd.read_csv(PATH + sys.argv[1], names=['x','y'])


x_loc_list = list()
y_loc_list = list()


len_num = len(data["x"])
# print(len(data["x"]))

for i in range(len(data["x"]) - 1):
    x_loc_list.append(float(data["x"][i]))
    y_loc_list.append(float(data["y"][i]))


# print(x_loc_list)


plt.plot(x_loc_list,y_loc_list,"-r")
plt.plot([-5, x_loc_list[-1]],[-1.75,-1.75],"-b")
plt.plot([-5, x_loc_list[-1]],[1.75,1.75],"-b")
plt.plot([-5, x_loc_list[-1]],[1.75*3,1.75*3],"-b")
plt.show()

#python ..\plot_traj.py ".\2022-04-10_233228.csv"