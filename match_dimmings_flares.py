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
    
def determine_best_cme(time_match, big_match, verbose=False):
    """This is where the logic is for choosing the best flare when the cme 
    closest in time is not the biggest. The inputs are the time difference 
    between the biggest cme and the dimming (big_diff), the time difference 
    between the closest cme in time and the dimming (time_diff), the size of 
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
    
    
def print_summary_flares(dimming_vals, flare_vals, hand_vals=None):
    """input is the dimming, flare and (optional) the hand matches
    routine prints the dimming and the matching flare values and the 
    hand match (if present)"""

    for ind in range(len(dimming_vals)):  #step through the matches
        print("  ")
        print("Target dimming ", dimming_vals[ind])     
        print("auto match flare:            ", best_init, best_loc, best_xraysize)
        print("hand match flare:            ", hand_init, hand_loc, hand_flare)
#TODO update this routine
        if is_nat(hand_init)==False and auto!=None:

            best_init=xray_flares['init_date'][auto]
            best_loc=xray_flares['location'][auto]
            best_xraysize=xray_flares['xray_class'][auto]+str(xray_flares['xray_size'][auto]/10.)


            hand_loc=hand_matches["loc"][manual]
            hand_flare=hand_matches["flare_class"][manual]+str(hand_matches["flare_size"][manual]/10.)


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
        
       
def calc_overall_stats(best, conf, mat, xray_flares, hand_matches, target):
    """calculates the number of auto matches that are the same as the hand-
    selected matches"""
    
    same=0
    diff=0
    auto_nohand=0
    hand_noauto=0
    null=0

    if isinstance(best, pd.DataFrame): #if it's a dataframe make it a list
        temp=[]
        for ind in range(len(best)):
            temp.append(best.loc[ind])
        best=temp
            
    for ind in range(len(best)):  #step through the matches

#        print("ind", ind)
#        print("Here's the zeroth!", best)
#        print(best.loc[ind])
#        print("!!!Type", type(best))
        auto=best[ind]   #this is to simplify the indices of indices problem 
        auto=auto["init_date"]
#        print("!!!auto", auto)
        manual=mat[ind]

        hand_init=hand_matches['init_date'][manual]

#        print("hand_init", hand_init)
#        print("auto", auto)
        #if both the auto and by hand methods find a match
        if is_nat(hand_init)==False and is_nat(auto)==False:

            if auto==hand_init:
                same+=1
            else:
                diff+=1
        
        #automated match found, no hand match
        elif is_nat(hand_init)==True and is_nat(auto)==False:
            auto_nohand+=1
            
        #hand match found, no automated match
        elif is_nat(hand_init)==False and is_nat(auto)==True:
            hand_noauto+=1
            
        #no automated or hand match
        elif is_nat(hand_init)==True and is_nat(auto)==True:
            null+=1
            
    return ([same, diff, auto_nohand, hand_noauto, null])

def determine_conf_best_flare(time_ind, big_ind, dist_ind, target_time, xray_flares, verbose=False):
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
    
def determine_conf_best_cme(time_ind, big_ind, dist_ind, target_time, cmes, verbose=False):
    #determine confidence level

    if time_ind==None:
#        print("No matching flare")
        return (None, -1)
    
    if verbose==True:
        print("CME closest in time:       ", cmes['date'][time_ind], cmes['pa'][time_ind], cmes['width'][time_ind])
        if big_ind==None:
            print("no largest CME")
        else:
            print("CME largest in size:       ", cmes['date'][big_ind], cmes['pa'][big_ind], cmes['width'][big_ind])
        if dist_ind==None:
            print("No closest cme")
        else:
            print("CME closest in distance:   ", cmes['date'][dist_ind], cmes['pa'][dist_ind], cmes['width'][dist_ind])

    penalty=0.0
    if time_ind!=None and cmes['PA'][time_ind]!=None:
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
        big_diff=abs(target_time-cmes['date'][big_ind])
        time_diff=abs(target_time-cmes['date'][time_ind])
        big_size=cmes['width'][big_ind]
        time_size=cmes['width'][time_ind]
        time_match={"time_diff":time_diff, "size":time_size, "index":time_ind}
        big_match={"time_diff":big_diff, "size":big_size, "index":big_ind}

        (best_match, conf)=determine_best_cme(time_match, big_match, verbose=False)
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
#                print("CHECKIT", date[-1])
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
    print("CHECK INIT", data["init_date"])
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
        return None

def compare_flare_hand(target, auto, events, conf):
    hand_matches=read_hand_flares()   
    print(target.keys())
    ind2=0
    mat=[]
    
    for index in range(len(target["time"])):


        while target["dim_name"][index][0:13]!=hand_matches["dim_name"][ind2][0:13]:
            ind2=ind2+1 

            if ind2>len(hand_matches)-1:
                break

        mat.append(ind2)            
        
    [same, diff, auto_nohand, hand_noauto, null] = calc_overall_stats(auto, conf, mat, events, hand_matches, target["dim_name"])       
    
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
    for ind in range(len(auto)):
        if ind==None: #if there is no match
            is_location.append(False)  ###determines whether nulls go into no location or location piles
        elif auto['location'][ind]==None:
            is_location.append(False)
        else:
            is_location.append(True)
            
#    is_location=[False if x==None  else True for x in xray_flares['location'][auto]]
#    print(is_location)
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
            auto_loc.append(auto.loc[ind])
            conf_loc.append(conf[ind])
            mat_loc.append(mat[ind])
            target_name_loc.append(target["dim_name"][ind])
#        else:
#            auto_noloc.append(auto[ind])
#            conf_noloc.append(conf[ind])
#            mat_noloc.append(mat[ind])
#            target_name_noloc.append(target_name[ind])
            
    
    [same, diff, auto_nohand, hand_noauto, null] = calc_overall_stats(auto_loc, conf_loc, mat_loc, events, hand_matches, target_name_loc)
           
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
    
def flare_size(mag, size):

    if mag=='B':
        return size
    elif mag=='C':
        return size*10.
    elif mag=='M':
        return size*100.
    elif mag=='X':
        return size*1000.
    else:
        print("flare size not valid")
        return None        
           
        
def match_dimmings_flaresCMEs(event_type='flares', max_hours=4, print_results=False, hand_compare=False):
    dimmings=read_Lars_alldim()
    if event_type=='flares':
        (events, ha_flares)=get_flare_catalog(2013, 2014)
        events['date']=events['peak_date']  #this can be used to chose initial_date if needed
    elif event_type == 'cmes':
        events=get_yashiro_catalog()
    else:
        print("not a valid event selection")
        
    #first check to make sure there is some overlap in dates
    min_dimtime=min(dimmings['time'])
    max_dimtime=max(dimmings['time'])
    
    min_event=min(events['date'])
    max_event=max(x for x in events['date'] if x is not None)
    
    print("event times", min_event, max_event)
    print("dimming times", min_dimtime, max_dimtime)
    
    if ((min_event<min_dimtime and max_event>min_dimtime) or (min_event<max_dimtime and max_event>max_dimtime)):
        print("we have overlap!!")

    #let's start with stepping through the dimmings
    match_time=[]
    match_dist=[]
    match_big=[]
    target_time=[]
    target_name=[]

    for ind1 in range(len(dimmings['time'])):

        dim_ew=dimmings['mean_EW'][ind1]
        dim_ns=dimmings['mean_NS'][ind1]
        
        target_time.append(dimmings['time'][ind1])
        target_name.append(dimmings['dim_name'][ind1])

        possibilities=[]
        distance=[]

        for ind2 in range(len(events['date'])):
            timediff=timedelta(hours=max_hours)
            dimtime=dimmings['time'][ind1]
            eventtime=events['date'][ind2]

            if eventtime !=None and eventtime<(dimtime+timediff) and eventtime>(dimtime-timediff):
                #now check location
                if event_type=='flares':
                    event_loc=events['location'][ind2]

                    dist=calc_loc_diff(event_loc, dim_ns, dim_ew)

                    if dist == None or dist<30:
                        possibilities.append(ind2)
                        distance.append(dist)
                if event_type=='cmes':
                    dim_pa=int(round(coord2pa(dim_ew, dim_ns)))
                    cme_pa=int(events['mpa'][ind2])

                    pa_diff=abs(cme_pa-dim_pa)

                    if pa_diff == None or pa_diff<30:
                        possibilities.append(ind2)
                        distance.append(pa_diff)
                        
        if len(possibilities)==0: #no flares in 4 hours before or after dimming
            match_time.append(None)
            match_dist.append(None)
            match_big.append(None)
            
        elif len(possibilities)==1: #only one possibility, if the distance is close enough, select it
            
            x=possibilities[0]

            match_time.append(possibilities[0])
            match_dist.append(possibilities[0])
            match_big.append(possibilities[0])

        elif len(possibilities)>1:

            dist=[]
            time_diff=[]
            event_size=[]

            for x in possibilities:

                t_diff=(dimtime - events['date'][x])
                time_diff.append(round((t_diff.days*86400+t_diff.seconds)/60./60., 2))

                if event_type=='flares':

                    event_size.append(flare_size(events['xray_class'][x], events['xray_size'][x]))
                if event_type=="cmes":
                    event_size.append(events["width"][x])
                
            biggest=event_size.index(max(event_size))

            match_big.append(possibilities[biggest])


            tdiff_absfloat=[abs(float(x)) for x in time_diff]
            shortest_time=tdiff_absfloat.index(min(tdiff_absfloat))


            dist_exists=False
            for val in dist:
                if val!=None:
                    dist_exists=True
                    
            if len(dist)>0 and dist_exists: 
                shortest_dist=dist.index(min(dist))
                #require within 30 degrees
                if shortest_dist>30:
                    print("does this ever happen?  It should get caught above")
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


    conf=[]
    auto=[]
#    print("events.keys", events.keys())
    nulls=[None for x in events.keys()] #fill value for events with no matches

    
#    print("len target time", len(target_time))
#    print("len dimmings", len(dimmings["time"]))
    #initialize match dataframe
    if event_type=="flares":
        (best, confidence)= determine_conf_best_flare(match_time[0], match_big[0], match_dist[0], target_time[0], events)
    elif event_type=="cmes":
        (best, confidence)= determine_conf_best_cme(match_time[0], match_big[0], match_dist[0], target_time[0], events)
    conf=[confidence]
    auto=[best]
    matches=[]


    for index in range(len(target_time)): 
        if event_type=="flares":
            (best, confidence)=determine_conf_best_flare(match_time[index], match_big[index], match_dist[index], target_time[index], events)
        elif event_type=="cmes":
            (best, confidence)= determine_conf_best_cme(match_time[index], match_big[index], match_dist[index], target_time[index], events)
        conf.append(confidence)
        auto.append(best)

        if best !=None:
            matches.append(events.ix[best].tolist())#, keys=events.keys())      
        else:
            matches.append(nulls)#, keys=events.keys())

    matches=pd.DataFrame(matches, columns=events.keys())

    if print_results==True:

        print_events(matches, dimmings)
    
    if hand_compare==True:
        compare_flare_hand(dimmings, matches, events, conf)
    return matches
    

    
def print_events(auto, dimmings, hand=True, event_type="flares"):
    if hand==True and event_type=="flares":
        hand_matches=read_hand_flares()
    if hand==True and event_type=="cmes":
        hand_matches=read_hand_cmes()
    print("auto vals", hand_matches.keys())
#    print(len(auto["date"]), len(dimmings["time"]))
    if len(auto["date"])!=len(dimmings["time"]):
        print("what!? Auto and dimmings are not the same length.  This sucks!!")
    for index in range(len(auto["date"])):
        print("  ")
        dim=dimmings.iloc[[index]]
        au=auto.iloc[[index]]
        print("Dimming", dim["dim_name"].values[0])#.tolist())
        if event_type=="flares":
#            print(au["peak_date"].values[0])
            if pd.isnull(au["peak_date"].values[0]):  #how to check for NaTs! evaluates to true if it is an NaT
                print("Auto match: None")
            else:
                print("Auto match", pd.to_datetime(au["peak_date"].values[0]).strftime("%Y-%m-%d %H:%M"), au["xray_class"].values[0], au["xray_size"].values[0]/10., au["location"].values[0])#.tolist())

        elif event_type=="cmes":
            print("Auto match", au["date"].values[0], au["PA"].values[0], au["width"].values[0])#.tolist()  
        if hand==True:
            hand_mat=hand_matches.iloc[[index]]
            print("hand_mat", hand_mat)
            try:
                print("hand match", pd.to_datetime(hand_mat["date"].values[0]).strftime("%Y-%m-%d %H:%M"), hand_mat["flare_class"].values[0], hand_mat["flare_size"].values[0])#.tolist())
#            if hand_mat["date"].values[0] == np.datetime64('NaT'):
            except:
                print("Hand match: None")
#            else:                
#                print("hand match", pd.to_datetime(hand_mat["date"].values[0]).strftime("%Y-%m-%d %H:%M"), hand_mat["flare_class"].values[0], hand_mat["flare_size"].values[0])#.tolist())

    
        
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
#    print("dimming time", dimmings['time'])
    min_dimtime=min(dimmings['time'])
    max_dimtime=max(dimmings['time'])

    
    min_cme=min(cmes['date'])
    max_cme=max(x for x in cmes['date'] if x is not None)
    
    print("cme times", min_cme, max_cme)
    print("dimming times", min_dimtime, max_dimtime)
    
    if ((min_cme<min_dimtime and max_cme>min_dimtime) or (min_cme<max_dimtime and max_cme>max_dimtime)):
        print("we have overlap!")

    #let's start with stepping through the dimmings
    match_time=[]
    match_dist=[]
    target_time=[]
    target_loc=[]
    dist_time=[]
    dist_loc=[]
    time_time=[]
    time_loc=[]
    target_name=[]

    
    for ind1 in range(len(dimmings['time'])):
        print("   ")
        print("   ")
        dim_ew=dimmings['mean_EW'][ind1]
        dim_ns=dimmings['mean_NS'][ind1]
        dim_pa=int(round(coord2pa(dim_ew, dim_ns)))

        
        target_time.append(dimmings['time'][ind1])
        target_name.append(dimmings['dim_name'][ind1])
        target_loc.append(dim_pa)

        possibilities=[]
        for ind2 in range(len(cmes['date'])):
            timediff=timedelta(hours=4)
            dimtime=dimmings['time'][ind1]
            cmetime=cmes['date'][ind2]

            if cmetime !=None and cmetime<(dimtime+timediff) and cmetime>(dimtime-timediff):
                #now check location
                cme_pa=int(cmes['mpa'][ind2])

                pa_diff=abs(cme_pa-dim_pa)

                if pa_diff == None or pa_diff<30:
                    possibilities.append(ind2)

        if len(possibilities)==0:
            print("no matching cmes")
            match_time.append(None)
            match_dist.append(None)
        elif len(possibilities)==1:
            print("one matching cme")
            
            x=possibilities[0]
            cme_pa=int(cmes['mpa'][x])
            print("cme PA", cme_pa)

            print("cme time", cmes['date'][x])
            print("cme_width", cmes['width'][x])
            pa_diff=abs(cme_pa-dim_pa)
            print("time diff", dimtime - cmes['date'][x])

            match_time.append(possibilities[0])
            match_dist.append(possibilities[0])
        elif len(possibilities)>1:
            print("possible flare summary:")
            pa_diff=[]
            time_diff=[]

            for x in possibilities:
                CME_pa=int(cmes['mpa'][x])

                print("cme PA", CME_pa)
                print("cme time", cmes['date'][x])
                print("cme_width", cmes['width'][x])
                pa_diff_val=abs(CME_pa-dim_pa)
                t_diff=(dimtime - cmes['date'][x])
                time_diff.append(round((t_diff.days*86400+t_diff.seconds)/60./60., 2))
                pa_diff.append(pa_diff_val)

          
            print("event summary")
            print("pa diffs: ", pa_diff)


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

            match_time.append(possibilities[shortest_time])
            if shortest_pa==None or shortest_pa==shortest_time:
                match_dist.append(None)
            else:
                match_dist.append(possibilities[shortest_pa])            
#    
#    
#    ind2=0
#    diff=0
#    hand_noauto=0
#    auto_nohand=0
#    same=0
#    null=0

#    for index in range(len(target_time)): 
#
#        while target_name[index][0:13]!=hand_matches["dim_name"][ind2][0:13]:
#            ind2=ind2+1 
#
#
##        print("Target dimming:", target_name[index], target_time[index], target_loc[index])
#
#        if match_time[index]!=None:
##            print("Best flare based on time")
#
##            pa=cmes['pa'][match_time[index]]
#
#            print("CME closest in time:       ", cmes['date'][match_time[index]], cmes['PA'][match_time[index]], cmes['width'][match_time[index]])#, xraysize)#, xray_flares['xray_class'][match_time[index]], xray_flares['xray_size'][match_time[index]])
#        else:
#            print("No cme match")
#            if match_dist[index]!=None:
#                print("What?? There's a problem here")
#        if match_dist[index]!=None:
##            print(match_dist[index])
#            print("CME closest in distance:   ", cmes['date'][match_dist[index]], cmes['PA'][match_dist[index]], cmes['width'][match_time[index]])
#
#        else:
#            print("No CME match based on distance")  
#        mat=hand_matches["date"][ind2]
#
#
#        if is_nat(mat)==False and match_time[index]!=None:
#
#            init=cmes["date"][match_time[index]]
#            cme_PA=cmes["PA"][match_time[index]]
#            hand_PA=hand_matches["PA"][index]
#
#            if pd.isnull(hand_PA):
#                hand_PA="no location"
#
#            hand_cme=hand_matches["width"][index]
#            print("auto match CME:            ", init, cme_PA)
#            print("hand match CME:            ", mat, hand_PA, hand_cme)
#
#            
#            if init==mat:
#                print("SAME")
#                same+=1
#            else:
#                print("DIFFERENT!!")
#                diff+=1
#        elif is_nat(mat)==True and match_time[index]!=None:
#            print("automated match but no hand match")
#            auto_nohand+=1
#        elif is_nat(mat)==False and match_time[index]==None:
#            print("hand match but no automated match")
#            hand_noauto+=1
#        elif is_nat(mat)==True and match_time[index]==None:
#            print("no hand or auto match")
#            null+=1
            

    for index in range(len(target_time)): 

        while target_name[index][0:13]!=hand_matches["dim_name"][ind2][0:13]:
            ind2=ind2+1 

        mat.append(ind2)

        (best, confidence)=determine_conf_best_CME(match_time[index], match_big[index], match_dist[index], target_time[index], cmes)

        conf.append(confidence)
        auto.append(best)
        
            
        
    [same, diff, auto_nohand, hand_noauto, null] = calc_overall_stats(auto, conf, mat, cmes, hand_matches, target_name)       
    
            
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
auto_matches=match_dimmings_flaresCMEs(event_type='flares', print_results=True, hand_compare=True)
#print_events(auto_matches, dimmings)
    