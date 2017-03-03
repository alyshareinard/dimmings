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

def determine_best_flare(time_match, big_match, verbose=False):
    """This is where the logic is for choosing the best flare when the flare 
    closest in time is not the biggest. The inputs are the time difference 
    between the biggest flare and the dimming (big_diff), the time difference 
    between the closest flare in time and the dimming (time_diff), the size of 
    the biggest flare (big_size) and the size of the flare closest in 
    time (time_size) and the indices for each (big_ind and time_ind)"""
    
    if verbose==True:
        print("Time difference from biggest flare to dimming: ", big_match["time_diff"])
        print("Time difference from closest flare in time to dimming: ", time_match["time_diff"])
    if big_match["time_diff"]<timedelta(hours=0): #if the biggest is less than 0 hour from dimming start time, it's the best one
        best_match=big_match["index"]

    else:
        best_match=time_match["index"]
        
    conf=0.8 #any penalty for having no location will be removed in the parent routine
    return (best_match, conf)        
            
def calc_overall_stats(best, conf, mat, xray_flares, hand_matches, target):
    """calculates the number of auto matches that are the same as the hand-
    selected matches"""
    
    same=0
    diff=0
    auto_nohand=0
    hand_noauto=0
    null=0

    for ind in range(len(best)):  #step through the matches
        print("  ")
        print("Target dimming ", target[ind])
        auto=best[ind]   #this is to simplify the indices of indices problem 
        manual=mat[ind]

        hand_init=hand_matches['init_date'][manual]

        #if both the auto and by hand methods find a match
        if is_nat(hand_init)==False and auto!=None:

            best_init=xray_flares['init_date'][auto]
            best_loc=xray_flares['location'][auto]
            best_xraysize=xray_flares['xray_class'][auto]+str(xray_flares['xray_size'][auto]/10.)


            hand_loc=hand_matches["loc"][manual]
            hand_flare=hand_matches["flare_class"][manual]+str(hand_matches["flare_size"][manual]/10.)

            print("auto match flare:            ", best_init, best_loc, best_xraysize)
            print("hand match flare:            ", hand_init, hand_loc, hand_flare)

            if best_init==hand_init:
                same+=1
                print("SAME")
            else:
                diff+=1
                print("DIFFERENT!")
        
        #automated match found, no hand match
        elif is_nat(hand_init)==True and auto!=None:
            print("automated match but no hand match")
            auto_nohand+=1
            
        #hand match found, no automated match
        elif is_nat(hand_init)==False and auto==None:
            print("hand match but no automated match")
            hand_noauto+=1
            
        #no automated or hand match
        elif is_nat(hand_init)==True and auto==None:
            print("no hand or automated match")
            null+=1
            
    return ([same, diff, auto_nohand, hand_noauto, null])

def determine_conf(time_ind, big_ind, dist_ind, target_time, xray_flares, verbose=False):
    #determine confidence level

    if time_ind==None:
#        print("No matching flare")
        return (None, -1)
    
    if verbose==True:
        print("Flare closest in time:       ", xray_flares['init_date'][time_ind], xray_flares['location'][time_ind], xray_flares['xray_class'][time_ind], xray_flares['xray_size'][time_ind]/10.)
        if big_ind==None:
            print("no largest flare")
        else:
            print("Flare largest in size:       ", xray_flares['init_date'][big_ind], xray_flares['location'][big_ind], xray_flares['xray_class'][big_ind], xray_flares['xray_size'][big_ind]/10.)
        if dist_ind==None:
            print("No closest flare")
        else:
            print("Flare closest in distance:   ", xray_flares['init_date'][dist_ind], xray_flares['location'][dist_ind], xray_flares['xray_class'][dist_ind], xray_flares['xray_size'][dist_ind]/10.)

    penalty=0.0
    if time_ind!=None and xray_flares['location'][time_ind]!=None:
        penalty=0.5  #large drop in confidence if there is no flare location

    if time_ind==None: #no match found
        best_match=-1
        conf=-1  #no match/fill val of -1 for confidence level
    elif time_ind==big_ind and time_ind==dist_ind: #all match -- very confident
        best_match=time_ind
        conf=1.0
    elif time_ind==big_ind: #if biggest and closest in time are same -- pretty confident
        best_match=time_ind
        conf=0.9-penalty
    
    #the logic for picking biggest flare or closest in time is in the routine determine_best_flare
    else: 
        big_diff=abs(target_time-xray_flares['init_date'][big_ind])
        time_diff=abs(target_time-xray_flares['init_date'][time_ind])
        big_size=xray_flares['xray_class'][big_ind]+str(xray_flares['xray_size'][big_ind]/10.)
        time_size=xray_flares['xray_class'][time_ind]+str(xray_flares['xray_size'][time_ind]/10.)
        time_match={"time_diff":time_diff, "size":time_size, "index":time_ind}
        big_match={"time_diff":big_diff, "size":big_size, "index":big_ind}

        (best_match, conf)=determine_best_flare(time_match, big_match, verbose=False)
        conf=conf-penalty
        
        
    conf=math.floor(conf*10)/10.
    if verbose==True:
        print("CONFIDENCE LEVEL", conf)
    return(best_match, conf)
        
