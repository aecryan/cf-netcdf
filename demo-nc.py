# Python script to generate CF-1.8 compliant netCDF file
# Produced as a tool for the Africa Rainfall project by Nick van de Giesen at TU Delft
# Author: Ashley Cryan
# Date created: May 10, 2021

import netCDF4
import numpy as np
from datetime import date, datetime, timedelta
from cftime import date2num
from pyproj import Proj

## CREATE COORDINATE AND TIME DATA

start = datetime.utcnow().replace(hour=22, minute=0, second=0, microsecond=0)
times = np.array([start + timedelta(hours=h) for h in range(25)]) #24 hours of hourly output startting at 22Z today

time_units = 'hours since {:%Y-%m-%d 00:00}'.format(times[0])
time_vals = date2num(times, time_units)

# 1km spacing in x and y
x = np.arange(-150, 153, 1)
y = np.arange(-100, 100, 1)

zs = np.array(range(0,52)) #52 interger values between 0 and 51 representing height
temps = np.random.randint(273, 318, size=(times.size, zs.size, y.size, x.size)) #create an array of random values between 273 and 318 with the shape 51x51x52

## CREATE A NEW FILE
nc = netCDF4.Dataset('demo.nc',mode='w',format='NETCDF3_64BIT_OFFSET') 

## ADD GLOBAL ATTRIBUTES
# see http://www.unidata.ucar.edu/software/thredds/current/netcdf-java/formats/DataDiscoveryAttConvention.html
nc.title = 'Demo Climate Data'
nc.summary = 'These data were created to demonstrate use of a python script to create CF-compliant netCDF files for climate data.'
nc.keywords = 'temperature, climate, Africa'
nc.Conventions = 'CF-1.8'
nc.naming_authority = 'nl.tudelft'
nc.source = 'Created to emulate outputs from WRF-V3.9.1.1'
nc.history = str(datetime.utcnow()) + ' Python'
nc.license = 'CC-BY'
nc.creator_name = 'Ashley Cryan'
nc.project = 'Africa Rain DCC Support'
nc.projection = 'Lambert Conformal'
nc.cdm_data_type = 'Grid'
nc.metadata_link = 'https://africarain.readthedocs.io/en/latest/'

## ADD DIMENSIONS
nc.createDimension('time', None)
nc.createDimension('x', x.size)
nc.createDimension('y', y.size)
nc.createDimension('z', zs.size) #vertical grid dimension

## CREATE DATA VARIABLE(S)

airtemp=nc.createVariable('air_temperature', datatype=np.float32, dimensions=('time', 'z', 'y', 'x'), zlib=True)
airtemp[:]=temps
airtemp.standard_name = 'air_temperature'
airtemp.long_name = 'bulk temperature of the air'
airtemp.units = 'K'
airtemp.missing_value = -9999

# CREATE AUXILLARY VARIABLES

x_var=nc.createVariable('x', np.float32, ('x',))
x_var[:] = x
x_var.long_name = 'x-coordinate in projected coordinate system'
x_var.standard_name = 'projection_x_coordinate'
x_var.units = 'km'
x_var.axis = 'X'

y_var=nc.createVariable('y', np.float32, ('y',))
y_var[:] = y
y_var.standard_name = 'projection_y_coordinate'
y_var.long_name = 'y-coordinate in projected coordinate system'
y_var.units = 'km'
y_var.axis = 'Y'

z_var=nc.createVariable('z', np.float32, ('z',))
z_var[:]=zs
nc.variables['z'].long_name = 'height above ground surface in meters'
nc.variables['z'].standard_name = 'height'
nc.variables['z'].units = 'm'
nc.variables['z'].axis = 'Z'

time_var = nc.createVariable('time', np.int32, ('time',))
time_var[:] = time_vals
time_var.units = time_units
time_var.axis = 'T'  
time_var.standard_name = 'time' 
time_var.long_name = 'time'

# CONVERT DISTANCE COORDINATES INTO PROJECTED COORDINATES (LCC)

X, Y = np.meshgrid(x, y)
lcc = Proj({'proj':'lcc', 'lon_0':-105, 'lat_0':40, 'a':6371000.,
            'lat_1':25})
lon, lat = lcc(X * 1000, Y * 1000, inverse=True)

lon_var = nc.createVariable('lon', np.float64, ('y', 'x'))
lon_var[:] = lon
lon_var.units = 'degrees_east'
lon_var.standard_name = 'longitude' 
lon_var.long_name = 'longitude'

lat_var = nc.createVariable('lat', np.float64, ('y', 'x'))
lat_var[:] = lat
lat_var.units = 'degrees_north'
lat_var.standard_name = 'latitude'
lat_var.long_name = 'latitude'

proj_var = nc.createVariable('lambert_projection', np.int32, ())
proj_var.grid_mapping_name = 'lambert_conformal_conic'
proj_var.standard_parallel = 25.
proj_var.latitude_of_projection_origin = 40.
proj_var.longitude_of_central_meridian = -105.
proj_var.semi_major_axis = 6371000.0
proj_var

# ATTACH LAT/LON COORDINATES TO DATA VARIABLE

airtemp.coordinates = 'lon lat'
airtemp.grid_mapping = 'lambert_projection' 

