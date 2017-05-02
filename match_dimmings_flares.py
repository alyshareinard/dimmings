# -*- coding: utf-8 -*-
"""
Created on Tue May  3 16:02:21 2016

@author: alyshareinard
"""

from datetime import timedelta, datetime
import math
import os
import numpy as np
import pandas as pd
import get_yashiro_catalog as CMEs
from get_flare_catalog import get_flare_catalog
from read_Lars_peakdim import read_Lars_peakdim

global data_path
data_path=os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")

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
        print("Time difference from biggest cme to dimming: ", big_match["time_diff"])
        print("Time difference from closest cme in time to dimming: ", time_match["time_diff"])
    if big_match["time_diff"]<timedelta(hours=1): #if the biggest is less than 1 hour from dimming start time, it's the best one
        best_match=big_match["index"]

    else:
        best_match=time_match["index"]
        
    conf=0.8 #any penalty for having no location will be removed in the parent routine
    return (best_match, conf)  
    
    
def print_summary_flares(dimming_vals, flare_vals, matches, hand=False):
    """input is the dimming, flare and (optional) the hand matches
    routine prints the dimming and the matching flare values and the 
    hand match (if present)"""
    
    if hand==True:
        hand_matches=read_hand_flares()

    for ind in range(len(dimming_vals)):  #step through the dimmings
        dimming=dimming_vals.loc[ind]
        auto=matches.loc[ind]
        print("  ")
        print("Target dimming ", dimming["dim_name"], dimming["date"], dimming["mean_EW"], dimming["mean_NS"])   
        
        print("Auto match flare: ", auto["date"], auto["location"], auto["xray_class"], auto["xray_size"]/10., auto["NOAA_AR"])
        
        if hand==True:
            hand_mat=hand_matches.loc[ind]
            print("Hand match flare: ", hand_mat["date"], hand_mat["loc"], hand_mat["flare_class"], hand_mat["flare_size"]/10., hand_mat["LarAR"])
    
            if pd.isnull(hand_mat["date"]) and pd.isnull(auto["date"]):
                print("Same NULL")
            elif pd.isnull(hand_mat["date"])==False and pd.isnull(auto["date"]):
                print("Hand match, but no auto match")
            elif pd.isnull(hand_mat["date"]) and pd.isnull(auto["date"])==False:
                print("Auto match but no hand match")
            elif hand_mat["date"]==auto["date"]:
                print("Same Flare")
            else: 
                print("Different flare")
                
    
def output_summary_flares(dimming_vals, matches, filename="flare_output.txt"):
    """input is the dimming, flare and (optional) the hand matches
    routine prints the dimming and the matching flare values and the 
    hand match (if present)"""

    output=[]
    print("\nSaving output to ", filename)
    for ind in range(len(dimming_vals)):  #step through the dimmings
        dimming=dimming_vals.loc[ind]
        auto=matches.loc[ind]

        output.append((dimming.dim_name, auto.date, auto.location, auto.xray_class, auto.xray_size, auto.NOAA_AR))

    np.savetxt(filename, output, fmt="%s")

def output_summary_cmes(dimming_vals, matches, filename="cme_output.txt"):
    """input is the dimming, flare and (optional) the hand matches
    routine prints the dimming and the matching flare values and the 
    hand match (if present)"""

    
    output=[]
    print("\nSaving output to ", filename)
    for ind in range(len(dimming_vals)):  #step through the dimmings
        dimming=dimming_vals.loc[ind]
        auto=matches.loc[ind]

        output.append((dimming.dim_name, auto.date, auto.mass, auto.width, auto.PA))

    np.savetxt(filename, output, fmt="%s")
    
