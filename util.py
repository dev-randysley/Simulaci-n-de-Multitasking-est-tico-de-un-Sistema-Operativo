import csv

def parse_csv(filename):
    records = []
    with open(filename) as f:
        for line in f:
            if(line != '\n'):
                records.append(line)
    return records