def find_mag_bigger(mag1, mag2):
    """determines if mag1 is bigger than mag2 -- used for flare sizes B-X"""

    if mag1==mag2:
        return False
    if mag1=='B' or mag2=='X':
        return False
    if mag1=='X' or mag2=='B':
        return True
    #now we're left with Cs and Ms, so repeat
    if mag1=='C' or mag2=="M":
        return False
    else:
        return True


def find_largest_flare(fl_mag, fl_size):
    """from lists of flare magnitude and flare size the program returns the 
    index of the largest flare.  This works for lists of any size"""
    
    biggest_mag='B'
    biggest_size=1.0
    biggest_index=-1
    for index in range(len(fl_mag)):
        if find_mag_bigger(fl_mag[index], biggest_mag):
            biggest_index=index
            biggest_size=fl_size[index]
            biggest_mag=fl_mag[index]            
        if fl_mag[index]==biggest_mag:
            if fl_size[index]>biggest_size:
                biggest_index=index
                biggest_size=fl_size[index]
                biggest_mag=fl_mag[index]
    return biggest_index

def is_nat(npdatetime):
    """program to determine if a date is not a time -- 
    for picking out missing/fill values"""
    try:
        npdatetime.strftime('%x')
        return False
    except:
        return True
  
def create_datetime_cme(ymd, hm):
    date=[]
    #unpack ymd and fix year

    for item, ihm in zip(ymd, hm):

        if pd.isnull(item)==True:
            date.append(None)
            continue
    
        datestr=str(item).split("/")
        year=int(datestr[0])
        month=int(datestr[1])
        day=int(datestr[2])
        print(ihm)
        hms=ihm.split(":")
        hour=int(hms[0])
        minute=int(hms[1])

        try:
            date.append(datetime(year, month, day, hour, minute))

        except:
            print(year, month, day, hour, minute, "is not a valid date, skipping")
            date.append(None)
    return date
      
def create_datetime2(ymd, hm):
    """create datetime for CME data"""
    
    date=[]
    #unpack ymd and fix year

    for item, ihm in zip(ymd, hm):

        if item=="  " or np.isnan(item)==True:
            date.append(None)
            continue
        
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

            try:
                date.append(datetime(year, month, day, hour, minute))
            except:
                print(year, month, day, hour, minute, "is not a valid date, skipping")
                date.append(None)
        else:
            date.append(None)
    return date
    
def read_hand_flares():
    """reads in file containing the flares matches chosen by hand"""
    
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
    return data
    
def read_hand_cmes():
    """reads in file containing the CMEs chosen by hand"""
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

def calc_loc_diff(flare_loc, dim_ns, dim_ew):

    if flare_loc !=None:   
        ns=int(flare_loc[1:3])
        if flare_loc[0]=="S": ns=-ns
        ew=int(flare_loc[4:6])
        if flare_loc[3]=="E": ew=-ew
      
        ns_diff=ns-dim_ns
        ew_diff=ew-dim_ew

        ##this is kind of a cludge -- assumes 2D not 3D -- not sure a more robust method is necessary
        dist=math.sqrt(ns_diff*ns_diff+ew_diff*ew_diff)
        return dist
    else:
        return 9999

def match_dimmings_flares():
    dimmings=read_Lars_alldim()
    hand_matches=read_hand_flares()
    

    (xray_flares, ha_flares)=get_flare_catalog(2013, 2014)

    #first check to make sure there is some overlap in dates

    min_dimtime=min(dimmings['time'])
    max_dimtime=max(dimmings['time'])

    
    min_xray=min(xray_flares['peak_date'])
    max_xray=max(x for x in xray_flares['peak_date'] if x is not None)
    
    print("xray times", min_xray, max_xray)
    print("dimming times", min_dimtime, max_dimtime)
    
    if ((min_xray<min_dimtime and max_xray>min_dimtime) or (min_xray<max_dimtime and max_xray>max_dimtime)):
        print("we have overlap!")

    #let's start with stepping through the dimmings
    match_time=[]
    match_dist=[]
    match_big=[]
    target_time=[]
    target_loc=[]
    target_name=[]

    
    for ind1 in range(len(dimmings['time'])):
