# local imports

from dnppy import raster

import os

# arcpy imports
import arcpy
if arcpy.CheckExtension('Spatial')=='Available':
    arcpy.CheckOutExtension('Spatial')
    arcpy.env.overwriteOutput = True


def mosaic(filelist, outdir = None, pixel_type = "32_BIT_FLOAT",
                 bands = "1", m_method = "LAST", m_colormap = "FIRST"):

    """
    Automatically identify appropriate files and mosaic them.

     This script will find and mosaic all MODIS tiles groups with different time names in a
     directory. It will automatically identify the date ranges in the MODIS filenames and
     iterate through the entire range while skipping dates for which there are not at least
     two tiles. Users should be mindful of file suffixes from previous processing.

     This script centers around the 'arcpy.MosaicToNewRaster_management' tool
     [http://help.arcgis.com/en/arcgisdesktop/10.0/help/index.html#//001700000098000000]

     Inputs:
       filelist        the directory containing MODIS data or a list of modis files.
       pixel_type      exactly as the input for the MosaicToNewRaster_management tool.
                       defaults to "32_BIT_FLOAT"
       bands           exactly as the input for the MosaicToNewRaster_management tool.
                       defaults to 1
       m_method        exactly as the input for the MosaicToNewRaster_management tool.
                       defaults to "LAST"
       m_colormap      exactly as the input for the MosaicToNewRaster_management tool.
                       defaults to "FIRST"
       outdir          the directory to save output files to. If none is specified, a
                       default directory will be created as '[indir]_Mosaicked'

     Outputs:
       failed          mosaic opperations which failed due to one or more missing tiles

     Example usage:

           import ND
           indir=      r'C:\Users\jwely\Desktop\Shortcuts\Testbed\Test tiles\MODIS LST\2013\day'
           pixel_type= "16_BIT_UNSIGNED"
           bands=      "1"
           m_method=   "LAST"
           m_colormap= "FIRST"

           ND.mosaic_modis(indir, pixel_type, bands, m_method, m_colormap, 'day')
    """

    # typically unchanged parameters of raster dataset. Change at will.
    coordinatesys   = "#"
    cellsize        = "#"

    # Set up initial arcpy modules, workspace, and parameters, and sanitize inputs.
    if outdir is not None:
        OUT = outdir

    filelist = raster.enf_rastlist(filelist)

    # initialize empty lists for tracking
    mosaiclist  = []
    yearlist    = []
    daylist     = []
    productlist = []
    tilelist    = []
    suffixlist  = []
    failed      = []

    # grab info from all the files left in the filelist.
    for item in filelist:
        info = raster.grab_info(item, 'MODIS', 365)
        yearlist.append(int(info.year))
        daylist.append(int(info.j_day))

        # find all tiles present
        if info.tile not in tilelist:
            tilelist.append(info.tile)
            
        # find all MODIS products present
        if info.product not in productlist:
            productlist.append(info.product)

        # find all suffixes present
        if info.suffix not in suffixlist:
            suffixlist.append(info.suffix)
            
    # define the range of years and days to look for
    years = range(min(yearlist), max(yearlist)+1)
    days  = range(min(daylist), max(daylist)+1)

    # print some status updates to the screen
    print("=== modis.mosaic summary ===")
    print("Found tiles : {0}".format(tilelist))
    print("Found tiles from years: {0}".format(years))
    print("Found tiles from days:  {0}".format(days))
    print("Found tiles from product: {0}".format(productlist))
    print("Found tiles with suffixes: {0}".format(suffixlist))

    # now that we know what to look for, lets go back through and mosaic everything
    for suffix in suffixlist:
        for product in productlist:
            for year in years:
                for day in days:

                    # build the search criteria
                    search = [(product +'.A'+ str(year)+str(day).zfill(3))]
                    
                    # find files meeting the criteria and sanitize list of metadata files
                    for filename in filelist:
                        if all(x in filename for x in ['.tif'] + search + [suffix]):
                            if not any(x in filename for x in ['.aux','.xml','.ovr','mosaic']):
                                mosaiclist.append(filename)

                    # only continue with the mosaic if more than one file was found!
                    if len(mosaiclist)>1:
                    
                        # if user did not specify an outdir, make folder next to first mosaic file
                        if not outdir:
                            head, tail  = os.path.split(mosaiclist[0])
                            OUT         = os.path.join(head, 'Mosaic')

                        # make the output directory if it doesnt exist already    
                        if not os.path.isdir(OUT):
                            os.makedirs(OUT)

                        # grab suffix from input files for better naming of output files
                        info = raster.grab_info(mosaiclist[0],False,True)
                        
                        # define the output name based on input criteria
                        path, filename   = os.path.split(mosaiclist[0])
                        outname         = filename.replace(info.tile,'mosaic')
                        
                        # perform the mosaic!
                        try:
                            arcpy.MosaicToNewRaster_management(mosaiclist, OUT,
                                outname, coordinatesys, pixel_type, cellsize, bands,
                                m_method, m_colormap)
                            
                            # make sure the mosaic list is empty!
                            print("mosaiced " + outname)
                            
                        except:
                            print("Failed to mosaic files! " + outname)
                            failed = failed + mosaiclist
                            
                    # do not attempt a mosaic if only one tile on given day exists!    
                    elif len(mosaiclist)==1:
                        print("More than one file is required for mosaicing!: "+ str(search))
                        failed = failed + mosaiclist

                    # delete the list of search parameters for this mosaic operation
                    del search[:]
                    del mosaiclist[:]

                    
    print("Finished mosaicing all tiles! \n")
    return failed


# testing area
if __name__ == "__main__":

    tifdir = r"C:\Users\jwely\Desktop\troubleshooting\test\MOD10A1\frac_snow\FracSnowCover"
    mosaic(tifdir, pixel_type = "8_BIT_UNSIGNED")