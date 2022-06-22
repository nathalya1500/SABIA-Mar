import numpy as np

def initbin(numrows):
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
    row = int((90 + lat)*numrows/180.0)
    if(row >= numrows):
        row = numrows - 1
    return row

def constrain_lon(lon):
    while(lon < -180):
        lon += 360
    while(lon >  180):
        lon -= 360 
    return lon

def constrain_lat(lat):
    if(lat >  90):
        lat = 90
    if(lat < -90): 
        lat = -90 
    return lat

def rowlon2bin(row, lon, numbin, basebin):
    lon = constrain_lon(lon)
    col = int((lon + 180.0)*numbin[row]/360.0)
    if(col >= numbin[row]):
        col = numbin[row] - 1

    return basebin[row] + col

def latlon2bin(numrow,lat,lon,numbin,basebin):
    lat = constrain_lat(lat)
    lon = constrain_lon(lon)

    row = lat2row(lat, numrow)
    binlon = rowlon2bin(row, lon, numbin, basebin)

    return binlon 

def bin2latlon (_bin, numrows, basebin, numbin, latbin):
    row = numrows - 1
    if(_bin < 1):
        _bin = 1

    while(_bin < basebin[row]):
        row-=1

    clat = latbin[row]
    clon = 360.0*(_bin - basebin[row] + 0.5)/numbin[row] - 180.0
    
    return clat,clon

def bin2bounds(_bin, numrows, basebin, numbin, latbin):
    row = numrows - 1
    if(_bin < 1):
        _bin = 1

    while(_bin < basebin[row]):
        row-=1

    north = latbin[row] + 90.0/numrows
    south = latbin[row] - 90.0/numrows
    lon = 360.0*(_bin - basebin[row] + 0.5)/numbin[row] - 180.0
    west = lon - 180.0/numbin[row]
    east = lon + 180.0/numbin[row]
    return north,south,west,east

