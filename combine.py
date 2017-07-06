%config IPCompleter.greedy=True

import numpy as np
import copy
from random import*
from math import*

def partition(range_list, depth=0):
    
    k = len(range_list[0]) # cal number of dimensions
    axis = depth % k # Select axis based on depth so that axis cycles through all valid values  
    if abs(range_list[0][axis][1] - range_list[0][axis][0]) < epsilon:  #Set the condition that the range cann't be divided 
        axis_hat = axis
        axis = (axis + 1)%k
        while((abs(range_list[0][axis][1] - range_list[0][axis][0]) < epsilon and axis != axis_hat)):
            axis = (axis + 1)%k
        if axis == axis_hat:
            return (range_list,depth)
        
    
    #print(cuttingPoint)
    left_range_list = copy.deepcopy(range_list)
    right_range_list = copy.deepcopy(range_list) 
    for j in range(len(range_list)):
        cuttingPoint = (range_list[j][axis][1] + range_list[j][axis][0])/2
        left_range_list[j][axis] = (range_list[j][axis][0],cuttingPoint)
        right_range_list[j][axis] = (cuttingPoint,range_list[j][axis][1])
    range_list = left_range_list+ right_range_list
    return (range_list, depth+1) 
    

def criteria(region_list, iteration): 
    numberofSubregion = len(region_list)
    dim = len(region_list[0])   
    N = ceil(log(alpha/(2)**iteration) / log(1-delta)) # number of sample point we need in one subregion
    R = ceil(log(alpha/(2)**iteration / (2 * numberofSubregion-1)) / log(0.5)) #number of replication
    X_matrix = np.zeros((numberofSubregion,N,dim))
    for m in range(numberofSubregion) :
        for n in range(N):
            for d in range(dim):                
                X_matrix[m,n,d] = np.random.uniform(region_list[m][d][0],region_list[m][d][1])
    # f(X) with noise
    fofx = 0.01 * X_matrix[:,:,0]**2 + X_matrix[:,:,1]**2-100
    tempfofx = fofx.repeat(R)
    noise = np.random.normal(mean,sigma,N*R*numberofSubregion)
    #noise = 0
    fofx = tempfofx+noise
    hatFofx = fofx.reshape(numberofSubregion,N,R)
    #print('hatFox=',hatFofx)
    #print(hatFofx[1][1])
    avgfofx = np.average(hatFofx,axis=2).reshape(numberofSubregion,N,1)
    #print('avgfofx=',avgfofx)
    bestRegion = int(np.argmin(avgfofx)/N)
    #print('bestRegion=',bestRegion)
    bestPointinbestRegion = np.argmin(avgfofx[bestRegion])
    best_object_value = avgfofx[bestRegion][bestPointinbestRegion]  #final objective value
    best_x_solution = X_matrix[bestRegion][bestPointinbestRegion]  #final optimal solution x
    worstPointwithNoise = hatFofx[bestRegion][bestPointinbestRegion][np.argmax(hatFofx[bestRegion][bestPointinbestRegion])]
    #print('worstPointwithNoise=',worstPointwithNoise)
    
    notbestRegion = np.argmin(avgfofx,axis = 1)
    #print('notbestRegion',notbestRegion)
    
    remainRegion = []
    remainRegion.append(region_list[bestRegion])
    for i in range(numberofSubregion):

        if i == bestRegion:
            pass
        elif hatFofx[i,notbestRegion[i],np.argmin(hatFofx[i][notbestRegion[i]])] < worstPointwithNoise:
            remainRegion.append(region_list[i])
    return(remainRegion,best_x_solution,best_object_value)


range_list=[[(2,50),(-50,50)]]
delta = 0.01 #clossness parameter
alpha = 0.25 #error rate
epsilon = 0.01 #condition to terminate subregion with continuous case 
mean,sigma = 0,0.0001   # distribution of noise
#M = 2 #number of subregions

newRange_list,depth = partition(range_list)
bestRegion_list = range_list[:]
newRange_list.sort()
range_list.sort()
iteration = 1
while(newRange_list != range_list):
    range_list,best_x,best_object_value = criteria(newRange_list,iteration)
    newRange_list,depth = partition(range_list,depth)
    bestRegion_list = range_list[:]
    newRange_list.sort()
    range_list.sort()   
    iteration += 1
#final output is x(1)(1),hatfofx,remainging subregion
print(best_x,best_object_value)    
print(bestRegion_list)
    
