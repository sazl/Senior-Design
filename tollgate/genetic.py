# ===============================================================================
# Chromosome:
# ===============================================================================
#   (price, edge_id, min_edge_length, edge_offset, operating_hours)
# -------------------------------------------------------------------------------
# price: MIN - MAX
# -------------------------------------------------------------------------------
# edge_id: in edges
# min_edge_length: MIN
# edge_offset: N
#    min_edge_length > edge_offset
# -------------------------------------------------------------------------------
# operating_hours:
#   1 = 16:00 - 00:00
#   2 = 08:00 - 16:00
#   4 = 00:00 - 08:00
#   3 = 08:00 - 16:00, 16:00 - 00:00
#   5 = 00:00 - 08:00, 16:00 - 00:00
#   6 = 00:00 - 08:00, 08:00 - 16:00
#   7 = 00:00 - 08:00, 08:00 - 16:00, 16:00 - 00:00
# -------------------------------------------------------------------------------

import random
import numpy

from deap import base
from deap import tools
from deap import creator
from deap import algorithms

from constant   import *
from options    import settings
from simulation import state, run_genetic_algorithm
from tollgate   import tollgate

NPOP = 100
NGEN = 10000
IND_SIZE = 5
CXPB = 0.7
MUTPB = 0.001

toolbox = base.Toolbox()

def individual_to_tollgates(individual):
    return [Tollgate(*individual[i:i+INDIVIDUAL_SIZE])
            for i in range(0, len(individual), INDIVIDUAL_SIZE)]
            
def evaluate_fitness(individual):
    tollgates = individual_to_tollgates(individual)
    run_genetic_algorithm(tollgates)
    return     

def initialize():
    random.seed()
    creator.create("FitnessMax", base.Fitness, weights=(-1.0, 1.0))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    toolbox.register("price", random.uniform,
                     settings.tollgate_min_price,
                     settings.tollgate_max_price)
    tooblox.register("edge_id", random.sample, state.edges, 1)
    toolbox.register("edge_offset", random.randint,
                     settings.tollgate_min_offset,
                     settings.tollgate_min_lane_length)
    toolbox.register("operating_hours", random.randint, 1, 7)
    toolbox.register("individual", tools.initRepeat, creator.Individual,
                     ( toolbox.price,
                       toolbox.edge_id,
                       toolbox.min_edge_length,
                       toolbox.edge_offset,
                       toolbox.operating_hours )
    )
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("mate", tools.cxBlend, alpha=settings.crossover_blend_alpha)
    toolbox.register("mutate", tools.mutGaussian,
                     mu=settings.mutation_guassian_mean,
                     sigma=settings.mutation_guassian_sigma,
                     indpb=settings.mutation_independent_probability)
    toolbox.register("select", tools.selTournament, tournsize=3)
    toolbox.register("evaluate", evaluate_fitness)

def run():
    stats = tools.Statistics(key=lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)
    pop, logbook = algorithms.eaSimple(pop, toolbox,
                                       settings.crossover_probability,
                                       settings.mutation_probability,
                                       settings.generation_size,
                                       stats=stats, verbose=settings.verbose)


