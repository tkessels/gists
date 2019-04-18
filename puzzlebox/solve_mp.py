import pprint
import operator
import numpy as np
import math
from copy import copy, deepcopy
import profile

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

def set_cube_vals(cursors,cube,value):
    for cursor in cursors:
        cube[cursor[0]][cursor[1]][cursor[2]]=value

def is_valid(piece,position):
    global sizeofcube
    upper_x=sizeofcube-position[0]
    upper_y=sizeofcube-position[1]
    upper_z=sizeofcube-position[2]
    for (x,y,z) in piece:
        if x<-position[0] or x>upper_x:
            return False
        if y<-position[1] or y>upper_y:
            return False
        if z<-position[2] or z>upper_z:
            return False
    return True

def put_piece_in_cube(piece,cube,position,index):
    if is_valid(piece,position):
        # cursors = [np.add(position,p) for p in piece]
        # for cursor in cursors:
        cursors=[]
        for (x,y,z) in piece:
            cursor=[(x+position[0]),(y+position[1]),(z+position[2])]
            cursors.append(cursor)
            try:
                if cube[cursor[0]][cursor[1]][cursor[2]]!=0:
                    return False
            except:
                return False
        set_cube_vals(cursors, cube, index)
        return True
    else:
        return False

def remove_piece_in_cube(piece,cube,position):
    cursors = [np.add(position,p) for p in piece]
    set_cube_vals(cursors, cube, 0)

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
                for p in range(0,len(piece)):
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

def printstats():
    global stat_counter
    global stats
    stat_counter=stat_counter+1
    if stat_counter%10000==0:
        print(stat_counter)
        for x in stats:
            print("{}:{}".format(x,stats[x]))
            if x>5:
                break

def parallel_pool_init():
    global stats
    global solutions
    stats=dict()
    solutions=list()


def parallel_solve(cube):
    global all_rotations
    all_rotations=generate_rotations(piece)
    pieces=set(all_rotations.copy())
    first_position=(0,0,0)
    while len(pieces)>0:
        piece=pieces.pop()
        if put_piece_in_cube(piece, cube, first_position, index):
            stats["jobid"]={"0"=>len(pieces)}

            solve(cube, 2,):


def solve(cube,index,jobid):
    global stats
    global solutions
    global all_rotations
    pieces=set(all_rotations.copy())

    # print("{}:find empty spot#########################".format(index))
    empty_pos=find_empty_spot(cube)

    if empty_pos==None:
        pprint.pprint(cube)
        draw_cube(cube)
        solutions.append(cube)
        return False
    else:
        (x,y,z)=empty_pos
        while len(pieces)>0:
            #use copy of cube without my parts
            piece=pieces.pop()
            if put_piece_in_cube(piece, cube, (x,y,z), index):
                # print("{}:found fitting piece {} ({} left)".format(index,piece,len(pieces)))
                stats[index]=len(pieces)
                if solve(cube, index+1):
                    return True
                else:
                    remove_piece_in_cube(piece, cube, (x,y,z))
        #nothing fits return fail
        return False


# maxindex=0
# stat_counter=0
# stats=dict()
# last_stats=dict()

def main():
    parallel_solve(init_cube())

if __name__ == '__main__':
    # profile.run('main()')
    main()
