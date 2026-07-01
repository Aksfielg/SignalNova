import numpy as np
import pandas as pd
import os
from astropy.timeseries import LombScargle

PROCESSED_DIR = "data/processed"

def run_lomb_scargle(tic_id):
    fname = f"{PROCESSED_DIR}/tic_{tic_id}_clean.npz"
    if not os.path.exists(fname):
        return None
    data = np.load(fname, allow_pickle=True)
    time = data['time'].astype(float)
    flux = data['flux'].astype(float)

    ls = LombScargle(time, flux)
    frequency, power = ls.autopower(
        minimum_frequency=1/20.0,
        maximum_frequency=1/0.5,
        samples_per_peak=10
    )
    best_freq = frequency[np.argmax(power)]
    ls_period = 1.0 / best_freq
    fap = ls.false_alarm_probability(power.max())

    return {
        'tic_id': tic_id,
        'ls_period_days': round(float(ls_period), 6),
        'ls_power': round(float(power.max()), 4),
        'ls_false_alarm_prob': round(float(fap), 6),
    }

def run_all():
    bls_path = f"{PROCESSED_DIR}/bls_results.csv"
    if not os.path.exists(bls_path):
        print("Run 03_bls_search.py first.")
        return
    bls_df = pd.read_csv(bls_path)
    results = []
    for tic_id in bls_df['tic_id'].unique():
        r = run_lomb_scargle(int(tic_id))
        if r:
            results.append(r)
            print(f"  TIC {tic_id}: LS period={r['ls_period_days']:.4f}d  FAP={r['ls_false_alarm_prob']:.2e}")

    if not results:
        print("No results generated.")
        return

    ls_df = pd.DataFrame(results)
    merged = bls_df.merge(ls_df, on='tic_id', how='left')
    merged['period_agreement_pct'] = (
        abs(merged['best_period_days'] - merged['ls_period_days']) /
        merged['best_period_days'] * 100
    )
    merged['methods_agree'] = (merged['period_agreement_pct'] < 5.0).astype(int)
    merged.to_csv(bls_path, index=False)
    print(f"\nLomb-Scargle cross-check complete.")
    print(f"Methods agree (within 5%): {merged['methods_agree'].sum()}/{len(merged)} stars")

if __name__ == "__main__":
    run_all()
