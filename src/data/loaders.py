def load_raw_data(file_path):
    import pandas as pd
    return pd.read_csv(file_path)

def load_processed_data(file_path):
    import pandas as pd
    return pd.read_csv(file_path)

def save_processed_data(data, file_path):
    data.to_csv(file_path, index=False)

def load_data(file_path, processed=False):
    if processed:
        return load_processed_data(file_path)
    else:
        return load_raw_data(file_path)