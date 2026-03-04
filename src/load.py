from sqlalchemy import create_engine
import os

def load_to_postgres(df, table_name):
    conn_string = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    engine = create_engine(conn_string)
    
    # Use 'append' to simulate a real pipeline adding new data
    df.to_sql(table_name, engine, if_exists='replace', index=False)
    print(f" Data successfully loaded into {table_name} table.")