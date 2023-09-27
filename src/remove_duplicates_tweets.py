import csv


def remove_duplicates_tweets():

    # Input and output filenames
    input_file = 'tweets.csv'
    output_file = 'tweets_unique.csv'


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
                key = row[0]
                if key not in unique_keys:
                    unique_keys.add(key)
                    # Write the entire row to the output file
                    writer.writerow(row)

    print("Duplicate rows based on the first column removed. Output saved to", output_file)
