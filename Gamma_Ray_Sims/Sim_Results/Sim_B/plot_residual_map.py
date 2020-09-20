#imports
from astropy.io import fits
import matplotlib.pyplot as plt
from astropy.wcs import WCS
import aplpy
import colorcet as cet
import numpy as np

this_file = "sim_residuals.fits"

hdu = fits.open(this_file)
data = hdu[0].data

this_max = np.max(data)
print this_max
savefile = "simulated_residual_map.png"

fig = aplpy.FITSFigure(this_file,convention='calabretta')
fig.show_colorscale(interpolation='none',smooth=1,cmap='cet_coolwarm',vmin=-5,vmax=5)

#fig.add_grid()

plt.title("Residual Map", fontsize = 6)

#fig.show_contour('foot_print.fits',levels=1,smooth=None,linewidths=0.2,filled=False,colors='black',alpha=0.6)

fig.add_colorbar()
fig.colorbar.set_location('right')

fig.colorbar.set_axis_label_text('data - model') 
fig.colorbar.set_axis_label_font(size=6)
fig.colorbar.set_ticks([-5,0,5])
fig.colorbar.set_font(size=6)

fig.axis_labels.show()
fig.axis_labels.set_font(size='6')

#fig.tick_labels.hide_y()
fig.ticks.set_yspacing(1.0)
fig.tick_labels.set_font(size='6')
fig.tick_labels.set_xformat('ddd.d')
fig.tick_labels.set_yformat('ddd.d')

fig.recenter(325,0,width=50,height=4.01)

plt.savefig(savefile,bbox_inches='tight',dpi=300)
plt.show()
plt.close()
