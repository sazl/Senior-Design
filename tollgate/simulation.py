import itertools
import os
import random
import subprocess
import sys

import traci
import traci.constants as tc

from util      import *
from process   import *
from constants import *
from options   import *

import genetic

class State:
    initialized = False
    step        = 0
    edges       = {}
    tollgates   = {}
    population  = {}

state = State()

""""
def generate_detectors():
    with open(DETECTOR_FILE, "w") as tollgates:
        print >> tollgates, '<e1Detector freq="{}" file="map.out"/>'.format(
            settings.tollgate_collection_frequency)
"""

def get_edge_lanes(lanes=None):
    lanes_by_edge = {}
    for l in traci.lane.getIDList():
        e = traci.lane.getEdgeID(l)
        if e in lanes_by_edge:
            lanes_by_edge[e].append(l)
        else:
            lanes_by_edge[e] = [l]
    if lanes is None:
        return lanes_by_edge
    else:
        edges = map(traci.lane.getEdgeID, lanes)
        return { e : lanes_by_edge[e] for e in edges }

def select_valid_edges():
    lanes = traci.lane.getIDList()
    choice = filter(lambda x: traci.lane.getLength(x) > settings.tollgate_min_lane_length, lanes)
    state.edges = get_edge_lanes(choice)
    if len(state.edges) > settings.tollgate_max_count:
        state.edges = dict(random.sample(list(state.edges.iteritems()), settings.tollgate_max_count))

def initialize_state():
    select_valid_edges()
    genetic.initialize()
    state.initialized = True
    genetic.run()

def run_genetic_algorithm(tollgates):
    sumoProcessCmd = run_sumo(SUMO)
    generate_tollgates(tollgates)
    sumoProcessCmd.wait()
    sumoProcessCmd = run_sumo(SUMOGUI if settings.gui else SUMO)
    run_simulation(sumoProcessCmd)


def generate_tollgates(tollgates):
    traci.init(PORT)
    if not state.initialized:
        initialize_state()
    
    
    with open(POLY_FILE, "w+") as poly_file:
        print >> tollgates, '<additional>'
        ident = 0
        for e, ls in state.edges.iteritems():
            lane_length = int(traci.lane.getLength(ls[0]))
            pos = random.randrange(settings.tollgate_min_offset, lane_length)
            for tg in ls:
                ok_print("\nPlacing toolgate: id = {}, position = {}, lane = {}\n".format(
                    ident, pos, tg))
                print >> tollgates, INDUCTION_LOOP_FMT.format(ident, tg, pos,
                                                              settings.tollgate_collection_frequency,
                                                              TOLLGATE_OUTPUT)
                ident += 1
        print >> tollgates, '</additional>'
    traci.close()

def run_sumo(sumoExe=SUMO):
    return subprocess.Popen(
        [
            sumoExe, "-c", SIMULATION_CONFIG,
            "--tripinfo-output", TRIP_INFO_OUTPUT,
            "-l", LOG_OUTPUT,
            "--remote-port", str(settings.port)
        ],
        stdout=settings.stdout,
        stderr=settings.stderr
    )

def calculate_statistics():
    for d in traci.inductionloop.getIDList():
        a = traci.inductionloop.getLastStepOccupancy(d)
        b = traci.inductionloop.getLastStepMeanSpeed(d)
        if a != -1 and b != -1:
            print a, b

def update_tollgates():
    pass

def simulation_step():
    state.step += 1
    if settings.verbose:
        print "step", state.step
    traci.simulationStep()
    calculate_statistics()

def run_simulation(sumoProcessCmd):
    traci.init(PORT)
    traci.simulation.subscribe()
    try:
        while state.step < settings.step_limit:
            simulation_step()
    finally:
        traci.close()
        sumoProcessCmd.wait()

def preamble():
    random.seed()
    if settings.import_map:
        import_map(settings.import_map)
    if settings.random_trips:
        import_random_trips()

def initialize():
    preamble()
