import argparse
import subprocess

import osm
import numpy as np
from geopy.distance import geodesic


# eculedian and geodistance
edistance, gdistance = lambda u, v: np.sqrt(np.sum((u-v)**2)), lambda u, v: geodesic(set(u), set(v))

# process region osm file
def process(region):
    # create region direactory
    subprocess.run(['mkdir', '-p', f'csv/{region}'])

    # extract data from osm file
    shopHandler = osm.ShopHandler(region)
    shopHandler.apply_file(f'region/{region}.osm')

    # save extracted data to csv files
    shopHandler.to_csv()

    # trasform lat, lon to xy coordinates
    xytransform(region, shopHandler.minlat, shopHandler.minlon)

# lat, lon are minimum lattitude and longitude in entire region
def xytransform(region, lat, lon):
    df = pd.read_csv(f'csv/{region}/shops.csv')

    size = df.shape[0]
    for i in range(size):
        u = df.iloc[i]
        for j in range(size):
            v = df.iloc[j]
            e, g = edistance(u, v), gdistance(u, v).km
            ratios.append(g/e)

    constants = pd.Series(ratios)
    transformed = constants.mean() * (df - np.array([lat, lon]))
    transformed.to_csv(f'csv/{region}/shops.xy.csv', index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-region', '--region', help='process osm file', type=str)
    region = parser.parse_args().region

    process(region)
