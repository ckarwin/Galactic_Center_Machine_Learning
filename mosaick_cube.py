#imports:
from astropy.io import fits
from reproject.mosaicking import find_optimal_celestial_wcs
from reproject import reproject_interp
from reproject import reproject_exact
from reproject.mosaicking import reproject_and_coadd
import numpy as np
from astropy import wcs
from astropy import units as u
import matplotlib.pyplot as plt
from scipy.ndimage.filters import gaussian_filter
from astropy.convolution import convolve, Gaussian2DKernel

#needs to match input
#if not the error will tell you right size to use
total_array = np.zeros((17,35,1552))

#make input file list:
long_list = np.arange(300.5,350.5,1)

#make file list:
long_list = []
#a = np.arange(300.5,350,0.5) #for all fields, separated by 0.5
a = np.arange(300.5,350,1) #for all fields, separated by 1.0
for each in a:
        if each - int(each) == 0.5:
            long_list.append(each)
        else: long_list.append(int(each))
print()
print(long_list)
print()

#for testing:
#long_list = [311.5]

#set resolution and savefile:
#savefile = "Mopra_resolution_true_5_bins_cube.fits"
savefile = "Fits_Files/mopra_17vbins_1o32_res.fits"
#resolution = 8.33333333333E-03
resolution = 1/32.0

#to run with reproject_and_coadd requires 2d format
#so I run separate for each velocity bin, then combine at the end
for i in range(0,17):
    file_list = []
    for each in long_list:
    
        this_path = "/Users/chriskarwin/Desktop/GC_PS_Analysis/Mopra_CO_Data/12CO_Velocity_Bins_17_Data/"
        this_file = this_path + "G" + str(each) + "-12CO_VB17.fits"
        hdu = fits.open(this_file)
        header = hdu[0].header
    
        CRPIX1 = header["CRPIX1"]
        CRPIX2 = header["CRPIX2"]
        CRVAL1 = header["CRVAL1"]
        CRVAL2 = header["CRVAL2"]

        world = wcs.WCS(header)

        new_world = wcs.WCS(naxis=2)
        new_world.wcs.crpix = [CRPIX1,CRPIX2]
        new_world.wcs.cdelt = np.array([-8.33333333333E-03,8.33333333333E-03])
        new_world.wcs.crval = [CRVAL1,CRVAL2]
        new_world.wcs.ctype = ["GLON-SIN","GLAT-SIN"]

        array = hdu[0].data[i]
        file_list.append((array,new_world))

    #find wcs:
    wcs_out, shape_out = find_optimal_celestial_wcs(file_list,projection="SIN",resolution=resolution * u.deg)
    
    #combine array:
    array, footprint = reproject_and_coadd(file_list,wcs_out,shape_out=shape_out,reproject_function=reproject_interp,match_background=False)
    total_array[i,:,:] = array[:,:]
    
    #clip array at zero, and set nan to zero. 
    total_array[i,:,:] = np.nan_to_num(total_array[i,:,:])
    total_array[i,:,:] = np.clip(total_array[i,:,:], a_min=0, a_max=None)
    
        
    #smooth array:
    #gauss_kernel = Gaussian2DKernel(2.)
    #total_array[i,:,:] = convolve(total_array[i,:,:], gauss_kernel)

#write output:
this_header = wcs_out.to_header()
CRPIX1 = this_header["CRPIX1"]
CRPIX2 = this_header["CRPIX2"]
CRVAL1 = this_header["CRVAL1"]
CRVAL2 = this_header["CRVAL2"]

final_world = wcs.WCS(naxis=3)
final_world.wcs.crpix = [CRPIX1,CRPIX2,0]
final_world.wcs.cdelt = np.array([-1*resolution,resolution,1])
final_world.wcs.crval = [CRVAL1,CRVAL2,0]
final_world.wcs.ctype = ["GLON-SIN","GLAT-SIN",""]

final_header = final_world.to_header()
final_hdu = fits.PrimaryHDU(total_array,header=final_header)
hdu1 = fits.HDUList([final_hdu])
hdu1.writeto(savefile,overwrite=True)

final_foot_world = wcs.WCS(naxis=2)
final_foot_world.wcs.crpix = [CRPIX1,CRPIX2]
final_foot_world.wcs.cdelt = np.array([-1*resolution,resolution])
final_foot_world.wcs.crval = [CRVAL1,CRVAL2]
final_foot_world.wcs.ctype = ["GLON-SIN","GLAT-SIN"]

foot_print_header = final_foot_world.to_header()
foot_print_hdu = fits.PrimaryHDU(footprint,header=foot_print_header)
hdu2 = fits.HDUList([foot_print_hdu])
hdu2.writeto("foot_print.fits",overwrite=True)

#add BINS extension to specify radial bins:
hdu = fits.open(savefile)
#rad = np.array([(0.0,2.5),(2.5,5.0),(5.0,7.0),(7.0,10.0),(10.0,50.0)], dtype= [('Rmin','>f4'),('Rmax','>f4')])#for 5 velocity bins
#rad = np.array([(0.0,25),(25,50)], dtype= [('Rmin','>f4'),('Rmax','>f4')]) #for 2 velocity bins
rad = np.array([(0.0,1.5),(1.5,2.0),(2.0,2.5),(2.5,3.0),(3.0,3.5),(3.5,4.0),(4.0,4.5),(4.5,5.0),(5.0,5.5)
                ,(5.5,6.5),(6.5,7.0),(7.0,8.0),(8.0,10.0),(10.0,11.5),(11.5,16.5),(16.5,19),(19,50)], dtype= [('Rmin','>f4'),('Rmax','>f4')]) #17 velocity bins
hdu.append(fits.BinTableHDU(rad))
header_1 = hdu[1].header
header_1['TUNIT1'] = "kpc"
header_1['TUNIT2'] = "kpc"
hdu[1].name = "BINS"
hdu.writeto(savefile,clobber=True)

plt.figure(figsize=(40, 10))
ax1 = plt.subplot(1, 2, 1)
im1 = ax1.imshow(array, origin='lower')
ax1.set_title('Mosaic')
ax2 = plt.subplot(1, 2, 2)
im2 = ax2.imshow(footprint, origin='lower')
ax2.set_title('Footprint')
plt.savefig("footprint.png")
plt.show()

#print "*****************"
#print wcs_out.to_header()
#print shape_out
