import glob
import os

os.environ.setdefault("GDAL_DRIVER_PATH", r"C:\Program Files\QGIS 3.44.3\apps\gdal\lib\gdalplugins")

from osgeo import gdal, osr

gdal.UseExceptions()

LON, LAT = 141.4610595, -36.0478845
ROOT = r"I:\Elevation"

wgs = osr.SpatialReference()
wgs.ImportFromEPSG(4326)
wgs.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)

files = [
    p
    for p in glob.glob(os.path.join(ROOT, "**", "*.tif"), recursive=True)
    if "hillshade" in os.path.basename(p).lower()
]
total = len(files)

for i, path in enumerate(files, 1):
    if i % 200 == 0 or i == total:
        print(f"[{i}/{total}]", flush=True)
    try:
        ds = gdal.Open(path)
        srs = ds.GetSpatialRef()
        srs.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)
        tx = osr.CoordinateTransformation(wgs, srs)
        x, y, _ = tx.TransformPoint(LON, LAT)
        gt = ds.GetGeoTransform()
        px = (x - gt[0]) / gt[1]
        py = (y - gt[3]) / gt[5]
        if 0 <= px < ds.RasterXSize and 0 <= py < ds.RasterYSize:
            col, row = int(px), int(py)
            band = ds.GetRasterBand(1)
            valid = band.GetMaskBand().ReadAsArray(col, row, 1, 1)[0][0] != 0
            if valid:
                print("  MATCH:", os.path.abspath(path), flush=True)
    except Exception as e:
        print("  SKIPPED:", path, "-", e, flush=True)
