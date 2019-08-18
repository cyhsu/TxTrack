import numpy as np
import xarray as xr
import os
from datetime import datetime, timedelta

np.random.seed(417)

class fetch(object):
    def __init__(self,site_lon, site_lat, start_time, end_time):
        threddsURL= 'http://hfrnet-tds.ucsd.edu/thredds/dodsC/HFR/USEGC/6km/hourly/GNOME/' + \
                                'HFRADAR,_US_East_and_Gulf_Coast,_6km_Resolution,_Hourly_RTV_(GNOME)_best.ncd'
        self.site_lon, self.site_lat = site_lon, site_lat
        self.start_time, self.end_time = np.datetime64(start_time), np.datetime64(end_time)
        self.ds = xr.open_dataset(threddsURL).sel(time=slice(start_time,end_time))
        self.ntim, self.nlat, self.nlon = self.ds.time.size, self.ds.lat.size, self.ds.lon.size

    def particle_move(self,ux,vx):
        lon_var = ux.interp(lon=self.site_lon,lat=self.site_lat)
        lat_var = vx.interp(lon=self.site_lon,lat=self.site_lat)
        return lon_var, lat_var

    def particle_newloc(self,ensemble,pertb):
        return ensemble[0]+pertb[0], ensemble[1]+pertb[1]

    def dataset_difference(ds):
        perturb01, perturb02 = self.perturb(), self.perturb()
        ux = (ds.isel(time=0).water_u + perturb01 - ds.isel(time=1).water_u + perturb02)
        vx = (ds.isel(time=0).water_v + perturb01 - ds.isel(time=1).water_v + perturb02)
        return ux,vx

    def particle_integrate(self,nperturb=2):
        center = [[self.site_lon, self.site_lat]]
        ensembles = {}
        ensembles[0] = center.copy()
        for tid in range(1,self.ntim-1):
            #-- center run calculation
            ds_diff = self.ds.isel(time=slice(tid-1,tid+1)).diff('time')
            lon_var, lat_var = self.particle_move(ds_diff)
            self.center([self.center[tid][0]+lon_var, self.center[tid][1]+lat_var])

            #-- ensemble runs
            ensemble = []
            for r in range(len(ensembles[tid-1])):
                ensemble += [self.particle_newloc(ensembles[tid][r],
                    self.particle_move(self.dataset_difference(self.ds.isel(time=slice(tid-1,tid+1)))
                )) for r2 in range(nperturb)

                # ensemble.extend([
                #     self.particle_newloc(
                #         ensembles[tid][r], self.particle_move(
                #             self.dataset_difference(
                #                 self.ds.isel(time=slice(tid-1,tid+1))
                # ))) for r2 in range(nperturb)
                # ])
            ensembles[tid] = ensemble
        return ensembles

    def perturb(self):
        #-- generate noise if data is not exist.
        #-- Based on the previous studies, the error of RMS or STD can reach to 50 cm /s, either on the Eastern
        #--  Coast of the USA or the Western Coast of the USA. I will take 5% of the 50 cm /s as the
        #-- randon noise range to perturb our GOM Dataset at each time step in order to obtain the
        #-- purterbation initial to derive the particle trajectory.
        purb = 50 * 0.05
        return np.random.uniform(-1*purb,purb,[self.nlat, self.nlon])



    def json(self):
        #-- output json format of the particle trajectory with time.
        return None

start_time = '2018-06-01'
end_time  = '2018-07-01'
index_unit = np.timedelta64(1,'h')
start_time = np.datetime64(start_time)
end_time  = np.datetime64(end_time)
