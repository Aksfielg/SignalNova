import numpy as np
import pandas as pd
import os
import sys
sys.path.insert(0, 'src')
from utils import preprocess_lightcurve_simple, preprocess_lightcurve_savgol, compute_flux_stats

RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"
os.makedirs(PROCESSED_DIR, exist_ok=True)

def process_all():
    files = [f for f in os.listdir(RAW_DIR) if f.endswith('.npz')]
    print(f"Found {len(files)} raw files to process")
    results = []
    for fname in files:
        tic_id = int(fname.replace('tic_','').replace('.npz',''))
        data = np.load(f"{RAW_DIR}/{fname}", allow_pickle=True)
        time_arr = data['time'].astype(float)
        flux_arr = data['flux'].astype(float)

        try:
            t_clean, f_clean = preprocess_lightcurve_simple(time_arr, flux_arr)
            np.savez(
                f"{PROCESSED_DIR}/tic_{tic_id}_clean.npz",
                time=t_clean, flux=f_clean, tic_id=tic_id
            )
            s = compute_flux_stats(f_clean)
            s['tic_id'] = tic_id
            s['n_points'] = len(t_clean)
            results.append(s)
            print(f"  TIC {tic_id}: OK (median filter) — {len(t_clean)} clean points")
        except Exception as e:
            print(f"  TIC {tic_id}: median filter FAILED — {e}")
            continue

        try:
            t_sg, f_sg = preprocess_lightcurve_savgol(time_arr, flux_arr)
            np.savez(
                f"{PROCESSED_DIR}/tic_{tic_id}_savgol.npz",
                time=t_sg, flux=f_sg, tic_id=tic_id
            )
            print(f"  TIC {tic_id}: OK (savgol) — {len(t_sg)} clean points")
        except Exception as e:
            print(f"  TIC {tic_id}: savgol FAILED — {e}")

    if results:
        pd.DataFrame(results).to_csv(
            f"{PROCESSED_DIR}/preprocessing_summary.csv", index=False
        )
    print(f"\nProcessed {len(results)} light curves successfully (median filter method)")
    print("Savgol versions saved alongside for comparison in report")

if __name__ == "__main__":
    process_all()