def print_summary_cmes(dimming_vals, cme_vals, matches, hand=False):
    """input is the dimming, flare and (optional) the hand matches
    routine prints the dimming and the matching flare values and the 
    hand match (if present)"""
    
    if hand==True:
        hand_matches=read_hand_cmes()

    for ind in range(len(dimming_vals)):  #step through the dimmings
        dimming=dimming_vals.loc[ind]
        auto=matches.loc[ind]
        print("  ")
        print("Target dimming ", dimming["dim_name"], dimming["date"], dimming["mean_EW"], dimming["mean_NS"])   
        
        print("Auto match CME: ", auto["date"], auto["PA"], auto["width"], auto["mass"])
        
        if hand==True:
            hand_mat=hand_matches.loc[ind]
            print("Hand match CME: ", hand_mat["date"], hand_mat["PA"], hand_mat["width"])
    
            if pd.isnull(hand_mat["date"]) and pd.isnull(auto["date"]):
                print("Same NULL")
            elif pd.isnull(hand_mat["date"])==False and pd.isnull(auto["date"]):
                print("Hand match, but no auto match")
            elif pd.isnull(hand_mat["date"]) and pd.isnull(auto["date"])==False:
                print("Auto match but no hand match")
            elif hand_mat["date"]==auto["date"]:
                print("Same CME")
            else: 
                print("Different CME")
       
def calc_overall_stats(best, conf, mat, hand_matches, target):
    """calculates stats for auto vs hand selected matches"""
    
    same=0
    diff=0
    auto_nohand=0
    hand_noauto=0
    null=0
            
    for ind in range(len(best)):  #step through the matches

        auto=best[ind]   #this is to simplify the indices of indices problem 
        manual=mat[ind]

        hand_init=hand_matches[manual]
        
        if is_nat(hand_init)==False and is_nat(auto)==False:

            if auto==hand_init:
                same+=1
#                print("SAME")
            else:
                diff+=1
#                print("DIFF")
        
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
    """takes a given dimming with possible flare matches, makes a rough calculation of the confidence 
    of the final match based on whether the largest/biggest/closest flares are the same or not
    and runs the routine that finds the best flare"""

    if time_ind==None:
        if verbose:
            print("No matching flare")
        return (None, -1)
    
    if verbose:
        print("Flare closest in time:       ", xray_flares['date'][time_ind], xray_flares['location'][time_ind], xray_flares['xray_class'][time_ind], xray_flares['xray_size'][time_ind]/10.)
        if big_ind==None:
            print("no largest flare")
        else:
            print("Flare largest in size:       ", xray_flares['date'][big_ind], xray_flares['location'][big_ind], xray_flares['xray_class'][big_ind], xray_flares['xray_size'][big_ind]/10.)
        if dist_ind==None:
            print("No closest flare")
        else:
            print("Flare closest in distance:   ", xray_flares['date'][dist_ind], xray_flares['location'][dist_ind], xray_flares['xray_class'][dist_ind], xray_flares['xray_size'][dist_ind]/10.)

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
        big_diff=abs(target_time-xray_flares['date'][big_ind])
        time_diff=abs(target_time-xray_flares['date'][time_ind])
        big_size=xray_flares['xray_class'][big_ind]+str(xray_flares['xray_size'][big_ind]/10.)
        time_size=xray_flares['xray_class'][time_ind]+str(xray_flares['xray_size'][time_ind]/10.)
        time_match={"time_diff":time_diff, "size":time_size, "index":time_ind}
        big_match={"time_diff":big_diff, "size":big_size, "index":big_ind}

        (best_match, conf)=determine_best_flare(time_match, big_match, verbose=False)
        conf=conf-penalty 
        
    conf=math.floor(conf*10)/10.
    if verbose:
        print("CONFIDENCE LEVEL", conf)
    return(best_match, conf)
    
