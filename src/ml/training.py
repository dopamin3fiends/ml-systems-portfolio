from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pandas as pd

def load_data(file_path):
    """Load dataset from a CSV file."""
    data = pd.read_csv(file_path)
    return data

def preprocess_data(data):
    """Preprocess the data for training."""
    # Example preprocessing steps
    data.fillna(0, inplace=True)
    X = data.drop('target', axis=1)
    y = data['target']
    return X, y

def train_model(X, y, n_estimators=100, test_size=0.2):
    """Train a Random Forest model."""
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
    model = RandomForestClassifier(n_estimators=n_estimators)
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    return model, accuracy

def save_model(model, file_path):
    """Save the trained model to a file."""
    import joblib
    joblib.dump(model, file_path)

def load_model(file_path):
    """Load a trained model from a file."""
    import joblib
    model = joblib.load(file_path)
    return model

# Example usage:
# data = load_data('data/processed/dataset.csv')
# X, y = preprocess_data(data)
# model, accuracy = train_model(X, y)
# save_model(model, 'models/checkpoints/model.joblib')