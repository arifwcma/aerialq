import glob
import os

os.environ.setdefault("GDAL_DRIVER_PATH", r"C:\Program Files\QGIS 3.44.3\apps\gdal\lib\gdalplugins")

from osgeo import gdal, osr

gdal.UseExceptions()

#LON, LAT = 141.4571796, -36.0478994
#LON, LAT = 142.2612340, -36.0124498
LON, LAT = 142.2626683, -36.1022719

FOLDER = r"I:\Elevation\WMPP2006_DEM\regular_surface\hillshade"

wgs = osr.SpatialReference()
wgs.ImportFromEPSG(4326)
wgs.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)

files = sorted(glob.glob(os.path.join(FOLDER, "*.tif")))
total = len(files)

for i, path in enumerate(files, 1):
    #print(f"[{i}/{total}] {os.path.basename(path)}", flush=True)
    ds = gdal.Open(path)
    srs = ds.GetSpatialRef()
    srs.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)
    tx = osr.CoordinateTransformation(wgs, srs)
    x, y, _ = tx.TransformPoint(LON, LAT)
    gt = ds.GetGeoTransform()
    px = (x - gt[0]) / gt[1]
    py = (y - gt[3]) / gt[5]
    if 0 <= px < ds.RasterXSize and 0 <= py < ds.RasterYSize:
        print("  MATCH:", path, flush=True)
