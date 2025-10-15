# Project 1: Penguin Data Analysis
# Your name: Harold Wilson
# Your student id: 45483282 
# Your email: hwil@umich.edu
# I used GenAi in order to find out what is wrong with the code and to explain the code.


# Function: import_data
def import_data(filename):
    # Reads the CSV file and turns each line into a dictionary.
    # Each key is a column name, and the value is the data for that penguin.
    # It also converts numbers to floats and replaces "NA" with None.
    data = []
    data = []
    file = open(filename, "r")
    lines = file.readlines()
    file.close()

    headers = lines[0].strip().split(",")

    for line in lines[1:]:
        values = line.strip().split(",")
        row = {}
        for i in range(len(headers)):
            value = values[i]
            if value == "NA" or value == "":
                row[headers[i]] = None
            else:
                try:
                    row[headers[i]] = float(value)
                except:
                    row[headers[i]] = value
        data.append(row)
    return data

# Function: get_average
def get_average(values):
    # Takes a list of numbers and returns their average, ignoring missing values.
    total = 0
    count = 0
    for v in values:
        if v is not None:
            total = total + v
            count = count + 1
    if count == 0:
        return 0
    else:
        return total / count
    
# Function: calc_avg_flipper_by_species_and_sex
def calc_avg_flipper_by_species_and_sex(data):
    # Groups penguins by species AND sex.
    # Example key: ("Adelie", "male")
    # Then calculates the average flipper length for each group.
    grouped = {}
    for row in data:
        species = row.get("species")
        sex = row.get("sex")
        flipper = row.get("flipper_length_mm")
        if species is not None and sex is not None and flipper is not None:
            key = (species, sex)
            if key not in grouped:
                grouped[key] = []
            grouped[key].append(flipper)

    results = {}
    for key in grouped:
        results[key] = get_average(grouped[key])
    return results

# Function: calc_ratio_by_species
def calc_ratio_by_species(data):
    # For each species, calculates:
    # ratio = (average flipper length) / (average bill length)
    # This shows how the penguin's flippers compare to its beak in size!
    grouped = {}
    for row in data:
        species = row.get("species")
        flipper = row.get("flipper_length_mm")
        bill = row.get("bill_length_mm")
        if species is not None and flipper is not None and bill is not None:
            if species not in grouped:
                grouped[species] = {"flipper": [], "bill": []}
            grouped[species]["flipper"].append(flipper)
            grouped[species]["bill"].append(bill)

    results = {}
    for species in grouped:
        avg_flipper = get_average(grouped[species]["flipper"])
        avg_bill = get_average(grouped[species]["bill"])
        if avg_bill == 0:
            ratio = 0
        else:
            ratio = avg_flipper / avg_bill
        results[species] = ratio
    return results

# Function: write_results_to_file
def write_results_to_file(filename, results1, results2):
    # Writes the results of both calculations to a text file.
    # This serves as a report summarizing the findings.
    f = open(filename, "w")
    f.write("Average Flipper Length by Species and Sex\n")
    for key in results1:
        species, sex = key
        avg = round(results1[key], 2)
        f.write(species + " (" + sex + "): " + str(avg) + " mm\n")

    f.write("\nRatio of Average Flipper to Bill Length (per Species)\n")
    for species in results2:
        ratio = round(results2[species], 3)
        f.write(species + ": " + str(ratio) + "\n")

    f.close()