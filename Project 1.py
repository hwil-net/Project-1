# Project 1: Penguin Data Analysis
# Your name: Harold Wilson
# Your student id: 45483282 
# Your email: hwil@umich.edu
# I used GenAi in order to find out what is wrong with the code and to explain the code.

# Data Loading and Processing Functions
import csv

def import_data(filename):
    """
    Reads a CSV file using the csv module to correctly handle formatting.
    
    This function converts numeric values to floats and handles missing data
    by converting 'NA' or empty strings to None.
    """
    data = []
    try:
        with open(filename, "r", newline="") as file:
            # DictReader automatically uses the first row as headers
            # and reads each subsequent row as a dictionary.
            # Creats a reader object that maps rows to dictionarys
            reader = csv.DictReader(file)
            
            for row in reader:
                processed_row = {}
                # The first column is unnamed, so we can ignore it.
              
                for key, value in row.items():
                    # Skip the empty first column header if it exists
                    if key is None or key == "":
                        continue
                    
                    # Convert 'NA' or empty strings to None
                    if value == "NA" or value == "":
                        processed_row[key] = None
                    else:
                        # Try to convert to a number, otherwise keep as string
                        # Atempt to convert value to a float
                        try:
                            processed_row[key] = float(value)
                        except ValueError:
                            processed_row[key] = value
                data.append(processed_row)

    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        return [] # Return an empty list if file doesn't exist
        
    return data

def get_average(values):
    """Takes a list of numbers and returns their average, ignoring None values."""
    
    # Filter out any None values form the list
    valid_values = [v for v in values if v is not None]
    
    if not valid_values:
        return 0.0
    
    # Calculate teh average
    return sum(valid_values) / len(valid_values)

# Analysis Functions

def calc_avg_flipper_by_species_and_sex(data):
    """
    Groups penguins by species and sex to calculate the average flipper length.
    """
    grouped = {}
    for row in data:
        # Using .get() is safe as it returns None if a key is missing
        species = row.get("species")
        sex = row.get("sex")
        flipper = row.get("flipper_length_mm")

        # Ensure all required data points are present before processing
        # We only want rows with complete data for this calclation
        if species and sex and flipper is not None:
            key = (species, sex)
            if key not in grouped:
                grouped[key] = []
            grouped[key].append(flipper)

    # Use a dictionary comprehension for a more compact and Pythonic way to build the result
    # Calculate the averge for each group
    results = {key: get_average(lengths) for key, lengths in grouped.items()}
    return results

def calc_ratio_by_species(data):
    """
    For each species, calculates the ratio of average flipper length to average bill length.
    """
    grouped = {}
    for row in data:
        species = row.get("species")
        flipper = row.get("flipper_length_mm")
        bill = row.get("bill_length_mm")

        if species and flipper is not None and bill is not None:
            # If we hav'nt seen this species before, initialize it
            if species not in grouped:
                # Initialize with empty lists for both metrics
                grouped[species] = {"flipper": [], "bill": []}
            grouped[species]["flipper"].append(flipper)
            grouped[species]["bill"].append(bill)

    results = {}
    for species, measurements in grouped.items():
        avg_flipper = get_average(measurements["flipper"])
        avg_bill = get_average(measurements["bill"])
        
        # Avoid division by zero
        # Make shure we dont divide by zero
        if avg_bill != 0:
            results[species] = avg_flipper / avg_bill
        else:
            results[species] = 0.0
    return results

# Output Function

def write_results_to_file(filename, results1, results2):
    """Writes the analysis results to a summary text file."""
    
    # Open the file in 'w' rite mode
    with open(filename, "w") as f:
        f.write("Average Flipper Length by Species and Sex\n")
        f.write("-----------------------------------------\n")
        for (species, sex), avg in results1.items():
            # Write the formated result string
            f.write(f"{species} ({sex}): {avg:.2f} mm\n")

        f.write("\nRatio of Average Flipper to Bill Length (per Species)\n")
        f.write("-----------------------------------------------------\n")
        for species, ratio in results2.items():
            f.write(f"{species}: {ratio:.3f}\n")

# Main Function

def main():
    """Main function to run the data analysis pipeline."""
    # Step 1: Read the penguin data from the CSV file
    # Call our function to load the data frum the file
    data = import_data("penguins.csv")
    
    # If data loading failed, stop execution.
    if not data:
        print("Halting analysis due to data loading error.")
        return

    # Step 2: Perform both calculations
    avg_flipper_lengths = calc_avg_flipper_by_species_and_sex(data)
    flipper_to_bill_ratios = calc_ratio_by_species(data)

    # Step 3: Save the results to a file
    # Save the results too a text file
    write_results_to_file("penguin_results.txt", avg_flipper_lengths, flipper_to_bill_ratios)

    # Step 4: Inform the user
    print("Analysis is now complete. The results are saved as penguin_results.txt and can be found in the same folder as you ran this file.")

if __name__ == "__main__":
    # I uncommented because the tests were successful
    # test_calc_avg_flipper_by_species_and_sex()
    # test_calc_ratio_by_species()
    
    # Run the main program
    # This is the main entry point of the script
    main()