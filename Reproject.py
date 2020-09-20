from astropy.io import fits
from reproject import reproject_interp
import numpy as np

for i in range(0,17):
    this_file = "pion_decay_H2R_mapcube_comp_%s_56_Mopra.gz" %i
    
    savefile = 'reprojected_' + this_file
    
    hdu = fits.open(this_file)[0]
    new_header = hdu.header.copy() 

    new_header['CRVAL1'] = 355
    new_header['CDELT1'] = -0.03125
    new_header['CRPIX1'] = 0

    new_image, footprint = reproject_interp(hdu, new_header)

    fits.writeto(savefile, new_image,new_header, overwrite=True)

    #add energy extenstion:
    hdu = fits.open(this_file)[1]
    energy = hdu.data
    energy = np.array(energy, dtype=(np.record, [('Energy', '>f8')]))
    
    hdu_2 = fits.open(savefile)
    hdu_2.append(fits.BinTableHDU(energy))
    header_1 = hdu_2[1].header
    header_1["TTYPE1"] = 'Energy'
    header_1["TUNIT1"] = 'MeV'
    header_1["EXTNAME"] = 'ENERGIES'
    hdu_2.writeto(savefile,overwrite=True)
