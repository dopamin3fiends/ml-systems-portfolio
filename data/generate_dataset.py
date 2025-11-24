from pathlib import Path
import sys
from sklearn.datasets import load_iris
import pandas as pd


def main():
	# Determine directory relative to this script to avoid surprises with CWD
	base_dir = Path(__file__).resolve().parent
	processed_dir = base_dir / "processed"
	processed_dir.mkdir(parents=True, exist_ok=True)

	try:
		iris = load_iris(as_frame=True)
	except Exception as e:
		print("Failed to load Iris dataset:", e, file=sys.stderr)
		raise

	# Prefer the provided frame if available
	if hasattr(iris, "frame") and iris.frame is not None:
		df = iris.frame.copy()
	else:
		df = pd.DataFrame(iris.data, columns=iris.feature_names)

	# Ensure a target column exists
	if "target" not in df.columns:
		if hasattr(iris, "target"):
			df["target"] = iris.target
		else:
			# Fallback: try target_names or raise
			raise RuntimeError("Iris dataset has no target information")

	output_path = processed_dir / "dataset.csv"
	df.to_csv(output_path, index=False)

	print("Dataset saved to:", output_path)
	print("File exists after write:", output_path.exists())


if __name__ == "__main__":
	main()