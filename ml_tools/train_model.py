import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import os
import sys
import glob

# Ensure we can import from app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.feature_extractor import extract_features

# Define paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'app', 'model.joblib')
DATA_DIR = os.path.join(BASE_DIR, 'data')

def train_model():
    """
    Main training function.
    Checks for real data first. If found, trains on it.
    Otherwise, trains a dummy model for testing.
    """
    human_files = glob.glob(os.path.join(DATA_DIR, 'human', '*.mp3')) + \
                  glob.glob(os.path.join(DATA_DIR, 'human', '*.wav'))
    
    ai_files = glob.glob(os.path.join(DATA_DIR, 'ai', '*.mp3')) + \
               glob.glob(os.path.join(DATA_DIR, 'ai', '*.wav'))
    
    if human_files and ai_files:
        print(f"Found {len(human_files)} Human samples and {len(ai_files)} AI samples.")
        train_real_model(human_files, ai_files)
    else:
        print("Real data not found in 'data/human' or 'data/ai'.")
        print("Training DUMMY model with synthetic noise (FOR TESTING ONLY).")
        train_dummy_model()

def train_real_model(human_files, ai_files):
    X = []
    y = []
    
    print("Extracting features from Human files...")
    for i, f in enumerate(human_files, 1):
        print(f"  [{i}/{len(human_files)}] Processing: {os.path.basename(f)}")
        feats = extract_features(f)
        if feats is not None:
            X.append(feats)
            y.append(1) # 1 = HUMAN
        else:
            print(f"    ⚠️  Failed to extract features")

    print("Extracting features from AI files...")
    for i, f in enumerate(ai_files, 1):
        print(f"  [{i}/{len(ai_files)}] Processing: {os.path.basename(f)}")
        feats = extract_features(f)
        if feats is not None:
            X.append(feats)
            y.append(0) # 0 = AI_GENERATED
        else:
            print(f"    ⚠️  Failed to extract features")
            
    X = np.array(X)
    y = np.array(y)
    
    if len(X) == 0:
        print("Error: No valid features extracted.")
        return

    # Train
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('clf', RandomForestClassifier(n_estimators=200, class_weight='balanced', random_state=42))
    ])
    
    print(f"Training on {len(X)} samples with {X.shape[1]} features...")
    pipeline.fit(X, y)
    
    print(f"Saving model to {MODEL_PATH}...")
    joblib.dump(pipeline, MODEL_PATH)
    print("Model saved successfully (Real Data).")

def train_dummy_model():
    print("Generating synthetic data for prototype...")
    
    # Feature size must match extract_features (34)
    n_features = 34 
    n_samples = 100
    
    # Synthetic Human Data (Label 1)
    X_human = np.random.normal(loc=0.5, scale=0.5, size=(n_samples // 2, n_features))
    y_human = np.ones(n_samples // 2) 
    
    # Synthetic AI Data (Label 0)
    X_ai = np.random.normal(loc=0.0, scale=0.3, size=(n_samples // 2, n_features))
    y_ai = np.zeros(n_samples // 2) 
    
    X = np.vstack([X_human, X_ai])
    y = np.hstack([y_human, y_ai])
    
    # Shuffle
    perm = np.random.permutation(n_samples)
    X = X[perm]
    y = y[perm]
    
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('clf', RandomForestClassifier(n_estimators=100, random_state=42))
    ])
    
    print("Training model...")
    pipeline.fit(X, y)
    
    print(f"Saving model to {MODEL_PATH}...")
    joblib.dump(pipeline, MODEL_PATH)
    print("Model saved successfully.")

if __name__ == "__main__":
    train_model()
