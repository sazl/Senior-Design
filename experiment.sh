#!/bin/sh

mkdir experiments && \
mkdir experiments/exp1 && \
mkdir experiments/exp2 && \
mkdir experiments/exp3

time python main.py -i data/Simple.osm -r \
    --step-limit 100000 \
    --output experiments/exp1/output.out \
    --output-statistics experiments/exp1/stats.out \
    --population-size 100 --generation-size 100 \
    --tollgate-max-count 10
#    -g --screenshot-directory experiments/exp1

time python main.py -i data/Simple.osm -r \
    --step-limit 10000 \
    --output experiments/exp2/output.out \
    --output-statistics experiments/exp2/stats.out \
    --population-size 50 --generation-size 75 \
    --tollgate-max-count 6
#    -g --screenshot-directory experiments/exp2

time python main.py -i data/Simple.osm -r \
    --output experiments/exp3/output.out \
    --output-statistics experiments/exp3/stats.out \
    --population-size 10 --generation-size 10 \
    --tollgate-max-count 4
#    -g --screenshot-directory experiments/exp3
