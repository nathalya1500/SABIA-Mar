import numpy as np
import h5py as h5
#import l3prossesor
#import l3_spatial
from l3prossesor import *
from l3_spatial import *

numrows = 4320

grid = L3Grid(numrows)
grid.initbin()

import os

Path = "/home/facu/Downloads/2022160/2022160/"
filelist = os.listdir(Path)
listl2 = []
for f in filelist:
    l2modis = h5.File(Path + f,'r')
    listl2.append(l2modis)

modisprod = list(listl2[0]['geophysical_data'].keys())[:-1]
spatial = L3Spatial(grid, listl2, modisprod)

bines, N, NSEG, SUMX, SUMXX, W = spatial.temporal_binnign()

A = np.stack([SUMX[bines], SUMXX[bines]], axis=2)
dt = {'names':['sum', 'sum_squared'], 'formats':[np.float64, np.float64]}
A.dtype=dt
A = np.squeeze(A)

a = np.stack([bines, N[bines].astype(int), NSEG[bines].astype(int), W[bines]], axis =1)
dt = np.dtype([('bin_num', np.int32), ('nobs', np.int32), ('nscenes', np.int32), ('weights', np.float64)])
B = np.array(list(map(tuple, a)), dtype=dt)

l3bd = {modisprod[i]: A[:, i] for i in range(20)}
l3bd['BinList'] = B

f=h5.File('test.nc','w')    
grp=f.create_group('level-3_binned_data')
adict = l3bd

for k,v in adict.items():
  grp.create_dataset(k,data=v)