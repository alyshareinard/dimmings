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
    match=[]
    for ind1 in range(len(dimmings['time'])):
        print("   ")
        print("target dimming", dimmings['time'][ind1])
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
#        print("possibilities", possibilities)
#        print("dimming location EW, NS", dimmings['mean_EW'][ind1], dimmings['mean_NS'][ind1])
#        print("flare location", [xray_flares['location'][x] for x in possibilities])
        if len(possibilities)==0:
            print("no matching flares")
            match.append(None)
        elif len(possibilities)==1:
            print("one matching flare")
            dim_ew=dimmings['mean_EW'][ind1]
            dim_ns=dimmings['mean_NS'][ind1]
            print("dimming ns, ew", dim_ns, dim_ew)
            x=possibilities[0]
            flare_loc=xray_flares['location'][x]
            print("flare loc", flare_loc)
            print("flare time", xray_flares['initial_time'][x], xray_flares['peak_time'][x], xray_flares['final_time'][x])
            print("flare size", xray_flares['xray_class'][x], xray_flares['xray_size'][x])

            match.append(possibilities)
        elif len(possibilities)>1:
            dim_ew=dimmings['mean_EW'][ind1]
            dim_ns=dimmings['mean_NS'][ind1]
            flare_ew=[]
            flare_ns=[]
            print("dimming ns, ew", dim_ns, dim_ew)
            for x in possibilities:
                flare_loc=xray_flares['location'][x]
                print("possible flare summary:")
                print("flare loc", flare_loc)
                print("flare time", xray_flares['initial_time'][x], xray_flares['peak_time'][x], xray_flares['final_time'][x])
                print("flare size", xray_flares['xray_class'][x], xray_flares['xray_size'][x])
                print("len", len(flare_loc), flare_loc)
                if len(flare_loc)==6 and flare_loc !="      ":
                    ns=int(flare_loc[1:3])
                    if flare_loc[0]=="S": ns=-ns
                    flare_ns.append(ns)
                    ew=int(flare_loc[4:6])
                    if flare_loc[3]=="E": ew=-ew
                    flare_ew.append(ew)
                  
                    ns_diff=ns-dim_ns
                    ew_diff=ew-dim_ew
                    print("ns_diff, ew_diff", ns_diff, ew_diff, ns, ew, dim_ns, dim_ew)
                else:
                    print("no flare location")
        

          
        
#          print(dim_ew, dim_ns, flare_loc, flare_ew, flare_ns)
          
          
match_dimmings_flares()
    
    