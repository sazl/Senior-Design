/****************************************************************************/
/// @file    bezier.h
/// @author  Daniel Krajzewicz
/// @author  Michael Behrisch
/// @date    2003-11-19
/// @version $Id: bezier.h 16005 2014-03-24 12:46:02Z cschmidt87 $
///
// missing_desc
/****************************************************************************/
// SUMO, Simulation of Urban MObility; see http://sumo-sim.org/
// Copyright (C) 2003-2014 DLR (http://www.dlr.de/) and contributors
/****************************************************************************/
//
//   This file is part of SUMO.
//   SUMO is free software: you can redistribute it and/or modify
//   it under the terms of the GNU General Public License as published by
//   the Free Software Foundation, either version 3 of the License, or
//   (at your option) any later version.
//
/****************************************************************************/
#ifndef bezier_h
#define bezier_h


// ===========================================================================
// included modules
// ===========================================================================
#ifdef _MSC_VER
#include <windows_config.h>
#else
#include <config.h>
#endif


/* Bezier curve subroutine */
void
bezier(int npts, SUMOReal b[], int cpts, SUMOReal p[]);


#endif

/****************************************************************************/

