# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 16:05:09 2016

@author: alyshareinard
"""

import sys
sys.path.append('../common/')
from scipy.io.idl import readsav
import os
import pandas as pd
from datetime import datetime, timezone
from sunpy_time import parse_time

def read_Lars_alldim(training=False):
 #   rootdir=os.getcwd()+"/Lars dimmings/Example_dimmings/"  
#    print("root first", rootdir)
    
#    print("root", rootdir)
  #  dim_num=[]
    area_mm=[]
    time=[]
    east_coos=[]
    west_coos=[]
    north_coos=[]
    south_coos=[]
    dim_name=[]
    if os.sep=="/":
        osdir=os.path.join("/Users", "alyshareinard", "Dropbox", "Work")
    else:
        osdir=os.path.join("C:"+os.sep+"Users", "alysha.reinard", "Documents")

    rootdir=os.path.join(osdir, "PROJECTS", "Larisza", "dimming_shared", "SAV_files")+os.sep
    print("fulldir", rootdir)
        
    files=os.listdir(rootdir+os.sep)
    
    count=0
    for file in files:
        if "_alldim_props" in file:
            count+=1

    training_number=int(count/2.)
    count=0
    print("!!!!!!!!", training, training_number, len(files))
    for file in files:
        if "_peakdim_props" in file:
            print("reading", file)
            count+=1

            if training == True and count>training_number:
                print("half of dimmings returned for testing")
                break
            data=readsav(rootdir+file) #contains dim_name, area_mm, time, euv_min, bz_mean, absbz_mean, bz_max, north_coos, south_coos, east_coos, west_coos
            print(data)
            try:
                data=data['alldim']
            except:
                data=data['dimall']      
            name=data.dim_name[0].decode('utf-8')
#            print("name", name)#.decode('utf-8'))
            area=data.area_mm[0][0]
            east=data.east_coos[0][0]
            west=data.west_coos[0][0]
            north=data.north_coos[0][0]
            south=data.south_coos[0][0]
            time_val=parse_time(data.time[0][0], time_format="utime")
#                    print(time_val, data['dimstr3'].time)

   
#            print("name try", name)
            dim_name.append(name)            
            area_mm.append(area)
            east_coos.append(east)
            west_coos.append(west)
            north_coos.append(north)
            south_coos.append(south)
            time.append(time_val)

    mean_EW=[(x+y)/2 for x,y in zip(east_coos, west_coos)]
    mean_NS=[(x+y)/2 for x,y in zip(north_coos, south_coos)]
   
    dimmings={'dim_name':dim_name, 'date':time, 'area':area_mm, 'eastedge':east_coos, \
    'westedge':west_coos, 'northedge':north_coos, 'southedge':south_coos, \
    'mean_EW':mean_EW, 'mean_NS':mean_NS}
    dimmings=pd.DataFrame(dimmings)
#    print("in routine", type(dimmings))
    return dimmings

read_Lars_alldim()