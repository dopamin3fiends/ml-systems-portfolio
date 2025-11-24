from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd

class ML_Pipeline:
    def __init__(self, model, data):
        self.model = model
        self.data = data
        self.pipeline = None

    def preprocess_data(self):
        # Implement data preprocessing steps here
        X = self.data.drop('target', axis=1)
        y = self.data['target']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        return X_train, X_test, y_train, y_test

    def create_pipeline(self):
        # Example pipeline with scaling and model
        self.pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('model', self.model)
        ])

    def train(self):
        X_train, X_test, y_train, y_test = self.preprocess_data()
        self.create_pipeline()
        self.pipeline.fit(X_train, y_train)
        predictions = self.pipeline.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        return accuracy

    def predict(self, new_data):
        if self.pipeline is None:
            raise Exception("Pipeline not trained. Call train() before predicting.")
        return self.pipeline.predict(new_data)