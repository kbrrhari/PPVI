#!/usr/bin/env python

import numpy as np
import xarray as xr
#import matplotlib.pyplot as plt
from array import array
import os.path
###########################
def reset_pv_binary():
    pv = np.array(ds.pv)
    pv[pv>0]=1
    pv[pv<0]=-1
    pv[pv==0]=-1
    
    return pv
###########################
# Main function
maskdir = '/archive/twb/pv_inversion/2017/NAtl/10/GFS/2017091700/mask/'
#rootdir = '/arch5/twb/pv_inversion/2017/NAtl/10/SHiELD_gfsIC/'
rootdir = '/archive/twb/pv_inversion/2017/NAtl/10/' 
modeldir = 'GFS/2017091700/20170917_00Z_sqinvph.nc'
# Positive PVs (low pressure systems)
#ds = xr.open_dataset('/archive/twb/pv_inversion/2017/NAtl/10/SHiELD_gfsIC/2017091700/20170917_00Z_sqinvph.nc')
ds = xr.open_dataset(rootdir+modeldir)

file1 = open(rootdir+'/GFS/2017091700/center.txt')

lines = file1.readlines();lines

for i in np.arange(0,len(ds.time)):
#for i in np.arange(0,1):
    line = lines[i].split()
    lat = line[1] # lat is second column
    lon = line[2] # lon is third column
    
    lat_array = np.array(ds.lat)
    lon_array = np.array(ds.lon)

    ind_lat = np.abs(lat_array-float(lat)).argmin()
    pos_lat = lat_array[ind_lat]
    ind_lon = np.abs(lon_array-float(lon)).argmin()
    pos_lon = lon_array[ind_lon]    
    
### NE quadrant #####################################################
    # reset pv binary array
    pv = reset_pv_binary()
    pv = pv[i,:,:,:]
    
    for j in np.arange(1,7): # ind for 925 to 300 hpa levels 
        pv[j,0:ind_lat,:]=-1
        pv[j,:,0:ind_lon]=-1

        #test: compare grads with plot here
        #fig = plt.figure(figsize=(11,8))
        #ax = fig.add_subplot(111)
        #plt.pcolormesh(pv[j,:,:])
        #plt.title('NE, Time ind: '+str(i+1)+';   '+'Lev: '+str(float(ds.lev[j])))

    # save file
    filename = maskdir + 'ne.' + str(i+1)
    with open(filename, 'ab') as wf:
      binary_array = array('i', pv.flatten(order='A'))
      binary_array.tofile(wf)
    wf.close()
    print(filename, ' saved!')

### SE quadrant #####################################################
    # reset pv binary array
    pv = reset_pv_binary()
    pv = pv[i,:,:,:]
    
    for j in np.arange(1,7): # ind for 925 to 300 hpa levels 
        pv[j,ind_lat:,:]=-1
        pv[j,:,0:ind_lon]=-1

        # test: compare grads with plot here
        #fig = plt.figure(figsize=(11,8))
        #ax = fig.add_subplot(111)
        #plt.pcolormesh(pv[j,:,:])
        #plt.title('SE, Time ind: '+str(i+1)+';   '+'Lev: '+str(float(ds.lev[j])))

    # save file
    filename = maskdir + 'se.' + str(i+1)
    with open(filename, 'ab') as wf:
      binary_array = array('i', pv.flatten(order='A'))
      binary_array.tofile(wf)
    wf.close()
    print(filename, ' saved!')

### SW quadrant #####################################################
    # reset pv binary array
    pv = reset_pv_binary()
    pv = pv[i,:,:,:]
    
    for j in np.arange(1,7): # ind for 925 to 300 hpa levels 
        pv[j,ind_lat:,:]=-1
        pv[j,:,ind_lon:]=-1

        # test: compare grads with plot here
        #fig = plt.figure(figsize=(11,8))
        #ax = fig.add_subplot(111)
        #plt.pcolormesh(pv[j,:,:])
        #plt.title('SW, Time ind: '+str(i+1)+';   '+'Lev: '+str(float(ds.lev[j])))

    # save file
    filename = maskdir + 'sw.' + str(i+1)
    with open(filename, 'ab') as wf:
      binary_array = array('i', pv.flatten(order='A'))
      binary_array.tofile(wf)
    wf.close()
    print(filename, ' saved!')
    
