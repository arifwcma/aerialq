from osgeo import gdal
import numpy as np
from itertools import permutations

ds = gdal.Open(r"c:\Users\m.rahman\qgis\aerialq\data\dimboola\dimboola_2016dec22_air_cir_10cm_mga54.ecw")

cx, cy = ds.RasterXSize // 2, ds.RasterYSize // 2
sz = 2000
x0, y0 = cx - sz, cy - sz

bands = {}
for i in range(1, 5):
    bands[i] = ds.GetRasterBand(i).ReadAsArray(x0, y0, sz * 2, sz * 2)

mem_drv = gdal.GetDriverByName("MEM")
png_drv = gdal.GetDriverByName("PNG")

for idx, (r, g, b) in enumerate(permutations([1, 2, 3])):
    fname = f"c:\\Users\\m.rahman\\qgis\\aerialq\\_combo_R{r}_G{g}_B{b}.png"
    mem = mem_drv.Create("", sz * 2, sz * 2, 3, gdal.GDT_Byte)
    mem.GetRasterBand(1).WriteArray(bands[r])
    mem.GetRasterBand(2).WriteArray(bands[g])
    mem.GetRasterBand(3).WriteArray(bands[b])
    png_drv.CreateCopy(fname, mem)
    mem = None
    print(f"Saved: _combo_R{r}_G{g}_B{b}.png")

ds = None