def determine_conf_best_cme(time_ind, big_ind, dist_ind, target_time, cmes, verbose=False):
    """takes a given dimming with possible cme matches, makes a rough calculation of the confidence 
    of the final match based on whether the largest/biggest/closest flares are the same or not
    and runs the routine that finds the best cme"""

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
#        print(ihm)
        hms=ihm.split(":")
        hour=int(hms[0])
        minute=int(hms[1])

        try:
            date.append(datetime(year, month, day, hour, minute))

        except:
            print(year, month, day, hour, minute, "is not a valid date, skipping")
            date.append(None)
    return date
      
def create_datetime_flare(ymd, hm):
    """create datetime for hand selected flare data"""
    
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
    """reads in file containing the flares chosen by hand"""
    
    file=os.path.join(data_path, "dim_flare_hand.txt")
    
    names=["dim_name", "date", "start", "end", "peak", "loc", "flare_class", 
    "flare_size", "station", "something", "AR", "LarAR"]
    data=pd.read_csv(file, sep=" ", header=None, names=names)

    data["init_date"]=create_datetime_flare(data["date"], data["start"])
    data["peak_date"]=create_datetime_flare(data["date"], data["peak"])
    data["final_date"]=create_datetime_flare(data["date"], data["end"])    

    data["date"]=data["peak_date"]
    return data
    
def read_hand_cmes():
    """reads in file containing the CMEs chosen by hand"""

    file=os.path.join(data_path, "dim_cme_hand.txt")
    
    names=["dim_name", "date", "time", "PA", "width", "speed_lin", "speed_20init", 
    "speed_20final", "speed_2020", "accel", "mass", "ke", "mpa"]
    data=pd.read_csv(file, sep=" ", header=None, names=names)
#    print("all the times", data)
    data["date"]=create_datetime_cme(data["date"], data["time"])
#    print(data["date"])
    return data

def calc_loc_diff(flare_loc, dim_ns, dim_ew):
    """takes a flare coordinate location and a dimming NS and EW and determines
    the cartesian distance between the dimming and flare"""
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
    """steps through dimmings and compares the auto matches to the hand matches"""
    
    hand_matches=read_hand_flares()   

    ind2=0
    mat=[]
    
    for index in range(len(target["date"])):
        while target["dim_name"][index][0:13]!=hand_matches["dim_name"][ind2][0:13]:
            ind2=ind2+1 

            if ind2>len(hand_matches)-1:
                break

        mat.append(ind2)            
        
    [same, diff, auto_nohand, hand_noauto, null] = calc_overall_stats(auto['date'], conf, mat, hand_matches['date'], target["dim_name"])       
    
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
            
    auto_loc=[]
    conf_loc=[]
    mat_loc=[]
    target_name_loc=[]

    #take only events with location
    auto_date=auto['date']
    for ind in range(len(is_location)):
        if is_location[ind]:
            auto_loc.append(auto_date[ind])
            conf_loc.append(conf[ind])
            mat_loc.append(mat[ind])
            target_name_loc.append(target["dim_name"][ind])
                
    [same, diff, auto_nohand, hand_noauto, null] = calc_overall_stats(auto_loc, conf_loc, mat_loc, hand_matches["date"], target_name_loc)
           
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
            
    
def compare_cme_hand(target, auto, events, conf):
    """steps through dimmings and compares the auto matches to the hand matches"""
    
    hand_matches=read_hand_cmes()   
    ind2=0
    mat=[]
    
    for index in range(len(target["date"])):


        while target["dim_name"][index][0:13]!=hand_matches["dim_name"][ind2][0:13]:
            ind2=ind2+1 

            if ind2>len(hand_matches)-1:
                break

        mat.append(ind2)            
        
    [same, diff, auto_nohand, hand_noauto, null] = calc_overall_stats(auto['date'], conf, mat, hand_matches['date'], target["dim_name"])       
    
    print(" ")
    print(" ")
    print("Overall statistics")
    print("same CME: ", same)
    print("same null: ", null)
    print("hand match but no automated match", hand_noauto)
    print("automated match but no hand match", auto_nohand)
    print("different CME: ", diff)
    print("accuracy: ", 100*round((same+null)/(same+null+diff+hand_noauto+auto_nohand), 3), "%")
    
