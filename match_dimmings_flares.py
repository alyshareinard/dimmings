# -*- coding: utf-8 -*-
"""
Created on Tue May  3 16:02:21 2016

@author: alyshareinard
"""

import sys
from datetime import timedelta
import math
import os
import numpy as np
import pandas as pd
#import read_Lars_dimmings

sys.path.append('../common/')

def is_nat(npdatetime):
    try:
        npdatetime.strftime('%x')
        return False
    except:
        return True
  
def create_datetime_cme(ymd, hm):
    date=[]
    #unpack ymd and fix year

    for item, ihm in zip(ymd, hm):
#        print("len(date): ", len(date))
        print("item", item)
        print("ihm", ihm)
        if pd.isnull(item)==True:
##            print("blank line")
            date.append(None)
            continue
        
#        print(item)
        
#        print(datestr)
    
        datestr=str(item).split("/")
        year=int(datestr[0])
        month=int(datestr[1])
        day=int(datestr[2])
        print(ihm)
        hms=ihm.split(":")
        hour=int(hms[0])
        minute=int(hms[1])
        second=int(hms[1])
    
#        print(day, month, year, hour, minute)
#        print(datetime(year, month, day, hour, minute))
        try:
            date.append(datetime(year, month, day, hour, minute))
#                print("here ", date[-1])
#            print(datetime(year, month, day, hour, minute))
        except:
            date.append(None)
    return date
      
def create_datetime2(ymd, hm):
    date=[]
    #unpack ymd and fix year

    for item, ihm in zip(ymd, hm):
#        print("len(date): ", len(date))
        print("item", item)
        if item=="  " or np.isnan(item)==True:
#            print("blank line")
            date.append(None)
            continue
        
#        print(item)
        
#        print(datestr)
        datestr=str(item)
        year=int(datestr[0:2])
        month=int(datestr[2:4])
        day=int(datestr[4:6])

        #fix two year dates without messing up 4 year dates
        if year<70: 
            year=year+2000
        elif  year<100: 
            year+=1900
        
        if math.isnan(ihm)==False:
            hour=math.floor(ihm/100)
            minute=math.floor(ihm-hour*100)

            #now check to see if the time is past 2400 and adjust
            if hour>=24:
                hour-=24
                day+=1
                [day, month, year]=check_daymonth(day, month, year)
            #print(day, month, year, hour, minute)
            try:
                date.append(datetime(year, month, day, hour, minute))
#                print("here ", date[-1])
                #print(datetime(year, month, day, hour, minute))
            except:
                date.append(None)
        else:
            date.append(None)
    return date
    
def read_hand_flares():
    if os.sep=="/":
        osdir=os.path.join("/Users", "alyshareinard", "Dropbox", "Work")
    else:
        osdir=os.path.join("C:"+os.sep+"Users", "alysha.reinard", "Documents")
    file=os.path.join(osdir, "data", "Lars dimmings", "dim_flare_hand.txt")
    names=["dim_name", "date", "start", "end", "peak", "loc", "flare_class", 
    "flare_size", "station", "something", "AR", "LarAR"]
    data=pd.read_csv(file, sep=" ", header=None, names=names)

    data["init_date"]=create_datetime2(data["date"], data["start"])
    data["peak_date"]=create_datetime2(data["date"], data["peak"])
    data["final_date"]=create_datetime2(data["date"], data["end"])    
#    print(data)
    return data
    
def read_hand_cmes():
    if os.sep=="/":
        osdir=os.path.join("/Users", "alyshareinard", "Dropbox", "Work")
    else:
        osdir=os.path.join("C:"+os.sep+"Users", "alysha.reinard", "Documents")
    file=os.path.join(osdir, "data", "Lars dimmings", "dim_cme_hand.txt")
    names=["dim_name", "date", "time", "PA", "width", "speed_lin", "speed_20init", 
    "speed_20final", "speed_2020", "accel", "mass", "ke", "mpa"]
    data=pd.read_csv(file, sep=" ", header=None, names=names)
