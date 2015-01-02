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
    