def flare_size(mag, size):
    """ takes a flare magnitude and returns a decimal value indicating size"""

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
            
def coord2pa(ew_coord, ns_coord):
    """routine to translate ew/ns coordinates into position angle"""
    
    x=ew_coord*1.0
    y=ns_coord*1.0
    if y!=0:
        pa=np.arctan(-x/y)
    else:
        pa=3.1415926/2.  #limit of arctan(infinity)

    pa=pa*180.0/3.1415926

    if y<0:
        pa=pa+180    
    if pa<0:
        pa=pa+360
        
    if x==0 and y==0:
        pa=-1

    return pa
           
def match_dimmings_flaresCMEs(event_type='flares', print_results=False, hand_compare=False, training=False):
    """This is the main program. The inputs are several keywords
    
    event_type: which can be 'cmes' or 'flares'
    print_results: whether you get a printout of all the target dimmings/auto matches/hand matches
    hand_compare: whether you want to compare with a hand drawn list
    training: whether you want to take a portion of the data for training purposes or all of it
    
    Given that the program reads in the dimming data and the CME or flare data and does the automatching
    
    at the top of the file are some configurable parameters.  
    FDmaxDist: maximum distance in degrees that the routine will look for an associated flare
    CDmaxAngle: maximum angle in degrees that the routine will look for an associated CME
    Fmaxhours: maximum number of hours positive/negative that the routine will look for an associated flare
    Cmaxhours_before: maximum number of hours positive/negative that the routine will look for an associated CME
    Cmaxhours_after: maximum number of hours after the dimming that the routine will look for an associated CME
    """
    
    FDmaxDist=20
    CDmaxAngle=45
    Cmaxhours_before=4
    Cmaxhours_after=2
    Fmaxhours_before=4
    Fmaxhours_after=2
    
    if event_type=="flares":
        timeafter=timedelta(hours=Fmaxhours_after)
        timebefore=timedelta(hours=Fmaxhours_before)
    elif event_type=="cmes": 
        timeafter=timedelta(hours=Cmaxhours_after)
        timebefore=timedelta(hours=Cmaxhours_before)
        
    dimmings=read_Lars_peakdim(data_path, training=training)
    if event_type=='flares':
        (events, ha_flares)=get_flare_catalog(data_path, 2013, 2014)
        events['date']=events['peak_date']  #this can be used to chose initial_date if needed -- need to also change in read_hand_flares
    elif event_type == 'cmes':
        events=CMEs.get_yashiro_catalog(data_path)
    else:
        print("not a valid event selection")
        
    #first check to make sure there is some overlap in dates
    min_dimtime=min(dimmings['date'])
    max_dimtime=max(dimmings['date'])
    
    min_event=min(events['date'])
    max_event=max(x for x in events['date'] if x is not None)
    
    print("\nEvent times:", min_event, max_event)
    print("Dimming times:", min_dimtime, max_dimtime)
    
    if ((min_event<min_dimtime and max_event>min_dimtime) or (min_event<max_dimtime and max_event>max_dimtime)):
        print("Event times overlap with dimming times, calculating matches")
    else:
        print("event_times do not overlap with dimming times, returning")
        return 0

    #let's start with stepping through the dimmings
    match_time=[]
    match_dist=[]
    match_big=[]
    target_time=[]
    target_name=[]

    for ind1 in range(len(dimmings['date'])):

        dim_ew=dimmings['mean_EW'][ind1]
        dim_ns=dimmings['mean_NS'][ind1]
        
        target_time.append(dimmings['date'][ind1])
        target_name.append(dimmings['dim_name'][ind1])

        possibilities=[]
        distance=[]
        
        #we loop over all the events and create arrays for match_time, match_big, match_dist -- these may not be the same
        for ind2 in range(len(events['date'])):
            
            dimtime=dimmings['date'][ind1]
            eventtime=events['date'][ind2]

            if eventtime !=None and eventtime<(dimtime+timeafter) and eventtime>(dimtime-timebefore):
                #now check location
                if event_type=='flares':
                    event_loc=events['location'][ind2]

                    dist=calc_loc_diff(event_loc, dim_ns, dim_ew)

                    if dist == None or dist<FDmaxDist:
                        possibilities.append(ind2)
                        distance.append(dist)
                if event_type=='cmes':
                    dim_pa=int(round(coord2pa(dim_ew, dim_ns)))
                    cme_pa=int(events['mpa'][ind2])

                    pa_diff=abs(cme_pa-dim_pa)

                    if pa_diff == None or pa_diff<CDmaxAngle:
                        possibilities.append(ind2)
                        distance.append(pa_diff)
                        
        if len(possibilities)==0: #if no flare/cme Fmaxhours before or after dimming
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
                    event_size.append(events["mass"][x])
                
            biggest=event_size.index(max(event_size))  #index of the largest event in the small 
