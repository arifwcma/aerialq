from osgeo import gdal
import numpy as np
import time

t0 = time.time()

src = r"C:\Users\m.rahman\qgis\aerialq\data\dimboola\dimboola_2016dec22_air_cir_10cm_mga54.ecw"
dst = r"C:\Users\m.rahman\qgis\aerialq\data\dimboola\dimboola_2016dec22_air_natural_10cm_mga54.tif"

ds = gdal.Open(src)
w, h = ds.RasterXSize, ds.RasterYSize

drv = gdal.GetDriverByName("GTiff")
out = drv.Create(dst, w, h, 3, gdal.GDT_Byte, ["COMPRESS=LZW", "TILED=YES", "BIGTIFF=YES"])
out.SetGeoTransform(ds.GetGeoTransform())
out.SetProjection(ds.GetProjection())

chunk = 1000
for y in range(0, h, chunk):
    rows = min(chunk, h - y)
    nir = ds.GetRasterBand(1).ReadAsArray(0, y, w, rows).astype(np.float32)
    red = ds.GetRasterBand(2).ReadAsArray(0, y, w, rows).astype(np.float32)
    grn = ds.GetRasterBand(3).ReadAsArray(0, y, w, rows).astype(np.float32)

    out.GetRasterBand(1).WriteArray(np.clip(0.1 * nir + 0.9 * red, 0, 255).astype(np.uint8), 0, y)
    out.GetRasterBand(2).WriteArray(np.clip(0.3 * nir + 0.7 * grn, 0, 255).astype(np.uint8), 0, y)
    out.GetRasterBand(3).WriteArray(np.clip(0.1 * nir + 0.1 * red + 0.8 * grn, 0, 255).astype(np.uint8), 0, y)

    print(f"\r{y + rows}/{h} rows", end="", flush=True)

out.FlushCache()
out = None
ds = None

elapsed = time.time() - t0
print(f"\nDone in {elapsed:.1f}s → {dst}")
