# Two options
# 1. Create table and use Copy command
# 2. Load and create at the same time

#Using Option number 2

# Library
import psycopg2
import pandas as pd
from sqlalchemy import create_engine, text

# Define the database connection parameters
db_params = {
    'host': '192.168.0.50',
    'database': 'postgres',
    'user': 'testuser',
    'password': 'palomero'
}

# Create a connection to the PostgreSQL server
conn = psycopg2.connect(
    host=db_params['host'],
    database=db_params['database'],
    user=db_params['user'],
    password=db_params['password']
)

# Create a cursor object
cur = conn.cursor()

# Set automatic commit to be true, so that each action is committed without having to call conn.committ() after each command
conn.set_session(autocommit=True)

# Create the 'soccer' database
#cur.execute("CREATE DATABASE formuladata")

# Commit the changes and close the connection to the default database
conn.commit()
cur.close()
conn.close()

#Change database attr
db_params['database']='formuladata'

#Create engine with SQLAlchemy
engine= create_engine(f'postgresql://{db_params["user"]}:{db_params["password"]}@{db_params["host"]}/{db_params["database"]}')

#Define path to data files
path_to_files= r'C:\Users\palom\OneDrive\Documentos\GitHub\DataEngineeringF1\data'

#Get all csv file paths
csv_files = {
    'circuits': path_to_files+"\circuits.csv",
    'constructor_results': path_to_files+"\constructor_results.csv",
    'constructor_standings': path_to_files+"\constructor_standings.csv",
    'constructors': path_to_files+"\constructors.csv",
    'driver_standings': path_to_files+"\driver_standings.csv",
    'drivers': path_to_files+"\drivers.csv",
    'lap_times': path_to_files+"\lap_times.csv",
    'pit_stops': path_to_files+"\pit_stops.csv",
    'qualifying': path_to_files+"\qualifying.csv",
    'races': path_to_files+r"\races.csv",  #add "r" because of \r
    'results': path_to_files+r"\results.csv", #add "r" because of \r
    'seasons': path_to_files+"\seasons.csv",
    'sprint_results': path_to_files+"\sprint_results.csv",
    'status': path_to_files+"\status.csv"
}

# Check table structures
""""
for table_name, file_path in csv_files.items():
    print(f"Contents of '{table_name}' CSV file:")
    df = pd.read_csv(file_path)
    print(df.head(1))  # Display the first few rows of the DataFrame
    print("\n")
"""

# Use to_sql method to import tables to PostgreSQL from csv

for table_name, file_path in csv_files.items():
    df = pd.read_csv(file_path)
    df.to_sql(table_name, engine, if_exists='replace', index=False)
