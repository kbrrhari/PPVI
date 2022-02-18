#!/usr/bin/env python
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
#import cartopy.crs as ccrs
import scipy
#import matplotlib.gridspec as gs
from scipy.interpolate import RectBivariateSpline
import os.path
import datetime
######################################################################
# Functions
def map_proj(m):
    m.gridlines(
        draw_labels=True,
                crs=ccrs.PlateCarree(),linewidth=0.5, color='gray', alpha=0.5, linestyle='--')
    m.coastlines()
#     m.xlabels_top = False
#     m.ylabels_right = False
    return m
######################################################################
def vert_avg(array,axis):
    # array: [time,levels,lat,lon]
    # axis = choose levels index
    # returns array of averaged values [time,lat,lon]
    
    array_interp = np.mean(array[:,int(np.array(np.where(ds.lev==925))):int(np.array(np.where(ds.lev==300))),:,:],axis=1);
    
    return array_interp
######################################################################
def lines_to_da(ft_lines):
    # https://xarray.pydata.org/en/stable/user-guide/combining.html
    array = np.zeros([5,len(ft_lines)])
    time = []
    intensity_list = []

    for i in np.arange(0,len(ft_lines)):

        line = ft_lines[i]
        data = line.split()

        t = int(data[0])
        time.append(t)
        lon = float(data[1])
        lat = float(data[2])
        pressure = float(data[3])
        wspd = float(data[4])
        wdir = float(data[5])
        intensity = str(data[6])
        intensity_list.append(intensity)

        array[0,i] = lon
        array[1,i] = lat
        array[2,i] = pressure
        array[3,i] = wspd
        array[4,i] = wdir

    lon = xr.DataArray(name='longitude',data=array[0,:],dims=['time'],coords=dict(time=time))
    lat = xr.DataArray(name='latitude',data=array[1,:],dims=['time'],coords=dict(time=time))
    pressure = xr.DataArray(name='pressure',data=array[2,:],dims=['time'],coords=dict(time=time))
    wspd = xr.DataArray(name='wspd',data=array[3,:],dims=['time'],coords=dict(time=time))
    wdir = xr.DataArray(name='wdir',data=array[4,:],dims=['time'],coords=dict(time=time))
    inten = xr.DataArray(name='intensity',data=intensity_list,dims=['time'],coords=dict(time=time))
    ds_grid = [[lon,lat,pressure,wspd,wdir,inten]]
    da = xr.combine_nested(ds_grid, concat_dim=["time", None])

    return da
#####################################################################
def return_pos_ind(ds,lat,lon):
    # objective: return index of lat/lon position of boundaries
    # ds = xr.dataset
    # ds.lon, ds.lat are coordinates
    # lon, lat from forecast BT files to get lat/lon 5x5 gride
    
    print(int(lon)-5, int(lon)+5)
    lon_lower = int(ds.lon[np.abs((lon-5)-ds.lon).argmin()]);print('###',lon_lower)
    lon_upper = int(ds.lon[np.abs((lon+5)-ds.lon).argmin()]);print(lon_upper)
    lat_lower = int(ds.lat[np.abs((lat-5)-ds.lat).argmin()]);print(lat_lower)
    lat_upper = int(ds.lat[np.abs((lat+5)-ds.lat).argmin()]);print(lat_upper)
        # stuck in here forever while loop
   #     except:
   #         i=i-0.5
   #         continue
   # try:
   #     print('Using original forecast model BT as storm center')
   #     lon_lower = 0
   #     lon_upper = 0
   #     lat_lower = 0
   #     lat_upper = 0
   #     lat = lat
   #     lon = lon
   # except IndexError:
   #     print('Script broke. Exiting script')
    return lon_lower, lon_upper, lat_lower, lat_upper, lat, lon    
