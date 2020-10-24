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

def Integrate_Velocity(input_file,noise_file,bin_list,savefile):
    
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
    data = data
    shape = data.shape
    print shape[0]
    num_bins = len(bin_list)

    NaN = isnan(data)
    data[NaN] = 0

    #subtract noise:
    hdu_noise = fits.open(noise_file)
    noise = hdu_noise[0].data
    for n in range(0,shape[0]):
        clip_index = (data[n,:,:] > 0) & (data[n,:,:] <= 2*noise[:,:])
        data[n,clip_index] = 0.0  
    
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

            line_strength = False
            column_density = True

            #clip array for column density:
            #data = np.clip(data,0.2,None)
            #clip_index = data <= 0.2
            #data[clip_index] = 0.0

            data[a,:,:] = 0
            for i in range(a,b):
                
                if line_strength == True:
                    data[a,:,:] = data[a,:,:] + data[i,:,:]*delta_v
        
                if column_density == True:

                    #clip_index = data[i,:,:] <= 0.4
                    #data[i,clip_index] = 0.0

                    X_co13 = 7.5e5 #CO13 conversion factor
                    T_ex = 10 #units=K: excitation temperature
                    T_0 = 5.3 #units=K: energy level of J=1-0 transition
                    
                    coeff = 3.0e14*T_ex/(1-math.e**(-1*(T_0/T_ex)))
                
                    optical_depth = -1*np.log(1 - data[i,:,:]/5.3 * ( (math.e**(5.3/T_ex) - 1)**-1 - 0.16)**-1)
            
                    data[a,:,:] = data[a,:,:] + X_co13*coeff*optical_depth*delta_v
            

            data[a,:,:] = data[a,:,:]*(1/0.55) #correct for telescope efficiency
            subset[counter,:,:] = data[a,:,:]
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
    #rad = np.array([(0.0,1.5),(1.5,2.0),(2.0,2.5),(2.5,3.0),(3.0,3.5),(3.5,4.0),(4.0,4.5),(4.5,5.0),(5.0,5.5)
    #    ,(5.5,6.5),(6.5,7.0),(7.0,8.0),(8.0,10.0),(10.0,11.5),(11.5,16.5),(16.5,19),(19,50)], dtype= [('Rmin','>f4'),('Rmax','>f4')]) #17 bins
    rad = np.array([(0.0,2.5),(2.5,5.0),(5.0,7.0),(7.0,10.0),(10.0,50.0)], dtype= [('Rmin','>f4'),('Rmax','>f4')]) #combined bins
    hdu.append(fits.BinTableHDU(rad))
    header_1 = hdu[1].header
    header_1['TUNIT1'] = "kpc"
    header_1['TUNIT2'] = "kpc"
    hdu[1].name = "BINS"
    hdu.writeto(savefile,clobber=True)
