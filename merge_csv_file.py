import pandas as pd

def merge_csv_files(file_list, output_file='combined_file.csv'):
    """
    combine csv files into one file
    """
    combined_data = pd.DataFrame()

    for file_path in file_list:
        df = pd.read_csv(file_path)
        combined_data = pd.concat([combined_data, df], ignore_index=True)

    combined_data.to_csv(output_file, index=False)
