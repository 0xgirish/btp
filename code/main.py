import argparse
from sys import argv
from sklearn.cluster import KMeans
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

def kmean_draw(df, region):
    data = df.values[:, 1:]
    km = KMeans(n_clusters=12, random_state=0)
    km.fit(data)

    prediction = km.predict(data)
    centers = km.cluster_centers_

    sns.scatterplot(x="lat", y="lon", data=df, hue=prediction)
    plt.plot(centers[:, 0], centers[:, 1], 'o')
    plt.savefig(f'fig/{region}.kmean.png', format='png')
    plt.show()

# Create geneatic algorithm for set cover problem using fixed radius circles
if __name__ == '__main__':
    df, region, is_osm = parse_arguments()
    # util.draw(df, region)
    if is_osm:
        util.to_csv(df, region)
    # kmean_draw(df, region)
    Model.Init(df, RADIUS, N_CIRCLES)

    models = [Model() for _ in range(POPULATION)]
    fitness_per_iteration = []
    best_model_ceters = None

    for i in range(100):
        fitness = [model.fitness() for model in models]
        model_fitness = zip(fitness, models)
        model_fitness = sorted(model_fitness, key=lambda k: k[0], reverse=True)
        fitness_per_iteration.append(model_fitness[0][0])
        population = []

        for i in range(POPULATION):
            population.append(model_fitness[i][1])

        models = Model.new_generation(population)
        best_model_ceters = model_fitness[0][1].centers
        print(model_fitness[0][0])

    print('---------------------------------------')
    print(f'{best_model_ceters}')
    print('---------------------------------------')

    plt.plot([i for i in range(1, 101)], fitness_per_iteration)
    plt.xlabel('iterations')
    plt.ylabel('best fitness')
    plt.savefig(f'fig/{region}.genetic.png', format='png')
    plt.show()