#####################################################################
def return_pos_ind2(ds,lat,lon):
    # objective: return index of lat/lon position of boundaries
    # ds = xr.dataset
    # ds.lon, ds.lat are coordinates
    # lon, lat from forecast BT files to get lat/lon 5x5 gride
  
    try:
        lon_lower = np.where(ds.lon == int(lon)-5.5)[0][0]
        lon_upper = np.where(ds.lon == int(lon)+5.5)[0][0]
        lat_lower = np.where(ds.lat == int(lat)-5.5)[0][0]
        lat_upper = np.where(ds.lat == int(lat)+5.5)[0][0]
        
    except IndexError:
        try: 
            lon_lower = np.where(ds.lon == int(lon)-4.5)[0][0]
            lon_upper = np.where(ds.lon == int(lon)+4.5)[0][0]
            lat_lower = np.where(ds.lat == int(lat)-4.5)[0][0]
            lat_upper = np.where(ds.lat == int(lat)+4.5)[0][0]
            
        except IndexError:
            try: 
                lon_lower = np.where(ds.lon == int(lon)-3.5)[0][0]
                lon_upper = np.where(ds.lon == int(lon)+3.5)[0][0]
                lat_lower = np.where(ds.lat == int(lat)-3.5)[0][0]
                lat_upper = np.where(ds.lat == int(lat)+3.5)[0][0]

            except IndexError:
                try: 
                    lon_lower = np.where(ds.lon == int(lon)-2.5)[0][0]
                    lon_upper = np.where(ds.lon == int(lon)+2.5)[0][0]
                    lat_lower = np.where(ds.lat == int(lat)-2.5)[0][0]
                    lat_upper = np.where(ds.lat == int(lat)+2.5)[0][0]

                except IndexError:
                    try: 
                        lon_lower = np.where(ds.lon == int(lon)-1.5)[0][0]
                        lon_upper = np.where(ds.lon == int(lon)+1.5)[0][0]
                        lat_lower = np.where(ds.lat == int(lat)-1.5)[0][0]
                        lat_upper = np.where(ds.lat == int(lat)+1.5)[0][0]

                    except IndexError:
                        try: 
                            print('Using original forecast model BT as storm center')
                            lon_lower = 0
                            lon_upper = 0
                            lat_lower = 0
                            lat_upper = 0
                            lat = lat
                            lon = lon
                        except IndexError:
                            print('Exiting script')
 
    # returns indices of lat/lon boundaries
    return lon_lower, lon_upper, lat_lower, lat_upper, lat, lon 
######################################################################
def find_min_ind(array):
    ind = np.where(array == np.max(array))
    return ind
######################################################################

# Main Function
# objective: get lat and lon position of storm center for each storm for all forecast times

# storm
    # forecast_time 1
    # forecast_time 2
    # ...
f = open('/archive/jhc/DATA/EC_IFS_fore/20170801_20171031_from_Linus/Analysis/TC/match/2017.NAtl.10.txt','r')
#f = open('/archive/jhc/NGGPS/NCEP_fore/Analysis/TC/2017hurr/match/2017.NAtl.10.txt','r')
#f = open('/archive/jhc/fvGFS_201806/fvgfs_201806b_test/2017hurr_ifsIC/Analysis/TC/match/2017.NAtl.10.txt','r')
#f = open('/archive/jhc/fvGFS_201806/fvgfs_201806b_test/2017hurr_ifsIC/Analysis/TC/match/2017.NAtl.10.txt','r')
textfile = f.readlines()
f.close()

obs_times = textfile[0]
initialization_times = obs_times.split()[8:]
#print(initialization_times)
lines = textfile[1:]
ind = 0
ind_list = []
it_list = []
 
for line in lines:
    if 'overlap_BT_for' in line:
        ind_list.append(ind)
        tmp = line.split()[2]
        it_list.append(tmp)
    if 'forecast' in line:
        ind_list.append(ind)
        tmp = line.split()[2]
        it_list.append(tmp)
        
    ind+=1
#test
initialization_times = ['2017091700']
print(it_list)
#rootdir = '/arch5/twb/pv_inversion/2017/NAtl/10/SHiELD_ifsIC/'
rootdir = '/archive/twb/pv_inversion/2017/NAtl/10/IFS/'
for t in initialization_times:
    print('Opening PV file for forecast time: ',t)    
    date = t[0:8]
    hr = t[8:]
    ds = xr.open_dataset(rootdir+t+'/'+date+'_'+hr+'Z_pv.nc')    
    
    pv_interp = vert_avg(array=ds.pv,axis=1)

    # create 40 forecast times starting at each init time to point to times in model forecast BT data
    forecast_time_list = []
    i = 0
    ini_hour = t 
    while len(forecast_time_list) < 40: 
        dt_obj = datetime.datetime.strptime(ini_hour,'%Y%m%d%H')
        dt_obj = dt_obj + datetime.timedelta(hours=6)
        dt_str = datetime.datetime.strftime(dt_obj, '%Y%m%d%H')
        ini_hour = dt_str
        #print(ini_hour)
        forecast_time_list.append(dt_str)
        i+=1       
    try:
        init = it_list.index(t) + 1 # init forecast ind 
        fin = it_list.index(t) + 2 # end of forecast ind
        it_lines = lines[ind_list[init]:ind_list[fin]][1:] # ignore header
    except IndexError:
        init = it_list.index(t) + 1 # init forecast ind
        fin = it_list.index(t) + 2 # end of forecast ind
        it_lines = lines[ind_list[init]:][1:] # ignore header 
    except ValueError:
        continue
    #except ValueError:
    #    print('end of BT location file')
    #    break

