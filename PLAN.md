# Aerial Imagery Pipeline

1. **ECW→TIF batch conversion** — `batch_convert.py` running with `TEST=False, CIR=False`. Converts all ECW files to georeferenced TIF. May take a full day.

2. **CIR spectral conversion** — Rerun `batch_convert.py` with temporary logic to process only `_cir_` files (`CIR=True`). Overwrites the TIFs generated in step 1 for those files.

3. **Load TIFs into QGIS project** — Write a script to add all TIFs from `I:\Raster\UPDATED_AERIALS` into the QGIS project with all layers unchecked by default. Test first with 3–4 small files to verify the "unchecked" behaviour works.
