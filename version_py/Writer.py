import csv
import json

# all functions that will be used to write shortest path experiments stats to csv files


def writeExp1StatsToCsv(stats, header, filename):
    """
    Takes a dictionary of statistics and write rows in csv file
    => keys = title for 1 row, values = 1 row data
    ex : {"Dijkstra" : {"CT": 0.1}, "ALT": {"CT": 0.2}}
        Dijkstra,   0.1
        ALT,        0.2
    """
    with open(filename, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)

        # write the header
        writer.writerow(header)

        for p in stats.keys():
            data = [p] + list(stats[p].values())

            # write the data
            writer.writerow(data)

def writePreprocessingStatsToCsv(stats, header, filename):
    with open(filename, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)

        # write the header
        writer.writerow(header)

        # write the data
        writer.writerow(stats)

def writeExp7StatsToCsv(stats, header, filename):
    with open(filename, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)

        # write the header
        writer.writerow(header)

        for p in stats.keys():
            data = stats[p]

            # write the data
            writer.writerow(data)
