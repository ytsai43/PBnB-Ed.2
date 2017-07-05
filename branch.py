%config IPCompleter.greedy=True

import numpy as np
import copy
from random import*

def partition(range_list, m=2, depth=0):
    
    k = len(range_list[0]) # cal number of dimensions
    axis = depth % k # Select axis based on depth so that axis cycles through all valid values  
    if abs(range_list[0][axis][1] - range_list[0][axis][0]) < 1.1:  #Set the condition that the range cann't be divided 
        axis_hat = axis
        axis = (axis + 1)%k
        print(axis)
        while((abs(range_list[0][axis][1] - range_list[0][axis][0]) < 2 and axis != axis_hat)):
            axis = (axis + 1)%k
        if axis == axis_hat:
            return range_list
        
    cuttingPoint = (range_list[0][axis][1] + range_list[0][axis][0])/2
    #print(cuttingPoint)
    left_range_list = copy.deepcopy(range_list)
    right_range_list = copy.deepcopy(range_list) 
    for j in range(len(range_list)):
        left_range_list[j][axis] = (range_list[0][axis][0],cuttingPoint)
        right_range_list[j][axis] = (cuttingPoint,range_list[0][axis][1])
    range_list = left_range_list+ right_range_list
    return range_list 
    
range_list=[[(0,2),(0,4),(0,2)]]

for i in range(4):
    range_list = kdtree(range_list, 2, i)
    print(range_list)
