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

basin = 'NAtl'
#case = '06' # irma
#ini_times = [
#'2017082700','2017082712',
#'2017082800','2017082812',
#'2017082900','2017082912',
#'2017083000','2017083012',
#'2017083100','2017083112',
#'2017090100','2017090112',
#'2017090200','2017090212',
#'2017090300','2017090312',
#'2017090400','2017090412',
#'2017090500','2017090512',
#'2017090600','2017090612',
#'2017090700','2017090712',
#'2017090800','2017090812',
#'2017090900','2017090912',
#'2017091000','2017091012',
#'2017091100','2017091112',
#'2017091200','2017091212',
#]

case = '10' # maria
#ini_times = [ 
#'2017091400','2017091412',
#'2017091500','2017091512',
#'2017091600','2017091612',
#'2017091700','2017091712',
#'2017091800','2017091812',
#'2017091900','2017091912',
#'2017092000','2017092012',
#'2017092100','2017092112',
#'2017092200','2017092212',
#'2017092300','2017092312',
#'2017092400','2017092412',
#'2017092500','2017092512',
#'2017092600','2017092612',
#'2017092700','2017092712',
#'2017092800','2017092812',
#'2017092900','2017092912',
#'2017093000','2017093012',
#'2017093100','2017093112',
#]

## test times
ini_times = [ '2017091800','2017091812','2017091900','2017091912'] 

#models = [ 'gfdl_gfs', 'gfs']
#models = [ 'gfdl2', 'dwd2', 'ec_oper','ukmo']
#models = [ 'gfdl2', 'dwd2', 'ec_oper', 'meteofrance2', 'gfs', 'gfsic' ]
#models = [ 'gfdl2', 'dwd2', 'ec_oper', 'he2f','meteofrance2','cmc2' ]

outfile_dir = '/archive/twb/track_plots/test/'
match_file_dir_root = [ \
                    '/archive/jhc/NGGPS/NCEP_fore/Analysis/TC/2017hurr/match/',                                      \
                    '/archive/jhc/DATA/EC_IFS_fore/20170801_20171031_from_Linus/Analysis/TC/match/',                 \
                    '/archive/jhc/fvGFS_201806/fvgfs_201806b_test/2017hurr_gfsIC/Analysis/TC/match/',                \
                    '/archive/jhc/fvGFS_201806/fvgfs_201806b_test/2017hurr_ifsIC/Analysis/TC/match/',                \
                  ] 


tag = "comp_ntu"
exps = [ 'GFS', 'IFS', 'SHiELD_gfsic', 'SHiELD_ifsic' ]
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
#    sx = 265
#    ex = 355
#    sy = 5
#    ey = 55
    sx = 270
    ex = 340
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
# function to plot one TC track
########################################################################
def plot_the_track(m,record,col,leg,lab_on,msize,sym):

## initialize arrays and assign data
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
## chop off tail of TC track (only plot first 5 days)


    plt.legend(loc='upper right',frameon=True)

######################################################################
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
#TC_names_file = "/home/Jan-Huey.Chen/Util/BT/201806_201906/"+basin+'_name.txt'
TC_names_file = "/home/Jan-Huey.Chen/Util/BT/2017_hurr_only/"+basin+'_name.txt'

tcn = open (TC_names_file, "r")
TC_names = []
lines = tcn.readlines()
for line in lines:
    TC_name = str(line[3:20])
    TC_names.append(TC_name.strip())
storm_order =  int(case) -1
TC_name = TC_names[storm_order]

print("Plotting for ",TC_name)


for it in ini_times:
    # setup figure
    fig = plt.figure(figsize=(11,8))
    ax = fig.add_axes([0.06, 0.10, 0.9, 0.8])
    m = setup_m(ax)

    print("Init Time: ", it)

    ecount = 0
    for model in match_file_dir_root:
    
        exp = exps[ecount]
        col = cols[ecount]
        ecount = ecount + 1
    
        filename = model + "2017." + basin + "." + case + ".txt"
        
        print("Reading model: ", filename)
        fo = open (filename, "r")
        
        lines = fo.readlines()
        
        record_obs = []
        record_obs_overlap = []
        record_model = []
        
        counter = 0
	
	 
        for line in lines:
            counter = counter + 1
            if counter != 1:
            # If counter is not first line of txt file, do below

		if "+++" in line:      # if header line, get save_title
                    data = line.split()
                    storm_num = str(data[0][0:5])
                    save_title = str(data[1])
                    if save_title == "overlap_BT_for":     
                        ini_time = str(data[2])
    
                    if np.size(record_obs) > 1 and model == match_file_dir_root[0]:
		    #if np.size(record_obs) > 1: 
    			plot_the_track(m,record_obs,'grey','BT',True,7,tys)
                        plot_the_track(m,record_obs,'grey','BT',False,4,'o')
			print("obs size: "+str(np.shape(record_obs)))
                        record_obs = []
                    if np.size(record_obs_overlap) > 1 :
			tmp = len(record_obs_overlap)
			tmp = tmp/2
                        plot_the_track(m,record_obs_overlap[0:tmp],'k','BT',False,7,tys)
                        plot_the_track(m,record_obs_overlap[0:tmp],'k','BT',False,4,'o')
			print("obs overlap size : "+str(np.shape(record_obs_overlap)))
                        record_obs_overlap = []
                    if np.size(record_model) > 1:
			tmp = len(record_model)/2
                        plot_the_track(m,record_model[0:tmp],col,exp,True,4,'o')
			print("model size: "+str(np.shape(record_model)))
                        record_model = []
        
                else:
     
                    if save_title == "full_BT": # if save_title == full_BT, go through all lines below and get data
        
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
        		 print(np.shape(record_obs))
                    if save_title == "overlap_BT_for":
                        if ini_time == it:              ### only get data for ini_time!!!
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
 			    print(np.shape(record_obs_overlap))   
                    if save_title == "forecast":
                        if ini_time == it:             ### only get data for ini_time!!!
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
       			    print(np.shape(record_model)) 
        if np.size(record_model) > 1:
            plot_the_track(m,record_model,col,exp,True,4,'o')
            print(np.shape(record_model))
	    print(record_model)
            record_model = []
        
        fo.close
    
        
    # save figure
    title = TC_name + ' tracks    Ini_time = ' + it 
    ax.set_title(title)

#    ulx = 0 # xmin
#    uly = 180 #ymax 
#    lrx = 360 # xmax
#    lry = 0 # ymin
#
#    xmin,ymin = m(ulx,lry)
#    xmax,ymax = m(lrx,uly)
#    ax.set_xlim([xmin,xmax])
#    ax.set_ylim([ymin,ymax])
    #ax.set_extent([-150,-20,-90,90])
    #plt.show()
    outfile_name = outfile_dir + '/'+ basin+ '_' + TC_name+ '_'+ it + '_' +tag+'.png'
    fig.savefig(outfile_name,orientation='landscape',bbox_inches='tight')
    plt.close(fig)
