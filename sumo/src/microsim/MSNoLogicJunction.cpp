/****************************************************************************/
/// @file    MSNoLogicJunction.cpp
/// @author  Daniel Krajzewicz
/// @author  Michael Behrisch
/// @author  Jakob Erdmann
/// @date    Thu, 06 Jun 2002
/// @version $Id: MSNoLogicJunction.cpp 16290 2014-05-05 12:38:38Z namdre $
///
// -------------------
/****************************************************************************/
// SUMO, Simulation of Urban MObility; see http://sumo-sim.org/
// Copyright (C) 2002-2014 DLR (http://www.dlr.de/) and contributors
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

#include "MSNoLogicJunction.h"
#include "MSLane.h"
#include <algorithm>
#include <cassert>
#include <cmath>

#ifdef CHECK_MEMORY_LEAKS
#include <foreign/nvwa/debug_new.h>
#endif // CHECK_MEMORY_LEAKS


// ===========================================================================
// static member definitions
// ===========================================================================

// ===========================================================================
// method definitions
// ===========================================================================
MSNoLogicJunction::MSNoLogicJunction(const std::string& id,
                                     const Position& position,
                                     const PositionVector& shape,
                                     std::vector<MSLane*> incoming
#ifdef HAVE_INTERNAL_LANES
                                     , std::vector<MSLane*> internal
#endif
                                    ):
    MSJunction(id, position, shape),
    myIncomingLanes(incoming)
#ifdef HAVE_INTERNAL_LANES
    , myInternalLanes(internal)
#endif
{}


MSNoLogicJunction::~MSNoLogicJunction() {}


void
MSNoLogicJunction::postloadInit() {
    std::vector<MSLane*>::iterator i;
    // inform links where they have to report approaching vehicles to
    for (i = myIncomingLanes.begin(); i != myIncomingLanes.end(); ++i) {
        const MSLinkCont& links = (*i)->getLinkCont();
        for (MSLinkCont::const_iterator j = links.begin(); j != links.end(); j++) {
            (*j)->setRequestInformation(-1, false, false, std::vector<MSLink*>(), std::vector<MSLane*>());
        }
    }
}



/****************************************************************************/

