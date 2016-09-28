# -*- coding: utf-8 -*-
"""
Created on Tue May  3 16:02:21 2016

@author: alyshareinard
"""

import sys
from datetime import timedelta
#import read_Lars_dimmings

sys.path.append('../common/')

def match_dimmings_flares():
    dimmings=read_Lars_dimmings()
    print(type(dimmings))
    [ha_flares, xray_flares]=get_flare_catalog()
    print("!!!!", xray_flares['peak_time'])
    #first check to make sure there is some overlap in dates
    min_dimtime=min(dimmings['time'])
    max_dimtime=max(dimmings['time'])
    print("dimtime times", min_dimtime, max_dimtime)
    
    min_xray=min(x for x in xray_flares['peak_time'] if x is not None)
    max_xray=max(x for x in xray_flares['peak_time'] if x is not None)
    
    print("xray times", min_xray, max_xray)
    
    if ((min_xray<min_dimtime and max_xray>min_dimtime) or (min_xray<max_dimtime and max_xray>max_dimtime)):
        print("we have overlap!")
#        for index in range(len(dimmings['time'])):
#            print(dimmings['time'][index])
            
#    print(xray_flares['peak_time'])
    #let's start with stepping through the dimmings
    for ind1 in range(len(dimmings['time'])):
        print("dim", dimmings['time'][ind1])
#    for dim in dimmings:
        #this is going to be totally inefficient
        possibilities=[]
        for ind2 in range(len(xray_flares['peak_time'])):
            timediff=timedelta(hours=2)
            dimtime=dimmings['time'][ind1]
            flaretime=xray_flares['peak_time'][ind2]

#            print("ind2", ind1, ind2, len(xray_flares['peak_time']))
#            print("flare", ind1, ind2, flaretime)

            if flaretime !=None and flaretime<(dimtime+timediff) and flaretime>(dimtime-timediff):
                possibilities.append(ind2)
        print("possibilities", possibilities)
        print("dimming location EW, NS", dimmings['mean_EW'][ind1], dimmings['mean_NS'][ind1])
        print("flare location", [xray_flares['location'][x] for x in possibilities])
    
match_dimmings_flares()
    
    