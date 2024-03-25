# -*- coding: utf-8 -*-
__author__ = "Ran Tao"
__credits__ = "Copyright (c) 2018-01 Ran Tao"
__license__ = "New BSD License"
__version__ = "1.0.0"
__maintainer__ = "RiSE Group"
__email__ = "contacto@rise-group.org"

# Import necessary libraries
import time as tm
import numpy as np

from componentsAlg import calculateGetisG, calculateMoranI, calculateGearyC, calculateMultiGearyC
from contiguity import STweightsFromFlows

__all__ = ['execSpaceTimeFLOWLISA']

def execSpaceTimeFLOWLISA(AREAS1, AREAS2, FlowValue, FlowValue2, Time1, Time2, Spatstat, NeiLvl, Allyeardic):
    """Execute the SpaceTime FlowLISA analysis.
    
    Parameters:
    - AREAS1: List of Origin areas.
    - AREAS2: List of Destination areas.
    - FlowValue: OD pairs with non-zero value.
    - FlowValue2: OD pairs with non-zero value for year2.
    - Time1: the year of 1st dataset.
    - Time2: the year of 2nd dataset.
    - Spatstat: Specifies the type of spatial statistic to be used.
    - NeiLvl: Neighbor Level for weights computation.
    - Allyeardic: Dictionary of all years' OD pairs with non-zero value.
        
    Returns:
        - Formatted output string containing results.
    """
    
    start = tm.time()
    
    print("Running SpaceTime FlowLISA by Yuzhou&Ran Tao, built on clusterpy by Duque et al.")
    
    # Initialize key data structures
    areas1 = AREAS1
    areas2 = AREAS2
    flowvalue = FlowValue
    flowvalue2 = FlowValue2
    
    # Extract flow values and define dimensions
    y1 = areas1.Y
    y2 = areas2.Y
    Olength = len(y1)
    Dlength = len(y2)
    Flowlength = Olength * Dlength
    
    time1 = Time1
    time2 = Time2

    #create dictionary to extract the flow value for different times key:(O,D,T), value: flow value
    dic_flow1 = {}
    for key, value in flowvalue.iteritems():
        key = (key[0],key[1],time1)
        dic_flow1[key] = []
        dic_flow1[key].append(value)
    dic_flow2 = {}
    for key, value in flowvalue2.iteritems():
        key = (key[0],key[1],time2)
        dic_flow2[key] = []
        dic_flow2[key].append(value)

    dic_flow4 = dic_flow1.copy()
    dic_flow4.update(dic_flow2)
    
    # Prepare for computation based on Spatstat type
    y = flowvalue2
    yOutput = {k: [v] for k, v in y.items()} if Spatstat != 5 else flowvalue2
    yKeys = list(y.keys())
    
    # Obtain flow neighbors
    neighborLevel = NeiLvl
    Wflow = STweightsFromFlows(AREAS1, AREAS2, flowvalue, flowvalue2, time1, time2, neighborLevel)
    
    # Start calculations
    dataLength = len(y)
    dataMean = np.mean(list(Allyeardic.values()))
    dataStd = np.std(list(Allyeardic.values()))
    GMoranI = 0

    for s in yKeys:
        neighbors = Wflow.get(s, [])
        
        # Uni-I Calculation
        if Spatstat == 1:
            MoranI = calculateMoranI(s, neighbors, dataMean, dataStd, dic_flow4, dataLength) if neighbors else 0
            yOutput[s].extend([MoranI, 0])
            GMoranI += MoranI
        # GeisG Calculate
        if Spatstat == 2:
            GetisG = calculateGetisG(neighbors, dataMean, dataStd, dic_flow4, dataLength) if neighbors else 0
            yOutput[s].extend([GetisG, 0])
        # Geary C Calculate
        if Spatstat == 3:
            GearyC = calculateGearyC(s,neighbors, dic_flow4) if neighbors else 0
            yOutput[s].extend([GearyC, 0])
        # Multi-C Calculation
        if Spatstat == 5:
            MC = calculateMultiGearyC(s, neighbors, y, y, 2) if neighbors else 999
            yOutput[s].extend([MC, 0])
    
    # Monte-Carlo simulation for significance testing
    GMoranI_sim = [0] * 100
    for i in range(100):
        GMoranI_sim[i] = sum([calculateMoranI(perKey, Wflow.get(perKey, []), dataMean, dataStd, Allyeardic, dataLength) for perKey in yKeys])

    GMoranI_sim.sort()
    GMoranI_str = "Global Moran's I value is: {}".format(GMoranI)
    # Determine significance
    if GMoranI >= GMoranI_sim[95]:
        GMoranI_str += '. It is significantly positive at 0.05 level'
    elif GMoranI <= GMoranI_sim[4]:
        GMoranI_str += '. It is significantly negative at 0.05 level'
    else:
        GMoranI_str += '. It is insignificant at 0.05 level'
    
    # Prepare the results output string
    outputStrList = [GMoranI_str]
    if Spatstat == 1:
        outputStrList.append('O, D, Time, V, MoranI, p-value, I_Result')
        for k, v in yOutput.items():
            significance = "NS"
            if v[1] != 0 or v[2] != 0:
                if v[2] <= 0.05:
                    significance = "HH" if v[0] > dataMean else ("HL" if v[1] > 0 else ("LH" if v[0] <= dataMean else "LL"))
            outputStrList.append("{}, {}, {:.2f}, {}".format(k, v[0], v[1], significance))
    elif Spatstat == 5:
        outputStrList.append('O, D, Time, V1, V2, MC, p-value')
        for k, v in yOutput.items():
            outputStrList.append("{}, {}, {:.2f}, {:.2f}".format(k, v[0], v[1], v[2]))
    
    return '\n'.join(outputStrList)
