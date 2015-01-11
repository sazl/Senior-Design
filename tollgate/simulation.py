import itertools
import os
import random
import subprocess
import sys

import traci
import traci.constants as tc

from constants import *
from options   import *
from process   import *
from state     import state
from util      import *

def generate_detectors():
    with open(DETECTOR_FILE, "w") as tollgates:
        print >> tollgates, '<e1Detector freq="{}" file="map.out"/>'.format(
            settings.tollgate_collection_frequency)
    with open(POLY_FILE, "w") as poly_file:
        print >> poly_file, '<additional></additional>'

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
    choice = filter(
        lambda x: traci.lane.getLength(x) >= settings.tollgate_min_lane_length,
        lanes
    )
    state.edges = get_edge_lanes(choice)
    state.edges_list = list(state.edges)

def generate_rerouter(poly_file):
    for i, t in enumerate(state.tollgates):
        rerouter_name = REROUTER_FILE + '_' + str(i)
        effort = t.price / (settings.tollgate_max_price - settings.tollgate_min_price)
        neighbor_edges = []
        for l in state.edges[t.edge_id]:
            neighbor_lanes = traci.lane.getLinks(l)
            for x in neighbor_lanes:
                neighbor_edges.append(traci.lane.getEdgeID(x[0]))
        print >> poly_file, REROUTER_FMT.format(
            i, ' '.join(neighbor_edges), rerouter_name, effort)
        with open(rerouter_name, 'w') as rerouter_file:
            print >> rerouter_file, '<rerouter>'
            print >> rerouter_file, '<interval begin="{}" end="{}">'.format(
                0, settings.step_limit)
            print >> rerouter_file, '<closingReroute id="{}"/>'.format(t.edge_id)
            print >> rerouter_file, '</interval>'
            print >> rerouter_file, '</rerouter>'

def generate_tollgates():
    with open(POLY_FILE, "w") as poly_file:
        ident = 0
        print >> poly_file, '<additional>'
        generate_rerouter(poly_file)
        for t in state.tollgates:
            lanes = state.edges[t.edge_id]
            ok_print("Placing toolgate: id = {}, price = {}, position = {}, edge = {}".format(
                    ident, t.price, t.edge_offset, t.edge_id))
            for l in lanes:
                t.lane_ids.append(l)
                t.detector_ids.append(str(ident))
                print >> poly_file, INDUCTION_LOOP_FMT.format(ident, l, t.edge_offset,
                                                              settings.tollgate_collection_frequency,
                                                              TOLLGATE_OUTPUT)
                ident += 1
        print >> poly_file, '</additional>'

def run_sumo(sumoExe=SUMO):
    return subprocess.Popen(
        [
            sumoExe, "-c", SIMULATION_CONFIG,
            "--tripinfo-output", TRIP_INFO_OUTPUT,
            "-l", LOG_OUTPUT,
            "--remote-port", str(settings.port),
            '--no-step-log', '--no-duration-log',
            "-S", "-Q"
        ],
        stdout=settings.stdout,
        stderr=settings.stderr
    )

def calculate_statistics():
    for t in state.tollgates:
        t.update_statistics()

def simulation_step():
    state.step += 1
    traci.simulationStep()
    calculate_statistics()

def run_simulation():
    state.step = 0
    sumoProcessCmd = run_sumo(SUMOGUI if settings.gui else SUMO)
    traci.init(PORT)
    traci.simulation.subscribe()
    try:
        while state.step < settings.step_limit:
            simulation_step()
        if settings.gui and settings.screenshot_directory:
            fname = 'gen_{}_individual_{}.png'.format(
                state.generation,
                state.individual)
            save_name = os.path.join(settings.screenshot_directory, fname)
            try:
                traci.gui.screenshot('View #0', save_name)
            except Exception as e:
                error_print('Failed to take screenshot ' + save_name)
    finally:
        traci.close()
        sumoProcessCmd.wait()

def preamble():
    random.seed()
    if settings.import_map:
        import_map(settings.import_map)
    if settings.random_trips:
        import_random_trips()

def run_genetic_algorithm():
    sumoProcessCmd = run_sumo(SUMO)
    traci.init(PORT)
    generate_tollgates()
    traci.close()
    sumoProcessCmd.wait()
    run_simulation()

def simulation_fitness():
    occupancy, revenue = 0, 0
    for t in state.tollgates:
        t.finalize()
        occupancy += t.average_occupancy
        revenue += t.revenue
    occupancy /= len(state.tollgates)
    revenue /= len(state.tollgates)
    return occupancy, revenue

import genetic

def initialize_state():
    sumoProcessCmd = run_sumo(SUMO)
    traci.init(PORT)
    select_valid_edges()
    genetic.initialize()
    state.initialized = True
    traci.close()
    sumoProcessCmd.wait()

def initialize():
    preamble()
    generate_detectors()
    initialize_state()
    genetic.run()
