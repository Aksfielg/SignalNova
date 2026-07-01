import subprocess
import sys
import time

STEPS = [
    ("src/01_download.py", "Downloading TESS light curves"),
    ("src/02_preprocess.py", "Preprocessing and cleaning"),
    ("src/03_bls_search.py", "Running BLS transit search"),
    ("src/03b_lomb_scargle.py", "Cross-validating with Lomb-Scargle"),
    ("src/04_crowding_check.py", "Checking stellar crowding"),
    ("src/05_classifier.py", "Training ML classifier"),
    ("src/07_validate.py", "Validating on known exoplanets"),
    ("src/08_final_report.py", "Generating final star reports"),
]

def run_step(script, description):
    print("\n" + "="*60)
    print(f"STEP: {description}")
    print("="*60)
    result = subprocess.run([sys.executable, script], capture_output=False)
    if result.returncode != 0:
        print(f"\nWARNING: {script} exited with errors. Continuing anyway...")
        time.sleep(1)

if __name__ == "__main__":
    print("PS7 EXOPLANET DETECTION — FULL PIPELINE RUN")
    print(f"Running {len(STEPS)} steps in sequence\n")
    for script, desc in STEPS:
        run_step(script, desc)
    print("\n" + "="*60)
    print("PIPELINE COMPLETE")
    print("="*60)
    print("Next: run 'streamlit run app/streamlit_app.py' to view the dashboard")
    print("Or: run 'python report/generate_report.py' for the PDF report")
