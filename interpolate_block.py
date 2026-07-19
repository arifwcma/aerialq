import os

os.environ.setdefault("GDAL_DRIVER_PATH", r"C:\Program Files\QGIS 3.44.3\apps\gdal\lib\gdalplugins")

import numpy as np
from osgeo import gdal

gdal.UseExceptions()

TOP = r"I:\Elevation\WCMA2004\regular_surface\tiff_hillshade\wi5406006_hillshade.tif"
BOTTOM = r"I:\Elevation\WCMA2004\regular_surface\tiff_hillshade\wi5406012_hillshade.tif"
DST = r"C:\Users\m.rahman\src\aerialq\wi5406009_hillshade.tif"

ds_a = gdal.Open(TOP, gdal.GA_ReadOnly)
ds_b = gdal.Open(BOTTOM, gdal.GA_ReadOnly)

gt_a = ds_a.GetGeoTransform()
gt_b = ds_b.GetGeoTransform()

if gt_a[3] < gt_b[3]:
    ds_a, ds_b = ds_b, ds_a
    gt_a, gt_b = gt_b, gt_a

top_bottom_y = gt_a[3] + gt_a[5] * ds_a.RasterYSize
bottom_top_y = gt_b[3]

width = ds_a.RasterXSize
height = round((top_bottom_y - bottom_top_y) / -gt_a[5])

edge_top = ds_a.GetRasterBand(1).ReadAsArray(0, ds_a.RasterYSize - 1, width, 1).astype(np.float64)
edge_bottom = ds_b.GetRasterBand(1).ReadAsArray(0, 0, width, 1).astype(np.float64)

w = ((np.arange(height) + 0.5) / height).reshape(-1, 1)
data = (1 - w) * edge_top + w * edge_bottom
data = data.astype(ds_a.GetRasterBand(1).ReadAsArray(0, 0, 1, 1).dtype)

driver = gdal.GetDriverByName("GTiff")
out = driver.Create(DST, width, height, 1, ds_a.GetRasterBand(1).DataType, options=["COMPRESS=DEFLATE", "TILED=YES"])
out.SetGeoTransform((gt_a[0], gt_a[1], 0, top_bottom_y, 0, gt_a[5]))
out.SetProjection(ds_a.GetProjection())

nodata = ds_a.GetRasterBand(1).GetNoDataValue()
if nodata is not None:
    out.GetRasterBand(1).SetNoDataValue(nodata)

out.GetRasterBand(1).WriteArray(data)
out = None
print("done:", DST)
