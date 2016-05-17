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

def read_Lars_dimmings_simple():
 #   rootdir=os.getcwd()+"/Lars dimmings/Example_dimmings/"  
#    print("root first", rootdir)
    
#    print("root", rootdir)
  #  dim_num=[]
    area_mm_total=[]
    thresh=[]
    time=[]
    east_coos=[]
    west_coos=[]
    north_coos=[]
    south_coos=[]
    bad_files=[]
    if os.sep=="/":
        osdir=os.sep+os.path.join("Users", "alyshareinard")
    else:
        osdir=os.path.join("C:"+os.sep+"Users", "alysha.reinard.SWPC")

    rootdir=os.path.join(osdir, "Dropbox", "dimming_shared", "SAV_files")+os.sep
    print("fulldir", rootdir)
    data=readsav(rootdir+"0alldim_props.sav")
    print(data['alldim'].dim_name)

#                       thr=data['dimstr3'].thresh[0]
#                        area=sum(data['dimstr3'].area_mm_total[0])
#                        east=min(data['dimstr3'].east_coos[0])
#                        west=max(data['dimstr3'].west_coos[0])
#                        north=max(data['dimstr3'].north_coos[0])
#                        south=min(data['dimstr3'].south_coos[0])
#                        time_val=parse_time(data['dimstr3'].time, time_format="utime")
#    #                    print(time_val, data['dimstr3'].time)
#                        time_through=1
#                    else:
#    #                    print("time", data['dimstr3'].time)
#    #                    print("continuing in this directory")
#     #                   if dim !=data['dimstr3'].dim_num[0]:
#     #                       print("DIM!", dim[0], data['dimstr3'].dim_num[0])
#                        if thr !=data['dimstr3'].thresh[0]:
#                            print("THRESH!", thresh, data)
#                        if area<sum(data['dimstr3'].area_mm_total[0]):
#                            area=sum(data['dimstr3'].area_mm_total[0])
#                            time_val=parse_time(data['dimstr3'].time, time_format="utime")
#                            #print(time_val, data['dimstr3'].time)
#    
#    #                    print("north", north)
#    #                    print("new north", data['dimstr3'].north_coos[0])
#    #                    print("south", south)
#    #                    print("new south", data['dimstr3'].south_coos[0])
#    
#                        if east>min(data['dimstr3'].east_coos[0]):
#    #                        print("east is smaller", east, data['dimstr3'].east_coos[0])
#                            east=min(data['dimstr3'].east_coos[0])
#                            
#                        if west<max(data['dimstr3'].west_coos[0]):
#    #                        print("west change", west, data['dimstr3'].west_coos[0])
#                            west=max(data['dimstr3'].west_coos[0])
#    
#    
#                        if south>min(data['dimstr3'].south_coos[0]):
#    #                        print("south change", south, data['dimstr3'].south_coos[0])
#                            south=min(data['dimstr3'].south_coos[0])
#                            
#                        if north<max(data['dimstr3'].north_coos[0]):
#    #                        print("north is smaller", north, data['dimstr3'].north_coos[0])
#                            north=max(data['dimstr3'].north_coos[0])
#                            
#    #                        print("area", data['dimstr3'].area_mm_total)
#    #                        print("east", data['dimstr3'].east_coos, east)   
#    #                        print("west", data['dimstr3'].west_coos, west)
#    #                        print("north", data['dimstr3'].north_coos, north)
#    #                        print("south", data['dimstr3'].south_coos, south)
#        try:                
#            area_mm_total.append(area)
#            east_coos.append(east)
#            west_coos.append(west)
#            north_coos.append(north)
#            south_coos.append(south)
#            time.append(time_val)
#        except:
#            print("no data for directory", eachdir)
#                
#
#    print("area", area_mm_total)
#    print("east", east_coos)
#    print("west", west_coos)
#    print("north", north_coos)
#    print("south", south_coos)
#    for i in range(len(area_mm_total)):
#        print("time", time[i], "area: ", area_mm_total[i], "east: ", east_coos[i], "west: ", west_coos[i], "north: ", north_coos[i], "south: ", south_coos[i])

    dimmings={'time':time, 'area':area_mm_total, 'eastedge':east_coos, \
    'westedge':west_coos, 'northedge':north_coos, 'southedge':south_coos}
    print("in routine", type(dimmings))
    return dimmings

read_Lars_dimmings_simple()