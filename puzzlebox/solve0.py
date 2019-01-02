import numpy as np
import math
from operator import add
import matplotlib.pyplot as plt
import pprint
from mpl_toolkits.mplot3d import Axes3D

# g_cube=np.zeros((10,10,10))
n=6
g_cube=[[[0 for k in range(0,n)] for j in range(0,n)] for i in range(0,n)]

form=[[0,0,0],[1,0,0],[2,0,0],[3,0,0],[2,1,0]]



def set_origin(form,index):
    newform=list()
    for x in form:
        newform.append(np.subtract(x,form[index]))
    return newform

def vector_rotate(vector,angle,axis):
    if axis=='x':
        result=[vector[0],( ( vector[1]*math.cos(angle) ) - ( vector[2]*math.sin(angle) ) ),( ( vector[1]*math.sin(angle) ) + ( vector[2]*math.cos(angle) ) )]
    if axis=='y':
        result=[( ( vector[0]*math.cos(angle) ) + ( vector[2]*math.sin(angle) ) ),vector[1],( ( -vector[0]*math.sin(angle) ) + ( vector[2]*math.cos(angle) ) )]
    if axis=='z':
        result=[( ( vector[0]*math.cos(angle) ) - ( vector[1]*math.sin(angle) ) ),( ( vector[0]*math.sin(angle) ) + ( vector[1]*math.cos(angle) ) )]


def form_in_cube(form):
    for cursor in form:
        for element in cursor:
            if element<=0 or element>=n:
                return False
        return True

def put_in(form,cube,offset,piece=1):
    form_positions=[(x+offset[0],y+offset[1],z+offset[2]) for (x,y,z) in form]
    # form_positions=list([map(add,p,offset) for p in form])

    if form_in_cube(form_positions):
        for cursor in form_positions:
            cube[cursor[0]][cursor[1]][cursor[2]]=piece
            print("set ({},{},{}) to {}".format(cursor[0],cursor[1],cursor[2],piece))
    else:
        print("out")

def draw_field(g_cube):
    # g_cube=np.zeros((6,6,6))
    # g_cube=cube
    # prepare some coordinates
    # x, y, z = np.indices((6, 6, 6))
    x, y, z = np.indices((len(g_cube),len(g_cube[0]), len(g_cube[0][0])))
    farben=["red","blue","green","cyan","magenta","yellow"]

    list_of_cubes =list()
    for x_pos in range(0,len(g_cube)):
        for y_pos in range(0,len(g_cube[x_pos])):
            for z_pos in range(0,len(g_cube[x_pos][y_pos])):
                color=(g_cube[x_pos][y_pos][z_pos])
                if color>0:
                    print("Voxel by ({},{},{}) : {}".format(x_pos,y_pos,z_pos,type(g_cube[x_pos][y_pos][z_pos])))
                    farbe=farben[int((color+1)%len(farben))]
                    list_of_cubes.append({"cube":(x < x_pos) & (x >= (x_pos-1) ) & (y < y_pos) & (y >= (y_pos-1) ) & (z < z_pos) & (z >= (z_pos-1) ),"farbe":farbe})


    voxels=list_of_cubes[0]["cube"]
    colors = np.empty(voxels.shape, dtype=object)

    for x in list_of_cubes:
        voxels=voxels | x["cube"]
        colors[x["cube"]]=x["farbe"]

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.voxels(voxels, facecolors=colors, edgecolor='k')
    plt.show()


put_in(set_origin(form,3),g_cube,(1,2,1),1)
put_in(set_origin(form,4),g_cube,(2,2,2),2)
put_in(set_origin(form,3),g_cube,(3,2,3),1)
put_in(set_origin(form,4),g_cube,(4,2,4),2)
draw_field(g_cube)
