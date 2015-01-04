import os
import sys
from optparse import OptionParser

from util      import *
from constants import *

settings = None

def parse_options():
    usage = "usage: %prog [options]"
    optParser = OptionParser(usage=usage)
    
    optParser.add_option("-v", "--verbose", action="store_true", dest="verbose",
                         default=False, help="display detailed execution info")
    optParser.add_option("", "--output", action="store", dest="output",
                         default=None, help="save output to a file")
    optParser.add_option("-i", "--import-map", action="store",
                         dest="import_map", default=None,
                         help="Process and import map file")
    optParser.add_option("-g", "--gui", action="store_true", dest="gui",
                         default=False, help="run with GUI")
    optParser.add_option("-p", "--port", action="store", dest="port", type=int,
                         default=PORT, help="TraCI port")
    optParser.add_option("-s", "--step-limit", action="store", dest="step_limit",
                         default=STEP_LIMIT,
                         help="Simulation step limit")
    optParser.add_option("-u", "--step-length", action="store",
                         dest="step_length", type=float,
                         default=STEP_LENGTH,
                         help="Simulation step length")
    
    optParser.add_option("-r", "--random-trips", action="store_true",
                         dest="random_trips", default=None,
                         help="Generate random trip")
    optParser.add_option("-0", "--trip-start", action="store", dest="trip_start",
                         default=TRIP_START_TIME, type=int,
                         help="Starting time for the random trips")
    optParser.add_option("-e", "--trip-end", action="store", dest="trip_end",
                         default=TRIP_END_TIME, type=int,
                         help="Ending time for the random trip")
    optParser.add_option("-b", "--vehicle-count", action="store",
                         dest="vehicle_count", type=int,
                         default=VEHICLE_COUNT,
                         help="Number of vehicles in the simulation")
    optParser.add_option("-d", "--vehicle-spawn-duration", action="store",
                         dest="vehicle_spawn_duration", type=float,
                         default=None,
                         help="Duration of time between vehicle spawns")

    optParser.add_option("-m", "--tollgate-min-price", action="store",
                         dest="tollgate_min_price", type=float,
                         default=TOLLGATE_MIN_PRICE,
                         help="Tollgate minimum price")
    optParser.add_option("-n", "--tollgate-max-price", action="store",
                         dest="tollgate_max_price", type=float,
                         default=TOLLGATE_MAX_PRICE,
                         help="Tollgate maximum price")
    optParser.add_option("-c", "--tollgate-max-count", action="store",
                         dest="tollgate_max_count", type=int,
                         default=TOLLGATE_MAX_COUNT,
                         help="Maximum number of tollgates to be placed")
    optParser.add_option("-l", "--tollgate-min-lane-length", action="store",
                         dest="tollgate_min_lane_length", type=int,
                         default=TOLLGATE_MIN_LANE_LENGTH,
                         help="Minimum distance between tollgate and road")
    optParser.add_option("-o", "--tollgate-min-offset", action="store",
                         dest="tollgate_min_offset", type=int,
                         default=TOLLGATE_MIN_OFFSET,
                         help="Minimum distance between tollgate and road")
    optParser.add_option("-f", "--tollgate-collection-frequency", action="store",
                         dest="tollgate_collection_frequency", type=int,
                         default=TOLLGATE_COLLECTION_FREQUENCY,
                         help="Frequency with which tollgate collects stats")

    optParser.add_option("", "--individual_size", action="store",
                         dest="individual_size", type=int,
                         default=INDIVIDUAL_SIZE,
                         help="Genetic algorithm individual size")
    optParser.add_option("", "--population-size", action="store",
                         dest="population_size", type=int,
                         default=POPULATION_SIZE,
                         help="Genetic algorithm population size")
    optParser.add_option("", "--generation-size", action="store",
                         dest="generation_size", type=int,
                         default=GENERATION_SIZE,
                         help="Genetic algorithm generation size")
    
    optParser.add_option("", "--crossover-probability", action="store",
                         dest="crossover_probability", type=float,
                         default=CROSSOVER_PROBABILITY,
                         help="Genetic algorithm crossover probability")
    optParser.add_option("", "--crossover-blend-alpha", action="store",
                         dest="crossover_blend_alpha", type=float,
                         default=CROSSOVER_BLEND_ALPHA,
                         help="Genetic algorithm crossover blend alpha")

    optParser.add_option("", "--mutation-probability", action="store",
                         dest="mutation_probability", type=float,
                         default=MUTATION_PROBABILITY,
                         help="Genetic algorithm mutation probability")
    optParser.add_option("", "--mutation-gaussian-mean", action="store",
                         dest="mutation_gaussian_mean", type=float,
                         default=MUTATION_GAUSSIAN_MEAN,
                         help="Genetic algorithm mutation gaussian_mean")
    optParser.add_option("", "--mutation-guassian-sigma", action="store",
                         dest="mutation_gaussian_sigma", type=float,
                         default=MUTATION_GAUSSIAN_SIGMA,
                         help="Genetic algorithm mutation gaussian_sigma")
    optParser.add_option("", "--mutation-independent-probability",
                         action="store",
                         dest="mutation_independent_probability", type=float,
                         default=MUTATION_INDEPENDENT_PROBABILITY,
                         help="Genetic algorithm mutation indep. probability")
    
    (options, args) = optParser.parse_args()
    validate_options(options)
    return options

def validate_options(options):
    if options.tollgate_min_lane_length <= options.tollgate_min_offset:
        error_print('Lane length must be greater than tollgate offset')
        sys.exit(1)

if settings is None:
    devnull = open(os.devnull, 'w')
    settings = parse_options()
    settings.step = 0
    sys.stdout = open(settings.output, 'w') if settings.output else sys.stdout
    settings.stdout = sys.stdout if settings.verbose else devnull
    settings.stderr = sys.stderr if settings.verbose else devnull
