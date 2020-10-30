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

def main(cmd_line):

    sim = cmd_line[1]
    
    indir = "/zfs/astrohe/ckarwin/Machine_Learning_GC/Sim_2/Run_2/"
    outdir = indir + "Simulation_Output/sim_%s" %sim
    
    if(os.path.isdir(outdir)==True):
        shutil.rmtree(outdir)
    os.system('mkdir %s' %outdir)
    os.chdir(outdir)

    shutil.copy2('%s/bexpmap_00.fits' %indir, 'bexpmap_00.fits')
    shutil.copy2('%s/ccube_00.fits' %indir, 'ccube_00.fits')
    shutil.copy2('%s/config.yaml' %indir, 'config.yaml')
    shutil.copy2('%s/ft1_00.fits' %indir, 'ft1_00.fits')
    shutil.copy2('%s/LAT_Final_Excess_Template.fits' %indir, 'LAT_Final_Excess_Template.fits')

    #setup analysis:
    gta = GTAnalysis('config.yaml',logging={'verbosity' : 3})
    gta.setup()
    #gta.load_roi("after_setup")

    #set components to zero for simulations:
    gta.set_norm("MapSource",0.0) #excess template
    gta.set_norm("galdiff04",0.0) #CO12_0-5
    gta.set_norm("galdiff05",0.0) #CO12_6-9
    gta.set_norm("galdiff06",0.0) #CO12_10-12
    gta.set_norm("galdiff07",0.0) #CO12_13-16

    #run simulations:
    gta.simulate_roi(randomize=True)

    #delete sources that were simulated:
    gta.delete_source("galdiff00",delete_source_map=True)
    gta.delete_source("galdiff01",delete_source_map=True)
    gta.delete_source("galdiff02",delete_source_map=True)
    gta.delete_source("galdiff03",delete_source_map=True)

    #set random normalizations of sources for performing fit:
    #n4 =  np.random.normal(1.0,0.2)
    #n5 =  np.random.normal(1.0,0.2)
    #n6 =  np.random.normal(1.0,0.2)
    #nms = np.random.normal(1e-4,0.5e-4)
    gta.set_norm("galdiff04",0.8)
    gta.set_norm("galdiff05",0.8)
    gta.set_norm("galdiff06",1.2)
    gta.set_norm("galdiff07",1.0)
    
    #perform fit for null hypothesis:
    gta.free_sources(free=True)
    gta.free_source("galdiff07",free=False)
    gta.free_source("MapSource",free=False)
    Fit = gta.fit()
    null = Fit["loglike"]

    #set normalizations of sources for performing alternative fit:
    gta.set_norm("galdiff04",0.8)
    gta.set_norm("galdiff05",0.8)
    gta.set_norm("galdiff06",1.2)
    gta.set_norm("galdiff07",1.0)#this component is held constant
    gta.set_norm("MapSource",1e-4)

    gta.free_sources(free=True)
    gta.free_source("galdiff07",free=False)
    Fit2 = gta.fit()
    alternative = Fit2["loglike"]

    #calculte TS:
    TS = -2*(null - alternative)

    #write results:
    savefile = "TS_sim_%s.txt" %sim
    f = open(savefile,"w")
    f.write(str(TS))
    f.close()
    
    #rm ft file to reduce storage:
    os.system('rm ft1_00.fits')

    return

################################################
if __name__=="__main__":
        main(sys.argv)