#            print("these are the sizes", event_size)
#            print("this is the biggest", biggest)
            match_big.append(possibilities[biggest])


            tdiff_absfloat=[abs(float(x)) for x in time_diff]
            shortest_time=tdiff_absfloat.index(min(tdiff_absfloat))


            dist_exists=False
            for val in dist:
                if val!=None:
                    dist_exists=True
                    
            if len(dist)>0 and dist_exists: 
                shortest_dist=dist.index(min(dist))
            else:
                shortest_dist=None

            match_time.append(possibilities[shortest_time])
            if shortest_dist==None:
                match_dist.append(None)
            elif shortest_dist==shortest_time:
                match_dist.append(None)
            else:
                match_dist.append(possibilities[shortest_dist])            

    #now we've finished determining the match that's closest in time, distance, and the largest, 
    #so we use determine_conf_best_xxx to find the best match.  
    conf=[]
    auto=[]
    nulls=[None for x in events.keys()] #fill value for events with no matches

    
#    #initialize match dataframe -- we
#    if event_type=="flares":
#        (best, confidence)= determine_conf_best_flare(match_time[0], match_big[0], match_dist[0], target_time[0], events)
#    elif event_type=="cmes":
#        (best, confidence)= determine_conf_best_cme(match_time[0], match_big[0], match_dist[0], target_time[0], events)
#    conf=[confidence]
#    auto=[best]
    matches=[]


    for index in range(len(target_time)): 
        if event_type=="flares":
            (best, confidence)=determine_conf_best_flare(match_time[index], match_big[index], match_dist[index], target_time[index], events)
        elif event_type=="cmes":
            (best, confidence)= determine_conf_best_cme(match_time[index], match_big[index], match_dist[index], target_time[index], events)
        conf.append(confidence)
        auto.append(best)

        if best !=None:
            matches.append(events.ix[best].tolist())
        else:
            matches.append(nulls)

    matches=pd.DataFrame(matches, columns=events.keys())
    if event_type=="flares":
        output_summary_flares(dimmings, matches)
    elif event_type=="cmes":
        output_summary_cmes(dimmings, matches)

    if print_results==True and event_type=="flares":
        print_summary_flares(dimmings, events, matches, hand=hand_compare)#, event_type=event_type)
    elif print_results==True and event_type=="cmes":
        print_summary_cmes(dimmings, events, matches, hand=hand_compare)

    if hand_compare==True and event_type=="flares":
        compare_flare_hand(dimmings, matches, events, conf)
    elif hand_compare==True and event_type=="cmes":
        compare_cme_hand(dimmings, matches, events, conf)



    return matches
    

         
auto_matches=match_dimmings_flaresCMEs(event_type='cmes', print_results=False, hand_compare=False, training=False)
#print_events(auto_matches, dimmings)
    