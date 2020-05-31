'''
    Created during NASA COVID-19 SPACE APPS CHALLENGE for Team Impact! 
'''

import os
import json
import numpy as np 
import xarray as xr
import shapely.geometry
import IPython.display
import matplotlib.pyplot as plt 
from xcube_sh.cube import open_cube
from xcube_sh.config import CubeConfig
from xcube.core.maskset import MaskSet
from osgeo import gdal, gdal_array, ogr 

hc = dict(client_id = '58c01991-7cd8-4685-83d8-03c239419f1d',
          client_secret= 'I1_8i,1#-iC(T_*9N]Mr{dq}7~WhvpX@?2ZE{#aC') 
# expires in 24 hours, need to upgrade or create a new account for data access

dataset = "S2L2A"
spatialRes= 0.0009
bandNames= ["B02", "B03", "B04", "B08", "B11", "SCL"]
timePeriod = "10D" # 10 days interval for now  
fig = [20, 12]

# few parameters 
min_rgb = 0.04
max_red = 0.15
max_green = 0.15
max_blue = 0.4
max_ndvi = 0.7 
max_ndwi = 0.001
max_ndsi = 0.0001
min_b11 = 0.05
max_b11 = 0.55
min_green_ratio = 0.05
min_red_ratio = 0.1

# some locations to seek for EO data
#min Long, min lat, max long, min lat 
bboxDelhi= 76.28,27.78,78.17,29.44 
bboxLucknow = 79.92,26.16,81.60,27.53 
bboxMaha = 75.3051,17.1639,76.4847,18.1784 
bboxKala = 76.5829,17.0825,77.0869,17.5536 
bboxHydra = 78.0834,16.9797,78.8822,17.7607 
bboxVija = 79.8204,16.0397,81.1992,17.2551
bboxPatna = 84.0448,24.7575,86.1746,26.4275
bboxAhm = 73.3273,18.1127,77.1395,21.403
bboxNagpur = 76.85,19.49,80.66,22.75
bboxBengal = 76.35,9.49,79.03,13.91
bboxPunjab = 74.73,29.35,78.54,31.9

dates = ["2019-03-01", "2020-04-29", #2019
        "2020-03-01", "2020-04-29"] #2020


### specify these before running the code 
mdir = "NY" # Main directory
area = "Delhi" # sub directory 


aoi = bboxDelhi 

if not os.path.exists(mdir):
    os.mkdir(mdir)
    print("directory ", mdir, " created")
else:
    print("directory already exists")

path = os.path.join(mdir,area) 

if not os.path.exists(path):
    os.mkdir(path)
    print("Directory created: ",area)
else:
    print("Directory already exists: ", area)

area = str(area)
IPython.display.GeoJSON(shapely.geometry.box(*aoi).__geo_interface__)
d2= False 
for i in range(2):
    if (d2== False):
        data = "2019"
        date_x = dates[0]
        date_y = dates[1]
    else:
        data= "2020"
        date_x = dates[2]
        date_y = dates[3] 
    
    cube_con = CubeConfig(dataset_name = dataset,
            band_names = bandNames, 
            tile_size = [512, 512],
            geometry = aoi, # area of interest
            spatial_res= spatialRes, #0.00009
            time_range = [date_x, date_y],
            time_period = timePeriod)

    cube = open_cube(cube_con, **hc) #  **hc -> Sentinel Hub Credentials 
    scl = MaskSet(cube.SCL) 
    cube= cube.where((scl.clouds_high_probability + scl.clouds_medium_probability + scl.clouds_low_probability_or_unclassified + scl.cirrus) == 0)
    date = dates[0]
    t= cube.sel(time = cube.time[0])
    B02 = t.B02
    B03 = t.B03
    B04 = t.B04
    B08 = t.B08
    B11 = t.B11
    ndvi_mask = ((B08 - B04) / (B08 + B04)) < max_ndvi
    ndwi_mask = ((B02 - B11) / (B02 + B11)) < max_ndwi
    ndsi_mask = ((B03 - B11) / (B03 + B11)) < max_ndsi
    low_rgb_mask = (B02 > min_rgb) * (B03 > min_rgb) * (B04 > min_rgb)
    high_rgb_mask = (B02 < max_blue) * (B03 < max_green) * (B04 < max_red)
    b11_mask = ((B11 - B03) / (B11 + B03)) < max_b11
    b11_mask_abs = (B11 > min_b11) * (B11 < max_b11)
    roads_mask = ndvi_mask * ndwi_mask * ndsi_mask * low_rgb_mask * high_rgb_mask * b11_mask * b11_mask_abs
    
    # vehicles 
    bg_ratio = (B02 - B03) / (B02 + B03)
    br_ratio = (B02 - B04) / (B02 + B04)
    bg_low = (bg_ratio * roads_mask) > min_green_ratio 
    br_low = (br_ratio * roads_mask) > min_red_ratio
    vehicles = bg_low * br_low

    # save the data sample for testing
    #roads_mask.plot.imshow(vmin = 0, vmax = 1, cmap = "binary", figsize = [16, 8])
    #roads_mask.to_netcdf("roads_mask_example_" + date + ".nc")
    vehicles.to_netcdf(mdir + "/" + area + "/" + area + "vehicleDat" + data + ".nc")  
    if (d2== False): d2= True

B02.to_netcdf(mdir + "/" + area + "/B02" + area + ".nc")
B03.to_netcdf(mdir + "/" + area + "/B03" + area + ".nc")
B04.to_netcdf(mdir + "/" + area + "/B04" + area + ".nc")


