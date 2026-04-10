import os

total = 0
cir = 0
by_dir = {}

for root, _, files in os.walk(r"I:\Raster\UPDATED_AERIALS"):
    label = os.path.relpath(root, r"I:\Raster\UPDATED_AERIALS").split(os.sep)[0]
    for f in files:
        if f.lower().endswith(".tif"):
            total += 1
            by_dir[label] = by_dir.get(label, [0, 0])
            by_dir[label][0] += 1
            if "_cir_" in f.lower():
                cir += 1
                by_dir[label][1] += 1

for label, (t, c) in sorted(by_dir.items()):
    print(f"  {label:12s} → {t} tif, {c} cir")

print(f"\nTotal TIF: {total}")
print(f"CIR among them: {cir}")
