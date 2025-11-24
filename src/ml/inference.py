from sklearn.externals import joblib
import numpy as np

class InferenceModel:
    def __init__(self, model_path):
        self.model = joblib.load(model_path)

    def predict(self, input_data):
        processed_data = self.preprocess(input_data)
        prediction = self.model.predict(processed_data)
        return prediction

    def preprocess(self, input_data):
        # Implement preprocessing steps here
        # For example, scaling or encoding
        return np.array(input_data).reshape(1, -1)  # Example reshape for a single sample

def load_model(model_path):
    return InferenceModel(model_path)

def make_prediction(model, input_data):
    return model.predict(input_data)