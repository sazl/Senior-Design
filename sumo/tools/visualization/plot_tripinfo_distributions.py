#!/usr/bin/env python
"""
@file    plot_tripinfo_distributions.py
@author  Daniel Krajzewicz
@author  Laura Bieker
@date    2013-11-11
@version $Id: plot_tripinfo_distributions.py 16005 2014-03-24 12:46:02Z cschmidt87 $

This script plots measures from the tripinfor output, classified into bins
matplotlib (http://matplotlib.org/) has to be installed for this purpose
 

SUMO, Simulation of Urban MObility; see http://sumo-sim.org/
Copyright (C) 2013-2014 DLR (http://www.dlr.de/) and contributors

This file is part of SUMO.
SUMO is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.
"""

import os, subprocess, sys, random, helpers
from matplotlib import rcParams
from pylab import *
from matplotlib.ticker import FuncFormatter as ff
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'tools'))
sys.path.append(os.path.join(os.environ.get("SUMO_HOME", os.path.join(os.path.dirname(__file__), '..', '..')), 'tools'))
import sumolib.output





def main(args=None):
  """The main function; parses options and plots"""
  ## ---------- build and read options ----------
  from optparse import OptionParser
  optParser = OptionParser()
  optParser.add_option("-i", "--tripinfos-inputs", dest="tripinfos", metavar="FILE",
                         help="Defines the tripinfo-output files to use as input")
  optParser.add_option("-v", "--verbose", dest="verbose", action="store_true",
                         default=False, help="If set, the script says what it's doing")
  optParser.add_option("-m", "--measure", dest="measure", 
                         default="duration", help="Define which measure to plot")
  optParser.add_option("--bins", dest="bins", 
                         type="int", default=20, help="Define the bin number")
  optParser.add_option("--norm", dest="norm", 
                         type="float", default=1., help="Read values will be devided by this number")
  optParser.add_option("--minV", dest="minV", 
                         type="float", default=None, help="Define the minimum value boundary")
  optParser.add_option("--maxV", dest="maxV", 
                         type="float", default=None, help="Define the maximum value boundary")
  # standard plot options
  helpers.addInteractionOptions(optParser)
  helpers.addPlotOptions(optParser)
  # parse
  options, remaining_args = optParser.parse_args(args=args)

  if options.tripinfos==None:
    print "Error: at least one tripinfo file must be given"
    sys.exit(1)

  minV = options.minV
  maxV = options.maxV
  files = options.tripinfos.split(",")
  values = {}
  for f in files:
    if options.verbose: print "Reading '%s'..." % f
    nums = sumolib.output.parse_sax__asList(f, "tripinfo", [options.measure])
    fvp = sumolib.output.toList(nums, options.measure)
    fv = [x / options.norm for x in fvp]
    sumolib.output.prune(fv, options.minV, options.maxV)
     
    values[f] = fv 
    if minV==None: 
      minV = fv[0]
      maxV = fv[0]
    minV = min(minV, min(fv))
    maxV = max(maxV, max(fv))
  
  hists = {}
  binWidth = (maxV-minV) / float(options.bins)
  for f in files:
    h = [0] * options.bins
    for v in values[f]:
      i = min(int((v-minV)/binWidth), options.bins-1)
      h[i] = h[i] + 1
    hists[f] = h
  
  width = binWidth / float(len(files)) * .8
  offset = binWidth * .1
  center = []
  for j in range(0, options.bins):
    center.append(binWidth*j+offset)

  fig, ax = helpers.openFigure(options)
  for i,f in enumerate(files):
    c = helpers.getColor(options, i, len(files))
    l = helpers.getLabel(f, i, options)
    bar(center, hists[f], width = width, label=l, color=c)
    for j in range(0, options.bins):
      center[j] = center[j] + width
  helpers.closeFigure(fig, ax, options)

if __name__ == "__main__":
  sys.exit(main(sys.argv))
    