#    print("all the times", data)
    data["date"]=create_datetime_cme(data["date"], data["time"])
#    print(data["date"])
    return data


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
    dimmings=read_Lars_alldim()
    hand_matches=read_hand_flares()
    
#    print(type(dimmings))
    (xray_flares, ha_flares)=get_flare_catalog(2013, 2014)
#    print("!!!!", xray_flares['peak_time'])
    #first check to make sure there is some overlap in dates
#    print("dimming time", dimmings['time'])
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
    target_name=[]
#    print(xray_flares["init_date"])
    
    for ind1 in range(len(dimmings['time'])):
        print("   ")
        print("   ")
        dim_ew=dimmings['mean_EW'][ind1]
        dim_ns=dimmings['mean_NS'][ind1]
        print("target dimming", dimmings['dim_name'][ind1], dimmings['time'][ind1], "NS: ", dim_ns, "EW: ", dim_ew)
        
        target_time.append(dimmings['time'][ind1])
#        print("is this the target", dimmings['dim_name'][ind1])
        target_name.append(dimmings['dim_name'][ind1])
        if dim_ns<0:
            NS="S"
        else:
            NS="N"
        if dim_ew<0:
            EW="E"
        else:
            EW="W"
        target_loc.append([NS+str(int(abs(round(dim_ns))))+EW+str(int(abs(round(dim_ew))))])
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
                #now check location
                flare_loc=xray_flares['location'][ind2]
                (ns_diff, ew_diff)=print_loc_diff(flare_loc, dim_ns, dim_ew)
                if ns_diff !=None:      
                    dist=math.sqrt(ns_diff*ns_diff+ew_diff*ew_diff)
                else:
                    dist=None
#                print("!!!!DIST", dist)
                if dist == None or dist<30:
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
            if ns_diff !=None:      
                dist=math.sqrt(ns_diff*ns_diff+ew_diff*ew_diff) 
            else: dist=None
            match.append(possibilities[0])
            match_dist.append(possibilities[0])
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
                #require within 30 degrees
                if shortest_dist>30:
                    shortest_dist=None
            else:
                shortest_dist=None
            if min(dist)==9999: shortest_dist=None
            print("shortest_time", shortest_time)
            print("shortest_dist", shortest_dist)
            print(possibilities[shortest_time])
            match.append(possibilities[shortest_time])
            if shortest_dist==None or shortest_dist==shortest_time:
                match_dist.append(None)
            else:
                match_dist.append(possibilities[shortest_dist])            
    
#            dist_time.append(xray_flares['init_date'][x])
#          print(dim_ew, dim_ns, flare_loc, flare_ew, flare_ns)
    print("  ")
    print("  ")
    
#    print("matches", hand_matches["dim_name"][0:30])
    print("target", target_name)    
    print("summary of all events:")
    
    ind2=0
    diff=0
    hand_noauto=0
    auto_nohand=0
    same=0
    null=0
#    init=pd.to_datetime(xray_flares["init_date"])
#    print("what??", type(init))
    for index in range(len(target_time)): 
        print("  ")
        print("  ")
#        index+=1

#        ind2=index
#        if target_name[index][0:13]==hand_matches["dim_name"][ind2][0:13]:
#            print("matches!")
#        print("TARGET", target_name[index][0:13])
#        print("MATCH", matches["dim_name"][ind2][0:13])
#        print("testing...", index, ind2)
#        print(target_name[index][0:13])
#        print(hand_matches["dim_name"][ind2][0:13])
        while target_name[index][0:13]!=hand_matches["dim_name"][ind2][0:13]:
            ind2=ind2+1 
#            print("target", target_name[index][0:13])
#            print("match", hand_matches["dim_name"][ind2][0:13])

        print("Target dimming:", target_name[index], target_time[index], target_loc[index][0])

        
#        print("Hand match:               ", hand_matches["dim_name"][ind2], hand_matches["start"][index], hand_matches["loc"][index], hand_matches["flare_class"][index], hand_matches["flare_size"][index])
        
        
#        print("Time: ", target_time[index])
#        print("Location: ", target_loc[index])
#        print(" ")
        if match[index]!=None:
