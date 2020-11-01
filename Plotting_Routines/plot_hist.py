#imports
import matplotlib.pyplot as plt
from scipy.stats import norm
import matplotlib.mlab as mlab
import numpy as np

#path to Dame simulations:
dame_path = "/zfs/astrohe/ckarwin/Machine_Learning_GC/Sim_2/Dame_Maps/Simulation_Output/"

dame_list = []
mopra_list = []
for i in range(1,301):
    
    #get Mopra data:
    this_file = "sim_%s/TS_sim_%s.txt" %(str(i),str(i))
    f = open(this_file,'r')
    lines = f.readlines()
    mopra_list.append(float(lines[0]))

    #get Dame data:
    this_file = dame_path + "sim_%s/TS_sim_%s.txt" %(str(i),str(i))
    f = open(this_file,'r')
    lines = f.readlines()
    dame_list.append(float(lines[0]))


#setup figure:
plt.figure(figsize=(8,6))
#plt.xscale("log")

mopra_list = np.sqrt(mopra_list)
dame_list = np.sqrt(dame_list)

#plot Dame hist:
max_value = max(dame_list)
min_value = min(dame_list)
n, bins, patches = plt.hist(dame_list,density=True,bins=40,range=(min_value,max_value),histtype='step',label="_nolabel_",alpha=0.5,color="cornflowerblue")

nan_index = np.isnan(dame_list)
dame_list[nan_index]=12
zero_index = dame_list<1
print dame_list[zero_index]

(mu,sigma) = norm.fit(dame_list)
xmin, xmax = plt.xlim()
x = np.linspace(min_value,max_value,100)
p = norm.pdf(x,mu,sigma)
plt.plot(x,p,"r--",linewidth=2,color="cornflowerblue",label="Dame+01")
print
print "Dame:"
print "mean: " + str(mu)
print


#plot Mopra hist:
max_value = max(mopra_list)
min_value = min(mopra_list)
n, bins, patches = plt.hist(mopra_list,density=True,bins=40,range=(min_value,max_value),histtype='step',label="_nolabel_",alpha=0.5,color="purple")
(mu,sigma) = norm.fit(mopra_list)
xmin, xmax = plt.xlim()
x = np.linspace(xmin,xmax,100)
p = norm.pdf(x,mu,sigma)
plt.plot(x,p,"r--",linewidth=2,color="purple",label="Mopra")
print
print "Mopra:"
print "mean: " + str(mu)
print

#plt.xlim(0,15)
plt.xlabel("$\mathrm{\sqrt{TS}}$",fontsize=14)
plt.ylabel("Probability Density",fontsize=14)
plt.title("Point-like Excess Template", fontsize=14)
#plt.grid(color="grey",alpha=0.2,linewidth=4)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.legend(loc=0,frameon=False)
plt.savefig("Sim_results.pdf")
plt.show()