#        print("   ")
        dim_ew=dimmings['mean_EW'][ind1]
        dim_ns=dimmings['mean_NS'][ind1]
#        print("target dimming", dimmings['dim_name'][ind1], dimmings['time'][ind1], "NS: ", dim_ns, "EW: ", dim_ew)
        
        target_time.append(dimmings['time'][ind1])
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

        
        possibilities=[]
        for ind2 in range(len(xray_flares['peak_date'])):
            timediff=timedelta(hours=4)
            dimtime=dimmings['time'][ind1]
            flaretime=xray_flares['peak_date'][ind2]

            if flaretime !=None and flaretime<(dimtime+timediff) and flaretime>(dimtime-timediff):
                #now check location
                flare_loc=xray_flares['location'][ind2]
                dist=calc_loc_diff(flare_loc, dim_ns, dim_ew)

                if dist == 9999 or dist<30:
                    possibilities.append(ind2)

        if len(possibilities)==0:

            match_time.append(None)
            match_dist.append(None)
            match_big.append(None)
        elif len(possibilities)==1:
            
            x=possibilities[0]
            flare_loc=xray_flares['location'][x]

            dist=calc_loc_diff(flare_loc, dim_ns, dim_ew)

            match_time.append(possibilities[0])
            match_dist.append(possibilities[0])
            match_big.append(possibilities[0])
        elif len(possibilities)>1:

            dist=[]
            time_diff=[]
            fl_mag=[]
            fl_size=[]

            for x in possibilities:
                flare_loc=xray_flares['location'][x]

                distance=calc_loc_diff(flare_loc, dim_ns, dim_ew)

                t_diff=(dimtime - xray_flares['init_date'][x])
                time_diff.append(round((t_diff.days*86400+t_diff.seconds)/60./60., 2))
                dist.append(distance)

                fl_mag.append(xray_flares['xray_class'][x])
                fl_size.append(xray_flares['xray_size'][x])
                
            biggest=find_largest_flare(fl_mag, fl_size)
            match_big.append(possibilities[biggest])


            tdiff_absfloat=[abs(float(x)) for x in time_diff]
            shortest_time=tdiff_absfloat.index(min(tdiff_absfloat))


            dist_exists=False
            for val in dist:
                if val!=9999:
                    dist_exists=True
                    
            if len(dist)>0 and dist_exists: 
                shortest_dist=dist.index(min(dist))
                #require within 30 degrees
                if shortest_dist>30:
                    shortest_dist=None
            else:
                shortest_dist=None

            match_time.append(possibilities[shortest_time])
            if shortest_dist==None:
                match_dist.append(None)
            elif shortest_dist==shortest_time:
                match_dist.append(None)
            else:
                match_dist.append(possibilities[shortest_dist])            


    ind2=0
    diff=0
    hand_noauto=0
    auto_nohand=0
    same=0
    null=0
    conf=[]
    auto=[]
    mat=[]


    for index in range(len(target_time)): 

        while target_name[index][0:13]!=hand_matches["dim_name"][ind2][0:13]:
            ind2=ind2+1 

        mat.append(ind2)

        (best, confidence)=determine_conf(match_time[index], match_big[index], match_dist[index], target_time[index], xray_flares)

        conf.append(confidence)
        auto.append(best)
        
            
        
    [same, diff, auto_nohand, hand_noauto, null] = calc_overall_stats(auto, conf, mat, xray_flares, hand_matches, target_name)       
    
    print(" ")
    print(" ")
    print("Overall statistics")
    print("same flare: ", same)
    print("same null: ", null)
    print("hand match but no automated match", hand_noauto)
    print("automated match but no hand match", auto_nohand)
    print("diff: ", diff)
    print("accuracy: ", 100*round((same+null)/(same+null+diff+hand_noauto+auto_nohand), 3), "%")
 
    #make a location mask
    is_location=[]
    for ind in auto:
        if ind==None: #if there is no match
            is_location.append(False)  ###determines whether nulls go into no location or location piles
        elif xray_flares['location'][ind]==None:
            is_location.append(False)
        else:
            is_location.append(True)
            
#    is_location=[False if x==None  else True for x in xray_flares['location'][auto]]
    print(is_location)
    auto_loc=[]
    conf_loc=[]
    mat_loc=[]
    target_name_loc=[]
    auto_noloc=[]
    conf_noloc=[]
    mat_noloc=[]
    target_name_noloc=[]

#    print(xray_flares['location'][auto])

    #take only events with location
    for ind in range(len(is_location)):
        if is_location[ind]:
            auto_loc.append(auto[ind])
            conf_loc.append(conf[ind])
            mat_loc.append(mat[ind])
            target_name_loc.append(target_name[ind])
        else:
            auto_noloc.append(auto[ind])
            conf_noloc.append(conf[ind])
            mat_noloc.append(mat[ind])
            target_name_noloc.append(target_name[ind])
            
