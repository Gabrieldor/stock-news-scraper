import pandas as pd
from datetime import datetime

def convert_date_format(date_str):
    # Parse the input date string
    date_obj = datetime.strptime(date_str, "%d %b, %Y")
    # Convert to the desired format
    return date_obj.strftime("%b %d, %Y")

def process_csv(input_file, output_file, date_column):
    # Read the CSV file
    df = pd.read_csv(input_file)
    print(df.columns)
    
    # Apply the date format conversion
    df[date_column] = df[date_column].apply(convert_date_format)
    
    # Save the updated DataFrame to a new CSV file
    df.to_csv(output_file, index=False)

# Example usage
input_csv = 'data.csv'
output_csv = 'data2.csv'
date_column_name = 'date'  # Replace with the actual column name containing the dates

process_csv(input_csv, output_csv, date_column_name)
