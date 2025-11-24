# File: src/ml/inference.py
import argparse, json, hashlib, os
from datetime import datetime

# Import optional heavy deps with graceful fallback for editors/CI that
# can't resolve the packages. At runtime we raise a clear ImportError
# telling the user how to install the missing package.
try:
    import joblib  # type: ignore
except Exception as _e:  # pragma: no cover - runtime/import fallback
    joblib = None
    _joblib_import_error = _e

try:
    import numpy as np  # type: ignore
except Exception as _e:  # pragma: no cover - runtime/import fallback
    np = None
    _numpy_import_error = _e

try:
    import pandas as pd  # type: ignore
except Exception as _e:  # pragma: no cover - runtime/import fallback
    pd = None
    _pandas_import_error = _e

MODEL_PATH = "models/checkpoints/model.joblib"
METADATA_PATH = "models/metadata.json"
LOG_DIR = "logs"
LOG_PATH = os.path.join(LOG_DIR, "inference.log")

class InferenceModel:
    def __init__(self, model_path, features):
        # Ensure required runtime dependencies are present
        if joblib is None:
            raise ImportError(
                "joblib is required to load the model. Install with: pip install joblib"
            )
        if np is None:
            raise ImportError(
                "numpy is required for inference. Install with: pip install numpy"
            )

        self.model_path = model_path
        self.features = features
        self.model = joblib.load(model_path)
        self.model_hash = self._file_sha256(model_path)

    def predict(self, input_df):
        aligned = self._align_columns(input_df)
        return self.model.predict(aligned)

    def _align_columns(self, df):
        if np is None:
            raise ImportError("numpy is required for _align_columns")

        for c in [f for f in self.features if f not in df.columns]:
            df[c] = np.nan
        df = df[[c for c in self.features if c in df.columns]]
        return df

    @staticmethod
    def _file_sha256(path):
        h = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()

def load_metadata(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def log_event(event):
    os.makedirs(LOG_DIR, exist_ok=True)
    event["timestamp"] = datetime.utcnow().isoformat() + "Z"
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        json.dump(event, f)
        f.write("\n")

def parse_args():
    p = argparse.ArgumentParser(description="Audit-safe inference runner")
    p.add_argument("inputs", nargs="*", help="CSV path or feature values")
    p.add_argument("--model", default=MODEL_PATH)
    p.add_argument("--metadata", default=METADATA_PATH)
    p.add_argument("--output", default=None)
    p.add_argument("--no-log", action="store_true")
    return p.parse_args()

def build_input_dataframe(inputs, features):
    if pd is None:
        raise ImportError("pandas is required to build input dataframes. Install with: pip install pandas")

    if not inputs:
        raise ValueError("No inputs provided")
    if inputs[0].lower().endswith(".csv"):
        return pd.read_csv(inputs[0])
    values = [float(x) for x in inputs]
    if len(values) != len(features):
        raise ValueError(f"Expected {len(features)} values, got {len(values)}")
    return pd.DataFrame([values], columns=features)

def main():
    args = parse_args()
    meta = load_metadata(args.metadata)
    features, target_names = meta.get("features", []), meta.get("target_names")

    model = InferenceModel(args.model, features)
    input_df = build_input_dataframe(args.inputs, features)
    preds = model.predict(input_df)

    labels = None
    if target_names and np.issubdtype(np.array(preds).dtype, np.integer):
        labels = [target_names[int(i)] for i in preds]

    print("Predictions:", preds.tolist())
    if labels: print("Labels:", labels)

    if args.output:
        out_df = input_df.copy()
        out_df["prediction"] = preds
        if labels: out_df["label"] = labels
        os.makedirs(os.path.dirname(args.output), exist_ok=True)
        out_df.to_csv(args.output, index=False)
        print(f"Wrote predictions to {args.output}")

    if not args.no_log:
        log_event({
            "event": "inference_run",
            "model_path": args.model,
            "model_hash": model.model_hash,
            "features": features,
            "input_rows": len(input_df),
            "predictions": preds.tolist(),
            "labels": labels,
            "inputs_preview": input_df.head(3).to_dict(orient="list"),
            "metadata_path": args.metadata,
        })

if __name__ == "__main__":
    main()