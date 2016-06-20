# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 14:59:25 2016

@author: alyshareinard
"""



import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from astropy.io import fits
from urllib.request import urlopen
from sunpy.net import vso
from sunpy.map import Map
import os
from sunpy.instr.aia import aiaprep

def read_SDOfits():
    data_dir='/Users/alyshareinard/Dropbox/work/data/SDO/'
    client=vso.VSOClient()
    qr=client.query_legacy('2013/1/11 03:00:00', '2013/1/11 09:00:00', instrument='AIA', min_wave="193", max_wave="193", unit_wave="Angstrom")
    res=client.get(qr, path=data_dir+'{instrument}/{file}.fits').wait()
    for file in os.listdir(data_dir+'/SDO/'):
        original=Map(data_dir+file)
        prepped=aiaprep(original)
#        imgplot=plt.imshow(original)
#        plt.colorbar()
        fig = plt.figure(figsize=(15, 8))
        fig.add_subplot(1, 2, 1)
        original.plot()
        prepped.plot()        
        
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