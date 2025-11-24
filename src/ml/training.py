import joblib, json, os
from datetime import datetime
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

MODEL_DIR = "models/checkpoints"
METADATA_PATH = "models/metadata.json"

def main():
    iris = load_iris(as_frame=True)
    X, y = iris.data, iris.target
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    clf = RandomForestClassifier(random_state=42)
    clf.fit(X_train, y_train)
    acc = accuracy_score(y_test, clf.predict(X_test))
    print(f"Model trained successfully with accuracy: {acc:.2f}")

    os.makedirs(MODEL_DIR, exist_ok=True)
    model_path = os.path.join(MODEL_DIR, "model.joblib")
    joblib.dump(clf, model_path)
    print(f"Model saved to {model_path}")

    metadata = {
        "features": list(X.columns),
        "target_names": iris.target_names.tolist(),
        "trained_at": datetime.utcnow().isoformat() + "Z",
        "model_type": clf.__class__.__name__,
        "notes": "Iris demo model - replace with your real schema later."
    }
    os.makedirs(os.path.dirname(METADATA_PATH), exist_ok=True)
    with open(METADATA_PATH, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
    print(f"Metadata saved to {METADATA_PATH}")

if __name__ == "__main__":
    main()