from osgeo import gdal
import numpy as np

ds = gdal.Open(r"c:\Users\m.rahman\qgis\aerialq\data\test\cropped.tif")
print(f"Bands: {ds.RasterCount}, Size: {ds.RasterXSize}x{ds.RasterYSize}")

for i in range(1, ds.RasterCount + 1):
    b = ds.GetRasterBand(i)
    arr = b.ReadAsArray()
    ci_map = {0:"Undefined",1:"Gray",2:"Palette",3:"Red",4:"Green",5:"Blue",6:"Alpha"}
    print(f"Band {i}: interp={ci_map.get(b.GetColorInterpretation(),'?')} desc=[{b.GetDescription()}] "
          f"min={arr.min()} max={arr.max()} mean={arr.mean():.1f} std={arr.std():.1f}")

b1 = ds.GetRasterBand(1).ReadAsArray().astype(float)
b2 = ds.GetRasterBand(2).ReadAsArray().astype(float)
b3 = ds.GetRasterBand(3).ReadAsArray().astype(float)

print(f"\nPer-pixel: B1<B2 in {(b1<b2).mean()*100:.1f}% of pixels")
print(f"Per-pixel: B1<B3 in {(b1<b3).mean()*100:.1f}% of pixels")
print(f"Per-pixel: B2<B3 in {(b2<b3).mean()*100:.1f}% of pixels")

print(f"\nMean diff B2-B1: {(b2-b1).mean():.1f}")
print(f"Mean diff B3-B1: {(b3-b1).mean():.1f}")
print(f"Mean diff B3-B2: {(b3-b2).mean():.1f}")

ds = None
