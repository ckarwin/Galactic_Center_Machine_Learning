#imports
import matplotlib.pyplot as plt
from scipy.stats import norm
import matplotlib.mlab as mlab
import numpy as np
import xml.etree.ElementTree as ET

dame_path = "/zfs/astrohe/ckarwin/Machine_Learning_GC/Sim_2/Dame_Maps/Simulation_Output/"

index_listD = []
index_listM = []
for i in range(1,301):
    
    #get Dame values:
    this_fileD = dame_path + "sim_%s/after_alternative_fit_00.xml" %str(i)
    tree = ET.parse(this_fileD)
    root = tree.getroot()
    for source in root:
        if source.attrib["name"] == "MapSource":
            this_index = float(source[0][1].attrib['value'])
            index_listD.append(this_index)

    #get Mopra values:
    this_fileM = "sim_%s/after_alternative_fit_00.xml" %str(i)
    tree = ET.parse(this_fileM)
    root = tree.getroot()
    for source in root:
        if source.attrib["name"] == "MapSource":
            this_index = float(source[0][1].attrib['value'])
            index_listM.append(this_index)


plt.figure(figsize=(8,6))
ax = plt.gca()

#plot Dame:
max_value = max(index_listD)
min_value = min(index_listD)
n, bins, patches = plt.hist(index_listD,density=True,bins=40,range=(min_value,max_value),histtype='step',label="_nolabel_",alpha=0.5,color="cornflowerblue")

(mu,sigma) = norm.fit(index_listD)
xmin, xmax = plt.xlim()
x = np.linspace(xmin,xmax,100)
p = norm.pdf(x,mu,sigma)
plt.plot(x,p,"r--",linewidth=2,color="cornflowerblue",label="Dame+01")
print
print "Dame Maps:"
print "mean: " + str(mu)
print

#plot Mopra:
max_value = max(index_listM)
min_value = min(index_listM)
n, bins, patches = plt.hist(index_listM,density=True,bins=40,range=(min_value,max_value),histtype='step',label="_nolabel_",alpha=0.5,color="purple")

(mu,sigma) = norm.fit(index_listM)
xmin, xmax = plt.xlim()
x = np.linspace(xmin,xmax,100)
p = norm.pdf(x,mu,sigma)
plt.plot(x,p,"r--",linewidth=2,color="purple",label="Mopra")
print
print "Mopra Maps:"
print "mean: " + str(mu)
print

plt.xlim(1.5,3.5)
plt.ylim(0,5)
plt.xlabel("Spectral Index",fontsize=14)
plt.ylabel("Probability Density",fontsize=14)
plt.title("Point-like Excess Template", fontsize=14)
#plt.grid(color="grey",alpha=0.2,linewidth=4)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.legend(loc=1,frameon=False)
plt.savefig("index_hist.pdf")
plt.show()
