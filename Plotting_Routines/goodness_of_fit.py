#imports
import matplotlib.pyplot as plt
from scipy.stats import norm
import matplotlib.mlab as mlab
import numpy as np
import xml.etree.ElementTree as ET
import os
from astropy.io import fits

dame_path = "/zfs/astrohe/ckarwin/Machine_Learning_GC/Sim_2/Dame_Maps/Simulation_Output/"

#setup figure:
fig = plt.figure(figsize=(8,5))

for i in range(1,301):

    print
    print "working on sim " + str(i) + "..."
    home = os.getcwd()
    thisdir = dame_path + "sim_%s" %str(i) #Dame
    #thisdir = "sim_%s" %str(i) #Mopra
    os.chdir(thisdir)

    #open sim data cube
    hdu = fits.open("srcmap_00.fits")
    data = hdu[0].data
    header = hdu[0].header
    
    #open model cube
    hdu1 = fits.open("mcube_alternative_model_00.fits")
    data1 = hdu1[0].data

    energy_list = []
    E = hdu1[1].data
    for j in range(0,len(E)):
        this_E = E[j][1]
        energy_list.append(this_E)

    data_frac = []
    model_frac = []
    for E in range(0,20):
        this_data = np.sum(data[E,:,:])
        this_model = np.sum(data1[E,:,:])
        data_frac.append(this_data)
        model_frac.append(this_model)

    #calculate fractional residuals:
    this_data = np.array(data_frac)
    this_model = np.array(model_frac)
    resid = (this_data - this_model)/this_model
    resid_error = np.sqrt(this_data)/this_model

    #plot example residuals:
    if i == 9:
        plt.semilogx(energy_list,resid,marker = 'o', ms=8,markeredgecolor = 'none',zorder=0,ls = '', color = 'black',label="single simulation (example)")
        plt.errorbar(energy_list,resid,yerr=resid_error,marker = 'o', ms=8,markeredgecolor = 'none',ls = '', color = 'black',label="_nolabel_")

    #make array:
    if i == 1:
        this_array = np.array(resid.tolist())
    if i == 2:
        this_array = np.append([this_array],[resid.tolist()],axis=0)
    if i > 2:
        this_array = np.append(this_array,[resid.tolist()],axis=0)
    
    #go home:
    os.chdir(home)

#calculate mean and standard deviation of each energy bin:
#mean = np.mean(this_array,axis=0)
#std = np.std(this_array,axis=0)
mean = []
std = []
for i in range(0,this_array.shape[1]):
    this_column = this_array[:,i]
    (mu,sigma) = norm.fit(this_column)
    mean.append(mu)
    std.append(sigma)
mean = np.array(mean)
std = np.array(std)

low = mean - std
high = mean + std
low2 = mean - 2*std
high2 = mean + 2*std

#make brazilian plot:
plt.fill_between(energy_list,low,high,color="limegreen",alpha=1)
plt.fill_between(energy_list,low2,high2,color="yellow",alpha=1,zorder=0)
plt.plot([0.1],[0.1],label="68%",color="limegreen",lw=5)
plt.plot([0.1],[0.1],label="95%",color="yellow",lw=5)
plt.xscale("log")

plt.axhline(0.0,ls=':')
plt.xlabel('Energy [MeV]',fontsize=14)
plt.ylabel('(Data-Model)/Model',fontsize=14)
plt.title('fractional residuals (Dame)',fontsize=14,y=1.04)
plt.xlim((1e3,1e5))
plt.ylim((-0.3,0.3))
plt.xticks(size=14)
plt.yticks(size=14)
plt.legend(loc=2,frameon=False)
plt.savefig("fractional_residuals_Dame.pdf")
plt.show()
plt.close()
