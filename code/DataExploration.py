import xarray
import os
import matplotlib.pyplot as plt
import _pickle as pickle
import numpy as np
from scipy import signal
import random

# Constants
lonCajas = 280.75
latCajas = -2.85
latc = 1
lonc = 1
os.chdir('..')


def merger(product, variable, name):
    """"Junta todos los archivos de la carpeta data/product/variable en un solo archivo llamado name"""
    files = os.listdir(os.path.join('data', product, variable))
    data = xarray.open_dataset(os.path.join('data', product, variable, files[0]), engine='netcdf4')
    for file in files[1:]:
        data = xarray.merge(
            [data, xarray.open_dataset(os.path.join('data', product, variable, file), engine='netcdf4')])
    data.to_netcfd(os.path.join('data', product, variable, name), engine='netcdf4')


def add_month(date):
    """Agrega un mes a la fecha date"""
    if date[5:7] == '12':
        return str(int(date[:4]) + 1) + '-01'
    else:
        return date[:5] + str(int(date[5:7]) + 1).zfill(2)


def X_y_split(data):
    """Toma un arreglo de datos y lo separa en X e y"""
    X = []
    y = []
    data = data[:, :int(data.shape[1] / 84) * 84, :, 0]
    train = np.split(data, data.shape[1] / 84, axis=1)
    for arr in train:
        X += [arr[:, :72, :, :]]
        y += [arr[0, 72:, latc, lonc]]
    return X, y


def randomize_dataset(DATA):
    X_train = []
    y_train = []
    X_test = []
    y_test = []
    years = list(range(1978, 2023))
    months = []
    for i in range(1, 13):
        ryears = random.sample(years, 8)
        aux = list(map(lambda x: str(x) + '-' + str(i).zfill(2), ryears))
        months += aux
    months.sort()
    train = DATA.sel(time=slice('1978-01-01', months[0] + '01')).to_array().to_numpy()
    dummyX, dummyy = X_y_split(train)
    X_train += dummyX
    y_train += dummyy
    for i in range(len(months)):
        test = DATA.sel(time=slice(months[i] + '-01', add_month(months[i]) + '-01')).to_array().to_numpy()
        dummyX, dummyy = X_y_split(test)
        X_test += dummyX
        y_test += dummyy
    for i in range(len(months) - 1):
        train = DATA.sel(time=slice(add_month(months[i]) + '-01', months[i + 1] + '-01'))
        dummyX, dummyy = X_y_split(train)
        X_train += dummyX
        y_train += dummyy
    train = DATA.sel(time=slice(add_month(months[-1]) + '-01', '2023-01-01'))
    dummyX, dummyy = X_y_split(train)
    X_train += dummyX
    y_train += dummyy
    return np.array(X_train), np.array(y_train), np.array(X_test), np.array(y_test)
