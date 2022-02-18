#!/usr/bin/env python

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import numpy as np
import matplotlib.dates as mdates
import datetime as dt
import time
import sys
import glob

basin = 'NATL'
#case = '12'
#ini_times = ['2018092200','2018092500','2018092800','2018100100','2018100400','2018100700','2018101000']

case = '05'
ini_times = ['2018090100','2018090400','2018090700','2018091000','2018091300','2018091600']

#case = '07'
#ini_times = ['2018091000','2018091300','2018091600']

models = [ 'gfdl2', 'ec_oper',  'gfsic', 'gfs']
#models = [ 'gfdl2', 'dwd2', 'ec_oper','ukmo']
#models = [ 'gfdl2', 'dwd2', 'ec_oper', 'meteofrance2', 'gfs', 'gfsic' ]
#models = [ 'gfdl2', 'dwd2', 'ec_oper', 'he2f','meteofrance2','cmc2' ]

outfile_dir = '/archive/jhc/DIMOSIC/Analysis/TC/track_plots/'
match_file_dir_root = '/archive/jhc/DIMOSIC/Analysis/TC/match/' 

tag = "comp_ntu"
exps = [ 'SHiELD_ifsic', 'IFS', 'SHiELD_gfsic', 'GFS' ]
#exps = [ 'SHiELD', 'ICON','IFS', 'UM', 'ARPEGE','GFS', 'SHiELD_gfsic' ]
#exps = [ 'SHiELD', 'ICON','IFS','IFS_47r1','ARPEGE','CMC' ]

cols = ['r','b','g','y','orange','m','cyan','olive','indigo','gray','saddlebrown','teal']


########################################################################
# setup figures
########################################################################
def setup_m(ax):
    #sx = 295
    #ex = 355
    #sy = 25
    #ey = 45
    sx = 265
    ex = 355
    sy = 5
    ey = 55
    
    m = Basemap(projection='cyl',llcrnrlon=sx,llcrnrlat=sy,urcrnrlon=ex,urcrnrlat=ey,ax=ax,resolution='l')
    #m.bluemarble()

    m.drawcoastlines(color='dimgrey')
    m.drawmapboundary(fill_color='white')
    m.fillcontinents(color='white',lake_color='white')
    parallels = np.arange(-80.,81,10.)
    meridians = np.arange(10.,351.,20.)
    m.drawparallels(parallels,labels=[True,False,False,False],color='grey',linewidth=0.)
    m.drawmeridians(meridians,labels=[False,False,False,True],color='grey',linewidth=0.)

    return m
########################################################################
# funciton to plot one TC track
########################################################################
def plot_the_track(m,record,col,leg,lab_on,msize,sym):

    nn = np.shape(record)[0]
    x = np.zeros(nn)
    y = np.zeros(nn)
    w = np.zeros(nn)
    for i in np.arange(nn):
        y[i]=record[i]["lat"]
       	x[i]=record[i]["lon"]
       	w[i]=record[i]["wind"]

## remove the tail if it cross prime merdian (0E)
    for i in np.arange(nn):
        if (x[i]-x[i-1]) < -250.:
            newnn = i
            break
        else:
            newnn = 0

    if sym == tys:
       fill = 'none'
    else: 
       fill = 'full'


    if lab_on:
        if newnn != 0: 
            m.plot(x[0:newnn],y[0:newnn],label=leg,marker=sym,color=col,markeredgecolor=col,fillstyle=fill, linewidth=1.5, markersize=msize, markeredgewidth=1.5)
        else:
            m.plot(x,y,label=leg,marker=sym,color=col,markeredgecolor=col, fillstyle=fill,linewidth=1.5,markersize=msize,markeredgewidth=1.5)
    else:
        if newnn != 0: 
            m.plot(x[0:newnn],y[0:newnn],marker=sym,color=col,markeredgecolor=col,fillstyle=fill,linewidth=1.5,markersize=msize, markeredgewidth=1.5)
        else:
            m.plot(x,y,marker=sym,color=col,markeredgecolor=col,fillstyle=fill,linewidth=1.5,markersize=msize,markeredgewidth=1.5)

    plt.legend(loc='upper right',frameon=True)
