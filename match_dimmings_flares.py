# -*- coding: utf-8 -*-
"""
Created on Tue May  3 16:02:21 2016

@author: alyshareinard
"""

import sys

sys.path.append('../common/')

def match_dimmings_flares():
    dimmings=read_Lars_dimmings()
    print(type(dimmings))
    [ha_flares, xray_flares]=get_flare_catalog()
    
    #first check to make sure there is some overlap in dates
    min_dimtime=min(dimmings['time'])
    max_dimtime=max(dimmings['time'])
    print("dimtime times", min_dimtime, max_dimtime)
    
    min_xray=min(x for x in xray_flares['peak_time'] if x is not None)
    max_xray=max(x for x in xray_flares['peak_time'] if x is not None)
    
    print("xray times", min_xray, max_xray)
    
    if ((min_xray<min_dimtime and max_xray>min_dimtime) or (min_xray<max_dimtime and max_xray>max_dimtime)):
        print("we have overlap!")
        for index in range(len(dimmings['time'])):
            print(dimmings['time'][index])
#        TODO: here's where we put in the code to match up dimmings and flares
    
match_dimmings_flares()
    
    