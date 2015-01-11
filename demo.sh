#!/bin/sh
time python main.py -i data/Simple.osm -r \
    --step-limit 1000 \
    --output demo/output.out \
    --output-statistics demo/stats.out \
    --output-plots demo/ \
    --population-size 2 --generation-size 2 \
    --tollgate-max-count 4 \
    -g --screenshot-directory demo
