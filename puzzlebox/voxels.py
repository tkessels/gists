'''
==========================
3D voxel / volumetric plot
==========================

Demonstrates plotting 3D volumetric objects with ``ax.voxels``
'''

import matplotlib.pyplot as plt
import numpy as np
import pprint

# This import registers the 3D projection, but is otherwise unused.
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

g_cube=np.zeros((6,6,6))
# prepare some coordinates
x, y, z = np.indices((6, 6, 6))
farben=["red","blue","green","cyan","magenta","yellow"]
g_cube[2][2][2]=1
g_cube[3][1][1]=2
g_cube[5][5][5]=2

list_of_cubes =list()
color_counter=0
for x_pos in range(0,len(g_cube)):
    for y_pos in range(0,len(g_cube[x_pos])):
        for z_pos in range(0,len(g_cube[x_pos][y_pos])):
            if g_cube[x_pos][y_pos][z_pos]!=0:
                print("Voxel by ({},{},{})".format(x_pos,y_pos,z_pos))
                list_of_cubes.append({"cube":(x < x_pos) & (x >= (x_pos-1) ) & (y < y_pos) & (y >= (y_pos-1) ) & (z < z_pos) & (z >= (z_pos-1) ),"farbe":farben[color_counter]})
                color_counter=(color_counter + 1) % len (farben)

voxels=list_of_cubes[0]["cube"]
colors = np.empty(voxels.shape, dtype=object)

for x in list_of_cubes:
    voxels=voxels | x["cube"]
    colors[x["cube"]]=x["farbe"]

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.voxels(voxels, facecolors=colors, edgecolor='k')

plt.show()




    # draw cuboids in the top left and bottom right corners, and a link between them
#
# cube1 = (x < 3) & (y < 3) & (z < 3)
# cube2 = (x >= 5) & (y >= 5) & (z >= 5)
# link = abs(x - y) + abs(y - z) + abs(z - x) <= 2
#
# # combine the objects into a single boolean array
# voxels = cube1 | cube2 | link
#
# # set the colors of each object
# colors = np.empty(voxels.shape, dtype=object)
# colors[link] = 'red'
# colors[cube1] = 'blue'
# colors[cube2] = 'green'
#
# # and plot everything
# fig = plt.figure()
# ax = fig.gca(projection='3d')
# ax.voxels(voxels, facecolors=colors, edgecolor='k')
#
# plt.show()
