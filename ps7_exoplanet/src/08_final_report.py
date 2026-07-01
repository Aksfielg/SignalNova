import numpy as np
import pandas as pd
import json
import os
from datetime import datetime

PROCESSED_DIR = "data/processed"
REPORT_DIR = "data/processed/star_reports"
os.makedirs(REPORT_DIR, exist_ok=True)

def generate_star_report(row):
    report = {
        "star_id": f"TIC {int(row['tic_id'])}",
        "analysis_date": datetime.now().isoformat(),
        "transit_found": bool(row.get('above_snr_threshold', 0) == 1),
        "orbital_parameters": {
            "period_days": row.get('best_period_days', None),
            "transit_depth_ppm": row.get('transit_depth_ppm', None),
            "transit_duration_hours": row.get('transit_duration_hours', None),
            "transit_midpoint_btjd": row.get('t0', None),
        },
        "signal_quality": {
            "snr": row.get('snr', None),
            "bls_power": row.get('bls_power', None),
            "lomb_scargle_period_days": row.get('ls_period_days', None),
            "methods_agree": bool(row.get('methods_agree', 0) == 1),
        },
        "vetting_tests": {
            "secondary_eclipse_depth_ppm": row.get('secondary_eclipse_depth', None),
            "secondary_eclipse_flag": bool(row.get('is_eb_secondary_flag', 0) == 1),
            "odd_even_depth_ratio": row.get('odd_even_ratio', None),
            "odd_even_flag": bool(row.get('is_eb_oddeven_flag', 0) == 1),
            "dip_symmetry": row.get('dip_symmetry', None),
        },
        "crowding_assessment": {
            "target_magnitude": row.get('target_tmag', None),
            "bright_neighbors_21arcsec": row.get('bright_neighbors', None),
            "crowding_risk": row.get('crowding_risk', 'UNKNOWN'),
        },
        "additional_features": {
            "dip_area": row.get('dip_area', None),
            "autocorrelation_peak": row.get('autocorr_peak', None),
            "fft_dominant_freq": row.get('fft_dominant_freq', None),
        }
    }
    return report

def generate_all_reports():
    bls_path = f"{PROCESSED_DIR}/bls_results.csv"
    if not os.path.exists(bls_path):
        print("Run 03_bls_search.py first.")
        return
    df = pd.read_csv(bls_path)
    all_reports = []
    for _, row in df.iterrows():
        report = generate_star_report(row)
        all_reports.append(report)
        tic_id = int(row['tic_id'])
        with open(f"{REPORT_DIR}/TIC{tic_id}_report.json", 'w') as f:
            json.dump(report, f, indent=2, default=str)

    with open(f"{PROCESSED_DIR}/all_star_reports.json", 'w') as f:
        json.dump(all_reports, f, indent=2, default=str)

    print(f"Generated {len(all_reports)} individual star reports")
    print(f"Saved to {REPORT_DIR}/")

    candidates = [r for r in all_reports if r['transit_found']]
    print(f"\n{len(candidates)} stars flagged as transit candidates")
    for c in candidates[:5]:
        print(f"  {c['star_id']}: P={c['orbital_parameters']['period_days']}d")

if __name__ == "__main__":
    generate_all_reports()
