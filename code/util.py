import argparse
import subprocess
from sys import argv

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from geopy.distance import geodesic

from process import process
import osm
import constants

# get distance between two coordinates, e.g. geodistance((23.44, 78.234234), (34.13132, 76.432345))
geodistance = lambda u, v: geodesic(set(u), set(v)).km

# get distance between two xy coordinates, for xytrasformed data
distance = lambda u, v: np.sqrt(np.sum((u-v)**2))

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
    df.to_csv(f'csv/{region}.csv', index=False)

# parser arguments and create subdireactories for experiments
def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-exp-tag', '--tag', help='experiment tag to organize results', type=str)
    parser.add_argument('-region', '--region', help='name of the region for data', type=str)

    args = parser.parse_args()
    constants.change_seed(args.seed)
    initialize_exp(args.tag)
    return args.region, args.tag

def initialize_exp(tag):
     subprocess.run(['mkdir', '-p', f'experiments/#{tag}/csv', f'experiments/#{tag}/fig'])
