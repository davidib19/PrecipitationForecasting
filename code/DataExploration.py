import xarray
import os
import matplotlib.pyplot as plt
import _pickle as pickle
import numpy as np
from scipy import signal

maxLat = -3.5
minLat = -1.5
minLon = 280.
maxLon = 288.
lonCajas = 280.75
latCajas = -2.85
# Load data
os.chdir('..')


def merger(product, variable, name):
    """"Junta todos los archivos de la carpeta data/product/variable en un solo archivo llamado name"""
    files = os.listdir(os.path.join('data', product, variable))
    data = xarray.open_dataset(os.path.join('data', product, variable, files[0]), engine='netcdf4')
    for file in files[1:]:
        data = xarray.merge(
            [data, xarray.open_dataset(os.path.join('data', product, variable, file), engine='netcdf4')])
    data.to_netcfd(os.path.join('data', product, variable, name), engine='netcdf4')


data = xarray.open_dataset(os.path.join('data', 'ERA5', 'Wind', '2012-2016.nc'), engine='netcdf4')
data=xarray.merge([data,xarray.open_dataset(os.path.join('data', 'ERA5', 'Wind', '2017-2022.nc'), engine='netcdf4')])
data=xarray.merge([data,xarray.open_dataset(os.path.join('data', 'ERA5', 'AirTemperature', '2012-2022.nc'), engine='netcdf4')])
print(data)