#            print("Best flare based on time")
            if len(xray_flares['location'][match[index]])==6:
                loc=xray_flares['location'][match[index]]
            else: loc="no location"
            xraysize=xray_flares['xray_class'][match[index]]+str(xray_flares['xray_size'][match[index]]/10.)
            print("Flare closest in time:       ", xray_flares['init_date'][match[index]], loc, xraysize)#, xray_flares['xray_class'][match[index]], xray_flares['xray_size'][match[index]])
        else:
            print("No flare match")
            if match_dist[index]!=None:
                print("What?? There's a problem here")
        if match_dist[index]!=None:
#            print(match_dist[index])
            print("Flare closest in distance:", xray_flares['init_date'][match_dist[index]], xray_flares['location'][match_dist[index]])
#            print(xray_flares['location'][match_dist[index]])
#            print(xray_flares['init_date'][match_dist[index]])
        else:
            print("No flare match based on distance")  
        mat=hand_matches["init_date"][ind2]

        
        if is_nat(mat)==False and match[index]!=None:
#            print("match index", match[index])
            init=xray_flares["init_date"][match[index]]
            hand_loc=hand_matches["loc"][index]
#            print("hand_loc", hand_loc)
            if pd.isnull(hand_loc):
                hand_loc="no location"

            hand_flare=hand_matches["flare_class"][index]+str(hand_matches["flare_size"][index]/10.)
            print("auto match flare:            ", init, loc, xraysize)#, type(init))
            print("hand match flare:            ", mat, hand_loc, hand_flare)#, type(mat))
#            init=init.values
            
            if init==mat:
                print("SAME")
                same+=1
            else:
                print("DIFFERENT!!")
                diff+=1
        elif is_nat(mat)==True and match[index]!=None:
            print("automated match but no hand match")
            auto_nohand+=1
        elif is_nat(mat)==False and match[index]==None:
            print("hand match but no automated match")
            hand_noauto+=1
        elif is_nat(mat)==True and match[index]==None:
            print("no hand or auto match")
            null+=1
            
    print(" ")
    print(" ")
    print("Overall statistics")
    print("same flare: ", same)
    print("same null: ", null)
    print("hand match but no automated match", hand_noauto)
    print("automated match but no hand match", auto_nohand)
    print("diff: ", diff)
    
def coord2pa(ew_coord, ns_coord):
    x=ew_coord*1.0
    y=ns_coord*1.0

    pa=np.arctan(-x/y)

    pa=pa*180.0/3.1415926

    if y<0:
        pa=pa+180    
    if pa<0:
        pa=pa+360
        
    if x==0 and y==0:
        pa=-1

    return pa
        
    
    
def match_dimmings_CME():
    dimmings=read_Lars_alldim()
    hand_matches=read_hand_cmes()
    
#    print(type(dimmings))
    cmes=get_yashiro_catalog()
#    print("!!!!", xray_flares['peak_time'])
    #first check to make sure there is some overlap in dates
    print("dimming time", dimmings['time'])
    min_dimtime=min(dimmings['time'])
    max_dimtime=max(dimmings['time'])

    
    min_cme=min(cmes['date'])
#    min_xray=min(x for x in xray_flares['peak_date'] if x is not None)
    max_cme=max(x for x in cmes['date'] if x is not None)
    
    print("cme times", min_cme, max_cme)
    print("dimming times", min_dimtime, max_dimtime)
    
    if ((min_cme<min_dimtime and max_cme>min_dimtime) or (min_cme<max_dimtime and max_cme>max_dimtime)):
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
    target_name=[]
#    print(xray_flares["init_date"])
    
    for ind1 in range(len(dimmings['time'])):
        print("   ")
        print("   ")
        dim_ew=dimmings['mean_EW'][ind1]
        dim_ns=dimmings['mean_NS'][ind1]
        dim_pa=int(round(coord2pa(dim_ew, dim_ns)))
        print("target dimming", dimmings['dim_name'][ind1], dimmings['time'][ind1], "NS: ", dim_ns, "EW: ", dim_ew, "PA: ", dim_pa)

        
        target_time.append(dimmings['time'][ind1])
