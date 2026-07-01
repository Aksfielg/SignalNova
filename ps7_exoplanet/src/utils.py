import numpy as np
# numpy 2.0 compatibility
if not hasattr(np, 'trapz'):
    np.trapz = np.trapezoid

import pandas as pd
from scipy import stats
from scipy.ndimage import median_filter
from scipy.signal import savgol_filter

def force_numpy_array(arr):
    try: arr = arr.unmasked
    except: pass
    try: arr = arr.value
    except: pass
    try: return np.array(arr.tolist(), dtype=float)
    except: return np.array(list(arr), dtype=float)

def sigma_clip(flux, sigma=4):
    median = np.median(flux)
    std = np.std(flux)
    mask = np.abs(flux - median) < sigma * std
    return mask

def normalize_flux(flux):
    return flux / np.median(flux)

def compute_flux_stats(flux):
    return {
        'flux_mean': float(np.mean(flux)),
        'flux_std': float(np.std(flux)),
        'flux_skew': float(stats.skew(flux)),
        'flux_kurtosis': float(stats.kurtosis(flux)),
        'flux_range': float(np.max(flux) - np.min(flux)),
        'flux_pct_below_median': float(np.sum(flux < np.median(flux)) / len(flux)),
        'flux_p5': float(np.percentile(flux, 5)),
        'flux_p95': float(np.percentile(flux, 95)),
    }

def preprocess_lightcurve_simple(time, flux):
    time = force_numpy_array(time)
    flux = force_numpy_array(flux)
    valid = np.isfinite(flux) & np.isfinite(time)
    time = time[valid]
    flux = flux[valid]
    mask = sigma_clip(flux, sigma=4)
    time = time[mask]
    flux = flux[mask]
    flux = normalize_flux(flux)
    window = 201
    trend = median_filter(flux, size=window, mode='reflect')
    flux_flat = flux / trend
    flux_flat = normalize_flux(flux_flat)
    return time, flux_flat

def preprocess_lightcurve_savgol(time, flux, window_length=101, polyorder=2):
    time = force_numpy_array(time)
    flux = force_numpy_array(flux)
    valid = np.isfinite(flux) & np.isfinite(time)
    time = time[valid]
    flux = flux[valid]
    mask = sigma_clip(flux, sigma=4)
    time = time[mask]
    flux = flux[mask]
    flux = normalize_flux(flux)
    if window_length % 2 == 0:
        window_length += 1
    if window_length >= len(flux):
        window_length = len(flux) - 1 if len(flux) % 2 == 0 else len(flux) - 2
    if window_length < 5:
        return time, flux
    trend = savgol_filter(flux, window_length, polyorder)
    flux_flat = flux / trend
    flux_flat = normalize_flux(flux_flat)
    return time, flux_flat

def phase_fold(time, flux, period, t0):
    phase = ((time - t0) % period) / period
    phase[phase > 0.75] -= 1.0
    sort_idx = np.argsort(phase)
    return phase[sort_idx], flux[sort_idx]

def bin_light_curve(phase, flux, n_bins=200):
    bins = np.linspace(phase.min(), phase.max(), n_bins + 1)
    bin_centers = (bins[:-1] + bins[1:]) / 2
    binned_flux = np.zeros(n_bins)
    for i in range(n_bins):
        mask = (phase >= bins[i]) & (phase < bins[i+1])
        if mask.sum() > 0:
            binned_flux[i] = np.median(flux[mask])
        else:
            binned_flux[i] = 1.0
    return bin_centers, binned_flux

def check_secondary_eclipse(time, flux, period, t0, depth_primary):
    phase, flux_folded = phase_fold(time, flux, period, t0)
    mask_secondary = (phase > -0.05) & (phase < 0.05)
    if mask_secondary.sum() < 5:
        return 0.0, False
    secondary_depth = 1.0 - np.median(flux_folded[mask_secondary])
    is_likely_eb = secondary_depth > 0.2 * abs(depth_primary)
    return float(max(0, secondary_depth)), bool(is_likely_eb)

