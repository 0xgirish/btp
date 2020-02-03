import argparse
import subprocess
from sys import argv

from sklearn.cluster import KMeans
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from geopy.distance import vincenty

from process import process
import osm
import constants

# get distance between two coordinates, e.g. geodistance((23.44, 78.234234), (34.13132, 76.432345))
def geodistance(pos1, pos2):
    pos1, pos2 = set(pos1), set(pos2)
    return vincenty(pos1, pos2).km

def get_data(region):
    try:
        return pd.read_csv(f'csv/{region}/shops.csv')
    except FileNotFoundError:
        print(f'file not found: "csv/{region}/shops.csv"')
        return process(region)


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
    parser.add_argument('-exp-tag', '--tag', help='experiment tag to organize results', type=str)
    parser.add_argument('-region', '--region', help='name of the region for data', type=str)

    args = parser.parse_args()
    constants.change_seed(args.seed)
    initialize_exp(args.tag)
    return args.region, args.tag

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
