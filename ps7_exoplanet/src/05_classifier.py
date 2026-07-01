import numpy as np
import pandas as pd
import joblib
import os
import sys
sys.path.insert(0, 'src')
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.utils.class_weight import compute_sample_weight
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import xgboost as xgb

PROCESSED_DIR = "data/processed"
LABELED_DIR = "data/labeled"
MODELS_DIR = "models"
os.makedirs(MODELS_DIR, exist_ok=True)

FEATURE_COLS = [
    'best_period_days','transit_depth_ppm','transit_duration_hours',
    'snr','secondary_eclipse_depth','is_eb_secondary_flag',
    'odd_even_ratio','is_eb_oddeven_flag','dip_area','autocorr_lag',
    'autocorr_peak','fft_dominant_freq','fft_dominant_power','dip_symmetry',
    'flux_mean','flux_std','flux_skew','flux_kurtosis','flux_range',
    'flux_pct_below_median','flux_p5','flux_p95','bls_power'
]

def load_data():
    bls = pd.read_csv(f"{PROCESSED_DIR}/bls_results.csv")
    labels = pd.read_csv(f"{LABELED_DIR}/isro_labels.csv")
    merged = bls.merge(labels, on='tic_id', how='inner')
    print(f"Training examples: {len(merged)}")
    print(merged['label'].value_counts())
    return merged

def train():
    df = load_data()
    available_features = [c for c in FEATURE_COLS if c in df.columns]
    X = df[available_features].fillna(0)
    y = df['label']
    le = LabelEncoder()
    y_enc = le.fit_transform(y)
    print(f"Classes: {le.classes_}")

    if len(df) < 4:
        print("Not enough labeled data yet — need at least 4 examples.")
        model = xgb.XGBClassifier(n_estimators=10, random_state=42)
        model.fit(X, y_enc)
        joblib.dump(model, f"{MODELS_DIR}/xgboost_model.pkl")
        joblib.dump(le, f"{MODELS_DIR}/label_encoder.pkl")
        joblib.dump(available_features, f"{MODELS_DIR}/feature_cols.pkl")
        print("Placeholder model saved. Re-run after ISRO provides full labeled dataset.")
        return model, le

    X_train, X_test, y_train, y_test = train_test_split(
        X, y_enc, test_size=0.2, random_state=42, stratify=y_enc
    )

    sample_weights = compute_sample_weight(class_weight='balanced', y=y_train)
    print("\n=== CLASS IMBALANCE HANDLING ===")
    print("Training set class counts:")
    print(pd.Series(y_train).value_counts())
    print("Using compute_sample_weight(class_weight='balanced')")

    model = xgb.XGBClassifier(
        n_estimators=300, max_depth=6, learning_rate=0.05,
        subsample=0.8, colsample_bytree=0.8,
        eval_metric='mlogloss', random_state=42, n_jobs=-1
    )
    model.fit(X_train, y_train, sample_weight=sample_weights,
              eval_set=[(X_test, y_test)], verbose=100)

    y_pred = model.predict(X_test)
    print(f"\nAccuracy: {accuracy_score(y_test, y_pred):.4f}")
    print(classification_report(y_test, y_pred, target_names=le.classes_))

    joblib.dump(model, f"{MODELS_DIR}/xgboost_model.pkl")
    joblib.dump(le, f"{MODELS_DIR}/label_encoder.pkl")
    joblib.dump(available_features, f"{MODELS_DIR}/feature_cols.pkl")
    print(f"Model saved to {MODELS_DIR}/")

    fi = pd.Series(model.feature_importances_, index=available_features)
    print("\nTop 10 most important features:")
    print(fi.sort_values(ascending=False).head(10))

    return model, le

def predict_single(features_dict):
    model = joblib.load(f"{MODELS_DIR}/xgboost_model.pkl")
    le = joblib.load(f"{MODELS_DIR}/label_encoder.pkl")
    feature_cols = joblib.load(f"{MODELS_DIR}/feature_cols.pkl")
    X = pd.DataFrame([features_dict])[feature_cols].fillna(0)
    proba = model.predict_proba(X)[0]
    pred_idx = np.argmax(proba)
    pred_class = le.classes_[pred_idx]
    confidence = float(proba[pred_idx])
    all_probs = {cls: round(float(p)*100,1) for cls, p in zip(le.classes_, proba)}
    return pred_class, confidence, all_probs

if __name__ == "__main__":
    train()
