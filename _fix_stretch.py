from osgeo import gdal
import numpy as np

ds = gdal.Open(r"c:\Users\m.rahman\qgis\aerialq\data\test\cropped.tif")

out_bands = []
for i in range(1, 4):
    arr = ds.GetRasterBand(i).ReadAsArray().astype(float)
    lo, hi = np.percentile(arr, [2, 98])
    stretched = np.clip((arr - lo) / (hi - lo) * 255, 0, 255).astype(np.uint8)
    out_bands.append(stretched)

drv = gdal.GetDriverByName("GTiff")
out = drv.Create(
    r"c:\Users\m.rahman\qgis\aerialq\data\test\cropped_fixed.tif",
    ds.RasterXSize, ds.RasterYSize, 3, gdal.GDT_Byte
)
out.SetGeoTransform(ds.GetGeoTransform())
out.SetProjection(ds.GetProjection())
for i in range(3):
    out.GetRasterBand(i + 1).WriteArray(out_bands[i])
out.FlushCache()
out = None
ds = None
print("Done: cropped_fixed.tif")
