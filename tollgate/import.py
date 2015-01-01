import os
import shutil
import subprocess

from util import *
from constants import *
from options import settings

def import_map(map_name):
    ok_print('Importing map ' + map_name)
    remove_files = [MAP_OSM_XML_FILE, MAP_FILE, POLY_FILE]
    for f in remove_files:
        try:
            os.remove(os.realpath.join(IMPORT_PATH, f))
        except Exception as e:
            error_print(e)
    shutil.copyfile(os.path.join(DATA_PATH, map_name), MAP_OSM_XML_FILE)

    ok_print('Filtering nodes')
    subprocess.Popen(
        [
            OSMOSIS, '--read-xml', 'file=' + MAP_OSM_FILE,
            '--tf', 'accept-ways', 'highway=*',
            '--used-node', '--write-xml', 'file=' + MAP_OSM_XML_FILE
        ],
        stdout=sys.stdout,
        stderr=sys.stderr
    )

    
