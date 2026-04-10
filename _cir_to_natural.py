from osgeo import gdal
import numpy as np

ds = gdal.Open(r"C:\Users\m.rahman\qgis\aerialq\data\dimboola\dimboola_2016dec22_air_cir_10cm_mga54.ecw")
nir = ds.GetRasterBand(1).ReadAsArray().astype(float)
red = ds.GetRasterBand(2).ReadAsArray().astype(float)
grn = ds.GetRasterBand(3).ReadAsArray().astype(float)

out_r = np.clip(0.1 * nir + 0.9 * red, 0, 255).astype(np.uint8)
out_g = np.clip(0.3 * nir + 0.0 * red + 0.7 * grn, 0, 255).astype(np.uint8)
out_b = np.clip(0.1 * nir + 0.1 * red + 0.8 * grn, 0, 255).astype(np.uint8)

drv = gdal.GetDriverByName("GTiff")
out = drv.Create(
    r"c:\Users\m.rahman\qgis\aerialq\data\test\cropped_natural.tif",
    ds.RasterXSize, ds.RasterYSize, 3, gdal.GDT_Byte
)
out.SetGeoTransform(ds.GetGeoTransform())
out.SetProjection(ds.GetProjection())
out.GetRasterBand(1).WriteArray(out_r)
out.GetRasterBand(2).WriteArray(out_g)
out.GetRasterBand(3).WriteArray(out_b)
out.FlushCache()
out = None
ds = None
print("Done: cropped_natural.tif")
