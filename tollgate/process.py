import os
import shutil
import subprocess

from util import *
from constants import *
from options import settings

def import_map(map_path):
    map_path = os.path.realpath(map_path)
    ok_print('Importing map ' + map_path)
    remove_files = [MAP_FILE, POLY_FILE]
    for f in remove_files:
        try:
            p = os.path.join(IMPORT_PATH, f)
            if os.path.exists(p):
                os.remove(p)
        except Exception as e:
            error_print(unicode(e))

    ok_print('Filtering nodes')
    cmd = subprocess.Popen(
        [
            OSMOSIS, '--read-xml', 'file=' + map_path,
            '--tf', 'accept-ways', 'highway=*',
            '--used-node', '--write-xml', 'file=' + MAP_OSM_XML_FILE
        ],
        stdout=settings.stdout,
        stderr=settings.stderr
    )
    cmd.wait()

    ok_print('Converting to SUMO net file')
    cmd = subprocess.Popen(
        [
            NETCONVERT, '--osm-files', MAP_OSM_XML_FILE,
            '--output-file', MAP_FILE,
            '--ramps.guess', '--remove-edges.by-vclass',
            'hov,taxi,bus,delivery,transport,lightrail,cityrail,rail_slow,rail_fast,motorcycle,bicycle,pedestrian',
            '--remove-edges.isolated', '--geometry.remove', '--verbose',
            '--junctions.join', '--roundabouts.guess',
            '--tls.guess', '--tls.join',
            '--no-turnarounds.tls', '--tls.discard-simple'
        ],
        stdout=settings.stdout,
        stderr=settings.stderr
    )
    cmd.wait()

    ok_print('Generating polygon typemap')
    cmd = subprocess.Popen(
        [
            POLYCONVERT, '--net-file', MAP_FILE,
            '--osm-files', MAP_OSM_XML_FILE,
            '--type-file', TYPEMAP_FILE,
            '-o', POLY_FILE
        ],
        stdout=settings.stdout,
        stderr=settings.stderr
    )
    cmd.wait()
    ok_print('Done!')
    
def import_random_trips():
    ok_print('Generating random trips')
    try:
        if os.path.exists(TRIPS_FILE):
            os.remove(TRIPS_FILE)
    except Exception as e:
        error_print(unicode(e))
    ok_print('Deleted ' + TRIPS_FILE)
    vehicle_spawn_duration = settings.step_limit / settings.vehicle_count
    if settings.vehicle_spawn_duration:
        vehicle_spawn_duration = settings.vehicle_spawn_duration
    ok_print('Random trip with spawn duration = {} and number of vehicles = {}'.format(
        settings.vehicle_spawn_duration, settings.vehicle_count))
    cmd = subprocess.Popen(
        [
            RANDOM_TRIPS, '-n', MAP_FILE,
            '-p', str(vehicle_spawn_duration),
            '-b', '0',
            '-e', str(settings.step_limit),
            '-l', '-o', TRIPS_FILE
        ],
        stdout=settings.stdout,
        stderr=settings.stderr
    )
    cmd.wait()

    ok_print('Generating routes')
    cmd = subprocess.Popen(
        [
            'duarouter', '-n', MAP_FILE,
            '-t', TRIPS_FILE,
            '-o', ROUTE_FILE,
            '--ignore-errors',
            '--begin', '0',
            '--end', str(settings.step_limit),
            '--no-step-log'
        ],
        stdout=settings.stdout,
        stderr=settings.stderr
    )
    cmd.wait()
    ok_print('Done!')
