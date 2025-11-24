import pandas as pd
import numpy as np
import os

def extract_data(raw_data_path):
    """Extracts data from the specified raw data path."""
    data_files = [f for f in os.listdir(raw_data_path) if f.endswith('.csv')]
    data_frames = []
    
    for file in data_files:
        file_path = os.path.join(raw_data_path, file)
        df = pd.read_csv(file_path)
        data_frames.append(df)
    
    return pd.concat(data_frames, ignore_index=True)

def transform_data(df):
    """Transforms the extracted data."""
    # Example transformation: fill missing values and normalize
    df.fillna(method='ffill', inplace=True)
    df = (df - df.mean()) / df.std()  # Standardization
    return df

def load_data(df, processed_data_path):
    """Loads the transformed data to the specified processed data path."""
    if not os.path.exists(processed_data_path):
        os.makedirs(processed_data_path)
    
    output_file = os.path.join(processed_data_path, 'processed_data.csv')
    df.to_csv(output_file, index=False)

def main():
    raw_data_path = '../data/raw'
    processed_data_path = '../data/processed'
    
    # ETL process
    raw_data = extract_data(raw_data_path)
    transformed_data = transform_data(raw_data)
    load_data(transformed_data, processed_data_path)

if __name__ == "__main__":
    main()