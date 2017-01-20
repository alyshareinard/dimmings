# -*- coding: utf-8 -*-
"""
Created on Tue May  3 16:02:21 2016

@author: alyshareinard
"""

import sys
from datetime import timedelta
import math
#import read_Lars_dimmings

sys.path.append('../common/')

def print_loc_diff(flare_loc, dim_ns, dim_ew):
    if len(flare_loc)==6 and flare_loc !="      ":
        ns=int(flare_loc[1:3])
        if flare_loc[0]=="S": ns=-ns
        ew=int(flare_loc[4:6])
        if flare_loc[3]=="E": ew=-ew
      
        ns_diff=ns-dim_ns
        ew_diff=ew-dim_ew
        print("ns_diff, ew_diff", ns_diff, ew_diff)
        return (ns_diff, ew_diff)
    else:
        print("no flare location")
        return(None, None)

def match_dimmings_flares():
    dimmings=read_Lars_dimmings()
    print(type(dimmings))
    (xray_flares, ha_flares)=get_flare_catalog(2013, 2014)
#    print("!!!!", xray_flares['peak_time'])
    #first check to make sure there is some overlap in dates
    print("dimming time", dimmings['time'])
    min_dimtime=min(dimmings['time'])
    max_dimtime=max(dimmings['time'])

    
    min_xray=min(xray_flares['peak_date'])
#    min_xray=min(x for x in xray_flares['peak_date'] if x is not None)
    max_xray=max(x for x in xray_flares['peak_date'] if x is not None)
    
    print("xray times", min_xray, max_xray)
    print("dimming times", min_dimtime, max_dimtime)
    
    if ((min_xray<min_dimtime and max_xray>min_dimtime) or (min_xray<max_dimtime and max_xray>max_dimtime)):
        print("we have overlap!")
#        for index in range(len(dimmings['time'])):
#            print(dimmings['time'][index])
            
#    print(xray_flares['peak_time'])
    #let's start with stepping through the dimmings
    match=[]
    match_dist=[]
    target_time=[]
    target_loc=[]
    dist_time=[]
    dist_loc=[]
    time_time=[]
    time_loc=[]
    for ind1 in range(len(dimmings['time'])):
        print("   ")
        print("   ")
        dim_ew=dimmings['mean_EW'][ind1]
        dim_ns=dimmings['mean_NS'][ind1]
        print("target dimming", dimmings['time'][ind1], "NS: ", dim_ns, "EW: ", dim_ew)
        
        target_time.append(dimmings['time'][ind1])
        target_loc.append([str(dim_ns)+str(dim_ew)])
#    for dim in dimmings:
        #this is going to be totally inefficient
        possibilities=[]
        for ind2 in range(len(xray_flares['peak_date'])):
            timediff=timedelta(hours=4)
            dimtime=dimmings['time'][ind1]
            flaretime=xray_flares['peak_date'][ind2]

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
            match_dist.append(None)
        elif len(possibilities)==1:
            print("one matching flare")
            
            x=possibilities[0]
            flare_loc=xray_flares['location'][x]
            print("flare loc", flare_loc)
            print("NOAA AR", xray_flares["NOAA_AR"][x])
            print("flare time", xray_flares['init_date'][x])#, xray_flares['peak_date'][x], xray_flares['final_date'][x])
            print("flare size", xray_flares['xray_class'][x], xray_flares['xray_size'][x])
            (ns_diff, ew_diff)=print_loc_diff(flare_loc, dim_ns, dim_ew)
            print("time diff", dimtime - xray_flares['init_date'][x])
            
            match.append(possibilities)
            match_dist.append(None)
        elif len(possibilities)>1:
            print("possible flare summary:")
            ns_diff=[]
            ew_diff=[]
            time_diff=[]

            for x in possibilities:
                flare_loc=xray_flares['location'][x]

                print("flare loc", flare_loc)
                print("NOAA AR", xray_flares["NOAA_AR"][x])
                print("flare time", xray_flares['init_date'][x])#, xray_flares['peak_date'][x], xray_flares['final_date'][x])
                print("flare size", xray_flares['xray_class'][x], xray_flares['xray_size'][x])
                (ns_d, ew_d)=print_loc_diff(flare_loc, dim_ns, dim_ew)
                #                print("len", len(flare_loc), flare_loc)
                t_diff=(dimtime - xray_flares['init_date'][x])
                time_diff.append(round((t_diff.days*86400+t_diff.seconds)/60./60., 2))
                ns_diff.append(ns_d)
                ew_diff.append(ew_d)
                print("time diff", dimtime - xray_flares['init_date'][x])
        
                print("  ")
          
            print("event summary")
            print("NS diffs: ", ns_diff)
            print("EW diffs: ", ew_diff)
            print("time differences (in hours): ", time_diff)#, timediff.index(min([abs(x) for x in time_diff])))
#            print("time differences (in hours/float): ", [float(x) for x in time_diff])

            tdiff_absfloat=[abs(float(x)) for x in time_diff]
            shortest_time=tdiff_absfloat.index(min(tdiff_absfloat))
            #the following is not exactly right -- it's an approximation
            #need to put in equations for great circle angle
            #set distance to 9999 when there is no location information
            dist=[math.sqrt(ns*ns+ew*ew) if ns !=None else 9999 for ns, ew in zip(ns_diff, ew_diff)]
            print("dist", dist)
            if len(dist)>0: 
                shortest_dist=dist.index(min(dist))
            else:
                shortest_dist=None
            if min(dist)==9999: shortest_dist=None
            print("shortest_time", shortest_time)
            print("shortest_dist", shortest_dist)
            match.append(possibilities[shortest_time])
            if shortest_dist==None or shortest_dist==shortest_time:
                match_dist.append(None)
            else:
                match_dist.append(possibilities[shortest_dist])            
    
#            dist_time.append(xray_flares['init_date'][x])
#          print(dim_ew, dim_ns, flare_loc, flare_ew, flare_ns)
    print("summary of all events:")
    for index in range(len(target_time)): 
        print("  ")
        print("  ")
        print("Target dimming")
        print("Time: ", target_time[index])
        print("Location: ", target_loc[index])
        print(" ")
        if match[index]!=None:
            print("Best flare based on time")
            print(xray_flares['location'][match[index]])
            print(xray_flares['init_date'][match[index]])
        else:
            print("No flare match")
            if match_dist[index]!=None:
                print("What?? There's a problem here")
        if match_dist[index]!=None:
            print("Best flare based on distance")
            print(xray_flares['location'][match_dist[index]])
            print(xray_flares['init_date'][match_dist[index]])
        else:
            print("No flare match based on distance")           
            
          
match_dimmings_flares()
    
    