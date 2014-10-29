#!/bin/sh

rm -f map.osm.xml map.net.xml map.poly.xml

echo "\nFiltering nodes\n"
osmosis --read-xml file="map.osm" \
    --tf accept-ways highway=* \
    --used-node --write-xml file="map.osm.xml"

echo "\nConverting to SUMO net file\n"
netconvert --osm-files map.osm.xml --output-file map.net.xml \
    -t typemap.xml \
    --ramps.guess --remove-edges.by-vclass hov,taxi,bus,delivery,transport,lightrail,cityrail,rail_slow,rail_fast,motorcycle,bicycle,pedestrian \
    --remove-edges.isolated \
    --geometry.remove --verbose \
    --junctions.join --roundabouts.guess \
    --tls.guess --tls.join \
    --no-turnarounds.tls --tls.discard-simple

echo "\nGenerating polygon typemap\n"
polyconvert --net-file map.net.xml \
    --osm-files map.osm.xml \
    --type-file typemap.xml \
    -o map.poly.xml
