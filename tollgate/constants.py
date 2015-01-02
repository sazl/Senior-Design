import os, sys

PORT                = 8873
MAP_PATH            = os.path.realpath('data/')
SRC_PATH            = os.path.realpath('tollgate/')
IMPORT_PATH         = os.path.realpath('import/')
MAP_OSM_FILE        = os.path.join(IMPORT_PATH, 'map.osm')
MAP_OSM_XML_FILE    = os.path.join(IMPORT_PATH, 'map.osm.xml')
TYPEMAP_FILE        = os.path.join(IMPORT_PATH, 'typemap.xml')

DATA_PATH           = os.path.join(SRC_PATH, 'data')
SIMULATION_CONFIG   = os.path.join(DATA_PATH, 'map.sumocfg')
MAP_FILE            = os.path.join(DATA_PATH, 'map.net.xml')
DETECTOR_FILE       = os.path.join(DATA_PATH, 'map.det.xml')
POLY_FILE           = os.path.join(DATA_PATH, 'map.poly.xml')

OUTPUT_PATH         = os.path.join(SRC_PATH, 'output')
TRIP_INFO_OUTPUT    = os.path.join(OUTPUT_PATH, 'tripinfo.xml')
LOG_OUTPUT          = os.path.join(OUTPUT_PATH, 'output.log')



SUMO_HOME           = os.path.realpath(
    os.environ.get("SUMO_HOME",
                   os.path.join(os.path.dirname(__file__),
                                "..", "..", "..", "..")))
sys.path.append(os.path.join(SUMO_HOME, "tools"))

try:
    from sumolib import checkBinary
except ImportError:
    def checkBinary(name):
        return name

NETCONVERT  = checkBinary("netconvert")
POLYCONVERT = checkBinary("polyconvert")
SUMO        = checkBinary("sumo")
SUMOGUI     = checkBinary("sumo-gui")
OSMOSIS     = "osmosis"

VERBOSE             = False
STEP_LIMIT          = 10000
STEP_LENGTH         = 0.01

TRIP_START_TIME     = 0
TRIP_END_TIME       = 10000

TOLLGATE_MIN_LANE_LENGTH      = 50
TOLLGATE_MIN_PRICE            = 0
TOLLGATE_MAX_PRICE            = 100
TOLLGATE_MAX_COUNT            = 20
TOLLGATE_MIN_OFFSET           = 10
TOLLGATE_COLLECTION_FREQUENCY = 120
