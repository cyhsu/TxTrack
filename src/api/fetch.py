import numpy as np, xarray as xr, os
from datetime import datetime, timedelta
from glob import glob
global ensembles
np.random.seed(417)

class fetch(object):
    def __init__(self,site_lon, site_lat, start_time, end_time):

        self.site_lon, self.site_lat = site_lon, site_lat
        self.start_time, self.end_time = np.datetime64(start_time), np.datetime64(end_time)
        dt = np.timedelta64(1,'h')
        delta = int((self.end_time - self.start_time)/dt)
        self.tid_lists = ['{}'.format(
                            np.datetime_as_string(self.start_time +
                            i * dt)) for i in range(delta)]
        try:
            fid_lists = ['./src/download/hfradar_{}.nc'.format(
                         np.datetime_as_string(self.start_time +
                         i * dt)) for i in range(delta)]
            self.ds = xr.open_mfdataset(fid_lists,
                        combine='nested',
                        concat_dim='time').sel(time=slice(start_time,
                        end_time)).drop({'site_lon',
                                         'site_lat',
                                         'site_code',
                                         'site_netCode',
                                         'procParams',
                                         'time_offset',
                                         'time_run',
                                         'DOPx',
                                         'DOPy'})
            print('\t\t\t','Retrieve Dataset from local folder\n')
        except:
            threddsURL= 'http://hfrnet-tds.ucsd.edu/thredds/dodsC/HFR/USEGC/6km/hourly/GNOME/' + \
                        'HFRADAR,_US_East_and_Gulf_Coast,_6km_Resolution,_Hourly_RTV_(GNOME)_best.ncd'
            self.ds = xr.open_dataset(threddsURL).sel(time=slice(start_time,
                        end_time)).drop({'site_lon',
                                         'site_lat',
                                         'site_code',
                                         'site_netCode',
                                         'procParams',
                                         'time_offset',
                                         'time_run',
                                         'DOPx',
                                         'DOPy'})
            print('\t\t\t','Retrieve Dataset from UCSD HFRadar threddsURL\n')
        self.ds = self.ds.sel(lon=slice(site_lon-3, site_lon+3),
                              lat=slice(site_lat-3, 31))
        self.ntim, self.nlat, self.nlon = self.ds.time.size, self.ds.lat.size, self.ds.lon.size
    def particle_move(self,vel,loc):
        lon, lat = loc
        ux, vx = vel
        return ux.interp(lon=lon,lat=lat).data, vx.interp(lon=lon,lat=lat).data

    def particle_newloc(self,ensemble,loc,pertb=np.zeros(2)):
        if ~np.isnan(np.sum(loc)):
            value = [(pertb + ensemble + loc).tolist()]
        else: value = [ensemble]
        return value

    def dataset_difference(self,ds):
        ds = ds.diff('time')
        ux, vx = ds.water_u, ds.water_v
        return ux,vx

    def particle_integrate(self,nperturb=1):
        center = [[self.site_lon, self.site_lat]]
        ensembles = {}
        ensembles[0] = center.copy()
        for tid in range(1,self.ntim-1):
            # print(tid)
            # print('\t\t\t  datetime process: {}'.format(self.ds.isel(time=tid).time.data))
            #-- center run calculation
            vel = self.dataset_difference(self.ds.isel(time=slice(tid-1,tid+1)))
            loc = self.particle_move(vel, center[-1])
            center += self.particle_newloc(center[-1],loc)
            if nperturb >= 1:
                #-- ensemble runs
                ensemble = []
                for loc_previous in ensembles[tid-1]:
                    loc = self.particle_move(vel, loc_previous)
                    for r2 in range(nperturb):
                        ensemble += self.particle_newloc(loc_previous,
                                                        loc, pertb = self.perturb())
                ensembles[tid] = ensemble
        return center, ensembles

    def perturb(self):
        purb = 50 * 0.05
        return np.random.uniform(-1*purb,purb,[2])



    def json(self):
        #-- output json format of the particle trajectory with time.
        #center, ensembles = self.particle_integrate()
        Json01 = {
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [-96.40, 27.42],
                    [-96.30, 27.82],
                    [-96.20, 27.82],
                    [-95.60, 27.20]
                ]
                # "coordinates": [
                #     [-96.67, 27.43],
                #     [-96.33, 27.33],
                #     [-96.22, 27.00],
                #     [-96.58, 28.42]
                # ]
                # "coordinates": np.squeeze(center)
            },
            "properties":{
                "times": self.tid_lists
            }
        }
        return Json01


# index_unit = np.timedelta64(1,'h')
# start_time = np.datetime64(start_time)
# end_time  = np.datetime64(end_time)

if __name__ == '__main__':
    start_time = '2018-07-01'
    end_time  = '2018-07-03'
    cls = fetch(-94.88, 29.11,start_time,end_time)
    cls.particle_integrate()