def check_odd_even_depths(time, flux, period, t0):
    transit_times = []
    t = t0
    while t < time.max():
        if t > time.min():
            transit_times.append(t)
        t += period
    odd_depths = []
    even_depths = []
    for i, tt in enumerate(transit_times):
        mask = np.abs(time - tt) < period * 0.05
        if mask.sum() < 3:
            continue
        depth = 1.0 - np.min(flux[mask])
        if i % 2 == 0:
            odd_depths.append(depth)
        else:
            even_depths.append(depth)
    if not odd_depths or not even_depths:
        return 0.0, 0.0, 1.0
    odd_mean = float(np.mean(odd_depths))
    even_mean = float(np.mean(even_depths))
    ratio = odd_mean / even_mean if even_mean > 0 else 1.0
    return odd_mean, even_mean, float(ratio)

def compute_dip_area(flux, baseline=1.0):
    below_baseline = baseline - flux
    below_baseline[below_baseline < 0] = 0
    return float(np.trapz(below_baseline))

def compute_autocorrelation_peak(flux, max_lag=2000):
    try: flux = flux.unmasked
    except: pass
    try: flux = np.array(flux.tolist(), dtype=float)
    except: flux = np.array(list(flux), dtype=float)
    flux = flux[~np.isnan(flux)]
    if len(flux) == 0: return 0.0, 0.0
    flux_centered = flux - np.mean(flux)
    n = len(flux_centered)
    max_lag = min(max_lag, n // 2)
    autocorr = np.correlate(flux_centered, flux_centered, mode='full')
    autocorr = autocorr[n-1:n-1+max_lag]
    if autocorr[0] == 0:
        return 0.0, 0.0
    autocorr = autocorr / autocorr[0]
    search_start = 10
    if len(autocorr) > search_start:
        peak_lag = np.argmax(autocorr[search_start:]) + search_start
        peak_value = float(autocorr[peak_lag])
    else:
        peak_lag = 0
        peak_value = 0.0
    return float(peak_lag), peak_value

def compute_fft_dominant_frequency(flux, cadence_days=0.00139):
    try: flux = flux.unmasked
    except: pass
    try: flux = np.array(flux.tolist(), dtype=float)
    except: flux = np.array(list(flux), dtype=float)
    flux = flux[~np.isnan(flux)]
    if len(flux) == 0: return 0.0, 0.0
    flux_centered = flux - np.mean(flux)
    fft_vals = np.fft.rfft(flux_centered)
    fft_freq = np.fft.rfftfreq(len(flux_centered), d=cadence_days)
    power = np.abs(fft_vals) ** 2
    if len(power) > 1:
        dominant_idx = np.argmax(power[1:]) + 1
        dominant_freq = float(fft_freq[dominant_idx])
        dominant_power = float(power[dominant_idx])
    else:
        dominant_freq = 0.0
        dominant_power = 0.0
    return dominant_freq, dominant_power

def compute_dip_symmetry(time, flux, period, t0, duration_days):
    phase = ((time - t0) % period) / period
    phase[phase > 0.5] -= 1.0
    half_dur_phase = (duration_days / period) / 2
    in_transit = np.abs(phase) < half_dur_phase
    if in_transit.sum() < 6:
        return 1.0
    left_mask = in_transit & (phase < 0)
    right_mask = in_transit & (phase >= 0)
    if left_mask.sum() < 2 or right_mask.sum() < 2:
        return 1.0
    left_depth = 1.0 - np.min(flux[left_mask])
    right_depth = 1.0 - np.min(flux[right_mask])
    if max(left_depth, right_depth) == 0:
        return 1.0
    symmetry = min(left_depth, right_depth) / max(left_depth, right_depth)
    return float(symmetry)
