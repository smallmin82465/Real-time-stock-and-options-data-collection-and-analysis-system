import os
import pandas as pd
import sqlite3

def csv_to_sqlite(csv_files, db_path):
    """
    Merge the specified CSV files into a single SQLite database,
    with each table named after the CSV file name.

    :param csv_files: A list containing the paths of CSV files
    :param db_path: The path of the SQLite database
    """
    # Create or connect to the SQLite database
    conn = sqlite3.connect(db_path)

    # Process each CSV file individually
    for csv_file in csv_files:
        table_name = os.path.splitext(os.path.basename(csv_file))[0]  # Use the file name as the table name

        # Read the CSV file into a DataFrame
        df = pd.read_csv(csv_file)

        # Write the DataFrame to the SQLite database
        df.to_sql(table_name, conn, index=False, if_exists='replace')

    # Close the database connection
    conn.close()