# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 14:59:25 2016

@author: alyshareinard
"""




from astropy.io import fits
from urllib.request import urlopen
from sunpy.net import vso
from sunpy.map import Map
import os
from sunpy.instr.aia import aiaprep
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def read_SDOfits():
    print("in SDOfits")
    data_dir='/Users/alyshareinard/Dropbox/work/data/SDO/'
    data_dir='C:\\Users\\alysha.reinard.SWPC\\Dropbox\\Work\\data\\'
#    client=vso.VSOClient()
#    print("defined client")
#    qr=client.query_legacy('2013/1/11 03:00:00', '2013/1/11 09:00:00', instrument='AIA', min_wave="193", max_wave="193", unit_wave="Angstrom")
#    print("after client")
#    count=0
#    qr_10=[]
#    for item in qr:
#        if count==0:
#           qr_10.append(item)
#        count+=1
#        if count==10:
#            count=0
#    print("qr", len(qr))
#    print("qr_10", len(qr_10))
#    res=client.get(qr_10, path=data_dir+'{instrument}/{file}.fits').wait()
#    print("after wait")
    aia_cube = Map(data_dir+'/AIA/*.fits', cube=True)   
    print("First, what do we have here??", [m.data for m in aia_cube])
    print("same shape? ", aia_cube.all_maps_same_shape())
    aia_cube.plot
#    print("size?", aia_cube.size)
    aia_cube_array=aia_cube.as_array()
#    print("size", aia_cube_array.size)
#    count=0
#    for file in os.listdir(data_dir+'/AIA/'):
#        if file !=".DS_Store":
#            print("file", file)
#            print("full path", data_dir+"/AIA"+file)
#            original=Map(data_dir+'/AIA/'+file)
#            prepped=aiaprep(original)
#    #        imgplot=plt.imshow(original)
#    #        plt.colorbar()
#            if count==0:
#                pre_image=prepped
#                count=1
#            else:
#                fig = plt.figure(figsize=(15, 8))
#                fig.add_subplot(1, 2, 1)
#                print("meta", prepped.meta)
#                print("data", prepped.data)
#                prepped=prepped-pre_image
#                #            original.plot()
#                prepped.plot() 
#                break
        
#foundfile=file_search(lala)

#aia_prep, foundfile, [0], head, data
#index2map, head, data, map	
#aia_lct, rr, gg, bb, wavelnth=wavelength, /load	;loading colortables
#plot_image, alog(map.data)
#    web_stem="ftp://gong2.nso.edu/HA/haf/"
#    webpage=web_stem+"201604/20160408/"+"20160211000014Mh.fits.fz"
#    print("webpage:", webpage)
##    hdulist=fits.open("data/mrrpm010722dh5f.fits.gz")
##    hdulist=fits.open("data/20160211000014Mh.fits.fz")
#    hdulist=fits.open(webpage)
#    hdulist.info()
#    print(hdulist[0].header)
#    scidata=hdulist[1].data
#    imgplot = plt.imshow(scidata, cmap="gray")#[0,:,:])
#    plt.colorbar()
#    hdulist.close()
    
read_SDOfits()