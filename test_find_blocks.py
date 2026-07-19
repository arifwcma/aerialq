import glob
import os

os.environ.setdefault("GDAL_DRIVER_PATH", r"C:\Program Files\QGIS 3.44.3\apps\gdal\lib\gdalplugins")

from osgeo import gdal, osr

gdal.UseExceptions()

SAMPLE = r"I:\Elevation\WCMA2004\regular_surface\test_tiff_hillshade\wi646559145_hillshade.tif"
FOLDER = r"I:\Elevation\WCMA2004\regular_surface\test_tiff_hillshade"

wgs = osr.SpatialReference()
wgs.ImportFromEPSG(4326)
wgs.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)

ds = gdal.Open(SAMPLE)
gt = ds.GetGeoTransform()
cx = gt[0] + gt[1] * ds.RasterXSize / 2
cy = gt[3] + gt[5] * ds.RasterYSize / 2
srs = ds.GetSpatialRef()
srs.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)
to_wgs = osr.CoordinateTransformation(srs, wgs)
LON, LAT, _ = to_wgs.TransformPoint(cx, cy)
print(f"middle pixel: lon={LON:.7f} lat={LAT:.7f}")

files = sorted(glob.glob(os.path.join(FOLDER, "*.tif")))
total = len(files)

for i, path in enumerate(files, 1):
    print(f"[{i}/{total}] {os.path.basename(path)}", flush=True)
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
