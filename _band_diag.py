from osgeo import gdal
import numpy as np

ds = gdal.Open(r"c:\Users\m.rahman\qgis\aerialq\data\dimboola\dimboola_2016dec22_air_cir_10cm_mga54.ecw")

gt = ds.GetGeoTransform()
print(f"Origin: ({gt[0]}, {gt[3]})")
print(f"Pixel size: ({gt[1]}, {gt[5]})")
print(f"Size: {ds.RasterXSize} x {ds.RasterYSize}")

def sample(x_geo, y_geo, label):
    col = int((x_geo - gt[0]) / gt[1])
    row = int((y_geo - gt[3]) / gt[5])
    vals = [ds.GetRasterBand(i).ReadAsArray(col, row, 1, 1)[0][0] for i in range(1, 4)]
    print(f"{label:20s} → B1={vals[0]:3d}  B2={vals[1]:3d}  B3={vals[2]:3d}")

print("\n--- Sampling known features ---")
print("(Coords in MGA54)\n")

sample(591900, 5966300, "River water")
sample(591700, 5966400, "Riverside trees")
sample(591300, 5966200, "Oval/sports field")
sample(592100, 5966600, "Road intersection")
sample(592500, 5966800, "Building roof")

print("\n--- Band correlation analysis (random 5000 pixels) ---\n")
np.random.seed(42)
n = 5000
cols = np.random.randint(100, ds.RasterXSize - 100, n)
rows = np.random.randint(100, ds.RasterYSize - 100, n)

bands = []
for b in range(1, 4):
    band = ds.GetRasterBand(b)
    vals = np.array([band.ReadAsArray(int(c), int(r), 1, 1)[0][0] for c, r in zip(cols, rows)], dtype=float)
    bands.append(vals)

for i in range(3):
    print(f"Band {i+1}: mean={bands[i].mean():.1f}  std={bands[i].std():.1f}  median={np.median(bands[i]):.0f}")

print()
corr = np.corrcoef(bands)
print(f"Corr(B1,B2)={corr[0,1]:.3f}  Corr(B1,B3)={corr[0,2]:.3f}  Corr(B2,B3)={corr[1,2]:.3f}")

print("\n--- Spectral reasoning ---")
print("NIR band: highest std (veg vs non-veg contrast), lowest corr with visible bands")
print("Red band: low values on vegetation, moderate on urban")
print("Green band: moderate values everywhere, high corr with Red")

veg = bands[0][0:100]
ds = None
