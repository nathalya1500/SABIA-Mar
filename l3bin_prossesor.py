from sabial3 import L3Grid, L3Spatial

grid = L3Grid(numrows, lat, lon)
grid.initbin()
grid.latlon2bin()

spatial = L3Spatial(grid, listl2, products)

bines, N, SUMX, SUMXX, W = spatial.temporal_binnign()