import subprocess, random, sys, os
from optparse import OptionParser

from constants import *

import traci
import traci.constants as tc

class Setting:
    step = 0
    verbose = False

setting = Setting()
occupancy = {}
vehicleStatus = {}
persons = {}
waiting = {}

def generateDetectors():
    with open("data/map.det.xml", "w") as tollgates:
        print >> tollgates, """
        <e1Detector freq="{}" file="map.out"/>'
        """.format(INDUCTION_LOOP_FREQ)

def generateTollgates():
    traci.init(PORT)
    lanes = traci.lane.getIDList()
    choice = random.sample(lanes, NTOLLGATES)
    choice = filter(lambda x: traci.lane.getLength(x) > LANE_LENGTH_LIMIT, choice)
    fmt = '<inductionLoop id="{}" lane="{}" pos="{}" freq="{}" file="map.out"/>'

    with open("data/map.poly.xml", "w") as tollgates:
        print >> tollgates, '<additional>'

        for i, tg in enumerate(choice):
            lane_length = int(traci.lane.getLength(tg))
            pos = random.randrange(MIN_TOLLGATE_OFFSET, lane_length)
            other_pos = lane_length - pos            
            print "\nPlacing toolgate: id = {}, position = {}, lane = {}\n".format(
                i, pos, tg)
            print >> tollgates, fmt.format(i, tg, pos, INDUCTION_LOOP_FREQ)
            other_lane = tg[1:] if tg.startswith('-') else '-'+tg
            print >> tollgates, fmt.format((i+1)*NTOLLGATES, other_lane,
                                           other_pos, INDUCTION_LOOP_FREQ)
        print >> tollgates, '</additional>'
    traci.close()

def run_sumo(sumoExe=SUMO):
    return subprocess.Popen(
        [
            sumoExe, "-c", "data/map.sumocfg",
            "--tripinfo-output", "tripinfo.xml",
            "-l", "output.log",
            "--remote-port", str(PORT)
        ],
        stdout=sys.stdout,
        stderr=sys.stderr
    )

def parse_options():
    optParser = OptionParser()
    optParser.add_option("-v", "--verbose", action="store_true", dest="verbose",
                         default=False, help="tell me what you are doing")
    optParser.add_option("-g", "--gui", action="store_true", dest="gui",
                         default=False, help="run with GUI")
    optParser.add_option("-d", "--demand", type="int", dest="demand",
                         default=15, help="period with which the persons are emitted")
    return optParser.parse_args()

def initialize_settings(options, args):
    setting.verbose = options.verbose

def simulation_step():
    setting.step += 1
    if setting.verbose:
        print "step", setting.step
    traci.simulationStep()

def run_simulation(sumoProcessCmd):
    traci.init(PORT)
    traci.simulation.subscribe()
    try:
        while setting.step < STEP_LIMIT:
            simulation_step()
    finally:
        traci.close()
        sumoProcessCmd.wait()

def init():
    (options, args) = parse_options()
    initialize_settings(options, args)
    generateDetectors()
    sumoProcessCmd = run_sumo(SUMO)
    generateTollgates()
    sumoProcessCmd.wait()
    sumoProcessCmd = run_sumo(SUMOGUI if options.gui else SUMO)
    run_simulation(sumoProcessCmd)

def get_simulation_step():
    return setting.step

def get_vehicle_position(vehicleID):
    return vehicleStatus[vehicleID].edge


