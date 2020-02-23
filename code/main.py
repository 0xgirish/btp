import matplotlib.pyplot as plt

import util
from constants import RADIUS, N_CIRCLES, POPULATION
from algo import Model

# Create geneatic algorithm for set cover problem using fixed radius circles
if __name__ == '__main__':
    df, region, is_osm, expno = util.parse_arguments()
    # util.draw(df, region)
    if is_osm:
        util.to_csv(df, region)
    # kmean_draw(df, region)
    Model.Init(df, RADIUS, N_CIRCLES)

    models = [Model() for _ in range(POPULATION)]
    fitness_per_iteration = []
    best_model_centers = None

    EPOCHS = 150
    for i in range(EPOCHS):
        fitness = [model.fitness() for model in models]
        model_fitness = zip(fitness, models)
        model_fitness = sorted(model_fitness, key=lambda k: k[0], reverse=True)
        fitness_per_iteration.append(model_fitness[0][0])
        population = []

        for j in range(POPULATION):
            population.append(model_fitness[j][1])

        models = Model.new_generation(population)
        best_model_centers = model_fitness[0][1].centers
        print(f'iterations: {i}, fitness: {model_fitness[0][0]}')

    print('---------------------------------------')
    print(f'{best_model_centers}')
    print('---------------------------------------')

    plt.plot([i for i in range(0, EPOCHS)], fitness_per_iteration)
    plt.xlabel('iterations')
    plt.ylabel('best fitness')
    plt.savefig(f'experiments/exp-{expno}/fig/{region}.genetic.png', format='png')
#   plt.show()
