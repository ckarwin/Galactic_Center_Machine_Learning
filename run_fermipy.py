#imports
from time import sleep
from random import randint
import resource
import random,shutil,yaml
import os,sys
from math import *
import numpy as np
import matplotlib as matplotlib
matplotlib.use('agg')
from fermipy.gtanalysis import GTAnalysis
import pyLikelihood
from BinnedAnalysis import *
import pandas as pd

def CalcFlux(Fit,name):

    flux_list = []
    energy_mid_list = []

    energy_list = Fit.energies.tolist()
    for E in range(0,len(energy_list)-1):

        E_low = energy_list[E]
        E_high = energy_list[E+1]
        energy_mid = (E_low + E_high) / 2.0
        flux =  Fit.flux(name,E_low,E_high,energyFlux=True) #MeV/cm^2/s
        flux_list.append(flux)
        energy_mid_list.append(energy_mid)

    print flux_list
    print energy_list

    return energy_mid_list,flux_list

#setup analysis:
gta = GTAnalysis('config.yaml',logging={'verbosity' : 3})
gta.setup()
gta.write_roi('after_setup')
#gta.load_roi("after_sim")

#set components to zero for simulations:
gta.set_norm("MapSource",0.0) #excess template
#gta.set_norm("galdiff00",0.0) #modified_0-5
#gta.set_norm("galdiff01",0.0) #modified_6-9
#gta.set_norm("galdiff02",0.0) #modified_10-12
#gta.set_norm("galdiff03",0.0) #modified_13-16
gta.set_norm("galdiff04",0.0) #CO12_0-5
gta.set_norm("galdiff05",0.0) #CO12_6-9
gta.set_norm("galdiff06",0.0) #CO12_10-12
gta.set_norm("galdiff07",0.0) #CO12_13-16

#run simulations:
gta.write_roi('before_sim')
gta.simulate_roi(randomize=True)
gta.write_roi('after_sim')

#delete sources that were simulated:
gta.delete_source("galdiff00",delete_source_map=True)
gta.delete_source("galdiff01",delete_source_map=True)
gta.delete_source("galdiff02",delete_source_map=True)
gta.delete_source("galdiff03",delete_source_map=True)
#gta.delete_source("galdiff04",delete_source_map=True)
#gta.delete_source("galdiff05",delete_source_map=True)
#gta.delete_source("galdiff06",delete_source_map=True)
#gta.delete_source("galdiff07",delete_source_map=True)
#gta.delete_source("MapSource",delete_source_map=True)

#set normalizations of sources for performing fit:
gta.set_norm("galdiff04",0.8)
gta.set_norm("galdiff05",0.8)
gta.set_norm("galdiff06",1.2)
gta.set_norm("galdiff07",1.0)
gta.set_norm("MapSource",1e-4)

#perform fit:
#gta.load_roi("after_sim")
gta.free_sources(free=True)
gta.free_source("galdiff07",free=False)
gta.write_roi('before_fit')
#gta.free_sources(free=True,pars="norm")
#gta.free_source(name="galdiff05",free=False)
Fit = gta.fit()
gta.write_roi('after_fit')

print
print "**********"
print "logL"
print Fit["loglike"]
print

#calculate model map:
gta.write_model_map("MapSource",name="MapSource")

#calculate source spectrum:
ltcube = '/zfs/astrohe/ckarwin/Stacking_Analysis/UFOs/NGC_4151_Analysis/MakeLTCube/zmax_105/UFOs_binned_ltcube.fits'
obs = BinnedObs(srcMaps='srcmap_00.fits',expCube=ltcube,binnedExpMap='bexpmap_00.fits',irfs='P8R3_SOURCE_V2')
like = BinnedAnalysis(obs,'after_fit_00.xml',optimizer='MINUIT')
Elist,Flist = CalcFlux(like,'MapSource')
data = {"energ[MeV]":Elist,"flux[MeV/cm^2/s]":Flist}
df = pd.DataFrame(data=data)
df.to_csv("excess_flux.dat",sep="\t",index=False)

#gta.model_counts_map()

#calculate ts map:
#model = {'Index' : 2.0, 'SpatialModel' : 'PointSource'}
#gta.tsmap('test',model=model,write_fits=True)
#gta.residmap('fit1',model=model,make_plots=True)

#find new sources:
#model2 = {'Index' : 2.0, 'SpatialModel' : 'PointSource'}
#finder2 = gta.find_sources(prefix='find2',model=model2,sqrt_ts_threshold=2.0, min_separation=0.5,max_iter=1,sources_per_iter=50,tsmap_fitter='tsmap')
#gta.write_roi('/scratch1/ckarwin/ML_temp/Run_2/source_search')
