from vpython import *
from enum import IntEnum
import csv

class Direction(IntEnum):
    NORTH = 0
    EAST  = 1
    SOUTH = 2
    WEST  = 3

# construct the sample map
map = dict()
i=0
'''for i in range(1,7):
    map[i] = dict()'''

with open('/Users/angelhsia/Desktop/study material/一下/車車/自選題/output.csv', newline='') as csvfile:
    rows = csv.reader(csvfile)
    for row in rows:
        print(row)
        node_temp = row[0]
        if node_temp=="index":
            print("skip index")
        else:
            i += 1
            map[i] = dict()
            for index in range(1,5):
                neighbor = row[index]
                if neighbor!='':
                    map[i][Direction(index-1)] = [int(neighbor) , int(row[index+4])]

'''
# basic construction complete, now put the points and distance in:
map[1][Direction(0)] = [2, 30]
map[2][Direction(2)] = [1, 30]
map[2][Direction(1)] = [3, 20]
map[3][Direction(3)] = [2, 20]
map[3][Direction(2)] = [4, 60]
map[3][Direction(1)] = [5, 30]
map[4][Direction(0)] = [3, 60]
map[5][Direction(3)] = [3, 30]
map[5][Direction(2)] = [6, 10]
map[6][Direction(0)] = [5, 10]'''
print(map,'\n')

# finish the construction of map. now, start drawing via VPy:
canvas(width = 1200, height = 800, center = vector(0, 0, 0), background = color.white)

point_num = len(map)
node_position = vec(0,0,0)
points = list()
lines = list()
distance = 0

# place nodes
for node in range(point_num):
    point = box(size=vec(0.5,0.5,0.01) , axis=vec(0,1,0) , color=color.black , pos=node_position)
    points.append(point)
    # prepare for the next node
    if node==point_num-1: # 最後一個node
        break
    else:
        next_point = node+2
        for dir in map[next_point].keys():
            if map[next_point][dir][0] < next_point: # 找到任意與next_point相接且已經畫過的點
                dir_to_previous = dir
                last_node = map[next_point][dir][0]
                distance = map[next_point][dir][1]/4 #長度比例再調整
                break
    #print(last_node)
    if dir_to_previous==0:
        node_position = points[last_node-1].pos + vec(0,-distance,0)
    if dir_to_previous==1:
        node_position = points[last_node-1].pos + vec(-distance,0,0)
    if dir_to_previous==2:
        node_position = points[last_node-1].pos + vec(0,distance,0)
    if dir_to_previous==3:
        node_position = points[last_node-1].pos + vec(distance,0,0)
    print(node_position)

for node in range(point_num):
    for dir in map[node+1].keys():
        start_point = points[node].pos
        end_point = points[map[node+1][dir][0]-1].pos
        line = cylinder(radius=0.05 , color=color.red)
        line.pos = start_point
        line.axis = end_point-start_point
        line.length = mag(end_point-start_point)
        lines.append(line)