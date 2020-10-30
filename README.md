# Analysis Outline <br />
The diffuse gamma-ray emission in the Galaxy arises primarily from the interaction of high-energy cosmic rays (CR) with the interstellar gas and radiation fields.
Of particular interest in this analysis is the gas-related emission, which is due to CR protons interacting with the protons
of the gas, which genertes pions, that then quickly decays to gamma-ray photons. The gas is made up primarily of atomic hydrogen (HI), molecular hydrogen (H2), 
and so-called dark gas. The method developed in this analysis pertains to H2 in particular; however, it can be easily generalized to any of the gas components.

H2 is a symmetric molecule and therefore does not emit at a characterstic wavelength. Instead, the distribution of H2 in the Galaxy 
is typically infered from other tracers, and in particular, from the distribution of CO. The most abundant isotopologue of CO is CO12, 
and thus it is used as the primary tracer. However, there are also other rarer isotopologues, including CO13 and CO18.   

In regions of high gas density, CO12 may underestimate the colume density, due to the gas being optically thick. In such regions, CO13 and CO18 may be better tracers of the column density when they are detected, since they are more rare and thus optically thin. 

The goal of the method outlined in this repository is to construct a spatial template for the excess gamma-ray emission that result from 
underpredicted CO12 in regions of high gas density. 

## Getting the MOPRA Data <br />
Our analysis is based on the Mopra survey of CO12, CO13, and CO18, available [here](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/LH3BDN). 
The observations cover Galacic longitudes and latitudes from (degrees) 300 < l < 350 and |b|<0.5, respectively. The data is only available in 1x1 deg fields. 
<br />


## Converting the Mopra Data to Column Densities in Galactocentric Radii <br />

  - The brightness temperature of the gas is stored in a data cube, with dimensions of longitude, latitude, and gas velocity. The first step to process the
  data is to run **plot_rotation.py**, which calls **gas_strucutre_module.py**. 
  
 - The plot_rotation code defines the radial velocity of the
  gas relative to the local standard of rest, which is a funtion of Galactic longitude and Galactocentric radius. 
  The calculation is defined in terms of the Galactic rotational velocity curve from Clemons 1985, which is the GALPROP standard. 
  
  - The radial velocity is used to place the gas at Galactocentric radii, and we use 17 radial bins. 
  
  - The corresponding plot is shown below:
  
  ![Alt text](rotational_information.png)
  
  - For each longitude, a bin list is made, where each element of the list contains a lower velocity value and an upper velocity value, corresponding to the velocity range for each of the respective radial bins. This list is then based to gas_structure_module.py, which integrates over the velocity range in order to calculate either the line strength or the column density (both options are available).
  
  - Two versions of the gas structure module are provided in this repository, one for CO12 and the other for CO13. There are two main differences between the two codes, but otherwise they are the same. First, the CO12 version converts the line strength to column density using a radially dependent conversion factor. On the other hand, the CO13 code calulates the column density via the optical depth. Both methods are standard in radio astronomy. The second difference is that the CO13 code contains a function to clip the data at a specified noise level. The clipping function can also be used with the CO12 data, but its most important for CO13 since its used for making the modifed map.
  
  ## Making a Mosaic <br />
  
- In order to implement the Mopra data into GALPROP we convert the single 1x1 deg fields to a single mosaic. 
- The code for making the mosiac is given in **mosaic_cube.py**. 
- The code can also be used to change the resolution of the map. 

## Calculating the Gamma-Ray Model Maps with GALPROP <br />

- The mosaic is input to **GALPROP** in order to make the corresponding all-sky gamma-ray model maps. 
- We note that the code that is provided here has been developed for working with fits files; however, implementing new gas maps into the GALPROP code
would likely be easier if working with healpix files instead. 

## Processing the GALPROP Maps
The output maps from GALPROP need to be processed before using them in the Fermi Science Tools. To do this, these codes should be ran in order: **reproject.py**, **combine.py**, **mask.py**. 

- Reproject: Reprojects maps in Galactic coordinates.

- Combine: Combines the GALPROP maps in radial bins.

- Mask: When making the mosaic the data is not reliable in the overlap regions. This is likely due to the effect of trying to combine different backgrounds. Additionally, the pixels at the edge of the maps may not be the highest quality. This script masks the overlap region (given by the **footprint.fits**), as well as Galactic longitudes and latitudes at the edge of the mosaic. 

## Running the Gamma-Ray Simulations with Fermipy <br />

