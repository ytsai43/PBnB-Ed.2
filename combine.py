%cd C:\Users\ytsai\Desktop\python
%config IPCompleter.greedy=True
%reset
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
    fofx = (1-X_matrix[:,:,0])**2 + 100*((X_matrix[:,:,1]-X_matrix[:,:,0]**2))**2
    #fofx = np.sin(X_matrix[:,:,0])
    tempfofx = fofx.repeat(R)
    #noise = np.random.normal(mean,sigma,N*R*numberofSubregion)
    noise = 0
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

####### find threshold value
fxstar = 0
delta = 0.01 #clossness parameter
alpha = 0.5 #error rate
epsilon = 4 #condition to terminate subregion with continuous case 
mean,sigma = 0,1   # distribution of noise

n_sample = 10000000
x_set = np.zeros((n_sample,2))
x_set[:,0]= np.random.uniform(-2,2,n_sample) 
x_set[:,1]= np.random.uniform(-2,2,n_sample) 
fx = (1-x_set[:,0])**2 + 100*((x_set[:,1]-x_set[:,0]**2))**2
fx.sort()
target_threshold = fx[int(n_sample*delta)]
########

ps = 0
test_region = []
for i in range(1000):
    
    range_list=[[(-2,2),(-2,2)]]

    
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
    #print(best_x,best_object_value)    
    #print(bestRegion_list)
    test_region.append(bestRegion_list[0])
    dis_f = abs(best_object_value - fxstar)
    #dis_x = abs(((best_x[0]-1)**2 + (best_x[1]-1)**2)**1/2)
    
    if (best_object_value-target_threshold < 0):

        ps = ps + 1
    print(dis_f)
    #print(best_object_value)
print(ps/1000)
#test_region.sort()
#print(test_region)
    
  

    