#        print("is this the target", dimmings['dim_name'][ind1])
        target_name.append(dimmings['dim_name'][ind1])
#        if dim_ns<0:
#            NS="S"
#        else:
#            NS="N"
#        if dim_ew<0:
#            EW="E"
#        else:
#            EW="W"
        target_loc.append(dim_pa)#    for dim in dimmings:
        #this is going to be totally inefficient
        possibilities=[]
        for ind2 in range(len(cmes['date'])):
            timediff=timedelta(hours=4)
            dimtime=dimmings['time'][ind1]
            cmetime=cmes['date'][ind2]

#            print("ind2", ind1, ind2, len(xray_flares['peak_time']))
#            print("flare", ind1, ind2, flaretime)

            if cmetime !=None and cmetime<(dimtime+timediff) and cmetime>(dimtime-timediff):
                #now check location
                cme_pa=int(cmes['mpa'][ind2])
#                print("cme_pa", cme_pa)
#                print("dim_pa", dim_pa)
                pa_diff=abs(cme_pa-dim_pa)#[x-y for x,y in zip(cme_pa,dim_pa)]
#                print("!!!!DIST", dist)
                if pa_diff == None or pa_diff<30:
                    possibilities.append(ind2)
#        print("possibilities", possibilities)
#        print("dimming location EW, NS", dimmings['mean_EW'][ind1], dimmings['mean_NS'][ind1])
#        print("flare location", [xray_flares['location'][x] for x in possibilities])
        if len(possibilities)==0:
            print("no matching cmes")
            match.append(None)
            match_dist.append(None)
        elif len(possibilities)==1:
            print("one matching cme")
            
            x=possibilities[0]
            cme_pa=int(cmes['mpa'][x])
            print("cme PA", cme_pa)

            print("cme time", cmes['date'][x])#, xray_flares['peak_date'][x], xray_flares['final_date'][x])
            print("cme_width", cmes['width'][x])
            pa_diff=abs(cme_pa-dim_pa)
            print("time diff", dimtime - cmes['date'][x])

            match.append(possibilities[0])
            match_dist.append(possibilities[0])
        elif len(possibilities)>1:
            print("possible flare summary:")
            pa_diff=[]
            time_diff=[]

            for x in possibilities:
                CME_pa=int(cmes['mpa'][x])

                print("cme PA", CME_pa)
                print("cme time", cmes['date'][x])#, xray_flares['peak_date'][x], xray_flares['final_date'][x])
                print("cme_width", cmes['width'][x])
                pa_diff_val=abs(CME_pa-dim_pa)
                t_diff=(dimtime - cmes['date'][x])
                time_diff.append(round((t_diff.days*86400+t_diff.seconds)/60./60., 2))
                pa_diff.append(pa_diff_val)

                print("time diff", dimtime - cmes['date'][x])
        
                print("  ")
          
            print("event summary")
            print("pa diffs: ", pa_diff)

            print("time differences (in hours): ", time_diff)#, timediff.index(min([abs(x) for x in time_diff])))
#            print("time differences (in hours/float): ", [float(x) for x in time_diff])

            tdiff_absfloat=[abs(float(x)) for x in time_diff]
            shortest_time=tdiff_absfloat.index(min(tdiff_absfloat))
            #the following is not exactly right -- it's an approximation
            #need to put in equations for great circle angle
            #set distance to 9999 when there is no location information

            if len(pa_diff)>0: 
                shortest_pa=pa_diff.index(min(pa_diff))
                #require within 30 degrees
                if shortest_pa>30:
                    shortest_pa=None
            else:
                shortest_dist=None
            if min(pa_diff)==9999: shortest_dist=None
            print("shortest_time", shortest_time)
            print("shortest_pa", shortest_pa)