########################################################################
# hurricane symbol from
# https://stackoverflow.com/questions/44726675/custom-markers-using-python-matplotlib
########################################################################
def get_hurricane():
    u = np.array([  [2.444,7.553],
                    [0.513,7.046],
                    [-1.243,5.433],
                    [-2.353,2.975],
                    [-2.578,0.092],
                    [-2.075,-1.795],
                    [-0.336,-2.870],
                    [2.609,-2.016]  ])
    u[:,0] -= 0.098
    codes = [1] + [2]*(len(u)-2) + [2]
    u = np.append(u, -u[::-1], axis=0)
    codes += codes

    return mpath.Path(3*u, codes, closed=False)
#########################################################################
# Main program starts here:
#########################################################################

tys = get_hurricane()

# get TC's name with basin number for the year
TC_names_file = "/home/Jan-Huey.Chen/Util/BT/201806_201906/"+basin+'_name.txt'
tcn = open (TC_names_file, "r")
TC_names = []
lines = tcn.readlines()
for line in lines:
    TC_name = str(line[3:20])
    TC_names.append(TC_name.strip())
storm_order =  int(case) -1
TC_name = TC_names[storm_order]

print "Plotting for", TC_name


for it in ini_times:
    # setup figure
    fig = plt.figure(figsize=(11,8))
    ax = fig.add_axes([0.06, 0.10, 0.9, 0.8])
    m = setup_m(ax)

    ecount = 0
    for model in models:
    
        exp = exps[ecount]
        col = cols[ecount]
        ecount = ecount + 1
    
        filename = match_file_dir_root + model + "/" + basin + "." + case + ".txt"
        
        print "Reading", filename
        fo = open (filename, "r")
        
        lines = fo.readlines()
        
        record_obs = []
        record_obs_overlap = []
        record_model = []
        
        counter = 0
    
        for line in lines:
            counter = counter + 1
            if counter != 1:
        
                if "+++" in line:
                    data = line.split()
                    storm_num = str(data[0][0:5])
                    save_title = str(data[1])
                    if save_title == "overlap_BT_for":
                        ini_time = str(data[2])
    
                    if np.size(record_obs) > 1 and model == models[0]:
                        plot_the_track(m,record_obs,'grey','BT',True,7,tys)
                        plot_the_track(m,record_obs,'grey','BT',False,4,'o')
                        record_obs = []
                    if np.size(record_obs_overlap) > 1 :
                        plot_the_track(m,record_obs_overlap,'k','BT',False,7,tys)
                        plot_the_track(m,record_obs_overlap,'k','BT',False,4,'o')
                        record_obs_overlap = []
                    if np.size(record_model) > 1:
                        plot_the_track(m,record_model,col,exp,True,4,'o')
                        record_model = []
        
                else:
     
                    if save_title == "full_BT":
        
                         data = line.split()
                         time = int(data[0])
                         lon = float(data[1])
                         lat = float(data[2])
                         pres = float(data[3])
                         wind = float(data[4])
        
                         item = {}
        
                         item["time"] = time
                         item["lat"] = lat
                         item["lon"] = lon
                         item["wind"] = wind
                         item["pres"] = pres
                         record_obs.append(item)
        
                    if save_title == "overlap_BT_for":
                        if ini_time == it:
                            data = line.split()
                            time = int(data[0])
                            lon = float(data[1])
                            lat = float(data[2])
                            pres = float(data[3])
                            wind = float(data[4])
        
                            item = {}
        
                            item["time"] = time
                            item["lat"] = lat
                            item["lon"] = lon
                            item["wind"] = wind
                            item["pres"] = pres
                            record_obs_overlap.append(item)
    
                    if save_title == "forecast":
                        if ini_time == it:
                            data = line.split()
                            time = int(data[0])
                            lon = float(data[1])
                            lat = float(data[2])
                            pres = float(data[3])
                            wind = float(data[4])
        
                            item = {}
        
                            item["time"] = time
                            item["lat"] = lat
                            item["lon"] = lon
                            item["wind"] = wind
                            item["pres"] = pres
                            record_model.append(item)
        
        if np.size(record_model) > 1:
            plot_the_track(m,record_model,col,exp,True,4,'o')
            record_model = []
        
        fo.close
    
        
    # save figure
    title = TC_name + ' tracks    Ini_time = ' + it 
    ax.set_title(title)
    #plt.show()
    outfile_name = outfile_dir + '/'+ basin+ '_' + TC_name+ '_'+ it + '_' +tag+'.png'
    fig.savefig(outfile_name,orientation='landscape',bbox_inches='tight')
    plt.close(fig)
