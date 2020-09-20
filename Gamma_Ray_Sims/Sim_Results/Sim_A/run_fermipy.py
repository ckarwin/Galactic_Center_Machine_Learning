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

gta = GTAnalysis('config.yaml',logging={'verbosity' : 3})
gta.setup()
gta.write_roi('after_setup')
#gta.load_roi("after_fit.npy")

gta.write_roi('before_sim')
gta.simulate_roi(randomize=True)
gta.write_roi('after_sim')

gta.free_sources(free=False)
gta.set_norm("galdiff00",0.9)
gta.set_norm("galdiff01",0.8)
gta.set_norm("galdiff02",1.1)
gta.set_norm("galdiff03",1.2)
gta.free_sources(free=True,pars="norm")

gta.fit()
gta.write_roi('after_fit')
gta.write_model_map("sim_model")
gta.model_counts_map()

model = {'Index' : 2.0, 'SpatialModel' : 'PointSource'}
gta.tsmap('test',model=model,write_fits=True)
#gta.residmap('fit1',model=model,make_plots=True)

model2 = {'Index' : 2.0, 'SpatialModel' : 'PointSource'}
finder2 = gta.find_sources(prefix='find2',model=model2,sqrt_ts_threshold=2.0, min_separation=0.5,max_iter=1,sources_per_iter=50,tsmap_fitter='tsmap')
gta.write_roi('/scratch1/ckarwin/ML_temp/Run_2/source_search')
