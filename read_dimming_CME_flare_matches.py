# -*- coding: utf-8 -*-
"""
Created on Tue May 10 13:16:50 2016

@author: alyshareinard
"""
from datetime import datetime
import os
import random
import pickle
from scipy.io.idl import readsav

def strip_nan(data):
#    print(data)
#    print(type(data))
    if data==b'NaN' or str(data)=='nan':
#        print("data is nan")
        return None
    else:
        try:
            return int(data)
        except:
            return str(data)

            
def read_dimming_CME_flare_matches():
    if os.sep=="/":
        osdir=os.sep+os.path.join("Users", "alyshareinard")
    else:
        osdir=os.path.join("C:"+os.sep+"Users", "alysha.reinard.SWPC")

    rootdir=os.path.join(osdir, "Dropbox", "dimming_shared", "SAV_files")+os.sep
#    print("fulldir", rootdir)
    cme_data=readsav(rootdir+"0cdaw_cmeprops.sav")
#    print(cme_data['cme'].dim_name)
    flare_data=readsav(rootdir+"0goes15_flareprops.sav")
#    print(flare_data['flare'].dim_name)
    
    dim_name=[]
    cme_date=[]
    cme_pa=[]
    cme_width=[]
    cme_v_lin=[]
    cme_v_init=[]
    cme_v_fin=[]
    cme_v_20rs=[]
    cme_acc=[]
    cme_mass=[]
    cme_ke=[]
    cme_mpa=[]
    flare_start_date=[]
    flare_peak_date=[]
    flare_end_date=[]
    flare_loc=[]
    flare_class=[]
    flare_mag=[]
    flare_ar=[]
    
#    print(cme_data)
    for index in range(len(cme_data['cme'].dim_name[0])):
        if cme_data['cme'].dim_name[0][index]!=flare_data['flare'].dim_name[0][index]:
            print("dim_name", cme_data['cme'].dim_name[0][index], flare_data['flare'].dim_name[0][index])

            print("dim names don't match")
#            break
        dim_name.append(cme_data['cme'].dim_name[0][index])
        
        cme_pa.append(strip_nan(cme_data['cme'].cent_pa_deg[0][index]))
        cme_width.append(strip_nan(cme_data['cme'].ang_width_deg[0][index]))
        cme_v_lin.append(strip_nan(cme_data['cme'].v_lin_kms[0][index]))
        cme_v_init.append(strip_nan(cme_data['cme'].v_init_kms[0][index]))
        cme_v_fin.append(strip_nan(cme_data['cme'].v_fin_kms[0][index]))
        cme_v_20rs.append(strip_nan(cme_data['cme'].v_20rs_kms[0][index]))
        cme_acc.append(strip_nan(cme_data['cme'].acc_ms2[0][index]))
        cme_mass.append(strip_nan(cme_data['cme'].mass_g[0][index]))
        cme_ke.append(strip_nan(cme_data['cme'].e_kin_erg[0][index]))
        cme_mpa.append(strip_nan(cme_data['cme'].mpa_deg[0][index]))

        cdate=cme_data['cme'].cdaw_date[0][index]
        if cdate==b'NaN':
            cme_date.append(None)
        else:
            ctime=cme_data['cme'].cdaw_time[0][index]
            year=int(cdate[0:4])
            month=int(cdate[5:7])
            day=int(cdate[8:10])
            hour=int(ctime[0:2])
            minute=int(ctime[3:5])
#            print(cdate, ctime)
#            print(year, month, day, hour, minute)
            cme_date.append(datetime(year, month, day, hour, minute))
            
        
        
        flare_loc.append(strip_nan(flare_data['flare'].flare_loc_deg[0][index]))
        flare_class.append(strip_nan(flare_data['flare'].x_class[0][index]))
        flare_mag.append(strip_nan(flare_data['flare'].x_int[0][index]))
        flare_ar.append(strip_nan(flare_data['flare'].noaa_ar_num[0][index]))

        fdate=flare_data['flare'].date[0][index]
        if fdate!=b'NaN':
            year=int(fdate[0:2])+2000
            month=int(fdate[3:5])
            day=int(fdate[6:8])
            ftime=flare_data['flare'].start_time[0][index]
#            print("start time", ftime)
            hour=int(ftime[10:12])
            minute=int(ftime[13:15])
            
#            print(year,  month, day, hour, minute)
            
            flare_start_date.append(datetime(year, month, day, hour, minute))
            
            #peak time
            ftime=flare_data['flare'].max_time[0][index]
            hour=int(ftime[10:12])
            minute=int(ftime[13:15])
            flare_peak_date.append(datetime(year, month, day, hour, minute))

            #end time
            ftime=flare_data['flare'].end_time[0][index]
            hour=int(ftime[10:12])
            minute=int(ftime[13:15])
            flare_end_date.append(datetime(year, month, day, hour, minute))
        else:
            flare_start_date.append(None)
            flare_peak_date.append(None)
            flare_end_date.append(None)
            
    num_events=len(dim_name)
    indexes=[x for x in range(num_events)]