#    print(auto_loc)
#    print(auto_noloc)
    
    [same, diff, auto_nohand, hand_noauto, null] = calc_overall_stats(auto_loc, conf_loc, mat_loc, xray_flares, hand_matches, target_name_loc)
           
    print(" ")
    print(" ")
    print("When we know the location")    
    print("Overall statistics")
    print("same flare: ", same)
    print("same null: ", null)
    print("hand match but no automated match", hand_noauto)
    print("automated match but no hand match", auto_nohand)
    print("diff: ", diff)
    print("accuracy: ", 100*round((same+null)/(same+null+diff+hand_noauto+auto_nohand), 3), "%")
            
#    [same, diff, auto_nohand, hand_noauto, null] = calc_overall_stats(auto_noloc, conf_noloc, mat_noloc, xray_flares, hand_matches, target_name_noloc)
#       
#    print(" ")
#    print(" ")
#    print("When we don't know the location")    
#    print("Overall statistics")
#    print("same flare: ", same)
#    print("same null: ", null)
#    print("hand match but no automated match", hand_noauto)
#    print("automated match but no hand match", auto_nohand)
#    print("diff: ", diff)
#    print("accuracy: ", 100*round((same+null)/(same+null+diff+hand_noauto+auto_nohand), 3), "%")   
    
    
    
        
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
#        print("target dimming", dimmings['dim_name'][ind1], dimmings['time'][ind1], "NS: ", dim_ns, "EW: ", dim_ew, "PA: ", dim_pa)

        
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

                if pa_diff == None or pa_diff<30:
                    possibilities.append(ind2)

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

#                print("time diff", dimtime - cmes['date'][x])
        
#                print("  ")
          
            print("event summary")
            print("pa diffs: ", pa_diff)

#            print("time differences (in hours): ", time_diff)#, timediff.index(min([abs(x) for x in time_diff])))
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
#    print("  ")
#    print("  ")
    
#    print("matches", hand_matches["dim_name"][0:30])
#    print("target", target_name)    
#    print("summary of all events:")
    
    ind2=0
    diff=0
    hand_noauto=0
    auto_nohand=0
    same=0
    null=0
#    init=pd.to_datetime(xray_flares["init_date"])
#    print("what??", type(init))
    for index in range(len(target_time)): 
#        print("  ")
#        print("  ")
#        index+=1

#        ind2=index
#        if target_name[index][0:13]==hand_matches["dim_name"][ind2][0:13]:
#            print("matches!")
#        print("TARGET", target_name[index][0:13])
#        print("MATCH", hand_matches["dim_name"][ind2][0:13])
#        print("testing...", index, ind2)
#        print(target_name[index][0:13])
#        print(hand_matches["dim_name"][ind2][0:13])
        while target_name[index][0:13]!=hand_matches["dim_name"][ind2][0:13]:
            ind2=ind2+1 


#        print("Target dimming:", target_name[index], target_time[index], target_loc[index])

        if match_time[index]!=None:
#            print("Best flare based on time")

#            pa=cmes['pa'][match_time[index]]

            print("CME closest in time:       ", cmes['date'][match_time[index]], cmes['PA'][match_time[index]], cmes['width'][match_time[index]])#, xraysize)#, xray_flares['xray_class'][match_time[index]], xray_flares['xray_size'][match_time[index]])
        else:
            print("No cme match")
            if match_dist[index]!=None:
                print("What?? There's a problem here")
        if match_dist[index]!=None:
#            print(match_dist[index])
            print("CME closest in distance:   ", cmes['date'][match_dist[index]], cmes['PA'][match_dist[index]], cmes['width'][match_time[index]])
#            print(xray_flares['location'][match_dist[index]])
#            print(xray_flares['init_date'][match_dist[index]])
        else:
            print("No flare match based on distance")  
        mat=hand_matches["date"][ind2]

#        print("mat", mat)
#        print("match_time[index]", match_time[index])
        if is_nat(mat)==False and match_time[index]!=None:
#            print("match index", match_time[index])
            init=cmes["date"][match_time[index]]
            cme_PA=cmes["PA"][match_time[index]]
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
        elif is_nat(mat)==True and match_time[index]!=None:
            print("automated match but no hand match")
            auto_nohand+=1
        elif is_nat(mat)==False and match_time[index]==None:
            print("hand match but no automated match")
            hand_noauto+=1
        elif is_nat(mat)==True and match_time[index]==None:
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
    print("accuracy: ", (same+null)/(same+null+diff+hand_noauto+auto_nohand))
    
          
#match_dimmings_CME()
match_dimmings_flares()
    
    