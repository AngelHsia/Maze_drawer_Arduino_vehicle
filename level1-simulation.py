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

for node in range(point_num):
    for dir in map[node+1].keys():
        start_point = points[node].pos
        end_point = points[map[node+1][dir][0]-1].pos
        line = cylinder(radius=0.05 , color=color.red)
        line.pos = start_point
        line.axis = end_point-start_point
        line.length = mag(end_point-start_point)
        lines.append(line)

car = box(size=vec(2.5,4,0.01) , color=color.blue , axis=vec(1,0,0) , pos=vec(0,0,0))
car.pos = points[0].pos
car_speed = 2
car_direction = vec(0,1,0)
direction = 0
#next_node_number = 1
#distance_car_node = mag(car.pos - points[next_node_number].pos)
distance_car_node = list()
pre_distance = list()
dt = 0.0001

while(True):
    for node in range(point_num):
        pre_distance.insert(node , mag(car.pos - points[node].pos))
    for node in range(point_num):
        distance_car_node.insert(node , mag(car.pos - points[node].pos))
    time_interval = 0
    while(True):
        rate(50000)
        time_interval+=dt
        distance_min = 10
        node_min = 0
        car.pos += car_speed*dt*car_direction
        for node in range(point_num):
            distance_car_node[node] = mag(car.pos - points[node].pos)
            if distance_car_node[node] < distance_min:
                distance_min = distance_car_node[node]
                node_min = node
        if distance_min < 0.001 and pre_distance[node_min] > distance_min:
            break
        for node in range(point_num):
            pre_distance[node] = distance_car_node[node]
    car.pos = points[node_min].pos

    # TODO:藍芽回傳數值
    print("time = ",time_interval)

    # 跳出迴圈，接收接下來的方向
    # TODO:要改成藍芽傳方向
    direction = int(input('Please Enter The Direction: ')) # int
    if direction==4:
        break
    elif direction==0: # North
        car_direction = vec(0,1,0)
        car.axis = vec(1,0,0)
    elif direction==1: # East
        car_direction = vec(1,0,0)
        car.axis = vec(0,1,0)
    elif direction==2: # South
        car_direction = vec(0,-1,0)
        car.axis = vec(1,0,0)
    else: # West
        car_direction = vec(-1,0,0)
        car.axis = vec(0,1,0)
print("Car Has Stopped.")