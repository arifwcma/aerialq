import os
from pathlib import Path

DIRS_FILE = r"C:\Users\m.rahman\qgis\aerialq\dirs.txt"
OUT_ROOT = r"I:\Raster\UPDATED_AERIALS"


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


total = 0
done = 0
left = []

for label, src_dir in parse_dirs(DIRS_FILE):
    print(f"[{label}] Scanning {src_dir} ...", flush=True)
    if not os.path.isdir(src_dir):
        print(f"  NOT FOUND — skipping")
        continue

    out_dir = os.path.join(OUT_ROOT, label)
    ecws = find_ecws(src_dir)
    print(f"  Found {len(ecws)} ECW files. Checking TIFs ...", flush=True)

    grp_done = 0
    grp_left = 0
    for ecw in ecws:
        total += 1
        stem = Path(ecw).stem
        tif = os.path.join(out_dir, f"{stem}.tif")
        if os.path.exists(tif) and os.path.getsize(tif) > 0:
            done += 1
            grp_done += 1
        else:
            left.append(f"[{label}] {ecw}")
            grp_left += 1
    print(f"  Done: {grp_done}, Left: {grp_left}")

print(f"\nTotal ECW: {total}")
print(f"Done:      {done}")
print(f"Left:      {len(left)}")
