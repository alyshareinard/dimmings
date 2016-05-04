# -*- coding: utf-8 -*-
"""
Created on Tue May  3 16:02:21 2016

@author: alyshareinard
"""
sys.path.append('../common/')

def match_dimmings_flares():
    dimmings=read_Lars_dimmings()
    print(type(dimmings))
    [ha_flares, xray_flares]=get_flare_catalog()
    
    #first check to make sure there is some overlap in dates
    min_dimtime=min(dimmings['time'])
    max_dimtime=max(dimmings['time'])
    print("dimtime", min_dimtime, max_dimtime)
    
    min_xray=min(x for x in xray_flares['peak_time'] if x is not None)
    max_xray=max(x for x in xray_flares['peak_time'] if x is not None)
    
    print("xray", min_xray, max_xray)
    
match_dimmings_flares()
    
    