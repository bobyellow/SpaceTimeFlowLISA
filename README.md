# SpaceTimeFlowLISA
The Space-Time Flow LISA method to measure spatiotemporal autocorrelation of panel flow data.

Tao, R., Chen, Y., & Thill, J. C. (2023). A space-time flow LISA approach for panel flow data. Computers, Environment and Urban Systems, 106, 102042.https://doi.org/10.1016/j.compenvurbsys.2023.102042

A closely related version is the Flow LISA (spatial-only) to measure spatial autocorrelation of cross-sectional flow data.

Tao, R., & Thill, J. C. (2020). BiFlowLISA: Measuring spatial association for bivariate flow data. Computers, Environment and Urban Systems, 83, 101519. https://doi.org/10.1016/j.compenvurbsys.2020.101519

## Abstract
Spatial flow data represent meaningful spatial interaction (SI) phenomena between geographic regions that are often highly dynamic. However, most existing flow analytical methods are cross-sectional, and there is a lack of methods to measure spatiotemporal autocorrelation of flow data. To fill this gap, we proposed a new localized spatial statistical method called Space-Time Flow LISA. The method design is a combination of two existing method families, namely space-time LISA and Spatial Flow LISA. A critical component of the method is the spacetime weight matrix of flow data that blends pairwise spatial and temporal connectivities. We design three versions of the matrix, namely contemporaneous, lagged, and hybrid. We evaluate the method using both synthetic data and a case study of U.S. interstate migration from 2005 to 2017. The method is found to have high efficacy in finding spatiotemporal local autocorrelation patterns. Unlike the Spatial Flow LISA that tends to detect shortdistance migration corridor havens (‘HH’ flows) and long-distance migration corridor deserts (‘LL’ flows), the Space-Time Flow LISA is less impeded by the distance between flow origin and destination, as they can pick up local patterns that are less spatially explicit but temporally dependent. In addition, the new method is able to detect time-sensitive patterns such as the outmigration from Louisiana forced by Hurricane Katrina in 2005. By integrating spatial, temporal, and attributive associations into a one-step analysis, the proposed Space-Time Flow LISA can illustrate the spatiotemporal structure of flow phenomena well, and reveal dynamic distribution changes over time.

## How To Use
### For Space-Time FlowLISA

Before running the code, there are several steps you need to prepare. 
First, import the origin and destination shapefile.

```
AREAS1 = clusterpy.importArcData("yourpath/Origin_shapefile")
AREAS2 = clusterpy.importArcData("yourpath/Destination_shapefile")
```

Second, use the AllYearDictionary_sample.py to build the 'Allyeardic' dictionary

Third, this is the execute code for Space-Time FlowLISA
```
outputStr = execSpaceTimeFLOWLISA(AREAS1, AREAS2, FlowValue, FlowValue2, Time1, Time2, Spatstat, NeiLvl, Allyeardic)
    Parameters:
    - AREAS1: List of Origin areas.
    - AREAS2: List of Destination areas.
    - FlowValue: OD pairs with non-zero value.
    - FlowValue2: OD pairs with non-zero value for the 2nd year.
    - Time1: the year of 1st dataset.
    - Time2: the year of 2nd dataset.
    - Spatstat: Specifies the type of spatial statistic to be used. 1 = Moran's I; 2 = Getis G; 3 = Geary C; 5 = Multi-Geary C
    - NeiLvl: Neighbor Level for weights computation. 33 = Contemporary, 494 = Lagged; 55 = Hybrid
    - Allyeardic: Dictionary of all years' OD pairs with non-zero value. 
```
Fourth, we adopt Monte Carlo simulation based on conditional permutations to evaluate the statistical significance. The default number is 100 simulations while you can change it to 1000 or even 10000.

Finally, after executing the code, export the results to the path you want to save.		

```
outputFile = open('yourpath/file_name.txt','w')
outputFile.write(outputStr)
```

### For FlowLISA (spatial only)
First, import the origin and destination shapefile.

```
AREAS1 = clusterpy.importArcData("yourpath/Origin_shapefile")
AREAS2 = clusterpy.importArcData("yourpath/Destination_shapefile")
```

Second, this is the execute code for FlowLISA
```
execFLOWLISA(AREAS1, AREAS2, FlowValue, Spatstat, NeiLvl)
    Parameters:
    - AREAS1: List of Origin areas.
    - AREAS2: List of Destination areas.
    - FlowValue: OD pairs with non-zero value.
    - Spatstat: Specifies the type of spatial statistic to be used. 1 = Moran's I; 2 = Getis G; 3 = Geary C; 5 = Multi-Geary C
    - NeiLvl: Neighbor Level for weights computation. level 1 has O (D) the same, while D (O) is neighbor; level 2 has both O and D as neighbor; level 12 = level 1 + level 2
```

Third, we adopt Monte Carlo simulation based on conditional permutations to evaluate the statistical significance. The default number is 1000.

Finally, after executing the code, export the results to the path you want to save.
```
outputFile = open('yourpath/file_name.txt','w')
outputFile.write(outputStr)
```

## Citation 
```
@article{Rantao2023,
author = {Tao, R., Chen, Y., & Thill, J. C.},
doi = {10.1016/j.compenvurbsys.2023.102042},
journal = {Computers, Environment and Urban Systems},
number = {1},
pages = {102042},
title = {{A space-time flow LISA approach for panel flow data}},
url = {https://doi.org/10.1016/j.compenvurbsys.2023.102042},
volume = {106},
year = {2023}}
credits = "Copyright (c) 2018-01 Ran Tao"
license = "New BSD License"
version = "1.0.0"
email = "rtao@usf.edu"
```
