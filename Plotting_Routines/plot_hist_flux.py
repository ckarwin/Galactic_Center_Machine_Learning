#imports
import matplotlib.pyplot as plt
from scipy.stats import norm
import matplotlib.mlab as mlab
import numpy as np
from astropy.io import fits

dame_path = "/zfs/astrohe/ckarwin/Machine_Learning_GC/Sim_2/Dame_Maps/Simulation_Output/"

flux_listD = []
flux_listM = []
for i in range(1,301):
    
    #get Dame values:
    this_fileD = dame_path + "sim_%s/after_alternative_fit.fits" %str(i)
    hdu = fits.open(this_fileD)
    data = hdu[1].data
    flux = data["flux"][0]
    flux_listD.append(flux)
    
    #get Mopra values:
    this_fileM = "sim_%s/after_alternative_fit.fits" %str(i)
    hdu = fits.open(this_fileM)
    data = hdu[1].data
    flux = data["flux"][0]
    flux_listM.append(flux)
    
    
plt.figure(figsize=(8,6))
ax = plt.gca()

#plot Dame:
max_value = max(flux_listD)
min_value = min(flux_listD)
n, bins, patches = plt.hist(flux_listD,density=True,bins=40,range=(min_value,max_value),histtype='step',label="_nolabel_",alpha=0.5,color="cornflowerblue")

(mu,sigma) = norm.fit(flux_listD)
xmin, xmax = plt.xlim()
x = np.linspace(xmin,xmax,100)
p = norm.pdf(x,mu,sigma)
plt.plot(x,p,"r--",linewidth=2,color="cornflowerblue",label="Dame+01")
print
print "Dame Maps:"
print "mean: " + str(mu)
print

#plot Mopra:
max_value = max(flux_listM)
min_value = min(flux_listM)
n, bins, patches = plt.hist(flux_listM,density=True,bins=40,range=(min_value,max_value),histtype='step',label="_nolabel_",alpha=0.5,color="purple")

(mu,sigma) = norm.fit(flux_listM)
xmin, xmax = plt.xlim()
x = np.linspace(xmin,xmax,100)
p = norm.pdf(x,mu,sigma)
plt.plot(x,p,"r--",linewidth=2,color="purple",label="Mopra")
print
print "Mopra Maps:"
print "mean: " + str(mu)
print

#plt.xscale("log")
#plt.xlim(1.5,3.5)
#plt.ylim(0,10)
plt.xlabel("Photon Flux (1$-$100 GeV) [$\mathrm{ph \ cm^2 \ s^{-1}}$]",fontsize=14)
plt.ylabel("Probability Density",fontsize=14)
plt.title("Point-like Excess Template", fontsize=14)
#plt.grid(color="grey",alpha=0.2,linewidth=4)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.legend(loc=0,frameon=False)
plt.savefig("flux_hist.pdf")
plt.show()
