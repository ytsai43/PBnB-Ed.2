def criteria(region_list): 
    numberofSubregion = len(region_list)
    dim = len(region_list[0])   
    #N = ceil(log(alpha) / log(1-delta)) # number of sample point we need in one subregion
    #R = ceil(log(alpha / (2 * numberofSubregion-1)) / log(0.5)) #number of replication
    N=3
    R=2
    X_matrix = np.zeros((numberofSubregion,N,dim))
    for m in range(numberofSubregion) :
        for n in range(N):
            for d in range(dim):                
                X_matrix[m,n,d] = np.random.uniform(region_list[m][d][0],region_list[m][d][1])
    # f(X) with noise
    fofx = X_matrix[:,:,0] + X_matrix[:,:,1]
    tempfofx = fofx.repeat(R)
    noise = np.random.normal(0,1,N*R*numberofSubregion)
    fofx = tempfofx+noise
    hatFofx = fofx.reshape(numberofSubregion,N,R)
    print('hatFox=',hatFofx)
    #print(hatFofx[1][1])
    avgfofx = np.average(hatFofx,axis=2).reshape(numberofSubregion,N,1)
    print('avgfofx=',avgfofx)
    bestRegion = int(np.argmin(avgfofx)/N)
    print('bestRegion=',bestRegion)
    bestPointinbestRegion = np.argmin(avgfofx[bestRegion])
    print('bestPointinbestRegion=',bestPointinbestRegion)
    worstPointwithNoise = hatFofx[bestRegion][bestPointinbestRegion][np.argmax(hatFofx[bestRegion][bestPointinbestRegion])]
    print('worstPointwithNoise=',worstPointwithNoise)
    
    notbestRegion = np.argmin(avgfofx,axis = 1)
    print('notbestRegion',notbestRegion)
    remainRegion = []
    remainRegion.append(region_list[bestRegion])
    for i in range(numberofSubregion):
        if i == bestRegion:
            pass
        elif hatFofx[i,notbestRegion[i],np.argmin(hatFofx[i][notbestRegion[i]])] < worstPointwithNoise:
            remainRegion.append(region_list[i])
    return(remainRegion)                       
    print(remainRegion)
    

criteria([[(0,2),(3,5)],[(0,1),(4,6)]])
