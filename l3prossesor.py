# coding=utf-8

import numpy as np
#import pandas as pd
import matplotlib.pyplot as plt
import h5py as h5
import warnings
import time


class L3Grid(object):

  def __init__(self, numrows, lat, lon):
    self.numrows = numrows
    self.lat = lat
    self.lon = lon

  def initbin(self):
    '''
    given the total row number, this method returns above variables.
    '''

    self.basebin = np.zeros((self.numrows,))
    self.latbin = np.zeros((self.numrows,))
    self.numbin = np.zeros((self.numrows,))
    self.basebin[0] = 1

    for row in range(self.numrows):
        self.latbin[row] = ((row + 0.5)*180.0/self.numrows) - 90.0
        self.numbin[row] = int(2*self.numrows*np.cos(self.latbin[row]*np.pi/180.0) + 0.5)
        if(row > 0):
            self.basebin[row] = self.basebin[row - 1] + self.numbin[row - 1]
    self.totbins = self.basebin[self.numrows - 1] + self.numbin[self.numrows - 1] - 1 

    # return self.totbins, basebin, numbin, latbin

  def lat2row(self):
    '''
    This method
    '''
    self.row = 0*self.lat
    self.row = (90 + self.lat)*self.numrows/180.0
    self.row = self.row.astype(int)
    self.row[self.row >= self.numrows] = self.numrows - 1

    #return row

  def constrain_lon(self):
    '''
    This method
    '''
    self.lon[self.lon <= -180] = self.lon[self.lon < -180] % 180
    self.lon[self.lon >   180] = self.lon[self.lon>180] % -180
    
    # return lon

  def rowlon2bin(self):
    '''
    This method
    '''
    self.constrain_lon() #acá se pone l3 punto funcion ?
    self.col = ((self.lon + 180.0) * self.numbin[self.row] / 360.0)
    self.col = self.col.astype(int)
    mask = np.where(self.col >= self.numbin[self.row])
    self.col[mask] = self.numbin[self.row[mask]] - 1 

    return self.basebin[self.row] + self.col
  
  def constrain_lat(self):
    self.lat[self.lat >  90] = 90
    self.lat[self.lat < -90] = -90

    # return lat

  def latlon2bin(self):
    '''
    given the lat/lon, return the bin number
    lon has to be in the range of -180.0 to 180.0
    '''

    self.constrain_lat()
    self.constrain_lon()

    row = self.lat2row()
    self.bin = self.rowlon2bin(row)

  # return binlon

# self = numrows, lat, lon, basebin, latbin, numbin, totbins