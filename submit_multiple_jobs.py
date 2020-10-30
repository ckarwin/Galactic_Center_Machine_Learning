import pandas as pd
import os, sys
import time 


for i in range(3,101):

        f = open('multiple_batch_submission.pbs','w')

	f.write("#PBS -N simrun_%s\n" %str(i))
	f.write("#PBS -l select=1:ncpus=1:mem=12gb,walltime=72:00:00\n\n")
	f.write("#the Fermi environment first needs to be sourced:\n")
	f.write("cd /zfs/astrohe/Software\n")
	f.write("source fermi.sh\n\n")
	f.write("#change to working directory and run job\n")
	f.write("cd /zfs/astrohe/ckarwin/Machine_Learning_GC/Sim_2/Run_2\n")
	f.write("python run_fermipy_full_sims.py %s" %str(i))
	f.close()
	
	os.system("qsub multiple_batch_submission.pbs")
	time.sleep(10)
