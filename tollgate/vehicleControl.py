import subprocess, random, sys, os
from optparse import OptionParser

from constants import *

import traci
import traci.constants as tc

import statistics

class Manager:
    def personArrived(self, vehicleID, edge, target):
        raise NotImplementedError
    def cyberCarArrived(self, vehicleID, edge):
        raise NotImplementedError
    def cyberCarBroken(self, vehicleID, edge):
        pass
    def setNewTargets(self):
        pass

class Status:
    def __init__(self, edge, pos):
        self.edge = edge
        self.pos = pos
        self.parking = False
        self.target = None
        self.targetPos = None
        self.slot = None
        self.delay = None

    def __repr__(self):
        return "%s,%s" % (self.edge, self.pos)

class Setting:
    step = 0
    manager = None 
    verbose = False
    cyber = False

setting = Setting()
occupancy = {}
vehicleStatus = {}
persons = {}
waiting = {}

def generateDetectors():
    with open("data/map.det.xml", "w") as tollgates:
        print >> tollgates, """
        <e1Detector
          id="0" lane="{}"
          pos="5" freq="{}" file="map.out"/>'
        """.format(STARTING_LANE, INDUCTION_LOOP_FREQ)

def generateTollgates():
    traci.init(PORT)
    lanes = traci.lane.getIDList()
    choice = random.sample(lanes, NTOLLGATES)
    choice = filter(lambda x: traci.lane.getLength(x) > LANE_LENGTH_LIMIT, choice)
    fmt = '<inductionLoop id="{}" lane="{}" pos="{}" freq="{}" file="map.out"/>'

    with open("data/map.poly.xml", "w") as tollgates:
        print >> tollgates, '<additional>'
        for i, tg in enumerate(choice):
            pos = random.randrange(10, int(traci.lane.getLength(tg)))
            print "\nPlacing toolgate: id = {}, position = {}, lane = {}\n".format(
                i, pos, tg)
            print >> tollgates, fmt.format(i, tg, pos, INDUCTION_LOOP_FREQ)
        print >> tollgates, '</additional>'
    traci.close()

def init(manager, forTest=False):
    optParser = OptionParser()
    optParser.add_option("-v", "--verbose", action="store_true", dest="verbose",
                         default=False, help="tell me what you are doing")
    optParser.add_option("-g", "--gui", action="store_true", dest="gui",
                         default=False, help="run with GUI")
    optParser.add_option("-d", "--demand", type="int", dest="demand",
                         default=15, help="period with which the persons are emitted")
    (options, args) = optParser.parse_args()
    sumoExe = SUMO


    generateDetectors()
    sumoProcessCmd = subprocess.Popen(
        [
            sumoExe, "-c", "data/map.sumocfg",
            "--tripinfo-output", "tripinfo.xml",
            "--remote-port", str(PORT)
        ],
        stdout=sys.stdout,
        stderr=sys.stderr
    )
    generateTollgates()
    sumoProcessCmd.wait()

    if options.gui:
        sumoExe = SUMOGUI
    sumoProcessCmd = subprocess.Popen(
        [
            sumoExe, "-c", "data/map.sumocfg",
            "--tripinfo-output", "tripinfo.xml",
            "--remote-port", str(PORT)
        ],
        stdout=sys.stdout,
        stderr=sys.stderr
    )
    traci.init(PORT)
    traci.simulation.subscribe()
    setting.manager = manager
    setting.verbose = options.verbose
    try:
        while setting.step < STEP_LIMIT:
            doStep()
    finally:
        traci.close()
        sumoProcessCmd.wait()

def getStep():
    return setting.step

def getPosition(vehicleID):
    return vehicleStatus[vehicleID].edge

def stopAt(vehicleID, edge, pos=None):
    if pos == None:
        pos = STOP_POS
    traci.vehicle.changeTarget(vehicleID, edge)
    if setting.verbose:
        print "stopAt", vehicleID, edge, pos
        print vehicleStatus[vehicleID]
        print traci.vehicle.getRoute(vehicleID)
    traci.vehicle.setStop(vehicleID, edge, pos)
    vehicleStatus[vehicleID].target = edge
    vehicleStatus[vehicleID].targetPos = pos

def leaveStop(vehicleID, newTarget=None, delay=0.):
    v = vehicleStatus[vehicleID]
    if newTarget:
        traci.vehicle.changeTarget(vehicleID, newTarget)
    traci.vehicle.setStop(vehicleID, v.target, v.targetPos, 0, delay)
    v.target = None
    v.targetPos = None
    v.parking = False

def _rerouteCar(vehicleID):
    slotEdge = ""
    for rowIdx in range(DOUBLE_ROWS):
        for idx in range(SLOTS_PER_ROW):
            for dir in ["l", "r"]:
                slotEdge = "slot%s-%s%s" % (rowIdx, idx, dir)
                if not slotEdge in occupancy:
                    occupancy[slotEdge] = vehicleID
                    stopAt(vehicleID, slotEdge, SLOT_LENGTH-5.)
                    return

def _checkInitialPositions(vehicleID, edge, pos):
    if vehicleID in vehicleStatus:
        vehicleStatus[vehicleID].edge = edge
        vehicleStatus[vehicleID].pos = pos
    else:
        vehicleStatus[vehicleID] = Status(edge, pos)

def doStep():
    setting.step += 1
    if setting.verbose:
        print "step", setting.step
    traci.simulationStep()
    moveNodes = []
    for veh, subs in traci.vehicle.getSubscriptionResults().iteritems():
        moveNodes.append((veh, subs[tc.VAR_ROAD_ID], subs[tc.VAR_LANEPOSITION]))
    departed = traci.simulation.getSubscriptionResults()[tc.VAR_DEPARTED_VEHICLES_IDS]
    for v in departed:
        traci.vehicle.subscribe(v)
        subs = traci.vehicle.getSubscriptionResults(v)
        moveNodes.append((v, subs[tc.VAR_ROAD_ID], subs[tc.VAR_LANEPOSITION]))
    for vehicleID, edge, pos in moveNodes:
        _checkInitialPositions(vehicleID, edge, pos)
        vehicle = vehicleStatus[vehicleID]
    setting.manager.setNewTargets()
