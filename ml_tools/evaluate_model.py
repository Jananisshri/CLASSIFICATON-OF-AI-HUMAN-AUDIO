import os
import sys
import glob
import joblib
import numpy as np

# Ensure we can import from app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.feature_extractor import extract_features
from app.classifier import classifier

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

def evaluate():
    human_files = glob.glob(os.path.join(DATA_DIR, 'human', '*.mp3')) + \
                  glob.glob(os.path.join(DATA_DIR, 'human', '*.wav'))
    
    ai_files = glob.glob(os.path.join(DATA_DIR, 'ai', '*.mp3')) + \
               glob.glob(os.path.join(DATA_DIR, 'ai', '*.wav'))
    
    print(f"Human files: {len(human_files)}")
    print(f"AI files: {len(ai_files)}")
    
    results = []
    
    print("\nEvaluating Human Files (Expected: HUMAN)")
    for f in human_files:
        name = os.path.basename(f)
        try:
            label, conf, _ = classifier.predict_voice(f)
            correct = (label == "HUMAN")
            results.append(correct)
            print(f"  {name}: {label} ({conf:.2f}) {'✅' if correct else '❌'}")
        except Exception as e:
            print(f"  {name}: ERROR {e}")

    print("\nEvaluating AI Files (Expected: AI_GENERATED)")
    for f in ai_files:
        name = os.path.basename(f)
        try:
            label, conf, _ = classifier.predict_voice(f)
            correct = (label == "AI_GENERATED")
            results.append(correct)
            print(f"  {name}: {label} ({conf:.2f}) {'✅' if correct else '❌'}")
        except Exception as e:
            print(f"  {name}: ERROR {e}")
            
    if results:
        accuracy = sum(results) / len(results)
        print(f"\nOverall Accuracy: {accuracy:.2%}")

if __name__ == "__main__":
    evaluate()
