#!/usr/bin/env python
"""
@file    plot_csv_timeline.py
@author  Daniel Krajzewicz
@author  Laura Bieker
@date    2014-01-14
@version $Id: plot_csv_timeline.py 16005 2014-03-24 12:46:02Z cschmidt87 $


This script plots selected columns from a given .csv file (';'-separated).
The loaded time lines are visualised as lines.
matplotlib (http://matplotlib.org/) has to be installed for this purpose


SUMO, Simulation of Urban MObility; see http://sumo-sim.org/
Copyright (C) 2014-2014 DLR (http://www.dlr.de/) and contributors

This file is part of SUMO.
SUMO is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.
"""

import os, subprocess, sys, random, helpers
from matplotlib import rcParams
from pylab import *
import csv
        
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'tools'))
sys.path.append(os.path.join(os.environ.get("SUMO_HOME", os.path.join(os.path.dirname(__file__), '..', '..')), 'tools'))


  
def readValues(file, verbose, columns):
  if verbose: print "Reading '%s'..." % f
  ret = {}
  with open(file, 'rb') as f:
    reader = csv.reader(f, delimiter=';')
    for row in reader:
      if columns==None:
        columns = range(0, len(row))
      for i in columns:
        if i not in ret: ret[i] = []
        ret[i].append(float(row[i])) 
  return ret



def main(args=None):
  """The main function; parses options and plots"""
  ## ---------- build and read options ----------
  from optparse import OptionParser
  optParser = OptionParser()
  optParser.add_option("-i", "--input", dest="input", metavar="FILE",
                         help="Defines the input file to use")
  optParser.add_option("-v", "--verbose", dest="verbose", action="store_true",
                         default=False, help="If set, the script says what it's doing")
  optParser.add_option("-c", "--columns", dest="columns", 
                         default=None, help="Defines which columns shall be plotted")
  # standard plot options
  helpers.addInteractionOptions(optParser)
  helpers.addPlotOptions(optParser)
  # parse
  options, remaining_args = optParser.parse_args(args=args)
  
  if options.input==None:
    print "Error: an input file must be given"
    sys.exit(1)

  minV = 0
  maxV = 0
  if options.columns!=None: options.columns = [int(i) for i in options.columns.split(",")]
  nums = readValues(options.input, options.verbose, options.columns) 
  for f in nums:
    maxV = max(maxV, len(nums[f]))
  ts = range(minV, maxV+1)

  fig, ax = helpers.openFigure(options)
  for i in nums:
    v = nums[i]
    ci = i
    if options.columns!=None: ci = options.columns.index(i)
    c = helpers.getColor(options, ci, len(nums))
    l = helpers.getLabel(str(i), ci, options)
    plot(ts[0:len(v)], v, label=l, color=c)
  helpers.closeFigure(fig, ax, options)

if __name__ == "__main__":
  sys.exit(main(sys.argv))
    