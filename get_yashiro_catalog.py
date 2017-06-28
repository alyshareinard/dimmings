import os
import pandas as pd
from datetime import datetime

def parse_cme_data(file_name):
    print("\nReading CME data from: ", file_name)
    
    
    names=["ymd", "hour", "sep", "minute", "sep2", "sec", "PA", "width",
           "lin_speed", "20speed_init", "20speed_final", "20speed_20R", 
           "accel", "sep3", "mass", "sep4", "ke", "sep5", "mpa"]
    
    widths=[10, 4, 1, 2, 1, 2, 8, 8, 8, 8, 8, 6, 6, 1, 10, 1, 10, 1, 8]
    cmes=pd.read_fwf(file_name, widths=widths, header=3, names=names)#, parse_dates=[[1]])
    date=[]
    for i in range(len(cmes["ymd"])):
        ymd=cmes["ymd"][i].split("/")

        date.append(datetime(int(ymd[0]), int(ymd[1]), int(ymd[2]), cmes["hour"][i], cmes["minute"][i]))#, cmes["sec"][i]))
    
    cmes["date"]=date

    cmes["mass"]=cmes["mass"].replace("-------", "-1").replace("*******", "-1")
    cmes.mass=cmes.mass.astype(float)
    return cmes
 
    

def get_yashiro_catalog(data_path=os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")):
    """ program to read in yashiro CME catalog """

    #try to read from file this program creates -- delete if you want to redownload the data
    try:
        cmes=pd.read_csv("cmes.txt", sep=" ", index_col=0, parse_dates=["date"])

    except:
        #try downloading the data
        try:
            
            cme_file="https://cdaw.gsfc.nasa.gov/CME_list/UNIVERSAL/text_ver/univ_all.txt"
            cmes=parse_cme_data(cme_file)
            cmes.to_csv("cmes.txt", sep=" ")
        #if that doesn't work, use the local file
        except:
            cme_file=data_path+"/yashiro_all.txt"
            cmes=parse_cme_data(cme_file)
       
        

    return cmes