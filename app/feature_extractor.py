import librosa
import numpy as np
import warnings

# Suppress librosa warnings
warnings.filterwarnings("ignore")

def extract_features(audio_path: str):
    """
    Advanced feature extraction for AI voice detection.
    Extracts MFCCs (with deltas), Spectral features, and HNR.
    67 features in total for robust detection.
    """
    try:
        # Load audio (downsample to 22050 Hz)
        y, sr = librosa.load(audio_path, sr=22050)
        
        # 1. MFCCs (20 coefficients)
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)
        mfcc_mean = np.mean(mfccs, axis=1)
        mfcc_var = np.var(mfccs, axis=1)
        
        # 2. MFCC Deltas (Temporal dynamics)
        mfcc_delta = librosa.feature.delta(mfccs)
        mfcc_delta2 = librosa.feature.delta(mfccs, order=2)
        
        delta_mean = np.mean(mfcc_delta, axis=1)
        delta2_mean = np.mean(mfcc_delta2, axis=1)

        # 3. Spectral Features
        # Centroid (Brightness)
        cent = librosa.feature.spectral_centroid(y=y, sr=sr)
        cent_mean = np.mean(cent)
        cent_var = np.var(cent)
        
        # Spectral Flatness (AI voices often have unnatural flatness)
        flatness = librosa.feature.spectral_flatness(y=y)
        flat_mean = np.mean(flatness)
        
        # 4. Zero Crossing Rate (Micro-jitters)
        zcr = librosa.feature.zero_crossing_rate(y)
        zcr_mean = np.mean(zcr)
        zcr_var = np.var(zcr)
        
        # 5. Harmonic-to-Noise Ratio (HNR) - Naturalness check
        # Librosa doesn't have a direct HNR, but we can estimate via harmonic/percussive ratio
        harmonic, percussive = librosa.effects.hpss(y)
        hnr_est = np.mean(harmonic**2) / (np.mean(percussive**2) + 1e-6)

        # 6. Pitch Variance (Human voices have natural drift)
        pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
        pitch_vals = pitches[magnitudes > np.mean(magnitudes)]
        pitch_var = np.var(pitch_vals) if len(pitch_vals) > 0 else 0

        # Combine Features
        # 20 (mfcc_mean) + 20 (mfcc_var) + 20 (delta_mean) + 2 (cent) + 1 (flat) + 2 (zcr) + 1 (hnr) + 1 (pitch)
        # Note: We prioritize mean and var of core features.
        # Let's keep it simple: MFCC Mean (20) + MFCC Var (20) + Delta Mean (20) + Spectral (7) = 67 features
        features = np.hstack([
            mfcc_mean, mfcc_var,
            delta_mean,
            cent_mean, cent_var,
            flat_mean,
            zcr_mean, zcr_var,
            hnr_est,
            pitch_var
        ])
        
        return features

    except Exception as e:
        print(f"Error extracting features from {audio_path}: {e}")
        return None

FEATURE_NAMES = [
    *[f"mfcc_mean_{i}" for i in range(20)],
    *[f"mfcc_var_{i}" for i in range(20)],
    *[f"delta_mfcc_mean_{i}" for i in range(20)],
    "centroid_mean", "centroid_var",
    "spectral_flatness",
    "zcr_mean", "zcr_var",
    "hnr_estimate",
    "pitch_variance"
]
