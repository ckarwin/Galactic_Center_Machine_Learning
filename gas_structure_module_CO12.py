#imports
#import pyfits
import math
from numpy import *
import numpy as np 
from astropy.io import fits

#Finds pixel range corresponding to given velocity range.
#Needed for integration.
def find_bin(v,ref_v,ref_p,delta_v):
    
    this_k = (v - ref_v)/delta_v
    k = ref_p + this_k 
    
    return int(k)

def Integrate_Velocity(input_file,bin_list,savefile):
    
    #make intro:
    print
    print "###########################"
    print "###########################"
    print "    Make Velocity Bins     "
    print "###########################"
    print 

    #upload data:
    hdu = fits.open(input_file)
    header = hdu[0].header
    data = hdu[0].data
    shape = data.shape
    num_bins = len(bin_list)

    NaN = isnan(data)
    data[NaN] = 0

    print 
    print "###########################"
    print "# Data Cube Information"
    print "#"
    print 
    print "data shape: " + str(shape)
    print 
    print "number of velocity bins: " + str(num_bins)
    print
    print num_bins
    #define new dimensions and set to zero:
    subset = data[0:num_bins,:,:]
    subset[:,:,:] = 0

    #velocity master:
    ref_v = header["CRVAL3"]*1e-3 #convert m/s to km/s
    ref_p = header["CRPIX3"]
    delta_v = header["CDELT3"]*1e-3 #convert m/s to km/s
    
    print
    print "###########################"
    print "# Reference Information"
    print "#"
    print 
    print "reference velocity: " + str(ref_v) + " km/s"
    print "reference pixel: "  + str(ref_p) 
    print "delta velocity: " + str(delta_v) + " km/s"
    print

    #integrate over velocity:
    counter = 0
    for each in bin_list:
        
        v_low = each[0]
        v_high = each[1]

        if v_low == 0: 

            print
            print "#####################################"
            print "# Integration Information for Bin " + str(counter)
            print "#"
            print
            print "velocity low: " + str(v_low) + " km/s"
            print "velocity high: " + str(v_high) + " km/s"
            print "added zero array for this bin"
            print

            subset[counter,:,:] = 0
            counter += 1
        
        
        if v_low != 0:
        
            a = find_bin(v_low,ref_v,ref_p,delta_v)
            b = find_bin(v_high,ref_v,ref_p,delta_v)
        
            print 
            print "#####################################"
            print "# Integration Information for Bin " + str(counter)
            print "#"
            print 
            print "velocity low: " + str(v_low) + " km/s"
            print "velocity high: " + str(v_high) + " km/s"
            print "bin low: " + str(a)
            print "bin high: " + str(b)
            print 

            data[a,:,:] = 0
            for i in range(a,b):
                data[a,:,:] = data[a,:,:] + data[i,:,:]*delta_v
        
            data[a,:,:] = data[a,:,:]*(1/0.55) #correct for telescope efficiency
            subset[counter,:,:] = data[a,:,:]
            
            #convert to column density:
            column_density = True
            X_co12 = np.array([3.61934e19, 1.01355e20, 1.0438e20, 1.05894e20, 1.11434e20, 1.08569e20, 1.15424e20, 1.18716e20, 1.2047e20, 1.22475e20, 1.32743e20, 1.40205e20, 7.21006e19, 7.00169e20, 2.45472e21, 1.31792e22, 5.3247e22])
    
            if column_density == True:
                subset[counter,:,:] = subset[counter,:,:]*X_co12[counter]

            counter = counter+1
            
    #write new history notes:
    del header['history'] #delete old history first (just b/c there was a lot for Mopra data)
    header['history'] = "Deleted all old History (see original files)"
    header['history'] = "Combined into velocity bins"
    header['history'] = "beam efficiency has been accounted for with eta=0.55"

    #delete velocity header information, since it no longer applies:
    del header["CRVAL3"]
    del header["CRPIX3"]
    del header["CDELT3"]
    del header["CTYPE3"]

    #write file to data:
    hdu = fits.PrimaryHDU(subset,header=header)
    hdu.writeto(savefile, clobber=True)

    #add BINS extension to specify radial bins:
    hdu = fits.open(savefile)
    rad = np.array([(0.0,1.5),(1.5,2.0),(2.0,2.5),(2.5,3.0),(3.0,3.5),(3.5,4.0),(4.0,4.5),(4.5,5.0),(5.0,5.5)
       ,(5.5,6.5),(6.5,7.0),(7.0,8.0),(8.0,10.0),(10.0,11.5),(11.5,16.5),(16.5,19),(19,50)], dtype= [('Rmin','>f4'),('Rmax','>f4')]) #17 bins
    #rad = np.array([(0.0,2.5),(2.5,5.0),(5.0,7.0),(7.0,10.0),(10.0,50.0)], dtype= [('Rmin','>f4'),('Rmax','>f4')]) #combined bins
    hdu.append(fits.BinTableHDU(rad))
    header_1 = hdu[1].header
    header_1['TUNIT1'] = "kpc"
    header_1['TUNIT2'] = "kpc"
    hdu[1].name = "BINS"
    hdu.writeto(savefile,clobber=True)
