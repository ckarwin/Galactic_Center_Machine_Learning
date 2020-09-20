#imports 
from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import chi2

hdu = fits.open("test_pointsource_powerlaw_2.00_tsmap.fits")
data = hdu[0].data
data = np.ndarray.flatten(data)

df = 1
mean, var, skew, kurt = chi2.stats(df, moments='mvsk')
x = np.linspace(chi2.ppf(0.01, df),chi2.ppf(0.999999999, df), 100)
plt.plot(x, chi2.pdf(x, df)/2.0,color="black", lw=4, alpha=1, label='$\chi^2_1$/2')

n, bins, patches =plt.hist(data,bins=100,density=True,edgecolor="black",facecolor="green",label="_nolabel_")

plt.yscale("log")
plt.ylim(1e-4,1e0)
#plt.ylim(0,10000)
plt.xlim(0,15)
plt.xlabel("TS",fontsize=14)
plt.ylabel("Normalized Histogram",fontsize=14)
#plt.ylabel("Number of Pixels",fontsize=14)
plt.legend(loc=1,frameon=False)
plt.savefig("TS_dist.pdf")
plt.show()
