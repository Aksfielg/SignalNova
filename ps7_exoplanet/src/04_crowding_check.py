import numpy as np
import pandas as pd
import os

PROCESSED_DIR = "data/processed"

def check_crowding(tic_id, search_radius_arcsec=21):
    try:
        from astroquery.mast import Catalogs
        catalog = Catalogs.query_object(
            f"TIC {tic_id}", radius=search_radius_arcsec/3600, catalog="TIC"
        )
        target_row = catalog[catalog['ID'] == str(tic_id)]
        if len(target_row) == 0:
            return None
        target_mag = float(target_row['Tmag'][0])

        neighbors = catalog[catalog['ID'] != str(tic_id)]
        n_neighbors = len(neighbors)
        bright_neighbors = 0
        if n_neighbors > 0:
            bright_neighbors = int(np.sum(neighbors['Tmag'] < target_mag + 3))

        crowding_risk = "HIGH" if bright_neighbors >= 2 else (
            "MEDIUM" if bright_neighbors == 1 else "LOW"
        )

        return {
            'tic_id': tic_id,
            'target_tmag': round(target_mag, 2),
            'n_neighbors_21arcsec': n_neighbors,
            'bright_neighbors': bright_neighbors,
            'crowding_risk': crowding_risk,
        }
    except Exception as e:
        print(f"  TIC {tic_id}: crowding check failed — {e}")
        return {
            'tic_id': tic_id,
            'target_tmag': None,
            'n_neighbors_21arcsec': None,
            'bright_neighbors': None,
            'crowding_risk': 'UNKNOWN',
        }

def run_all():
    bls_path = f"{PROCESSED_DIR}/bls_results.csv"
    if not os.path.exists(bls_path):
        print("Run 03_bls_search.py first.")
        return
    bls_df = pd.read_csv(bls_path)
    results = []
    for tic_id in bls_df['tic_id'].unique():
        print(f"  Checking crowding for TIC {tic_id}...")
        r = check_crowding(int(tic_id))
        if r:
            results.append(r)
            print(f"    {r['crowding_risk']} risk")

    crowd_df = pd.DataFrame(results)
    merged = bls_df.merge(crowd_df, on='tic_id', how='left')
    merged.to_csv(bls_path, index=False)
    print(f"\nCrowding check complete for {len(results)} stars.")
    if 'crowding_risk' in merged.columns:
        high_risk = merged[merged['crowding_risk']=='HIGH']
        print(f"HIGH crowding risk: {len(high_risk)} stars")

if __name__ == "__main__":
    run_all()
