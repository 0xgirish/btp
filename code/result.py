import argparse
from sys import argv

from sklearn.cluster import KMeans
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
# from sklearn.cluster import KMeans
import util
from constants import RADIUS, N_CIRCLES, POPULATION
from algo import Model

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-format', '--format', help='format of the file from which to extract dataframe', type=str)
    parser.add_argument('-region', '--region', help='name of the region for data', type=str)
    parser.set_defaults(format='csv')

    args = parser.parse_args()
    df = util.get_restaurants(args.region, args.format == 'csv')
    return df, args.region, args.format != 'csv'

# Create geneatic algorithm for set cover problem using fixed radius circles
if __name__ == '__main__':
    df, region, is_osm = parse_arguments()
    # util.draw(df, region)
    if is_osm:
        util.to_csv(df, region)

    centers = pd.read_csv(f'csv/{region}.centers.csv').values[:, 1:]
    
    Model.Init(df, RADIUS, N_CIRCLES)
    model = Model(gnome=centers)
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
    plt.savefig(f'fig/{region}.gacluster.png', format='png')
    plt.show()
