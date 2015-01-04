import random
import numpy

from deap import base
from deap import tools
from deap import creator
from deap import algorithms


NPOP = 100
NGEN = 10000
IND_SIZE = 5
CXPB = 0.7
MUTPB = 0.001

random.seed()
creator.create("FitnessMax", base.Fitness,
               weights=(-1.0, 1.0))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("attr_float", random.uniform, 0, 100)
toolbox.register("attr_int", random.randint, 0, 100)
toolbox.register("attr_int", random.randint, 0, 100)
toolbox.register("attr_int", random.randint, 0, 100)
toolbox.register("attr_int", random.randint, 1, 7)
toolbox.register("individual", tools.initRepeat, creator.Individual,
                 toolbox.attr_float, n=IND_SIZE)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def evaluateInd(individual):
    a = sum(individual)
    b = len(individual)
    return a, 1. / b

toolbox.register("mate", tools.cxBlend, alpha=0.2)
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=2, indpb=0.01)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("evaluate", evaluateInd)

pop = toolbox.population(n=NPOP)
stats = tools.Statistics(key=lambda ind: ind.fitness.values)
stats.register("avg", numpy.mean)
stats.register("std", numpy.std)
stats.register("min", numpy.min)
stats.register("max", numpy.max)
pop, logbook = algorithms.eaSimple(pop, toolbox, CXPB, MUTPB, NGEN,
                                   stats=stats, verbose=False)
print logbook


# for g in range(NGEN):
#     # Select the next generation individuals
#     offspring = toolbox.select(pop, len(pop))
#     # Clone the selected individuals
#     offspring = map(toolbox.clone, offspring)

#     # Apply crossover on the offspring
#     for child1, child2 in zip(offspring[::2], offspring[1::2]):
#         if random.random() < CXPB:
#             toolbox.mate(child1, child2)
#             del child1.fitness.values
#             del child2.fitness.values

#     # Apply mutation on the offspring
#     for mutant in offspring:
#         if random.random() < MUTPB:
#             toolbox.mutate(mutant)
#             del mutant.fitness.values

#     # Evaluate the individuals with an invalid fitness
#     invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
#     fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
#     for ind, fit in zip(invalid_ind, fitnesses):
#         ind.fitness.values = fit

#     # The population is entirely replaced by the offspring
#     pop[:] = offspring
