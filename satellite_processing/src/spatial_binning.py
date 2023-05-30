import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import h5py as h5
from tqdm import tqdm
import warnings
import time
warnings.filterwarnings('ignore')


def initbin(numrows):
  '''
   initbin: given the total row number, this subroutine returns above variables.
  '''

  basebin = np.zeros((numrows,))
  latbin = np.zeros((numrows,))
  numbin = np.zeros((numrows,))
  basebin[0] = 1
  for row in range(numrows):
      latbin[row] = ((row + 0.5)*180.0/numrows) - 90.0
      numbin[row] = int(2*numrows*np.cos(latbin[row]*np.pi/180.0) + 0.5)
      if(row > 0):
          basebin[row] = basebin[row - 1] + numbin[row - 1]
  totbins = basebin[numrows - 1] + numbin[numrows - 1] - 1  
  return totbins, basebin, numbin, latbin


def lat2row(lat, numrows):
    row = 0*lat
    row = (90 + lat)*numrows/180.0
    row = row.astype(int)
    row[row>=numrows] = numrows - 1
    return row

def constrain_lon(lon):
    lon[lon <= -180] = lon[lon < -180] % 180
    lon[lon>180] = lon[lon>180] % -180
    # while(lon < -180):
    #     lon += 360
    # while(lon >  180):
    #     lon -= 360 
    return lon

def rowlon2bin(row, lon, numbin, basebin):
    lon = constrain_lon(lon)
    col = ((lon + 180.0)*numbin[row]/360.0)
    col = col.astype(int)
    mask = np.where(col >= numbin[row])
    col[mask] = numbin[row[mask]] - 1 

    return basebin[row] + col

def constrain_lat(lat):
    lat[lat>90] = 90
    lat[lat<-90] = -90
    # if(lat >  90):
    #     lat = 90
    # if(lat < -90): 
    #     lat = -90 
    return lat

def latlon2bin(numrow,lat,lon,numbin,basebin):
  '''
  given the lat/lon, return the bin number
  lon has to be in the range of -180.0 to 180.0
  '''
  lat = constrain_lat(lat)
  lon = constrain_lon(lon)

  row = lat2row(lat, numrow)
  binlon = rowlon2bin(row, lon, numbin, basebin)

  return binlon

def get_spatial_bin_vectorized(totbins, lat, lon, numrow, numbin, basebin, ds, products):
    SUMX = np.zeros((int(totbins), len(products)))
    SUMXX = np.zeros((int(totbins), len(products)))
    N =  np.zeros((int(totbins), ))
    # W =  np.zeros((int(totbins), ))
    NSEG = np.zeros((int(totbins), ))
    # TT = np.zeros((int(totbins), ))

    prod_stack = np.stack(ds['geophysical_data'][products[i]][:] for i in range(len(products))) # matriz de productos de dim (20, 2030, 1354)
    prod_rolled = np.rollaxis(np.rollaxis(prod_stack, 1,0), 2,1) # matriz de productos de dim (2030, 1354, 20)
    
    flags = ds['geophysical_data']['l2_flags'][:]

    boolean_mask = np.zeros(flags.shape)
    bad_flags = np.array([1, 2, 4, 5, 6, 9, 10, 11, 13, 15, 16, 17, 20, 22, 23, 26, 31])
    
    boolean_mask = ((flags & (2**(bad_flags - 1)).sum()) == 0)

    idx = latlon2bin(numrow, lat[boolean_mask], lon[boolean_mask], numbin, basebin)
    idx = idx.astype(int)

    XLOG = prod_rolled[boolean_mask]
    XXLOG = XLOG * XLOG
    
    unique, count = np.unique(idx, return_counts=True)

    for indice,nobs in tqdm(zip(unique, count)):
      m = np.where(idx == indice)
      SUMX[indice] = XLOG[m].sum(axis=0)
      SUMXX[indice] = XXLOG[m].sum(axis=0)
      N[indice] = nobs
      NSEG[indice] = 1
    
    return unique, N, NSEG,  SUMX, SUMXX 