#    rand_indexes=random.sample(indexes, round(num_events/4))
#    print(rand_indexes)
#    print(indexes)
    random.shuffle(indexes)
    print(indexes)
    training_set=indexes[0:round(0.6*num_events)]
    crossval_set=indexes[round(0.6*num_events):round(0.8*num_events)]
    testing_set=indexes[round(0.8*num_events):]
    
#    print("training", training_set)
#    print("crossval", crossval_set)
#    print("testing", testing_set)
#    print(len(training_set), len(crossval_set), len(testing_set), num_events)
    
    cme_training={'dim_name':[dim_name[x] for x in training_set], 
    'date':[cme_date[x] for x in training_set], 
    'PA':[cme_pa[x] for x in training_set], 
    'width':[cme_width[x] for x in training_set], 
    'v_lin':[cme_v_lin[x] for x in training_set],
    'v_init':[cme_v_init[x] for x in training_set], 
    'v_fin':[cme_v_fin[x] for x in training_set], 
    'v_20rs':[cme_v_20rs[x] for x in training_set], 
    'accel':[cme_acc[x] for x in training_set],
    'mass':[cme_mass[x] for x in training_set], 
    'ke':[cme_ke[x] for x in training_set], 
    'mpa':[cme_mpa[x] for x in training_set]} 
    
    cme_crossval={'dim_name':[dim_name[x] for x in crossval_set], 
    'date':[cme_date[x] for x in crossval_set], 
    'PA':[cme_pa[x] for x in crossval_set], 
    'width':[cme_width[x] for x in crossval_set], 
    'v_lin':[cme_v_lin[x] for x in crossval_set],
    'v_init':[cme_v_init[x] for x in crossval_set], 
    'v_fin':[cme_v_fin[x] for x in crossval_set], 
    'v_20rs':[cme_v_20rs[x] for x in crossval_set], 
    'accel':[cme_acc[x] for x in crossval_set],
    'mass':[cme_mass[x] for x in crossval_set], 
    'ke':[cme_ke[x] for x in crossval_set], 
    'mpa':[cme_mpa[x] for x in crossval_set]} 

    cme_testing={'dim_name':[dim_name[x] for x in testing_set], 
    'date':[cme_date[x] for x in testing_set], 
    'PA':[cme_pa[x] for x in testing_set], 
    'width':[cme_width[x] for x in testing_set], 
    'v_lin':[cme_v_lin[x] for x in testing_set],
    'v_init':[cme_v_init[x] for x in testing_set], 
    'v_fin':[cme_v_fin[x] for x in testing_set], 
    'v_20rs':[cme_v_20rs[x] for x in testing_set], 
    'accel':[cme_acc[x] for x in testing_set],
    'mass':[cme_mass[x] for x in testing_set], 
    'ke':[cme_ke[x] for x in testing_set], 
    'mpa':[cme_mpa[x] for x in testing_set]}     
    

    flare_training={'dim_name':[dim_name[x] for x in training_set], 
    'start_date':[flare_start_date[x] for x in training_set],
    'peak_date':[flare_peak_date[x] for x in training_set],
    'end_date':[flare_end_date[x] for x in training_set],
    'loc':[flare_loc[x] for x in training_set],
    'class':[flare_class[x] for x in training_set],
    'mag':[flare_mag[x] for x in training_set],
    'AR':[flare_ar[x] for x in training_set]}

    flare_crossval={'dim_name':[dim_name[x] for x in crossval_set], 
    'start_date':[flare_start_date[x] for x in crossval_set],
    'peak_date':[flare_peak_date[x] for x in crossval_set],
    'end_date':[flare_end_date[x] for x in crossval_set],
    'loc':[flare_loc[x] for x in crossval_set],
    'class':[flare_class[x] for x in crossval_set],
    'mag':[flare_mag[x] for x in crossval_set],
    'AR':[flare_ar[x] for x in crossval_set]}
    
    
    flare_testing={'dim_name':[dim_name[x] for x in testing_set], 
    'start_date':[flare_start_date[x] for x in testing_set],
    'peak_date':[flare_peak_date[x] for x in testing_set],
    'end_date':[flare_end_date[x] for x in testing_set],
    'loc':[flare_loc[x] for x in testing_set],
    'class':[flare_class[x] for x in testing_set],
    'mag':[flare_mag[x] for x in testing_set],
    'AR':[flare_ar[x] for x in testing_set]}
    
    fcd_matches={'cme_training':cme_training, 'cme_crossval':cme_crossval,
    'cme_testing':cme_testing, 'flare_training':flare_training, 
    'flare_crossval':flare_crossval, 'flare_testing':flare_testing}
      
    
    pickle.dump(fcd_matches, open("dimming_cme_flare_handmatches.p", 'wb'))
    
    
read_dimming_CME_flare_matches()
