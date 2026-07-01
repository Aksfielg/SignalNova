import lightkurve as lk
import numpy as np
import os
import time as time_module

OUTPUT_DIR = "data/raw"
os.makedirs(OUTPUT_DIR, exist_ok=True)

CONFIRMED_PLANETS = {
    25155310: "WASP-126 b",
    150428135: "TOI-700 d",
    400071468: "WASP-39 b",
    270341214: "L 98-59 b",
    307210830: "HD 21749 b",
    261136679: "Pi Men c",
}

def download_and_save(tic_id, label="unknown", sectors_to_try=[1, 2, 3, 7]):
    for sector in sectors_to_try:
        try:
            print(f"  Trying TIC {tic_id} ({label}) in Sector {sector}...")
            search = lk.search_lightcurve(
                f"TIC {tic_id}",
                sector=sector,
                cadence="short",
                author="SPOC"
            )
            if len(search) == 0:
                continue
            lc = search[0].download()
            t = lc.time.value
            f = lc.flux.value
            fe = lc.flux_err.value
            np.savez(
                f"{OUTPUT_DIR}/tic_{tic_id}.npz",
                time=t, flux=f, flux_err=fe, tic_id=tic_id, sector=sector
            )
            print(f"  TIC {tic_id} ({label}): SAVED from Sector {sector} — {len(t)} data points")
            return tic_id
        except Exception as e:
            continue
    print(f"  TIC {tic_id} ({label}): No data found in any tried sector")
    return None

if __name__ == "__main__":
    print("=== Downloading confirmed exoplanet host stars ===")
    for tic_id, name in CONFIRMED_PLANETS.items():
        download_and_save(tic_id, name)
        time_module.sleep(1)
    files = os.listdir(OUTPUT_DIR)
    print(f"\nDone. {len(files)} files saved in {OUTPUT_DIR}/")
