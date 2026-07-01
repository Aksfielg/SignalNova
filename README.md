# 🪐 SignalNova: AI-Enabled Exoplanet Detection Pipeline
> **Problem Statement (PS) 7 — ISRO Bharatiya Antariksh Hackathon (BAH) 2026**

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B.svg)](https://streamlit.io/)
[![Lightkurve](https://img.shields.io/badge/Lightkurve-TESS-9cf.svg)](https://docs.lightkurve.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📖 Project Overview

**SignalNova** is a highly automated, end-to-end data pipeline and interactive dashboard designed to detect, validate, and classify exoplanet transit signals from **NASA TESS (Transiting Exoplanet Survey Satellite)** astronomical light curves. 

Built specifically for the ISRO BAH 2026 hackathon, this project combines robust astronomical period-finding algorithms (Box Least Squares & Lomb-Scargle) with modern machine learning (XGBoost) and advanced data visualization to separate true exoplanets from astrophysical false positives (e.g., Eclipsing Binaries, Blends, and stellar variability).

---

## ✨ Key Features & Capabilities

* **Automated Data Retrieval & Preprocessing**: Native integration with `lightkurve` and MAST (Mikulski Archive for Space Telescopes) to automatically download, stitch, detrend, and normalize TESS light curves.
* **Dual-Algorithm Period Detection**: Uses the **Box Least Squares (BLS)** method optimized for transit detection, cross-validated against the **Lomb-Scargle Periodogram** to filter out harmonic false positives.
* **Astrophysical Vetting (Vetting Engine)**: Automated heuristics compute transit depths, dip symmetry, odd/even transit depth ratios, crowding metrics, and secondary eclipse depths to filter out Eclipsing Binaries.
* **Machine Learning Classification**: Extracts 23 physical and statistical features from the light curve and periodogram to feed into an **XGBoost Classifier**. It provides probabilistic classification across 4 categories: `PLANET`, `ECLIPSING_BINARY`, `BLEND`, and `OTHER`.
* **Interactive Mission Control Dashboard**: A custom-built, highly aesthetic, hero-styled **Streamlit application** that visualizes phase-folded light curves, periodograms, transit model fits, pixel centroid shifts, and AI interpretations.
* **Automated PDF Reporting**: Generates comprehensive PDF reports for each analyzed star, complete with metrics and plots for easy scientific dissemination.

---

## 🛠️ System Architecture

The pipeline is modular and executes in a sequential, highly traceable order:

1. `01_download.py` — Fetches raw TESS 2-minute cadence data from MAST.
2. `02_preprocess.py` — Cleans, detrends (Savitzky-Golay filtering), and removes stellar outliers.
3. `03_bls_search.py` — Executes the BLS transit search and identifies the highest SNR periods.
4. `03b_lomb_scargle.py` — Performs cross-validation using Lomb-Scargle frequencies.
5. `04_crowding_check.py` — Queries GAIA/TIC catalogs to calculate target crowding risk and potential blend scenarios.
6. `05_classifier.py` — Trains the XGBoost model on the labeled dataset.
7. `07_validate.py` — Validates the pipeline's detection accuracy against known NASA-confirmed planets.
8. `08_final_report.py` — Generates aggregated catalogs and detailed PDF summaries for individual candidates.
9. `streamlit_app.py` — Serves the interactive user interface.

---

## 🚀 Installation & Setup

1. **Clone the repository** (if not already local) and navigate into the project directory:
   ```bash
   cd ps7_exoplanet
   ```

2. **Set up a virtual environment** (recommended):
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Linux/Mac:
   source venv/bin/activate
   ```

3. **Install all dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## 🖥️ Usage Guide

### 1. Run the Entire Pipeline Automatically
To execute all data retrieval, processing, ML training, validation, and report generation in a single command, use the master script:
```bash
python run_full_pipeline.py
```

### 2. Run Individual Modules
If you wish to run the modules step-by-step to examine intermediate artifacts in `data/processed/`:
```bash
python src/01_download.py
python src/02_preprocess.py
python src/03_bls_search.py
python src/03b_lomb_scargle.py
python src/04_crowding_check.py
python src/05_classifier.py
python src/07_validate.py
python src/08_final_report.py
```

### 3. Launch the Interactive Dashboard
To explore the processed stars, view phase-folded light curves, and observe AI confidence scores:
```bash
streamlit run app/streamlit_app.py
```

---

## 📊 Validation & Results

The pipeline has been aggressively validated against NASA-confirmed exoplanets. It successfully recovers known exoplanet periods with **< 0.1% error** for short-period planets (e.g., WASP-126 b, Pi Men c, L 98-59 b).

* **SNR Thresholds:** Signals are automatically vetted. An SNR > 20 is considered an exceptionally strong candidate, while signals with SNR > 6 are passed to the classifier.
* **Multi-Sector Data:** Note that detecting long-period planets (like TOI-700 d, period ~37.4 days) requires multi-sector data. The pipeline is fully configured to handle multi-sector processing out of the box.

---

## 💻 Tech Stack

* **Astronomy / Science**: `lightkurve`, `astropy`, `astroquery`, `scipy`
* **Machine Learning**: `xgboost`, `scikit-learn`, `joblib`
* **Data Processing**: `pandas`, `numpy`
* **Visualization & UI**: `streamlit`, `plotly`, `reportlab`, HTML/CSS (Hero UI Design)

---

> *"Unlocking the universe, one light curve at a time."*
