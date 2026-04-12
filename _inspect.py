from osgeo import gdal

ds = gdal.Open(r"I:\Raster\UPDATED_AERIALS\Towns\serviceton_2016dec22_air_nir_10cm_mga54.tif")
print(f"Bands: {ds.RasterCount}, Size: {ds.RasterXSize}x{ds.RasterYSize}")

ci_map = {0:"Undefined",1:"Gray",2:"Palette",3:"Red",4:"Green",5:"Blue",6:"Alpha"}
for i in range(1, ds.RasterCount + 1):
    b = ds.GetRasterBand(i)
    stats = b.ComputeStatistics(True)
    print(f"Band {i}: interp={ci_map.get(b.GetColorInterpretation(),'?')} desc=[{b.GetDescription()}] min={stats[0]:.0f} max={stats[1]:.0f} mean={stats[2]:.1f}")

ds = None
