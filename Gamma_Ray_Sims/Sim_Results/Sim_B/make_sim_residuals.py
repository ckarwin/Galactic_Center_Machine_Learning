#imports
from astropy.io import fits
from astropy import wcs
import numpy as np
import matplotlib.pyplot as plt

sim_resid = False
frac_resid = True

#open sim data cube
hdu = fits.open("srcmap_00.fits")
data = hdu[0].data


#open model cube
hdu1 = fits.open("mcube_sim_model_00.fits")
data1 = hdu1[0].data
header = hdu1[0].header

energy_list = []
E = hdu1[1].data
for i in range(0,len(E)):
	this_E = E[i][1]
	energy_list.append(this_E)


#calculate sim residuals:
if sim_resid == True:
	for E in range(0,20):
		data1[E,:,:] = data[E,:,:] - data1[E,:,:]

	for E in range(1,20):
		data1[0,:,:] = data1[0,:,:] + data1[E,:,:]

	total_array = data1[0,:,:]
	savefile = "sim_residuals.fits"

        CRPIX1 = header["CRPIX1"]
        CRPIX2 = header["CRPIX2"]
        CRVAL1 = header["CRVAL1"]
        CRVAL2 = header["CRVAL2"]
        CDELT1 = header["CDELT1"]
        CDELT2 = header["CDELT2"]
        CTYPE1 = header["CTYPE1"]
        CTYPE2 = header["CTYPE2"]

        world = wcs.WCS(header)

        new_world = wcs.WCS(naxis=2)
        new_world.wcs.crpix = [CRPIX1,CRPIX2]
        new_world.wcs.cdelt = np.array([CDELT1,CDELT2])
        new_world.wcs.crval = [CRVAL1,CRVAL2]
        new_world.wcs.ctype = [CTYPE1,CTYPE2]

        final_header = new_world.to_header()
        final_hdu = fits.PrimaryHDU(total_array,header=final_header)
        hdu1 = fits.HDUList([final_hdu])
        hdu1.writeto(savefile,overwrite=True)

if frac_resid == True:
	
	data_frac = []
	model_frac = []
	for E in range(0,20):
		
		this_data = np.sum(data[E,:,:])
		this_model = np.sum(data1[E,:,:])
		data_frac.append(this_data)		
		model_frac.append(this_model)

	this_data = np.array(data_frac) 
	this_model = np.array(model_frac)
	resid = (this_data - this_model)/this_data
	resid_error = np.sqrt(this_data)/this_data
	
	fig = plt.figure(figsize=(8,5))
	plt.semilogx(energy_list,resid,marker = 'o', ms=8,markeredgecolor = 'none',ls = '', color = 'black',label="_nolabel_")
	plt.errorbar(energy_list,resid,yerr=resid_error,marker = 'o', ms=8,markeredgecolor = 'none',ls = '', color = 'black',label="baseline(randomize=True)")
	
	plt.axhline(0.0,ls=':')
	plt.xlabel('Energy [MeV]',fontsize=14)
        plt.ylabel('(Data-Model)/Model',fontsize=14)
        plt.title('fractional residuals',fontsize=14,y=1.04)
        #plt.xlim((20,200))
        #plt.ylim((-0.2,0.2))
	plt.xticks(size=14)
	plt.yticks(size=14)	
	plt.legend(loc=2,frameon=False)
	plt.savefig("fractional_residuals.pdf")
	plt.show()
	plt.close()

