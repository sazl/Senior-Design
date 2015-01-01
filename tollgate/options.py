from constants import *
from optparse import OptionParser

settings = None

def parse_options():
    usage = "usage: %prog [options]"
    optParser = OptionParser(usage=usage)
    
    optParser.add_option("-v", "--verbose", action="store_true", dest="verbose",
                         default=False, help="display detailed execution info")
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
    
    optParser.add_option("-b", "--trip-start", action="store", dest="trip_start",
                         default=TRIP_START_TIME,
                         help="Starting time for the random trips")
    optParser.add_option("-e", "--trip-end", action="store", dest="trip_end",
                         default=TRIP_END_TIME,
                         help="Ending time for the random trip")

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

    
    (options, args) = optParser.parse_args()
    return options

if settings is None:
    settings = parse_options()
    settings.step = 0