### NW quadrant #####################################################
    # reset pv binary array
    pv = reset_pv_binary()
    pv = pv[i,:,:,:]
    
    for j in np.arange(1,7): # ind for 925 to 300 hpa levels 
        pv[j,0:ind_lat,:]=-1
        pv[j,:,ind_lon:]=-1

        # test: compare grads with plot here
        #fig = plt.figure(figsize=(11,8))
        #ax = fig.add_subplot(111)
        #plt.pcolormesh(pv[j,:,:])
        #plt.title('NW, Time ind: '+str(i+1)+';   '+'Lev: '+str(float(ds.lev[j])))
        

    # save file
    filename = maskdir +  'nw.' + str(i+1)
    with open(filename, 'ab') as wf:
      binary_array = array('i', pv.flatten(order='A'))
      binary_array.tofile(wf)
    wf.close()
    print(filename, ' saved!')

###################################################################################
###################################################################################
# Negative PVs (high pressure systems)

#ds = xr.open_dataset('/archive/twb/pv_inversion/2017/NAtl/10/SHiELD_gfsIC/2017091700/20170917_00Z_sqinvph.nc')
ds = xr.open_dataset(rootdir+modeldir)
for t in np.arange(0,len(ds.time)):
    # assign variables
    lon_ind = np.abs(ds.lon-280.5).argmin()
    lat_ind = np.abs(ds.lat-30.5).argmin()
    lon_ind_end = np.abs(ds.lon-ds.lon[-1]).argmin()
    lon_ind_iterate = np.abs(ds.lon-280.5).argmin()
    pv = reset_pv_binary()
    
    for lev in np.arange(1,7): # 925 to 300 hpa
        ### BH ##############################################################
        # mask out CH slab 
        pv[t,lev,:,0:int(lon_ind)]=-1

        # # mask out  BH triangle
        for i in np.arange(int(lat_ind),len(ds.lat)):
            pv[t,lev,i:,lon_ind_iterate]=-1
            lon_ind_iterate+=1
        
        # reset index
        lon_ind_iterate = np.abs(ds.lon-280.5).argmin()

        # test 
        #fig = plt.figure()
        #ax = fig.add_subplot(111)
        #plt.pcolormesh(ds.lon,ds.lat,pv[t,lev,:,:])
        #plt.title('BH, Time ind: '+str(t+1)+';   '+'Lev: '+str(float(ds.lev[lev])))
        
     # save file
    filename = maskdir + 'bhigh.' + str(t+1)
    with open(filename, 'ab') as wf:
      binary_array = array('i', pv.flatten(order='A'))
      binary_array.tofile(wf)
    wf.close()
    print(filename, ' saved!')
        
##############################################################################
#ds = xr.open_dataset('/archive/twb/pv_inversion/2017/NAtl/10/SHiELD_gfsIC/2017091700/20170917_00Z_sqinvph.nc')
ds = xr.open_dataset(rootdir+modeldir)
pv = reset_pv_binary()

# assign variables
lon_ind = np.abs(ds.lon-280.5).argmin()
lat_ind = np.abs(ds.lat-30.5).argmin()
lon_ind_end = np.abs(ds.lon-ds.lon[-1]).argmin()
lon_ind_iterate = np.abs(ds.lon-280.5).argmin()
        
for t in np.arange(0,len(ds.time)):
    # assign variables
    lon_ind = np.abs(ds.lon-280.5).argmin()
    lat_ind = np.abs(ds.lat-30.5).argmin()
    lon_ind_end = np.abs(ds.lon-ds.lon[-1]).argmin()
    lon_ind_iterate = np.abs(ds.lon-280.5).argmin()
    pv = reset_pv_binary()
    
    for lev in np.arange(1,7): # 925 to 300 hpa
        ### CH ###############################################################
        # mask out BH slab
        pv[t,lev,0:int(lat_ind),int(lon_ind):]=-1

        # mask out BH triangle
        for i in np.arange(int(lat_ind),len(ds.lat)):
            pv[t,lev,i,int(lon_ind_iterate):]=-1
            lon_ind_iterate+=1
            
         # reset index
        lon_ind_iterate = np.abs(ds.lon-280.5).argmin()
        
        # test
        #fig = plt.figure()
        #ax = fig.add_subplot(111)
        #plt.pcolormesh(ds.lon,ds.lat,pv[t,lev,:,:])
        #plt.title('CH, Time ind: '+str(t+1)+';   '+'Lev: '+str(float(ds.lev[lev])))
        
    # save file
    filename = maskdir + 'chigh.' + str(t+1)
    with open(filename, 'ab') as wf:
      binary_array = array('i', pv.flatten(order='A'))
      binary_array.tofile(wf)
    wf.close()
    print(filename, ' saved!')

###############################################################
