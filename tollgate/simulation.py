import itertools
import os
import random
import subprocess
import sys

import traci
import traci.constants as tc

from constants import *
from options import *

class State:
    edges     = {}
    tollgates = {}

state = State()

def generate_detectors():
    with open("data/map.det.xml", "w") as tollgates:
        print >> tollgates, """
        <e1Detector freq="{}" file="map.out"/>'
        """.format(settings.tollgate_collection_frequency)

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

def generate_tollgates():
    traci.init(PORT)
    lanes = traci.lane.getIDList()
    choice = random.sample(lanes, settings.tollgate_max_count)
    choice = filter(lambda x: traci.lane.getLength(x) > settings.tollgate_min_lane_length, choice)    
    state.edges = get_edge_lanes(choice)
    fmt = '<inductionLoop id="{}" lane="{}" pos="{}" freq="{}" file="map.out"/>'

    with open("data/map.poly.xml", "w") as tollgates:
        print >> tollgates, '<additional>'
        ident = 0
        for e, ls in state.edges.iteritems():
            lane_length = int(traci.lane.getLength(ls[0]))
            pos = random.randrange(settings.tollgate_min_offset, lane_length)
            for tg in ls:
                print "\nPlacing toolgate: id = {}, position = {}, lane = {}\n".format(
                    ident, pos, tg)
                print >> tollgates, fmt.format(ident, tg, pos,
                                               settings.tollgate_collection_frequency)
                ident += 1
        print >> tollgates, '</additional>'
    traci.close()

def run_sumo(sumoExe=SUMO):
    return subprocess.Popen(
        [
            sumoExe, "-c", "tollgate/data/map.sumocfg",
            "--tripinfo-output", "tripinfo.xml",
            "-l", "output.log",
            "--remote-port", str(settings.port)
        ],
        stdout=settings.stdout,
        stderr=settings.stderr
    )

def calculate_statistics():
    for d in traci.inductionloop.getIDList():
        pass

def update_tollgates():
    pass

def simulation_step():
    settings.step += 1
    if settings.verbose:
        print "step", settings.step
    traci.simulationStep()
    calculate_statistics()
    update_tollgates()

def run_simulation(sumoProcessCmd):
    traci.init(PORT)
    traci.simulation.subscribe()
    try:
        while settings.step < settings.step_limit:
            simulation_step()
    finally:
        traci.close()
        sumoProcessCmd.wait()

def init():
    generate_detectors()
    sumoProcessCmd = run_sumo(SUMO)
    generate_tollgates()
    sumoProcessCmd.wait()
    sumoProcessCmd = run_sumo(SUMOGUI if settings.gui else SUMO)
    run_simulation(sumoProcessCmd)

def get_simulation_step():
    return setting.step
