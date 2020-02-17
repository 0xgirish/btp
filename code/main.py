import matplotlib.pyplot as plt
import pandas as pd

import util
import constants
from algo import Model
from result import show_gacluster
from process import process 

# Create geneatic algorithm for set cover problem using fixed radius circles
if __name__ == '__main__':
    region, tag = util.parse_arguments()
    df = util.get_data(region)
    constants.initialize(region, tag)

    Model.Init(df, constants.RADIUS, constants.N_CIRCLES)
    models = [Model() for _ in range(constants.POPULATION)]
    fitness_per_iteration = []
    best_model_centers = None

    EPOCHS = constants.EPOCHS
    for i in range(EPOCHS):
        fitness = [model.fitness() for model in models]
        model_fitness = zip(fitness, models)
        model_fitness = sorted(model_fitness, key=lambda k: k[0], reverse=True)
        fitness_per_iteration.append(model_fitness[0][0])
        population = []

        for j in range(constants.POPULATION):
            population.append(model_fitness[j][1])

        models = Model.new_generation(population)
        best_model_centers = model_fitness[0][1].centers
        print(f'iterations: {i}, fitness: {model_fitness[0][0]}')


    df.to_csv(f'experiments/#{tag}/csv/{region}.csv', index=False)
    pd.DataFrame(best_model_centers, columns=['lat', 'lon']).to_csv(f'experiments/#{tag}/csv/centers.{region}.csv', index=Flase)

    plt.plot([i for i in range(0, EPOCHS)], fitness_per_iteration)
    plt.xlabel('iterations')
    plt.ylabel('best fitness')
    plt.savefig(f'experiments/#{tag}/fig/{region}.genetic.png', format='png')
    plt.show()

    show_gacluster(df, region, tag)