#            print(possibilities[shortest_time])
            match.append(possibilities[shortest_time])
            if shortest_pa==None or shortest_pa==shortest_time:
                match_dist.append(None)
            else:
                match_dist.append(possibilities[shortest_pa])            
    
#            dist_time.append(xray_flares['init_date'][x])
#          print(dim_ew, dim_ns, flare_loc, flare_ew, flare_ns)
    print("  ")
    print("  ")
    
#    print("matches", hand_matches["dim_name"][0:30])
    print("target", target_name)    
    print("summary of all events:")
    
    ind2=0
    diff=0
    hand_noauto=0
    auto_nohand=0
    same=0
    null=0
#    init=pd.to_datetime(xray_flares["init_date"])
#    print("what??", type(init))
    for index in range(len(target_time)): 
        print("  ")
        print("  ")
#        index+=1

#        ind2=index
#        if target_name[index][0:13]==hand_matches["dim_name"][ind2][0:13]:
#            print("matches!")
        print("TARGET", target_name[index][0:13])
        print("MATCH", hand_matches["dim_name"][ind2][0:13])
#        print("testing...", index, ind2)
#        print(target_name[index][0:13])
#        print(hand_matches["dim_name"][ind2][0:13])
        while target_name[index][0:13]!=hand_matches["dim_name"][ind2][0:13]:
            ind2=ind2+1 
#            print("target", target_name[index][0:13])
#            print("match", hand_matches["dim_name"][ind2][0:13])

        print("Target dimming:", target_name[index], target_time[index], target_loc[index])

        
#        print("Hand match:               ", hand_matches["dim_name"][ind2], hand_matches["date"][index], hand_matches["PA"][index], hand_matches["width"][index])
        
        
#        print("Time: ", target_time[index])
#        print("Location: ", target_loc[index])
#        print(" ")
        if match[index]!=None:
#            print("Best flare based on time")

#            pa=cmes['pa'][match[index]]

            print("CME closest in time:       ", cmes['date'][match[index]], cmes['PA'][match[index]], cmes['width'][match[index]])#, xraysize)#, xray_flares['xray_class'][match[index]], xray_flares['xray_size'][match[index]])
        else:
            print("No cme match")
            if match_dist[index]!=None:
                print("What?? There's a problem here")
        if match_dist[index]!=None:
#            print(match_dist[index])
            print("CME closest in distance:   ", cmes['date'][match_dist[index]], cmes['PA'][match_dist[index]], cmes['width'][match[index]])
#            print(xray_flares['location'][match_dist[index]])
#            print(xray_flares['init_date'][match_dist[index]])
        else:
            print("No flare match based on distance")  
        mat=hand_matches["date"][ind2]

#        print("mat", mat)
#        print("match[index]", match[index])
        if is_nat(mat)==False and match[index]!=None:
#            print("match index", match[index])
            init=cmes["date"][match[index]]
            cme_PA=cmes["PA"][match[index]]
            hand_PA=hand_matches["PA"][index]
#            print("hand_loc", hand_loc)
            if pd.isnull(hand_PA):
                hand_PA="no location"

            hand_cme=hand_matches["width"][index]
            print("auto match CME:            ", init, cme_PA)#, type(init))
            print("hand match CME:            ", mat, hand_PA, hand_cme)#, type(mat))
#            init=init.values
            
            if init==mat:
                print("SAME")
                same+=1
            else:
                print("DIFFERENT!!")
                diff+=1
        elif is_nat(mat)==True and match[index]!=None:
            print("automated match but no hand match")
            auto_nohand+=1
        elif is_nat(mat)==False and match[index]==None:
            print("hand match but no automated match")
            hand_noauto+=1
        elif is_nat(mat)==True and match[index]==None:
            print("no hand or auto match")
            null+=1
            
    print(" ")
    print(" ")
    print("Overall statistics")
    print("same CME: ", same)
    print("same null: ", null)
    print("hand match but no automated match", hand_noauto)
    print("automated match but no hand match", auto_nohand)
    print("diff: ", diff)
          
match_dimmings_CME()
#match_dimmings_flares()
    
    