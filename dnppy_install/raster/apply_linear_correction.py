

from enf_rastlist import *
from from_numpy import *
from to_numpy import *
from dnppy import core
import os

__all_ = ["apply_linear_correction"]

def apply_linear_correction(rasterlist, factor, offset, suffix = 'lc',
                            outdir = None, floor = -999999):
    """
    Applies a linear correction to a raster dataset.
    
     New offset rasters are saved in the output directory with a suffix of "lc"
     unless one is specified. This may be used to apply any kind of linear relationship
     that can be described with "mx + b" such as conversion between between K,C, and F.
     Also useful when ground truthing satellite data and discovering linear errors.
     All outputs are 32 bit floating point values.

     Inputs:
       rastelrist      list of rasters, a single raster, or a directory full of tiffs to
                       Have a linear correction applied to them.
       factor          every pixel in the raster will be MULTIPLIED by this value. 
       offset          this offset value will be ADDED to every pixel in the raster.
       suffix          output files will take the same name as input files with this string
                       appended to the end. So input "FILE.tif" outputs "FILE_suffix.tif"
       outdir          directory to save output rasters. "None" will save output images
                       in the same folder as the input images.
       floor           Used to manage NoData. All values less than floor are set to floor
                       then floor is set to the new NoData value. defaults to -999,999


     Returns:
       outputpath       filepath to output files created by this function
       
     Example Usage:
           to convert from MODIS Land surface temperature from digital number to kelvin, you
           must simply multiply by 0.02 as the stated scale factor listed at the link below
           [https://lpdaac.usgs.gov/products/modis_products_table/myd11a1].

           Now that it is in kelvin, converting to Celsius can be done by adding (-273.15)
           So, use this function with
               factor = 0.02
               offset = -273.15
           and one may convert MODIS land surface temperature digital numbers directly to
           celsius!
     """

    output_filelist = []

    if outdir is not None and not os.path.isdir(outdir):
        os.makedirs(outdir)
    rasterlist = enf_rastlist(rasterlist)

    for raster in rasterlist:
        print("applying a linear correction to " + raster)
        image, metadata = to_numpy(raster, "float32")
        new_NoData = floor
        
        output = image * factor + offset
        low_value_indices = output < new_NoData
        output[low_value_indices] = new_NoData

        outname = core.create_outname(outdir,raster,suffix)
        from_numpy(output, metadata, outname, new_NoData)
        output_filelist.append(outname)

    print "Finished! \n "      
    return output_filelist
