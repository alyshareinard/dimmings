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
from sunpy_time import parse_time

def read_Lars_peakdim(data_path=os.path.join(os.path.dirname(os.path.realpath(__file__)), "data"), training=False):

    time=[]
    latloc=[]
    longloc=[]
    area=[]
    peakeuv=[]
    dim_name=[]

    rootdir=os.path.join(data_path, "SAV_files")+os.sep
    print("\nReading peak dimming information files from:", rootdir)
        
    files=os.listdir(rootdir+os.sep)
    
    count=0
    for file in files:
        if "_peakdim_props" in file:
            count+=1

    training_number=int(count/2.)
    count=0

    for file in files:
        if "_peakdim_props" in file:
#            print("reading", file)
            count+=1

            if training == True and count>training_number:
                print("half of dimmings returned for testing")
                break
            data=readsav(rootdir+file) #contains dim_name, peak_time, peakeuv_mean, peakeuv_max, peakeuv_min, peakbz_mean, peakabsbz_mean, peakbz_max
            #peakbz_min, peakarea_mm, ascend_period, descend_period, lifetime_hrs, peaktime_latloc, peaktime_longloc
#            try:
#                data=data['alldim']
#            except:
#                data=data['dimall']
            data=data['dimming']
            dim_name.append(data.dim_name[0].decode('utf-8'))
#            print("name", name)#.decode('utf-8'))
            area.append(data.peakarea_mm[0][0])
            latloc.append(data.peaktime_latloc[0][0])  
            longloc.append(data.peaktime_longloc[0][0])
            peakeuv.append(data.peakeuv_mean[0][0])
            time.append(parse_time(data.peak_time[0][0], time_format="utime"))
#                    print(time_val, data['dimstr3'].time)


   
    dimmings={'dim_name':dim_name, 'date':time, 'area':area, \
    'mean_EW':longloc, 'mean_NS':latloc, 'peakeuv':peakeuv}
    dimmings=pd.DataFrame(dimmings)
#    print("in routine", type(dimmings))
    return dimmings