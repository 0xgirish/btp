import argparse
from sys import argv
from sklearn.cluster import KMeans

import util

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-format', '--format', help='format of the file from which to extract dataframe', type=str)
    parser.add_argument('-region', '--region', help='name of the region for data', type=str)
    parser.set_defaults(format='csv')

    args = parser.parse_args()
    df = util.get_restaurants(args.region, args.format == 'csv')
    return df, args.region, args.format

# Create geneatic algorithm for set cover problem using fixed radius circles
if __name__ == '__main__':
    df, region, is_csv = parse_arguments()
    util.draw(df, region)
    if not is_csv:
        util.to_csv(df, region)
