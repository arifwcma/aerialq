import glob
import os

os.environ.setdefault("GDAL_DRIVER_PATH", r"C:\Program Files\QGIS 3.44.3\apps\gdal\lib\gdalplugins")

from osgeo import gdal, osr

gdal.UseExceptions()

LON, LAT = 142.2626683, -36.1022719
FOLDERS = [
    r"I:\Elevation\WCMA2004\regular_surface\tiff_hillshade",
    r"I:\Elevation\WMPP2006_DEM\regular_surface\hillshade",
]

wgs = osr.SpatialReference()
wgs.ImportFromEPSG(4326)
wgs.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)

for folder in FOLDERS:
    files = sorted(glob.glob(os.path.join(folder, "*.tif")))
    print(f"\n### {folder}  ({len(files)} tifs)")
    best = None
    inside = 0
    for path in files:
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
                inside += 1
                print("  INSIDE:", os.path.basename(path), f"px={px:.1f} py={py:.1f}")
            cx = px - ds.RasterXSize / 2
            cy = py - ds.RasterYSize / 2
            d = cx * cx + cy * cy
            if best is None or d < best[0]:
                best = (d, os.path.basename(path), px, py, ds.RasterXSize, ds.RasterYSize)
        except Exception as e:
            print("  SKIP", os.path.basename(path), e)
    print(f"  inside_count={inside}")
    if best:
        print(f"  nearest={best[1]} px={best[2]:.1f} py={best[3]:.1f} size={best[4]}x{best[5]}")
