#!/bin/sh

rm -f map.osm.xml map.net.xml map.poly.xml
cp ../data/InternationalCity.osm map.osm.xml

echo "\nFiltering nodes\n"
osmosis --read-xml file="map.osm" \
    --tf accept-ways highway=* \
    --used-node --write-xml file="map.osm.xml" 2> /dev/null

echo "\nConverting to SUMO net file\n"
netconvert --osm-files map.osm.xml --output-file map.net.xml \
    --ramps.guess --remove-edges.by-vclass hov,taxi,bus,delivery,transport,lightrail,cityrail,rail_slow,rail_fast,motorcycle,bicycle,pedestrian \
    --remove-edges.isolated \
    --geometry.remove --verbose \
    --junctions.join --roundabouts.guess \
    --tls.guess --tls.join \
    --no-turnarounds.tls --tls.discard-simple 1> /dev/null

echo "\nGenerating polygon typemap\n"
polyconvert --net-file map.net.xml \
    --osm-files map.osm.xml \
    --type-file typemap.xml \
    -o map.poly.xml 2> /dev/null

cp map.net.xml ../tollgate/data/map.net.xml
cp map.poly.xml ../tollgate/data/map.poly.xml
