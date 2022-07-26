from matplotlib.pyplot import grid
#import L3Grid
import numpy as np
#import pandas as pd
import matplotlib.pyplot as plt
import h5py as h5


class L3Spatial(object):

    

    def __init__(self, grid, listl2, products):

        self.totbins = grid.totbins
        self.numrows = grid.numrows
        self.basebin = grid.basebin
        self.listl2 = listl2
        self.products = products
        self.grid = grid

    #grid = L3Grid(self.numrows, self.lat, self.lon)

    def get_spatial_bin_vectorized(self, l2, lat, lon):
        SUMX = np.zeros((int(self.totbins), len(self.products)))
        SUMXX = np.zeros((int(self.totbins), len(self.products)))
        N =  np.zeros((int(self.totbins), ))
        # W =  np.zeros((int(self.totbins), ))
        NSEG = np.zeros((int(self.totbins), ))
        # TT = np.zeros((int(self.totbins), ))

        prod_stack = np.stack(l2['geophysical_data'][self.products[i]][:] for i in range(len(self.products))) # matriz de productos de dim (20, 2030, 1354)
        prod_rolled = np.rollaxis(np.rollaxis(prod_stack, 1,0), 2,1) # matriz de productos de dim (2030, 1354, 20)
        
        flags = l2['geophysical_data']['l2_flags'][:]

        boolean_mask = np.zeros(flags.shape)
        bad_flags = np.array([1, 2, 4, 5, 6, 9, 10, 11, 13, 15, 16, 17, 20, 22, 23, 26, 31])
        
        boolean_mask = ((flags & (2**(bad_flags - 1)).sum()) == 0)

        # grid.lat = lat[boolean_mask] 
        # grid.lon = lon[boolean_mask]

        self.grid.latlon2bin(lat[boolean_mask], lon[boolean_mask])
        idx = self.grid.bin
        idx = idx.astype(int)
        

        XLOG = prod_rolled[boolean_mask]
        XXLOG = XLOG * XLOG
        
        unique, count = np.unique(idx, return_counts=True)

        for indice,nobs in zip(unique, count):
            m = np.where(idx == indice)
            SUMX[indice] = XLOG[m].sum(axis=0)
            SUMXX[indice] = XXLOG[m].sum(axis=0)
            N[indice] = nobs
            NSEG[indice] = 1
            # W[indice] = np.sqrt(nobs)

            # SUMX[indice] = SUMX[indice] / W[indice]
            # SUMXX[indice]= SUMXX[indice]/W[indice]
        
        return unique, N, NSEG,  SUMX, SUMXX


    def temporal_binnign(self):
        sumx = np.zeros((int(self.totbins), len(self.products)))
        sumxx = np.zeros((int(self.totbins), len(self.products)))
        n =  np.zeros((int(self.totbins), ))
        w =  np.zeros((int(self.totbins), )) 
        nseg = np.zeros((int(self.totbins), ))
        # TT = np.zeros((int(self.totbins), ))
        bines = np.array([], dtype = int)
        
        for ds in self.listl2:
            lat = ds['navigation_data']['latitude'][:]
            lon = ds['navigation_data']['longitude'][:]
            binesi, Ni, NSEGI, SUMXi, SUMXXi = self.get_spatial_bin_vectorized(ds, lat, lon)
        
            sumx = sumx + SUMXi
            sumxx = sumxx + SUMXXi
            n = n + Ni
            nseg = nseg + NSEGI
            bines = np.union1d(bines,binesi)
            
        w = np.sqrt(n)
        for i in range(len(self.products)):
            sumx[bines,i] = sumx[bines,i] / w[bines]
            sumxx[bines,i] = sumxx[bines,i] / w[bines]
        
        return bines, n, nseg, sumx, sumxx, w