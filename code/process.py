import argparse
import subprocess

import osm

# process region osm file
def process(region):
    # create region direactory
    subprocess.run(['mkdir', '-p', f'csv/{region}'])

    # extract data from osm file
    shopHandler = osm.ShopHandler(region)
    shopHandler.apply_file(f'region/{region}.osm')

    # save extracted data to csv files
    shopHandler.to_csv()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-region', '--region', help='process osm file', type=str)
    region = parser.parse_args().region

    process(region)
