import pprint
import operator
import numpy as np
import math
from copy import copy, deepcopy

piece=[[0,0,0],[0,1,0],[0,2,0],[0,3,0],[1,2,0]]
sizeofcube=5

def init_cube(size=sizeofcube):
    return [[[0 for x in range(0,size)] for y in range(0,size)] for z in range(0,size)]

def move_start_position(piece,index):
    return [np.subtract(x, piece[index]) for x in piece]

def draw_cube(cube):
    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib.pyplot as plt
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.set_aspect('equal')
    ax.set_xlabel('x', fontsize=10)
    ax.set_ylabel('y', fontsize=10)
    ax.set_zlabel('z', fontsize=10)

    ma=np.array(cube)
    ax.voxels(ma, edgecolor="k")
    plt.show()

def put_piece_in_cube(piece,cube,position,index):
    cursors = [np.add(position,p) for p in piece]
    in_cube = [ max(c) < len(cube) and min(c) >= 0 for c in cursors]
    if all(in_cube):
        for cursor in cursors:
            try:
                if cube[cursor[0]][cursor[1]][cursor[2]]!=0:
                    return False
            except:
                return False
        for cursor in cursors:
            cube[cursor[0]][cursor[1]][cursor[2]]=index
        return True
    else:
        return False

def rotate_vector(vector,axis,angle):
    x,y,z=vector
    angle=math.radians(angle)
    if axis == "z":
        return (int(round((x*math.cos(angle)) - (y*math.sin(angle)))),int(round((x*math.sin(angle)) + (y*math.cos(angle)))),z)
    if axis == "y":
        return (int(round(x*math.cos(angle) + z*math.sin(angle))),y,int(round(-x*math.sin(angle) + z*math.cos(angle))))
    if axis == "x":
        return (x,int(round(y*math.cos(angle) - z*math.sin(angle))),int(round(y*math.sin(angle) + z*math.cos(angle))))

def rotate_piece(piece,axis,angle):
    return [rotate_vector(x, axis, angle) for x in piece]

def shift_piece(piece,anchor_index):
    anchor=piece[anchor_index]
    return [np.subtract(p,anchor) for p in piece]

def generate_rotations(piece):
    all_rotations=set()
    for i in range(0,4):
        for j in range(0,4):
            for k in range(0,4):
                for p in range(0,5):
                    rotated_piece=rotate_piece(rotate_piece(rotate_piece(shift_piece(piece,p),"x",k*90),"y",j*90),"z",i*90)
                    all_rotations.add(tuple(rotated_piece))
    return frozenset(all_rotations)

def find_empty_spot(cube):
    for z in range(0,sizeofcube):
        for y in range(0,sizeofcube):
            for x in range(0,sizeofcube):
                if cube[x][y][z]==0:
                    return (x,y,z)
    return None

def solve(cube,index):
    #make copy of cube
    global maxindex
    if index > maxindex:
        print(index)
        maxindex=index

    backup=deepcopy(cube)
    # draw_cube(backup)
    #make copy of available pieces
    global all_rotations
    pieces=set(all_rotations.copy())

    # print("{}:find empty spot#########################".format(index))
    empty_pos=find_empty_spot(backup)

    if empty_pos==None:
        pprint.pprint(cube)
        draw_cube(cube)
        return True
    else:
        (x,y,z)=empty_pos
        # print("{}:empty_spot at ({},{},{})".format(index,x,y,z))
        #found empty space > trying to fill it
        while len(pieces)>0:
            #use copy of cube without my parts
            local_cube=deepcopy(backup)
            piece=pieces.pop()
            if put_piece_in_cube(piece, local_cube, (x,y,z), index):
                # print("{}:found fitting piece {} ({} left)".format(index,piece,len(pieces)))
                if solve(local_cube, index+1):
                    return True
                else:
                    # print("{}:removing ({},{},{}):{}".format(index,x,y,z,len(pieces)))
                    pass
        #nothing fits return fail
        return False


maxindex=0


def main():
    global all_rotations
    all_rotations=generate_rotations(piece)
    solve(init_cube(),1)

if __name__ == '__main__':
    main()
