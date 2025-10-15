# Project 1: Penguin Data Analysis
# Your name: Harold Wilson
# Your student id: 45483282 
# Your email: hwil@umich.edu
# I used GenAi in order to find out what is wrong with the code and to explain the code.


# Function: import_data
def import_data(filename):
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
