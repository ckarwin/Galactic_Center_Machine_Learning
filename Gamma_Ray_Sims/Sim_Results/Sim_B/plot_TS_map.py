#imports
from astropy.io import fits
import matplotlib.pyplot as plt
from astropy.wcs import WCS
import aplpy
import colorcet as cet
import numpy as np

this_file = "test_pointsource_powerlaw_2.00_tsmap.fits"

hdu = fits.open(this_file)
data = hdu[0].data

this_max = np.max(data)
print this_max
savefile = "TS_map.png"
fig = aplpy.FITSFigure(this_file,dimensions=[0,1],slices=[0],figsize=(10,1),convention='calabretta')
fig.show_colorscale(interpolation='none',stretch="log",cmap='inferno',vmin=0.1,vmax=this_max)

plt.title("TS Map (Sim B)", fontsize = 6)

#fig.show_contour('foot_print.fits',levels=1,smooth=None,linewidths=0.2,filled=False,colors='black',alpha=0.6)

fig.add_colorbar()
fig.colorbar.set_location('right')

#fig.colorbar.set_axis_label_text('$\mathrm{N_{H_2}}$ [cm^-2]') #column density
fig.colorbar.set_axis_label_text('TS') #line strength
fig.colorbar.set_axis_label_font(size=6)
fig.colorbar.set_ticks([0.1,1,100,this_max])
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
#plt.savefig(savefile,bbox_inches='tight')
plt.show()
plt.close()
