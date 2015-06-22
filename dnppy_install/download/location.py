__author__ = 'jwely'


class location():
    """
    Location class who's methods allow translating a shapefile
    into sets of "tiles" that represent the same location in
    the system of landsat path/row, modis hv tiles, and
    single lat/lon transects used by ASTER.

    the intent of this class is to be combined with time
    data to make assembling arguments for "fetch" functions
    easy. The end goal is to enable a single line statement
    to input a shapefile representing the area under study,
    the date range of interest, and one or more key product
    strings of data products for download. Each of these files
    would then be automatically downloaded and extracted into
    an arcmap friendly format.
    """

    def __init__(self):
        pass

    def modis_tile(self):
        """
        method could be found here
        http://landweb.nascom.nasa.gov/developers/tilemap/note.html
        """
        pass

    def WRS2_tile(self):
        """ no method, but validation source.
        [https://landsat.usgs.gov/tools_latlong.php
        """

        pass

    def lat_lon_tile(self):
        """
        this function should be simple arithmetic
        """
        pass

