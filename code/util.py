import argparse
import subprocess
from sys import argv

import osmium as osm
from sklearn.cluster import KMeans
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from geopy.distance import vincenty

import constants

# get distance between two coordinates, e.g. geodistance((23.44, 78.234234), (34.13132, 76.432345))
def geodistance(pos1, pos2):
    pos1, pos2 = set(pos1), set(pos2)
    return vincenty(pos1, pos2).km


# ShopHandler extract restaurant's locations from the osm file
class ShopHandler(osm.SimpleHandler):
    def __init__(self):
        osm.SimpleHandler.__init__(self)
        self.osm_data = []

    def shops(self, elem):
        if ShopHandler.is_restaurant(elem):
            self.osm_data.append(ShopHandler.getLocation(elem.location))

    def node(self, n):
        self.shops(n)

    @staticmethod
    def is_restaurant(elem):
        for tag in elem.tags:
            if tag.v == 'restaurant':
                return True
        return False

    @staticmethod
    def getLocation(location):
        return [float(location.lat), float(location.lon)]

# get restaurant locations from the osm file as a pandas dataframe
def get_restaurants(region, csv=False):
    if csv:
        return pd.read_csv(f'csv/{region}.csv')

    shopHandler = ShopHandler()
    shopHandler.apply_file(f'region/{region}.osm')
    print(f'Number of restaurants in the region {region}: {len(shopHandler.osm_data)}')

    data_columns = ["lat", "lon"]
    return pd.DataFrame(shopHandler.osm_data, columns=data_columns)


# draw restaurants locations and save the figure
def draw(df, region, tag):
    sns.jointplot(x="lat", y="lon", data=df)
    plt.savefig(f'experiments/#{tag}/fig/{region}.png', format='png')
    plt.show()


# save the result of dataframe to csv file
def to_csv(df, region):
    df.to_csv(f'csv/{region}.csv')

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-format', '--format', help='format of the file from which to extract dataframe', type=str)
    parser.add_argument('-exp-tag', '--tag', help='experiment tag to organize results', type=str)
    parser.add_argument('-region', '--region', help='name of the region for data', type=str)
    parser.add_argument('-seed', '--seed', help='random seed for the experiment', type=int)
    parser.set_defaults(format='csv', seed=None)

    args = parser.parse_args()
    constants.change_seed(args.seed)
    initialize_exp(args.tag)
    df = get_restaurants(args.region, args.format == 'csv')
    return df, args.region, args.format != 'csv', args.tag

def kmean_draw(df, region, tag):
    data = df.values[:, 1:]
    km = KMeans(n_clusters=12, random_state=0)
    km.fit(data)

    prediction = km.predict(data)
    centers = km.cluster_centers_

    sns.scatterplot(x="lat", y="lon", data=df, hue=prediction)
    plt.plot(centers[:, 0], centers[:, 1], 'o')
    plt.savefig(f'experiments/#{tag}/fig/{region}.kmean.png', format='png')
    plt.show()

def initialize_exp(tag):
    subprocess.run(['mkdir', '-p', f'experiments/#{tag}/csv', f'experiments/#{tag}/fig'])
