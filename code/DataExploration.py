import xarray
import os
import matplotlib.pyplot as plt
import _pickle as pickle
import xrscipy.other.signal as dsp
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
"""
ecu = xarray.open_dataset(os.path.join('data', 'NOAA', 'AirTemperature', '1979.nc'), engine='netcdf4').sel(lat=slice(minLat, maxLat), lon=slice(minLon, maxLon))
for filename in os.listdir(os.path.join('data', 'NOAA', 'AirTemperature')):
    if filename.endswith(".nc") and filename != '1979.nc':
        ecu = xarray.merge([ecu, xarray.open_dataset(os.path.join('data', 'NOAA', 'AirTemperature', filename), engine='netcdf4').sel(lat=slice(minLat, maxLat), lon=slice(minLon, maxLon))])
#pickle ecu
print(ecu.lat.values)
pickle.dump(ecu, open(os.path.join('data', 'NOAA', 'AirTemperature', 'ecuador.p'), 'wb'))

cajas = ecu.sel(lat=latCajas, lon=lonCajas, method='nearest')
#pickle cajas
pickle.dump(cajas, open(os.path.join('data', 'NOAA', 'AirTemperature', 'cajas.p'), 'wb'))
plt.plot(cajas.time, cajas.air)
plt.show()
"""
with open(os.path.join('data', 'NOAA', 'AirTemperature', 'cajas.p'), 'rb') as f:
    cajas = pickle.load(f)
T= cajas.air.values.flatten()
print(T)
fs=1
f, t, Sxx = signal.spectrogram(T, fs,nperseg=10*365,noverlap=365)
f=f*365
t=t/365
plt.pcolormesh(t, f, Sxx, shading='gouraud')
plt.ylabel('Frequency [1/year]')
plt.xlabel('Time [year]')
plt.show()