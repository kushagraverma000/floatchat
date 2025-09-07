# scripts/01_env_check.py
import os
import sys
import xarray as xr

# path to one sample NetCDF file - update to your actual file
sample = "data/raw/2024/01/20240101_prof.nc"

print("Python", sys.version)
print("xarray version:", xr.__version__)

if not os.path.exists(sample):
    print("SAMPLE FILE NOT FOUND:", sample)
    print("List a few files in data/raw/2024/01 to confirm:")
    try:
        print(os.listdir("data/raw/2024/01")[:10])
    except Exception as e:
        print("Could not list directory:", e)
    raise SystemExit("Place at least one NetCDF in the sample path and re-run this script.")

print("Opening sample NetCDF:", sample)
ds = xr.open_dataset(sample)
print(ds)
print("\nVariables:", list(ds.variables)[:50])
ds.close()
print("OK - environment and test file opened successfully.")
