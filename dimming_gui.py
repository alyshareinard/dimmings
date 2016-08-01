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
import glob
from functools import reduce
import numpy as np
from sunpy.physics.transforms.solar_rotation import mapcube_solar_derotate


def read_SDOfits():
    print("in SDOfits")
    if os.name=='posix':
        data_dir='/Users/alyshareinard/Dropbox/work/data/SDO/'
    else:
        data_dir='C:\\Users\\alysha.reinard.SWPC\\Dropbox\\Work\\data\\SDO\\'
    client=vso.VSOClient()
    print("defined client")
    qr=client.query_legacy('2013/1/23 09:36:00', '2013/1/23 14:15:00', instrument='AIA', min_wave="193", max_wave="193", unit_wave="Angstrom")# , resolution=0.5)
    print("after client")
    count=0
    qr_10=[]
    for item in qr:
        if count==0:
           qr_10.append(item)
        count+=1
        if count==100: 
            count=0
#    print("qr", len(qr))
#    print("qr_10", len(qr_10))
#    print("qr_10 vals", qr_10[0])
#    data_dir='C:\\Users\\alysha.reinard.SWPC\\Dropbox\\Work\\data\\'
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
    res=client.get(qr_10, path=data_dir+'{instrument}/{file}.fits').wait()
    print("after wait")
    
def process_dimmings():  
#    filelist=os.listdir(os.path.join(data_dir,'AIA', '*.fits'))
    filelist=glob.glob(os.path.join(data_dir,'AIA', '*.fits'))
    print("filelist", filelist)
    preppedlist=[]
    difflist=[]
    count=0
    for file in filelist:
        print("file", file)
        if count==0:
            base=aiaprep(Map(file))
            print("base exp time", base.exposure_time)
            print("buffer line")
            count=1
        prepped_image=aiaprep(Map(file))

#        prepped_image.plot()
#        plt.show()
        preppedlist.append(prepped_image)
        
    prepped_cube=Map(preppedlist, cube=True)
    derotated_prepped_cube=mapcube_solar_derotate(prepped_cube, clip=False)
    print("len?", len(derotated_prepped_cube))
    for i in range(1, len(derotated_prepped_cube)):
        diffimage=derotated_prepped_cube[i]
        print("exposure time", diffimage.exposure_time)

#        diffimage1=copy(diffimage)
#        print("shape", diffimage.data.shape)
#        x=500
#        y=520
#        print("before", diffimage.data[x][x:y], diffimage.exposure_time)
#        base.plot(vmin=-1500, vmax=1500)
#        plt.show()
#        print("base", base.data[x][x:y], base.exposure_time)
#        diffimage.plot(vmin=-1500, vmax=1500)
#        plt.show()
        diffimage.data=diffimage.data-base.data
#        print("after", diffimage.data[x][x:y], diffimage.exposure_time)
        diffimage.plot(vmin=-1500, vmax=1500)
        plt.show()
        
        difflist.append(diffimage)
#        if count>0:
#            diffimage=prepped_image
#            diffimage.data=prepped_image.data-base.data
#            print(np.mean(diffimage.data), np.max(diffimage.data), np.min(diffimage.data))#, max(diffimage.data), min(diffimage.data))
#            print(base.data[0:20])
#            diffimage=prepped_image.data-base.data
#            diffimage.plot(vmin=-150, vmax=150)
#            plt.show()
#            difflist.append(prepped_image.data-base.data)
            
#    return [diffimage1, base, diffimage]
#    print("length", len(preppedlist[0]))
#    baseimage=preppedlist[0]
    
    
    
    
#    aia_cube = Map(data_dir+'/AIA/*.fits', cube=True)   
#    print("First, what do we have here??", [m.data for m in aia_cube])
#    print("same shape? ", aia_cube.all_maps_same_shape())
#    print(aia_cube[0])
#    print("after wait")
#    aia_cube = Map(data_dir+'\\AIA\\*.fits', cube=True)  

#    prepped_cube=aiaprep(aia_cube[0])
#    print("made cube")
#    print("First, what do we have here??", [m.data for m in aia_cube])
#    print("same shape? ", aia_cube.all_maps_same_shape())
#    plt.figure()
#    aia_cube.plot
#    plt.show()
#    print("plotted cube")
#    print("size?", aia_cube.size)
 #   aia_cube_array=aia_cube.as_array()
 #   prepped_cube=aiaprep(aia_cube_array)
#    print("size", aia_cube_array.size)
 #   print("made array")
 #   print("size", aia_cube_array.shape)
 #   size=aia_cube_array.shape
 #   (height, width, length)=size
 #   print(length)
 #   for val in range(length):
 #       if val==0:
 #           base=aia_cube_array[:, :, 0]
 #       else:
 #           aia_cube_array[:, :, val]=aia_cube_array[:, :, val]-base
 #   print("size after", aia_cube_array.shape)
 #   print("size of base", base.shape)
##    plt.plot(base)
 #   plt.imshow(aia_cube_array[:,:,4])
 #   plt.show
##    count=0
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
#    print("dir", data_dir+'AIA'+os.sep+'*.fits')
#    print("list", os.listdir(data_dir+"AIA"+os.sep+r"*.fits"))
#    for file in os.listdir(data_dir+'AIA'+os.sep+'*.fits'):
#
#        print("file", file)
#        print("full path", data_dir+"AIA"+os.sep+file)
#        original=Map(data_dir+'AIA'+os.sep+file)
#        prepped=aiaprep(original)
##        imgplot=plt.imshow(original)
##        plt.colorbar()
#        if count==0:
#            pre_image=prepped
#            count=1
#        else:
#            fig = plt.figure(figsize=(15, 8))
#            fig.add_subplot(1, 2, 1)
#            print("meta", prepped.meta)
#            print("data", prepped.data)
#            prepped=prepped-pre_image
#            #            original.plot()
#            prepped.plot() 
#            plt.plot([1, 2, 3, 4])
#            break
        
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