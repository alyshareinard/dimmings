# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 16:05:09 2016

@author: alyshareinard
"""

import sys
sys.path.append('../common/')
from scipy.io.idl import readsav
import os
from datetime import datetime, timezone
from sunpy_time import parse_time
import pandas as pd

def read_Lars_dimmings_simple():
 #   rootdir=os.getcwd()+"/Lars dimmings/Example_dimmings/"  
#    print("root first", rootdir)
    
#    print("root", rootdir)
  #  dim_num=[]
    area_mm_total=[]
#    thresh=[]
    time=[]
    east_coos=[]
    west_coos=[]
    north_coos=[]
    south_coos=[]
#    bad_files=[]


    if os.sep=="/":
        osdir=os.path.join("/Users", "alyshareinard", "Dropbox", "Work")
    else:
        osdir=os.path.join("C:"+os.sep+"Users", "alysha.reinard", "Documents")

    rootdir=os.path.join(osdir, "data", "Lars dimmings")+os.sep


    print("fulldir", rootdir)
    data=readsav(rootdir+"0alldim_props.sav", python_dict=True)
    print(data)
    data=data["alldim"] #contains dim_name, area_mm, time, euv_mean, euv_max, euv_min, bz_mean, absbz_mean, bz_max, bz_min, north_coos, south_coos, east_coos, west_coos
    print(data[0])
    #IT IS CONFUSING TO READ THIS IN SINCE THERE ARE ONLY "DIM NAME"s FOR EACH DIMMING AND EVERYTHING ELSE IS MULTPLE PER DIMMING
    dim_dict={"name": data["DIM_NAME"][0], "time":data["TIME"][0], "area": data["AREA_MM"][0], "EAST_COOS":data["EAST_COOS"][0], "WEST_COOS":data["WEST_COOS"][0], "NORTH_COOS":data["NORTH_COOS"][0], "SOUTH_COOS":data["SOUTH_COOS"][0]}
    print("NAME", len(dim_dict["name"]))
    print("area", len(dim_dict["area"]))
    
    dimming_df=pd.DataFrame.from_dict(dim_dict)
#    print(data['alldim'].area)
    print(dimming_df.keys())
#    print("time zero", dimming_df["TIME"].shape())
    
    time=dimming_df["time"]
    print(len(time))
    dimming_df["date"]=[parse_time(x, timezone.utc) for x in dimming_df["time"]]
    print(dimming_df["date"])

    return dimming_df
    #    dimmings={'time':time, 'area':area_mm_total, 'eastedge':east_coos, \
#    'westedge':west_coos, 'northedge':north_coos, 'southedge':south_coos}
#    print("in routine", type(dimmings))
#    return dimmings

read_Lars_dimmings_simple()