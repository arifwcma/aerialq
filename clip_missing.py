import os

os.environ.setdefault("GDAL_DRIVER_PATH", r"C:\Program Files\QGIS 3.44.3\apps\gdal\lib\gdalplugins")

from osgeo import gdal

gdal.UseExceptions()

REF = r"I:\Elevation\WCMA2004\regular_surface\tiff_hillshade\wi5406009_hillshade.tif"
SRC = r"I:\Elevation\SRTM\regular_surface\tiff_hillshade\s37_e141_1arc_v3_hillshade.tif"
DST = r"C:\Users\m.rahman\src\aerialq\missing.tif"

ref = gdal.Open(REF, gdal.GA_ReadOnly)
gt = ref.GetGeoTransform()
bounds = (
    gt[0],
    gt[3] + gt[5] * ref.RasterYSize,
    gt[0] + gt[1] * ref.RasterXSize,
    gt[3],
)

gdal.Warp(
    DST,
    SRC,
    dstSRS=ref.GetProjection(),
    outputBounds=bounds,
    xRes=gt[1],
    yRes=abs(gt[5]),
    resampleAlg="bilinear",
    creationOptions=["COMPRESS=DEFLATE", "TILED=YES"],
)
print("done:", DST)
