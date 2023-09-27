import csv
import pandas as pd

def remove_duplicates_end_process():

    # Input and output filenames
    input_file = 'end_process.csv'
    output_file = 'end_process_unique.csv'


    # Create a set to store unique keys from the first column
    unique_keys = set()

    # Open the input CSV file for reading and the output CSV file for writing
    with open(input_file, mode='r', newline='') as infile, open(output_file, mode='w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Iterate through the rows in the input file
        for row in reader:
            # Check if the row has at least one element
            if len(row) > 0:
                key = row[2]
                if key not in unique_keys:
                    unique_keys.add(key)
                    # Write the entire row to the output file
                    writer.writerow(row)

    print("Adresses : Duplicate rows based on the Address column removed. Output saved to", output_file)

def remove_duplicates_deployers():
    # Input and output filenames
    input_file = 'deployer_addresses.csv'
    output_file = 'deployer_addresses_unique.csv'


    # Create a set to store unique keys from the first column
    unique_keys = set()

    # Open the input CSV file for reading and the output CSV file for writing
    with open(input_file, mode='r', newline='') as infile, open(output_file, mode='w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Iterate through the rows in the input file
        for row in reader:
            # Check if the row has at least one element
            if len(row) > 0:
                key = row[2]
                if key not in unique_keys:
                    unique_keys.add(key)
                    # Write the entire row to the output file
                    writer.writerow(row)

    print("Deployers: Duplicate rows based on the Address column removed. Output saved to", output_file)

def order_by_date_deployers():
    # Load the CSV file into a DataFrame
    df = pd.read_csv('deployer_addresses_unique.csv')

    # Convert the 'Date' column to datetime format
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y', errors='coerce')

    # Sort the DataFrame by the 'Date' column in ascending order
    df = df.sort_values(by='Date', ascending=True)

    # Convert the 'Date' column back to the 'mm/dd/yyyy' format without the time part
    df['Date'] = df['Date'].dt.strftime('%m/%d/%Y')

    # Save the sorted DataFrame to a new CSV file
    df.to_csv('sorted_deployer_addresses_unique.csv', index=False)
    
def order_by_date_end_process():
        
    df = pd.read_csv('end_process_unique.csv')

    
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')

    
    df = df.sort_values(by='Date', ascending=True)

    
    # Convert the 'Date' column back to the original format if needed
    df['Date'] = df['Date'].dt.strftime('%m/%d/%Y')

    # Save the sorted DataFrame to a new CSV file
    df.to_csv('end_process_unique.csv', index=False)

def combine_df():
    # Load the second CSV file into a DataFrame
    df1 = pd.read_csv('sorted_deployer_addresses_unique.csv')
    # Load the second CSV file into a DataFrame
    df2 = pd.read_csv('end_process_unique.csv')

    # Filter the 'Address' column for rows with the value 'Address'
    filtered_df2 = df2[df2['Type'] == 'Address']
   
    # Concatenate both DataFrames vertically (stack them on top of each other)
    combined_df = pd.concat([df1, filtered_df2], ignore_index=True)

    combined_df['Date'] = pd.to_datetime(combined_df['Date'], format='%m/%d/%Y')

    
    combined_df = combined_df.sort_values(by='Date', ascending=True)

    
    # Convert the 'Date' column back to the original format if needed
    combined_df['Date'] = combined_df['Date'].dt.strftime('%m/%d/%Y')


    return combined_df

def write_non_matching_rows():
    # Load the existing combined CSV file, if it exists
    new_df = combine_df()
    
    try:
        combined_df = pd.read_csv('combined_file.csv')
    except FileNotFoundError:
        # If the file doesn't exist, assume an empty DataFrame
        combined_df = pd.DataFrame()

    # Check if the DataFrames have the same columns
    if not new_df.columns.equals(combined_df.columns):
        print("Columns in the provided DataFrame do not match with the combined CSV.")
        return

    # Find non-matching rows between the provided DataFrame and the combined CSV
    non_matching_rows = new_df[~new_df.isin(combined_df.to_dict('list')).all(axis=1)]
    

    if not non_matching_rows.empty:
        print("Found non-matching rows:")
        print(non_matching_rows)

        # Concatenate the non-matching rows with the existing combined DataFrame
        combined_df = pd.concat([combined_df, non_matching_rows])

        # Drop duplicate rows based on all columns
        combined_df.drop_duplicates(inplace=True, keep='first')

        # Save the updated combined DataFrame to the combined CSV file
        combined_df.to_csv('combined_file.csv', index=False)
        print("Combined CSV updated with non-matching rows.")
        return non_matching_rows

async def remove_duplicate_addresses():    
    remove_duplicates_end_process()
    remove_duplicates_deployers()
    order_by_date_end_process()
    order_by_date_deployers()
    new_addresses = write_non_matching_rows()
    return new_addresses

