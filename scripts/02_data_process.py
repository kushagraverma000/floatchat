# scripts/02_data_process.py
import os
import xarray as xr
import pandas as pd
from tqdm import tqdm

def process_profile(nc_path):
    ds = xr.open_dataset(nc_path)
    profiles = []

    for i in range(ds.sizes['N_PROF']):
        profile_data = {
            'file': os.path.basename(nc_path),
            'profile_index': i,
            'latitude': float(ds['LATITUDE'].values[i]),
            'longitude': float(ds['LONGITUDE'].values[i]),
            'date_time': pd.to_datetime(ds['JULD'].values[i]),  # <-- updated here
            'pressure_mean': float(ds['PRES'].isel(N_PROF=i).mean().values),
            'temperature_mean': float(ds['TEMP'].isel(N_PROF=i).mean().values),
            'salinity_mean': float(ds['PSAL'].isel(N_PROF=i).mean().values),
        }
        profiles.append(profile_data)

    ds.close()
    return pd.DataFrame(profiles)



def main():
    raw_dir = "data/raw/2024"
    processed_file = "data/processed/profiles_2024.csv"

    all_profiles = []
    for root, _, files in os.walk(raw_dir):
        for file in tqdm(files):
            if file.endswith(".nc"):
                file_path = os.path.join(root, file)
                try:
                    df = process_profile(file_path)
                    all_profiles.append(df)
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

    all_data = pd.concat(all_profiles, ignore_index=True)
    os.makedirs("data/processed", exist_ok=True)
    all_data.to_csv(processed_file, index=False)
    print(f"Processed data saved to {processed_file}")


if __name__ == "__main__":
    main()
