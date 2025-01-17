#Written by Chris Karwin, May 2019, UCI
#Purpose: Combine annuli for the GALPROP Maps.
#The code is setup for 4 bins but can be easily modified for any combination.

#imports:
from astropy.io import fits

#annuli to combine:
combine = [[0,5],[6,9],[10,12],[13,16]]

for each in combine:
    
    low = each[0]
    high = each[1]

    this_file = "reprojected_pion_decay_H2R_mapcube_comp_%s_56_Mopra.gz" % str(low)
    hdu = fits.open(this_file)
    data = hdu[0].data

    for i in range(low+1,high+1):

        this_file = "reprojected_pion_decay_H2R_mapcube_comp_%s_56_Mopra.gz" %i
        add_hdu = fits.open(this_file)
        add_data = add_hdu[0].data
        data += add_data

    hdu.writeto("reprojected_pion_decay_annuli_%s_%s.fits" % (str(low),str(high)), clobber=True)


