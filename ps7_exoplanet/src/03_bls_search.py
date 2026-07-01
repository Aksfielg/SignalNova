import numpy as np
import pandas as pd
import os
import sys
sys.path.insert(0, 'src')
from astropy.timeseries import BoxLeastSquares
from utils import (check_secondary_eclipse, check_odd_even_depths, compute_flux_stats,
                   compute_dip_area, compute_autocorrelation_peak,
                   compute_fft_dominant_frequency, compute_dip_symmetry)

PROCESSED_DIR = "data/processed"
PERIOD_MIN = 0.5
PERIOD_MAX = 20.0
SNR_THRESHOLD = 6.0

def run_bls_single(tic_id):
    fname = f"{PROCESSED_DIR}/tic_{tic_id}_clean.npz"
    if not os.path.exists(fname):
        return None
    data = np.load(fname, allow_pickle=True)
    time = data['time'].astype(float)
    flux = data['flux'].astype(float)

    bls = BoxLeastSquares(time, flux)
    durations = np.linspace(0.05, 0.3, 15)
    try:
        result = bls.autopower(
            durations,
            minimum_period=PERIOD_MIN,
            maximum_period=PERIOD_MAX,
            frequency_factor=1.0
        )
    except Exception as e:
        print(f"  TIC {tic_id} BLS error: {e}")
        return None

    best_idx = np.argmax(result.power)
    best_period = float(result.period[best_idx])
    best_power = float(result.power[best_idx])

    best_duration = float(result.duration[best_idx])
    best_t0 = float(result.transit_time[best_idx])

    try:
        bls_stats = bls.compute_stats(best_period, best_duration, best_t0)
        transit_depth = float(bls_stats['depth'][0])
        depth_err = float(bls_stats['depth'][1])
        transit_duration = best_duration
        t0 = best_t0
        
        in_mask = np.abs(((time - best_t0 + best_period/2) % best_period) - best_period/2) < best_duration/2
        out_mask = ~in_mask
        if in_mask.sum() > 0 and out_mask.sum() > 1:
            noise = np.std(flux[out_mask])
            signal = abs(np.median(flux[out_mask]) - np.median(flux[in_mask]))
            snr = signal / (noise / np.sqrt(in_mask.sum())) if noise > 0 else 0.0
        else:
            snr = 0.0
    except Exception as e:
        print(f"Exception in compute_stats: {e}")
        transit_depth = 0.001
        transit_duration = best_duration
        t0 = best_t0
        snr = 0.0

    depth_ppm = transit_depth * 1e6
    sec_depth, is_eb_sec = check_secondary_eclipse(time, flux, best_period, t0, transit_depth)
    odd_d, even_d, oe_ratio = check_odd_even_depths(time, flux, best_period, t0)
    flux_stats = compute_flux_stats(flux)
    dip_area = compute_dip_area(flux)
    autocorr_lag, autocorr_peak = compute_autocorrelation_peak(flux)
    fft_freq, fft_power = compute_fft_dominant_frequency(flux)
    symmetry = compute_dip_symmetry(time, flux, best_period, t0, transit_duration)

    row = {
        'tic_id': tic_id,
        'best_period_days': round(best_period, 6),
        'transit_depth_ppm': round(depth_ppm, 2),
        'transit_duration_hours': round(transit_duration * 24, 4),
        't0': round(t0, 6),
        'bls_power': round(best_power, 4),
        'snr': round(snr, 2),
        'secondary_eclipse_depth': round(sec_depth * 1e6, 2),
        'is_eb_secondary_flag': int(is_eb_sec),
        'odd_even_ratio': round(oe_ratio, 4),
        'is_eb_oddeven_flag': int(abs(oe_ratio - 1.0) > 0.3),
        'above_snr_threshold': int(snr >= SNR_THRESHOLD),
        'dip_area': round(dip_area, 6),
        'autocorr_lag': round(autocorr_lag, 2),
        'autocorr_peak': round(autocorr_peak, 4),
        'fft_dominant_freq': round(fft_freq, 6),
        'fft_dominant_power': round(fft_power, 4),
        'dip_symmetry': round(symmetry, 4),
    }
    row.update(flux_stats)
    return row

def run_bls_all():
    files = [f for f in os.listdir(PROCESSED_DIR) if f.endswith('clean.npz')]
    print(f"Running BLS on {len(files)} light curves...")
    all_results = []
    for i, fname in enumerate(files):
        tic_id = int(fname.replace('tic_','').replace('_clean.npz',''))
        print(f"  [{i+1}/{len(files)}] TIC {tic_id}...", end=" ")
        row = run_bls_single(tic_id)
        if row:
            all_results.append(row)
            print(f"period={row['best_period_days']:.4f}d snr={row['snr']:.1f} symmetry={row['dip_symmetry']:.2f}")
        else:
            print("SKIP")
    df = pd.DataFrame(all_results)
    df.to_csv(f"{PROCESSED_DIR}/bls_results.csv", index=False)
    cands = df[df['above_snr_threshold']==1] if len(df) > 0 else df
    print(f"\nDone. {len(cands)} candidates above SNR={SNR_THRESHOLD}")
    print(f"Saved to {PROCESSED_DIR}/bls_results.csv")
    return df

if __name__ == "__main__":
    run_bls_all()
