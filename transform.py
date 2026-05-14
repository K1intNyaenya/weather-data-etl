import json
import pandas as pd
from typing import List, Dict, Any

def normalize_json(data: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Normalize JSON data into a pandas DataFrame
    """
    df = pd.json_normalize(data)
    return df

def transform_weather_data(raw_data: Dict[str, Any]) -> pd.DataFrame:
    """
    Applying transformations to the raw weather data 
    """
    df = normalize_json([raw_data])

    # clean column names
    df.columns = df.columns.str.replace("location.", "", regex=False)
    df.columns = df.columns.str.replace("current.", "", regex=False)
    df.columns = df.columns.str.replace(".", "_", regex=False)
    df.columns = df.columns.str.replace("-", "_", regex=False)

    # handle epoch and string datetime columns separately
    epoch_cols = ['last_updated_epoch', 'localtime_epoch']
    string_cols = ['last_updated', 'localtime']

    for col in epoch_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], unit='s', utc=True)

    for col in string_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], utc=True)

    # drop unnecessary columns
    delete_cols = [
        'localtime_epoch',
        'last_updated_epoch',
        'air_quality_us_epa_index',
        'air_quality_gb_defra_index'
    ]
    df.drop(columns=delete_cols, inplace=True, errors='ignore')

    return df

if __name__ == "__main__":
    with open("nairobi_weather_data.json", "r") as file:
        raw_data = json.load(file)
    
    df = transform_weather_data(raw_data)
    print(df.head())