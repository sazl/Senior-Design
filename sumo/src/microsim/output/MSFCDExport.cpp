/****************************************************************************/
/// @file    MSFCDExport.cpp
/// @author  Daniel Krajzewicz
/// @author  Jakob Erdmann
/// @author  Mario Krumnow
/// @author  Michael Behrisch
/// @date    2012-04-26
/// @version $Id: MSFCDExport.cpp 16290 2014-05-05 12:38:38Z namdre $
///
// Realises dumping Floating Car Data (FCD) Data
/****************************************************************************/
// SUMO, Simulation of Urban MObility; see http://sumo-sim.org/
// Copyright (C) 2012-2014 DLR (http://www.dlr.de/) and contributors
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

#include <utils/iodevices/OutputDevice.h>
#include <utils/options/OptionsCont.h>
#include <utils/geom/GeoConvHelper.h>
#include <microsim/MSEdgeControl.h>
#include <microsim/MSEdge.h>
#include <microsim/MSLane.h>
#include <microsim/MSGlobals.h>
#include "MSFCDExport.h"
#include <microsim/MSNet.h>
#include <microsim/MSVehicle.h>
#include <microsim/MSPerson.h>

#ifdef HAVE_MESOSIM
#include <mesosim/MELoop.h>
#include <mesosim/MESegment.h>
#endif

#ifdef CHECK_MEMORY_LEAKS
#include <foreign/nvwa/debug_new.h>
#endif // CHECK_MEMORY_LEAKS


// ===========================================================================
// method definitions
// ===========================================================================
void
MSFCDExport::write(OutputDevice& of, SUMOTime timestep) {
    const bool useGeo = OptionsCont::getOptions().getBool("fcd-output.geo");
    const bool signals = OptionsCont::getOptions().getBool("fcd-output.signals");
    MSVehicleControl& vc = MSNet::getInstance()->getVehicleControl();
    MSVehicleControl::constVehIt it = vc.loadedVehBegin();
    MSVehicleControl::constVehIt end = vc.loadedVehEnd();

    of.openTag("timestep").writeAttr(SUMO_ATTR_TIME, time2string(timestep));
    for (; it != end; ++it) {
        const MSVehicle* veh = static_cast<const MSVehicle*>((*it).second);
        if (veh->isOnRoad()) {
            Position pos = veh->getPosition();
            MSLane* lane = veh->getLane();
            if (useGeo) {
                of.setPrecision(GEO_OUTPUT_ACCURACY);
                GeoConvHelper::getFinal().cartesian2geo(pos);
            }
            of.openTag(SUMO_TAG_VEHICLE);
            of.writeAttr(SUMO_ATTR_ID, veh->getID());
            of.writeAttr(SUMO_ATTR_X, pos.x());
            of.writeAttr(SUMO_ATTR_Y, pos.y());
            of.writeAttr(SUMO_ATTR_ANGLE, veh->getAngle());
            of.writeAttr(SUMO_ATTR_TYPE, veh->getVehicleType().getID());
            of.writeAttr(SUMO_ATTR_SPEED, veh->getSpeed());
            of.writeAttr(SUMO_ATTR_POSITION, veh->getPositionOnLane());
            of.writeAttr(SUMO_ATTR_LANE, lane->getID());
            of.writeAttr(SUMO_ATTR_SLOPE, lane->getShape().slopeDegreeAtOffset(veh->getPositionOnLane()));
            if (signals) {
                of.writeAttr("signals", toString(veh->getSignals()));
            }
            of.closeTag();
        }
    }
    // write persons
    MSEdgeControl& ec = MSNet::getInstance()->getEdgeControl();
    const std::vector<MSEdge*>& edges = ec.getEdges();
    for (std::vector<MSEdge*>::const_iterator e = edges.begin(); e != edges.end(); ++e) {
        const std::vector<MSPerson*>& persons = (*e)->getSortedPersons(timestep);
        for (std::vector<MSPerson*>::const_iterator it_p = persons.begin(); it_p != persons.end(); ++it_p) {
            MSPerson* p = *it_p;
            Position pos = p->getPosition();
            if (useGeo) {
                of.setPrecision(GEO_OUTPUT_ACCURACY);
                GeoConvHelper::getFinal().cartesian2geo(pos);
            }
            of.openTag(SUMO_TAG_PERSON);
            of.writeAttr(SUMO_ATTR_ID, p->getID());
            of.writeAttr(SUMO_ATTR_X, pos.x());
            of.writeAttr(SUMO_ATTR_Y, pos.y());
            of.writeAttr(SUMO_ATTR_ANGLE, p->getAngle());
            of.writeAttr(SUMO_ATTR_SPEED, p->getSpeed());
            of.writeAttr(SUMO_ATTR_POSITION, p->getEdgePos());
            of.writeAttr(SUMO_ATTR_EDGE, (*e)->getID());
            of.writeAttr(SUMO_ATTR_SLOPE, (*e)->getLanes()[0]->getShape().slopeDegreeAtOffset(p->getEdgePos()));
            of.closeTag();
        }
    }
    of.closeTag();
}

/****************************************************************************/