#    if t and 'forecast' not in lines:
 #       break
#    try: 
#        lines[ind_list[fin]];
#    except IndexError:
#        print('end of BT location file')
#        break
#      
    print(*it_lines)   
    da = lines_to_da(it_lines)
    datimes = np.array(da.time)
    datimes = [str(datime) for datime in datimes]
    
    # open file to write
    abs_fpath = os.path.join(rootdir+t+'/center.txt')
    file1 = open(abs_fpath,'w')

    # compare each forecast time to time in datimes
    ii=0
    for ft in forecast_time_list:

        ft_str = datetime.datetime.strptime(ft,'%Y%m%d%H')
        ft_str = datetime.datetime.strftime(ft_str,'%HZ%d%^b%Y')

        try:
            ind = datimes.index(ft)
        except:
            # if datime not in forecast time, skip and set as 0
            lat = 0
            lon = 0
            linestr = str(ft_str)+' '+str(lat)+' '+str(lon)+'\n'
            file1.write(linestr)
            print('Writing location data to file:')
            print(linestr)
            continue # skip to next ft
  
        lat_bt = float(da.latitude[ind])
        lon_bt = float(da.longitude[ind])

        #testing
#        lon_lower = int(ds.lon[np.abs(int(lon)-5)-ds.lon).argmin()]);print(lon_lower)
#        lon_upper = int(ds.lon[np.abs(int(lon)+5)-ds.lon).argmin()];print(lon_upper)        
        #print(lat_bt, lon_bt)

        #print(int(lon_bt-5)-ds.lon)
        #print(np.abs((lon_bt-5)-ds.lon).argmin())
        #print(ds.lon[np.abs((lon_bt-5)-ds.lon).argmin()])

        #break
        
        # get actual max PV value with 5x5 box around lat_bt and lon_bt
        lon_lower, lon_upper, lat_lower, lat_upper, lat, lon  = return_pos_ind(ds,lat_bt,lon_bt)
        print('#######',type(lon_lower))
        print(np.arange(lon_lower,lon_upper,1))
        print(np.arange(lat_lower,lat_upper,1))
        
        if lon_lower==lon_upper==lat_lower==lat_upper==0:
            # if boundaries == 0, use original forecast BT location
            linestr = str(ft_str)+' '+str(round(lat_bt,1))+' '+str(round(lon_bt,1))+'\n'
            file1.write(linestr)
            print('Writing location data to file:')
            print(linestr)
            continue # skip to next ft    
        else:

            tmp = pv_interp.sel({'lon':np.arange(lon_lower,lon_upper,1),'lat':np.arange(lat_lower,lat_upper,1)})
            # create higher-res grid for spline inter
            lat_fine = np.linspace(ds.lat[lat_lower],ds.lat[lat_upper],len(ds.lat[lat_lower:lat_upper])*10)
            lon_fine = np.linspace(ds.lon[lon_lower],ds.lon[lon_upper],len(ds.lon[lon_lower:lon_upper])*10)

           # create spline object using original coordinates (x,y) and gridded data (z)
            try:
                spl = RectBivariateSpline(ds.lat[lat_lower:lat_upper],ds.lon[lon_lower:lon_upper],tmp[ii,:,:])
            except:
                # cannot create spline, too little data (position close to edge domain), use forecast bt position 
                linestr = str(ft_str)+' '+str(round(lat_bt,1))+' '+str(round(lon_bt,1))+'\n'
                file1.write(linestr)
                print('Writing location data to file:')
                print(linestr)
                continue # skip to next ft
  
            
            pv_fine = spl(lat_fine,lon_fine)
            
            # find lat/lon position of min pv val
            pos = find_min_ind(pv_fine);
            lat_ind = pos[0][0]
            lon_ind = pos[1][0]
            lon = round(lon_fine[lon_ind],1)
            lat = round(lat_fine[lat_ind],1)

        # write lat/lon to text file
        linestr = str(ft_str)+' '+str(lat)+' '+str(lon)+'\n'
        file1.write(linestr)
        print('Writing location data to file:')
        print(linestr)
        
        # test plot
#         fig = plt.figure(figsize=(11,8))
#         ax = fig.add_subplot(1,1,1,projection=ccrs.PlateCarree())
#         m = map_proj(ax)
#         ct = plt.contour(lon_fine,lat_fine,pv_interp,transform=ccrs.PlateCarree())
#         plt.clabel(ct,fmt='%g',inline_spacing=2,fontsize=8)
#         plt.scatter(lon_fine[lon_ind],lat_fine[lat_ind],50,marker='o',color='red',transform=ccrs.PlateCarree())
        
        # iterate through pv time file
        ii+=1
