# -*- coding: utf-8 -*-
import os, sys

INFINITY = 1e400

PREFIX = "map"
DOUBLE_ROWS = 8
ROW_DIST = 35
STOP_POS = ROW_DIST-12
SLOTS_PER_ROW = 10
SLOT_WIDTH = 5
SLOT_LENGTH = 9
SLOT_FOOT_LENGTH = 5
CAR_CAPACITY = 3
CYBER_CAPACITY = 20
BUS_CAPACITY = 30
TOTAL_CAPACITY = 60
CYBER_SPEED = 5
CYBER_LENGTH = 9
WAIT_PER_PERSON = 5
OCCUPATION_PROBABILITY = 0.5
BREAK_DELAY = 1200

STEP_LIMIT = 10000
LANE_LENGTH_LIMIT = 50
INDUCTION_LOOP_FREQ = 120
NTOLLGATES = 20
MIN_TOLLGATE_OFFSET = 10

PORT = 8873
SUMO_HOME = os.path.realpath(os.environ.get("SUMO_HOME", os.path.join(os.path.dirname(__file__), "..", "..", "..", "..")))
sys.path.append(os.path.join(SUMO_HOME, "tools"))
try:
    from sumolib import checkBinary
except ImportError:
    def checkBinary(name):
        return name
NETCONVERT = checkBinary("netconvert")
SUMO = checkBinary("sumo")
SUMOGUI = checkBinary("sumo-gui")
