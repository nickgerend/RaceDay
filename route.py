# Written by: Nick Gerend, @dataoutsider
# Viz: "Race Day", enjoy!

import json
import csv
import os

def main():
    with open(os.path.dirname(__file__) + '/boston_marathon.geojson') as json_file: 
        geojson_data = json.load(json_file) 
    if geojson_data['type'] == 'FeatureCollection':
        out = open(os.path.dirname(__file__) + '/boston_marathon.csv', 'w') 
        parse_feature_collection(geojson_data['features'], out)
    else:
        print("Can currently only parse FeatureCollections, but I found ", geojson_data['type'], " instead")

def parse_feature_collection(features, outfile):

    # create the csv writer object
    csvwriter = csv.writer(outfile, lineterminator='\n') #, lineterminator='\n'os.linesep

    count = 0
    header = []
    for feature in features[0]['geometry']['coordinates']:
        if count == 0:
            header.append(['Longitude', 'Latitude'])
            csvwriter.writerow(header)
            count += 1
        csvwriter.writerow(feature)
    outfile.close()

if __name__ == "__main__":
    main()