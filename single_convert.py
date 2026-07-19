import os
import time

os.environ.setdefault("GDAL_DRIVER_PATH", r"C:\Program Files\QGIS 3.44.3\apps\gdal\lib\gdalplugins")

from osgeo import gdal

gdal.UseExceptions()
gdal.SetConfigOption("GDAL_TIFF_INTERNAL_MASK", "YES")
gdal.SetConfigOption("GDAL_CACHEMAX", "8192")
gdal.SetConfigOption("GDAL_SWATH_SIZE", "1073741824")
gdal.SetConfigOption("GDAL_NUM_THREADS", "ALL_CPUS")
gdal.SetConfigOption("COMPRESS_OVERVIEW", "JPEG")
gdal.SetConfigOption("PHOTOMETRIC_OVERVIEW", "YCBCR")

SRC = r"I:\Raster\WCMARURAL_2017\dataset_imagery\mosaic\wimmera-cma_2017feb03_20cm_mga54.ecw"
DST = r"I:\Raster\UPDATED_AERIALS\tif\Rural\wimmera-cma_2017feb03_20cm_mga54.tif"

t0 = time.time()
print("Translating ...", flush=True)
gdal.Translate(
    DST,
    SRC,
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
print(f"Translate done in {(time.time() - t0) / 3600:.2f} h", flush=True)

t1 = time.time()
print("Building overviews ...", flush=True)
ds = gdal.Open(DST, gdal.GA_Update)
ds.BuildOverviews("AVERAGE", [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096], callback=gdal.TermProgress_nocb)
ds = None
print(f"Overviews done in {(time.time() - t1) / 3600:.2f} h", flush=True)
print(f"Total {(time.time() - t0) / 3600:.2f} h")
