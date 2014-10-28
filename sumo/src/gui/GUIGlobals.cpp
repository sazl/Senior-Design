/****************************************************************************/
/// @file    GUIGlobals.cpp
/// @author  Daniel Krajzewicz
/// @author  Michael Behrisch
/// @date    2004
/// @version $Id: GUIGlobals.cpp 16231 2014-04-23 09:33:59Z behrisch $
///
// }
/****************************************************************************/
// SUMO, Simulation of Urban MObility; see http://sumo-sim.org/
// Copyright (C) 2001-2014 DLR (http://www.dlr.de/) and contributors
/****************************************************************************/
//
//   This file is part of SUMO.
//   SUMO is free software: you can redistribute it and/or modify
//   it under the terms of the GNU General Public License as published by
//   the Free Software Foundation, either version 3 of the License, or
//   (at your option) any later version.
//
/****************************************************************************/


// ===========================================================================
// included modules
// ===========================================================================
#ifdef _MSC_VER
#include <windows_config.h>
#else
#include <config.h>
#endif

#include "GUIGlobals.h"

#ifdef CHECK_MEMORY_LEAKS
#include <foreign/nvwa/debug_new.h>
#endif // CHECK_MEMORY_LEAKS


// ===========================================================================
// static member variables definitions
// ===========================================================================
bool GUIGlobals::gQuitOnEnd;


bool GUIGlobals::gRunAfterLoad;



/****************************************************************************/
