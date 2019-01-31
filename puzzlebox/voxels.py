'''
==========================
3D voxel / volumetric plot
==========================

Demonstrates plotting 3D volumetric objects with ``ax.voxels``
'''

import matplotlib.pyplot as plt
import numpy as np
import pprint
import random
from matplotlib import colors as mcolors

# This import registers the 3D projection, but is otherwise unused.
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

g_cube=np.zeros((6,6,6))
# prepare some coordinates
x, y, z = np.indices((6, 6, 6))

# farben=["red","blue","green","cyan","magenta","yellow"]
farben=[name for name in mcolors.CSS4_COLORS]
random.shuffle(farben)
g_cube=[[[1, 1, 1, 1, 22],
  [6, 6, 6, 6, 22],
  [2, 6, 9, 22, 22],
  [9, 9, 9, 9, 22],
  [10, 15, 15, 15, 15]],
 [[2, 11, 1, 19, 20],
  [2, 11, 13, 19, 21],
  [2, 11, 11, 19, 23],
  [2, 11, 17, 19, 24],
  [10, 14, 18, 15, 25]],
 [[3, 3, 3, 3, 20],
  [4, 13, 13, 19, 21],
  [8, 8, 8, 8, 23],
  [10, 14, 17, 17, 24],
  [10, 14, 18, 18, 25]],
 [[4, 12, 3, 20, 20],
  [4, 12, 13, 21, 21],
  [4, 12, 8, 23, 23],
  [4, 12, 17, 24, 24],
  [10, 14, 18, 25, 25]],
 [[5, 5, 5, 5, 20],
  [7, 5, 13, 16, 21],
  [7, 12, 16, 16, 23],
  [7, 7, 17, 16, 24],
  [7, 14, 18, 16, 25]]]


list_of_cubes =list()
color_counter=0
for x_pos in range(0,len(g_cube)):
    for y_pos in range(0,len(g_cube[x_pos])):
        for z_pos in range(0,len(g_cube[x_pos][y_pos])):
            if g_cube[x_pos][y_pos][z_pos]!=0:
                cur_farbe=g_cube[x_pos][y_pos][z_pos]%len(farben)
                print("Voxel by in {} for ({}>x>={}//{}>y>={}//{}>z>={}) )".format(farben[cur_farbe],x_pos,x_pos+1,y_pos,y_pos+1,z_pos,z_pos+1))
                list_of_cubes.append({"cube":(x > x_pos) & (x <= (x_pos+1) ) & (y > y_pos) & (y <= (y_pos+1) ) & (z > z_pos) & (z <= (z_pos+1) ),"farbe":farben[cur_farbe]})
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
