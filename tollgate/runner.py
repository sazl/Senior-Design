#!/usr/bin/env python
import os, sys
import optparse
import subprocess
import random

try:
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', "tools"))
    sys.path.append(os.path.join(os.environ.get("SUMO_HOME", os.path.join(os.path.dirname(__file__), "..", "..", "..")), "tools"))
    from sumolib import checkBinary
except ImportError:
    sys.exit("please declare environment variable 'SUMO_HOME' as the root directory of your sumo installation (it should contain folders 'bin', 'tools' and 'docs')")

import traci

PORT = 8873

def initialize():
    with open("data/cross.det.xml", "w") as tollgates:
        print >> tollgates, '<e1Detector id="0" lane="4i_0" pos="450" freq="30" file="cross.out"/>'


NSGREEN = "GrGr"
NSYELLOW = "yryr"
WEGREEN = "rGrG"
WEYELLOW = "ryry"
PROGRAM = [
    WEYELLOW,WEYELLOW,WEYELLOW,
    NSGREEN,NSGREEN,NSGREEN,
    NSGREEN,NSGREEN,NSGREEN,
    NSGREEN,NSGREEN,NSYELLOW,
    NSYELLOW,WEGREEN
]

def generate_routefile():
    N = 300
    pWE = 1./10
    pEW = 1./11
    pNS = 1./30
    with open("data/cross.rou.xml", "w") as routes:
        print >> routes, """<routes>
        <vType id="typeWE" accel="0.8" decel="4.5" sigma="0.5" length="5" minGap="2.5" maxSpeed="16.67" guiShape="passenger"/>
        <route id="right" edges="51o 1i 2o 52i" />
        <route id="left" edges="52o 2i 1o 51i" />
        <route id="down" edges="54o 4i 3o 53i" />
        """
        lastVeh = 0
        vehNr = 0
        for i in range(N):
            if random.uniform(0,1) < pWE:
                print >> routes, '    <vehicle id="right_%i" type="typeWE" route="right" depart="%i" />' % (vehNr, i)
                vehNr += 1
                lastVeh = i
            if random.uniform(0,1) < pEW:
                print >> routes, '    <vehicle id="left_%i" type="typeWE" route="left" depart="%i" />' % (vehNr, i)
                vehNr += 1
                lastVeh = i
        print >> routes, "</routes>"


NTOLLGATES = 10
CHROMOSOME = []

def generate_tollgates():
    traci.init(PORT)
    lanes = traci.lane.getIDList()
    choice = random.sample(lanes, NTOLLGATES)
    choice = filter(lambda x: traci.lane.getLength(x) > 20, choice)
    fmt = '<inductionLoop id="{}" lane="{}" pos="{}" freq="30" file="cross.out"/>'

    with open("data/cross.det.xml", "w") as tollgates:
        print >> tollgates, '<additional>'
        for i, tg in enumerate(choice):
            pos = random.randrange(10, int(traci.lane.getLength(tg)))
            print "\nPlacing toolgate: id = {}, position = {}, lane = {}\n".format(i, pos, tg)
            print >> tollgates, fmt.format(i, tg, pos)
        print >> tollgates, '</additional>'
    traci.close()

def run():
    traci.init(PORT)
    programPointer = len(PROGRAM)-1
    step = 0
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        programPointer = min(programPointer+1, len(PROGRAM)-1)
        numPriorityVehicles = traci.inductionloop.getLastStepVehicleNumber("0")
        if numPriorityVehicles > 0:
            if programPointer == len(PROGRAM)-1:
                programPointer = 0
            elif PROGRAM[programPointer] != WEYELLOW:
                programPointer = 3
            else:
                pass
        traci.trafficlights.setRedYellowGreenState("0", PROGRAM[programPointer])
        step += 1
    traci.close()
    sys.stdout.flush()

def get_options():
    optParser = optparse.OptionParser()
    optParser.add_option(
        "--nogui",
        action="store_true",
        default=False,
        help="run the commandline version of sumo"
    )
    options, args = optParser.parse_args()
    return options

if __name__ == "__main__":
    options = get_options()
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    initialize()
    generate_routefile()
    sumoProcessCmd = subprocess.Popen(
        [
            "sumo", "-c", "data/cross.sumocfg",
            "--tripinfo-output", "tripinfo.xml",
            "--remote-port", str(PORT)
        ],
        stdout=sys.stdout,
        stderr=sys.stderr
    )
    generate_tollgates()
    sumoProcessCmd.wait()

    sumoProcess = subprocess.Popen(
        [
            sumoBinary, "-c", "data/cross.sumocfg",
            "--tripinfo-output", "tripinfo.xml",
            "--remote-port", str(PORT)
        ],
        stdout=sys.stdout,
        stderr=sys.stderr
    )
    run()
    sumoProcess.wait()
