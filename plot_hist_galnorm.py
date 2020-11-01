#imports
import matplotlib.pyplot as plt
from scipy.stats import norm
import matplotlib.mlab as mlab
import numpy as np
import xml.etree.ElementTree as ET

dame_path = "/zfs/astrohe/ckarwin/Machine_Learning_GC/Sim_2/Dame_Maps/Simulation_Output/"
dame_file = dame_path + "sim_%s/after_alternative_fit_00.xml"
mopra_file = "sim_%s/after_alternative_fit_00.xml"

#setup figure:
plt.figure(figsize=(8,6))
ax = plt.gca()

Dame = {"file":dame_file,"color":"cornflowerblue","label":"(Dame+01)"}
Mopra = {"file":mopra_file,"color":"purple","label":"(Mopra)"}

plot_list = [Dame,Mopra]

for each in plot_list:

    this_color = each["color"]
    this_label = each["label"]
    this_style = ["-","--","-.",":"]

    for j in range(4,8):
        
        this_label = "A%s" %str(j-3) + " " + each["label"]
        galnorm_list = []
        
        for i in range(1,301):
        
            #read xml:
            this_file = each["file"] %str(i)
            tree = ET.parse(this_file)
            root = tree.getroot()

            for source in root:
                if source.attrib["name"] == "galdiff0%s" %str(j) :
                    this_norm = float(source[0][0].attrib['value'])
                    galnorm_list.append(this_norm)

        #plot:
        max_value = max(galnorm_list)
        min_value = min(galnorm_list)
        n, bins, patches = plt.hist(galnorm_list,density=True,bins=40,range=(min_value,max_value),histtype='step',label="_nolabel_",alpha=0.5,color=this_color)
        (mu,sigma) = norm.fit(galnorm_list)
        x = np.linspace(min_value,max_value,100)
        p = norm.pdf(x,mu,sigma)
        plt.plot(x,p,ls=this_style[j-4],linewidth=2,color=this_color,label=this_label)
        print
        print this_label
        print "mean: " + str(mu)
        print

plt.xlim(0.75,2.0)
#plt.ylim(0,15)
plt.xlabel("Galactic Diffuse Normalization",fontsize=14)
plt.ylabel("Probability Density",fontsize=14)
plt.yticks(fontsize=12)
plt.legend(loc=0,frameon=False)
plt.savefig("galnorm_hist.pdf")
plt.show()
