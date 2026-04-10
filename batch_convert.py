from osgeo import gdal
import numpy as np
import os
import time
from pathlib import Path
from datetime import datetime

TEST = False
CIR = False

DIRS_FILE = r"C:\Users\m.rahman\qgis\aerialq\dirs.txt"
OUT_ROOT = r"I:\Raster\UPDATED_AERIALS"
CHUNK = 1000


def parse_dirs(path):
    entries = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or ":" not in line:
                continue
            label, src = line.split(":", 1)
            entries.append((label.strip(), src.strip()))
    return entries


def find_ecws(directory):
    ecws = []
    for root, _, files in os.walk(directory):
        for f in files:
            if f.lower().endswith(".ecw"):
                ecws.append(os.path.join(root, f))
    return sorted(ecws)


def safe_name(out_dir, stem):
    tif = os.path.join(out_dir, f"{stem}.tif")
    if not os.path.exists(tif):
        return tif
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    return os.path.join(out_dir, f"{stem}_{ts}.tif")


def convert(src_path, dst_path, test, cir):
    if test:
        Path(dst_path).touch()
        return

    ds = gdal.Open(src_path)
    if ds is None:
        print(f"  SKIP (cannot open)")
        return
    w, h = ds.RasterXSize, ds.RasterYSize
    bands = ds.RasterCount
    out_bands = 3 if bands >= 3 else bands

    drv = gdal.GetDriverByName("GTiff")
    out = drv.Create(dst_path, w, h, out_bands, gdal.GDT_Byte, ["COMPRESS=LZW", "TILED=YES", "BIGTIFF=YES"])
    out.SetGeoTransform(ds.GetGeoTransform())
    out.SetProjection(ds.GetProjection())

    for y in range(0, h, CHUNK):
        rows = min(CHUNK, h - y)

        if cir and bands >= 3:
            nir = ds.GetRasterBand(1).ReadAsArray(0, y, w, rows).astype(np.float32)
            red = ds.GetRasterBand(2).ReadAsArray(0, y, w, rows).astype(np.float32)
            grn = ds.GetRasterBand(3).ReadAsArray(0, y, w, rows).astype(np.float32)
            out.GetRasterBand(1).WriteArray(np.clip(0.1 * nir + 0.9 * red, 0, 255).astype(np.uint8), 0, y)
            out.GetRasterBand(2).WriteArray(np.clip(0.3 * nir + 0.7 * grn, 0, 255).astype(np.uint8), 0, y)
            out.GetRasterBand(3).WriteArray(np.clip(0.1 * nir + 0.1 * red + 0.8 * grn, 0, 255).astype(np.uint8), 0, y)
        else:
            for b in range(1, out_bands + 1):
                data = ds.GetRasterBand(b).ReadAsArray(0, y, w, rows)
                out.GetRasterBand(b).WriteArray(data, 0, y)

        print(f"\r  {y + rows}/{h} rows", end="", flush=True)

    print()
    out.FlushCache()
    out = None
    ds = None


def main():
    t0 = time.time()
    entries = parse_dirs(DIRS_FILE)
    total_files = 0
    mode = "TEST" if TEST else ("CIR→Natural" if CIR else "ECW→TIF")
    print(f"Mode: {mode}\n")

    for label, src_dir in entries:
        print(f"[{label}] {src_dir}")
        if not os.path.isdir(src_dir):
            print(f"  NOT FOUND — skipping\n")
            continue

        out_dir = os.path.join(OUT_ROOT, label)
        os.makedirs(out_dir, exist_ok=True)

        ecws = find_ecws(src_dir)
        print(f"  Found {len(ecws)} ECW files")

        skipped = 0
        for i, ecw in enumerate(ecws, 1):
            stem = Path(ecw).stem
            existing = os.path.join(out_dir, f"{stem}.tif")
            if os.path.exists(existing):
                skipped += 1
                continue
            dst = safe_name(out_dir, stem)
            print(f"  {Path(ecw).name} → {dst}")
            convert(ecw, dst, TEST, CIR)
            total_files += 1
            print(f"  {i} ecw done")
        if skipped:
            print(f"  Skipped {skipped} (already exist)")

        print()

    elapsed = time.time() - t0
    print(f"Total: {total_files} files in {elapsed:.1f}s")


if __name__ == "__main__":
    main()
