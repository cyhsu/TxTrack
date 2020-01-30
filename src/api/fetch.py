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
                                        concat_dim='time'
                                       ).sel(time=slice(start_time,end_time))
            self.ds = self.ds[['water_u','water_v']]
            print('\t\t\t','Retrieve Dataset from local folder\n')
        except:
            threddsURL= 'http://hfrnet-tds.ucsd.edu/thredds/dodsC/HFR/USEGC/6km/hourly/GNOME/' + \
                        'HFRADAR,_US_East_and_Gulf_Coast,_6km_Resolution,_Hourly_RTV_(GNOME)_best.ncd'
            self.ds = xr.open_dataset(threddsURL).sel(time=slice(start_time,end_time))
            self.ds = self.ds[['water_u','water_v']]
            print('\t\t\t','Retrieve Dataset from UCSD HFRadar threddsURL\n')
        self.ds = self.ds.sel(lon=slice(site_lon-3, site_lon+3),
                              lat=slice(site_lat-3, 31)).load()
        print('\t\t\t', 'Load the entire dataset');
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

    def particle_location(self):
        locs = np.squeeze([[ (self.site_lon, self.site_lat)
                            for i1 in range(self.ntim)]
                            for i2 in range(self.ntim)])
        for tid in range(1, self.ntim):
            vel = self.ds.isel(time=tid).water_u, self.ds.isel(time=tid).water_v 
            for icon in range(tid):
                loc = self.particle_move(vel, locs[icon][tid-1])
                loc = np.squeeze(loc) if ~np.isnan(np.sum(loc)) else np.zeros(2)
                locs[icon][tid] = locs[icon][tid-1] + loc*3.600/np.array([96.,110.])
        return locs

    def particle_prob(self,nperturb=1):
        return 'Construction Working on....'

    def perturb(self):
        purb = 50 * 0.05
        return np.random.uniform(-1*purb,purb,[2])

    def json(self):
        #-- output json format of the particle trajectory with time.
        locations = self.particle_location()
        Json01 = []
        for num, loc in enumerate(locations):
            Json01.append({
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": loc.tolist()
                },
                "properties":{
                    "times": self.tid_lists
                }
            })
        return Json01


# index_unit = np.timedelta64(1,'h')
# start_time = np.datetime64(start_time)
# end_time  = np.datetime64(end_time)

if __name__ == '__main__':
    start_time = '2018-07-01'
    end_time  = '2018-07-03'
    cls = fetch(-94.88, 29.11,start_time,end_time)
    cls.particle_integrate()
