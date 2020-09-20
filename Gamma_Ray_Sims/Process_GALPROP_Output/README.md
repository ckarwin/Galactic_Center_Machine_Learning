# Stacking_Analysis
This repository contains all the code to run a gamma-ray stacking analysis with Fermi-LAT data. This stacking technique was originally developed by Marco Ajello, Vaidehi Paliya, and Abhishek Desai, and it has been succesfully applied to the study of extreme blazars [(link)](https://arxiv.org/pdf/1908.02496.pdf), star-forming galaxies [(link)](https://arxiv.org/pdf/2003.05493.pdf), the extragalaxtic background light [(link)](https://arxiv.org/pdf/1812.01031.pdf), and ultra-fast outflows (UFOs). In this repository the code is applied to the analysis of UFOs, but it can be easily generalized to study any gamma-ray source population.

The stacking analysis requires Fermipy, available [here](https://fermipy.readthedocs.io/en/latest/). 

The stacking analysis is also meant to be ran on a cluster. In particular, the UFO analysis has been developed using the Clemson University Palmetto Cluster. More information on the Palmetto Cluster can be found [here](https://www.palmetto.clemson.edu/palmetto/userguide_basic_usage.html). 

## Methodology 
The main assumption made with the stacking technique is that the source population can be characterized by average quantities, such as average flux and spectral index. Of course other parameters can also be stacked. 2D TS profiles are then constructed for each source using a binned likelihood analysis, and the individual profiles are summed to obtain the global significance of the signal. See the papers given above for more details.  

## Getting Started
The UFO directory contains all of the required code. Note that the paths will of course need to be updated accordingly, as for simplicity they have been left with the paths that were used in the original analysis.
