import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

def get_engine():
    """
    Create SQLAlchemy engine from environment variables.
    """
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME")

    if not all([db_user, db_password, db_host, db_name]):
        raise ValueError("Missing one or more required database environment variables.")

    conn_str = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}?sslmode=require"
    return create_engine(conn_str)


def load_to_db(df: pd.DataFrame, table_name: str = "crypto_paprika") -> None:
    """
    Load transformed DataFrame into PostgreSQL using SQLAlchemy.
    """
    if df.empty:
        print("Warning: DataFrame is empty. Skipping load.")
        return

    try:
        engine = get_engine()
        df.to_sql(
            name=table_name,
            con=engine,
            if_exists='replace',
            index=False,
            method='multi',
            chunksize=1000
        )
        print(f"Successfully loaded {len(df)} records into table '{table_name}'.")
    except Exception as e:
        print(f"Error loading data to database: {e}")
        raise