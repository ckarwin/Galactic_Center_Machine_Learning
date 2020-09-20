#imports
from astropy.io import fits
import matplotlib.pyplot as plt
from astropy.wcs import WCS
import aplpy
import colorcet as cet
import numpy as np
import pandas as pd 

#this_file = "Fits_Files/mopra_17vbins_1o32_res.fits"
#this_file = "Fits_Files/mopra_17vbins_1o32_res_column_density.fits"
this_file = "find2_sourcefind_00_pointsource_powerlaw_2.50_tsmap.fits"

hdu = fits.open(this_file)
data = hdu[0].data
#wcs = WCS(hdu[0].header)
#print data.shape

for i in range(0,1):
    print
    print "working on bin: " + str(i)
    print

    this_max = np.max(data[i])
    print this_max
    #savefile = "Images/Images_bins17_1o32_res/mosaic_bin_" + str(i) + ".png"
    #savefile = "Images/Images_bins17_1o32_res/Column_Density/column_density_mosaic_bin_" + str(i) + ".png"
    savefile = "TS_map.png"
    fig = aplpy.FITSFigure(this_file,figsize=(10,1),convention='calabretta')
    fig.show_colorscale(interpolation='none',stretch="log",cmap='viridis',vmin=0.1,vmax=1000)

    #upload 3FGL point sources:
    PS_file = "/Users/chriskarwin/Desktop/GC_PS_Analysis/3FGL_PS_Data/unassociated.csv"
    df = pd.read_csv(PS_file,skiprows=[0],sep='\t',names=["name","l [degree]","b [degree]"])
    l = df["l [degree]"]
    b = df["b [degree]"]
    l_list = l.tolist()
    b_list = b.tolist()

    #change l values>180 to negative for plotting:
    new_l_list = []
    for each in l_list:
        if each > 180:
            each = each - 360
            new_l_list.append(each)
        else: new_l_list.append(each)

    fig.show_markers(new_l_list,b_list)
    #plt.title("$\mathrm{H_2}$ Column Density (Mopra CO12) bin " + str(i), fontsize = 6)
    #plt.title("Mopra bin " + str(i), fontsize = 6)
    plt.title("Sim A (WO fluctuations) TS Map", fontsize = 6)

    #fig.show_contour('foot_print.fits',levels=1,smooth=None,linewidths=0.2,filled=False,colors='black',alpha=0.6)

    fig.add_colorbar()
    fig.colorbar.set_location('right')

    #fig.colorbar.set_axis_label_text('$\mathrm{N_{H_2}}$ [cm^-2]') #column density
    fig.colorbar.set_axis_label_text('TS') #line strength
    fig.colorbar.set_axis_label_font(size=6)
    fig.colorbar.set_ticks([0,this_max])
    fig.colorbar.set_font(size=6)

    fig.axis_labels.show()
    fig.axis_labels.set_font(size='6')

    #fig.tick_labels.hide_y()
    fig.ticks.set_yspacing(0.5)
    fig.tick_labels.set_font(size='6')
    fig.tick_labels.set_xformat('ddd.d')
    fig.tick_labels.set_yformat('ddd.d')

    fig.recenter(325,0,width=50,height=1)

    plt.savefig(savefile,bbox_inches='tight',dpi=1000)
    #plt.savefig(savefile,bbox_inches='tight')
    #plt.show()
    plt.close()
