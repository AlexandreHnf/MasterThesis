import csv
import json
from Constants import *


# all functions that will be used to write shortest path experiments stats to csv files


def writeDictDictStatsToCsv(stats, header, filename):
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


def writeSingleRowStatsToCsv(stats, header, filename):
    with open(filename, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)

        # write the header
        writer.writerow(header)

        # write the data
        writer.writerow(stats)


def writeDictStatsToCsv(stats, header, filename):
    with open(filename, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)

        # write the header
        writer.writerow(header)

        for p in stats.keys():
            data = stats[p]

            # write the data
            writer.writerow(data)


def dicToJson(stats, filename):
    # Serializing json

    with open(filename, "w") as outfile:
        json.dump(stats, outfile, indent=4)


def jsonToDic(filename):
    # Opening JSON file as a dictionary
    with open(filename) as json_file:
        data = json.load(json_file)

    return data


def getJsonData(filename):
    """
    parse json file and return all data in json format
    """
    # read file
    with open(filename, 'r', encoding=ENCODING) as myfile:
        data = myfile.read()
    return json.loads(data)
