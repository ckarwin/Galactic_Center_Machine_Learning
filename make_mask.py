#Written by Chris Karwin, Dec 2019, Clemson University
#Purpose: Mask the Galprop maps using the footprint, as well as Galactic latitude and longitude.

#imports:
from astropy.io import fits
from astropy.wcs import WCS
import astropy.wcs.utils as utils
import numpy as np

#upload footprint:
hdu = fits.open("foot_print.fits")
foot_header = hdu[0].header
footprint = hdu[0].data
foot_wcs = WCS(foot_header)

print
print "footprint shape:"
print footprint.shape
print 

#mask footprint pixels:
mask = np.argwhere(footprint > 1)

#make l and b lists: 
blist = []
llist = []
for each in mask:
    b = each[0]
    l = each[1]
    blist.append(b)
    llist.append(l)

#transfer pixels in foot_wcs to sky coordinates:
coords = utils.pixel_to_skycoord(llist,blist,foot_wcs)
print coords

#upload GALPROP:
combine = [[0,5],[6,9],[10,12],[13,16]]

for each in combine:

    low = each[0]
    high = each[1]

    this_file = "reprojected_pion_decay_annuli_%s_%s.fits" % (str(low),str(high))
    savefile = "masked_" + this_file

    hdu = fits.open(this_file)
    gal_header = hdu[0].header
    gal_data = hdu[0].data
    gal_wcs = WCS(gal_header)

    gal_shape = gal_data.shape
    print
    print "galprop shape:"
    print gal_shape
    print

    #convert sky coordinates to pixels in gal_wcs:
    pixs =  utils.skycoord_to_pixel(coords,gal_wcs)

    mask_index = np.array(pixs)
    mask_index = mask_index.astype(int)

    print "mask index:"
    print mask_index
    print

    #make mask:
    for E in range(0,21):

        #footprint mask:
        gal_data[E,mask_index[1],mask_index[0]] = 0.0

        #mask top and bottom region and bad field:
        for l in range(0,gal_shape[2]):
            for b in range (0,gal_shape[1]):
                this_world = gal_wcs.all_pix2world(np.array([[l,b,1]]),0)
                this_l = this_world[0][0]
                this_b = this_world[0][1]
                if this_l < 300:
                    gal_data[E,b,l] = 0
                if this_l > 350:
                    gal_data[E,b,l] = 0
                if this_b < -0.5 or this_b > 0.5:
                    gal_data[E,b,l] = 0
                if 326 <= this_l <= 327:
                    gal_data[E,b,l] = 0

    #savefile:
    hdu.writeto(savefile,overwrite=True)
