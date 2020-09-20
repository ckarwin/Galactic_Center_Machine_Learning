# Processing the GALPROP Maps
The output maps from GALPROP need to be processed before using them in the Science Tools. The codes should be ran in the order: reproject, combine, mask. 

Reproject: Reprojects maps in Galactic coordinates and adds energy extension needed for Science Tools.

Combine: Combines the GALPROP maps in radial bins.

Mask: When making the mosaic the data is not reliable in the overlap regions. This is likely due to the effect of trying to combine different backgrounds. Additionally, the pixels at the edge of the maps may not be the highest quality. This script masks the overlap region (given by the footprint), as well as Galactic longitudes and latitudes at the edge of the mosaic. 
