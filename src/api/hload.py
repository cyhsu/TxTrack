__author__ = 'Chuan-Yuan Hsu'
#--
#--  This is the api to download the hfradar from UCSD hfradar data thredds server directory
#--

import xarray as xr
import numpy as np
import os
import time
from glob import glob

#-- Last Time Updated:
head_dirc = '/TxTrack/download/'
flists = glob(head_dirc+'*.nc'); flists.sort()
print(os.getcwd(),'\n', len(flists))
try:
	LastTimeUpdate = flists[-1].split('hfradar_')[-1][:-3]
except: 
	LastTimeUpdate = '2017-01-01T00:00:00'
print(LastTimeUpdate,'\n\n\n')

threddsURL= 'http://hfrnet-tds.ucsd.edu/thredds/dodsC/HFR/USEGC/6km/hourly/GNOME/' + \
            'HFRADAR,_US_East_and_Gulf_Coast,_6km_Resolution,_Hourly_RTV_(GNOME)_best.ncd'

ds = xr.open_dataset(threddsURL).sel(lon=slice(-98,-76),
                                     lat=slice(20,35),
                                     time=slice(LastTimeUpdate,
                                                time.strftime('%Y-%m-%dT%H:%M:%S',
                                                              time.gmtime())))
print(LastTimeUpdate)
for tid in range(1,ds.time.size):
    dsoutput = ds.isel(time=tid)
    print('\t Load and Store Dataset at time: {}'.format(dsoutput.time.data))
    OutNC = head_dirc+'hfradar_{}.nc'.format(np.datetime_as_string(dsoutput.time.data)[:-10])
    print(OutNC)
    dsoutput.to_netcdf(OutNC)
    #break
