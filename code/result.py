import argparse
from sys import argv

from sklearn.cluster import KMeans
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
# from sklearn.cluster import KMeans
import util
import constants 
from algo import Model


def show_gacluster(df, region, tag):
    centers = pd.read_csv(f'experiments/#{tag}/csv/centers.{region}.csv').values
    
    Model.Init(df, constants.RADIUS, constants.N_CIRCLES)
    model = Model(gnome=centers, log=True)
    print(model.fitness())

    Y = [i for i in range(len(centers))]
    y = [len(centers) for i in range(df.shape[0])]
    nodes = df.values[:, 1:]
    for i in range(df.shape[0]):
        for j in range(len(centers)):
            if util.geodistance(nodes[i], centers[j]) <= Model.radius:
                y[i] = j
                break

    sns.scatterplot(x="lat", y="lon", data=df, hue=y)
    plt.plot(centers[:, 0], centers[:, 1], 'o')
    plt.savefig(f'experiments/#{tag}/fig/{region}.gacluster.png', format='png')
    plt.show()

# Create geneatic algorithm for set cover problem using fixed radius circles
if __name__ == '__main__':
    df, region, is_osm, tag = util.parse_arguments()
#   initialize constants for the region and create config file
    constants.initialize(region, tag)
    show_gacluster(df, region, tag)
