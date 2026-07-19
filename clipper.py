import os

os.environ.setdefault("GDAL_DRIVER_PATH", r"C:\Program Files\QGIS 3.44.3\apps\gdal\lib\gdalplugins")

from osgeo import gdal

SRC = r"I:\Raster\WCMARURAL_2017\dataset_imagery\mosaic\wimmera-cma_2017feb03_20cm_mga54.ecw"
SHP = r"C:\Users\m.rahman\src\aerialq\lga\Export_Output_2.shp"
DST = r"I:\Raster\UPDATED_AERIALS\tif\clipped.tiff"

gdal.UseExceptions()
gdal.SetConfigOption("GDAL_TIFF_INTERNAL_MASK", "YES")
gdal.SetConfigOption("GDAL_CACHEMAX", "8192")
gdal.SetConfigOption("GDAL_SWATH_SIZE", "1073741824")

vrt = gdal.Warp(
    "",
    SRC,
    format="VRT",
    cutlineDSName=SHP,
    cropToCutline=True,
    multithread=True,
    warpMemoryLimit=4096,
    warpOptions=["NUM_THREADS=ALL_CPUS"],
)

gdal.Translate(
    DST,
    vrt,
    bandList=[1, 2, 3],
    maskBand=4,
    creationOptions=[
        "COMPRESS=JPEG",
        "JPEG_QUALITY=90",
        "PHOTOMETRIC=YCBCR",
        "TILED=YES",
        "BIGTIFF=YES",
        "NUM_THREADS=ALL_CPUS",
    ],
    callback=gdal.TermProgress_nocb,
)

vrt = None
print("done:", DST)
