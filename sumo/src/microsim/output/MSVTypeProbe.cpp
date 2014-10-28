/****************************************************************************/
/// @file    MSVTypeProbe.cpp
/// @author  Tino Morenz
/// @author  Daniel Krajzewicz
/// @author  Jakob Erdmann
/// @author  Michael Behrisch
/// @date    Wed, 24.10.2007
/// @version $Id: MSVTypeProbe.cpp 15692 2014-02-22 09:17:02Z behrisch $
///
// Writes positions of vehicles that have a certain (named) type
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

#include <string>
#include <utils/common/WrappingCommand.h>
#include <microsim/MSNet.h>
#include <microsim/MSVehicle.h>
#include <microsim/MSLane.h>
#include <utils/iodevices/OutputDevice.h>
#include <utils/geom/GeoConvHelper.h>

#include "MSVTypeProbe.h"

#ifdef CHECK_MEMORY_LEAKS
#include <foreign/nvwa/debug_new.h>
#endif // CHECK_MEMORY_LEAKS


// ===========================================================================
// method definitions
// ===========================================================================
MSVTypeProbe::MSVTypeProbe(const std::string& id,
                           const std::string& vType,
                           OutputDevice& od, SUMOTime frequency)
    : Named(id), myVType(vType), myOutputDevice(od), myFrequency(frequency) {
    MSNet::getInstance()->getEndOfTimestepEvents().addEvent(this, 0, MSEventControl::ADAPT_AFTER_EXECUTION);
    myOutputDevice.writeXMLHeader("vehicle-type-probes");
}


MSVTypeProbe::~MSVTypeProbe() {
}


SUMOTime
MSVTypeProbe::execute(SUMOTime currentTime) {
    myOutputDevice.openTag("timestep") << " time=\"" << time2string(currentTime) << "\" id=\"" << getID() << "\" vType=\"" << myVType << "\"";
    MSVehicleControl& vc = MSNet::getInstance()->getVehicleControl();
    MSVehicleControl::constVehIt it = vc.loadedVehBegin();
    MSVehicleControl::constVehIt end = vc.loadedVehEnd();
    for (; it != end; ++it) {
        const MSVehicle* veh = static_cast<const MSVehicle*>((*it).second);
        if (myVType == "" || myVType == veh->getVehicleType().getID()) {
            if (!veh->isOnRoad()) {
                continue;
            }
            Position pos = veh->getLane()->getShape().positionAtOffset(veh->getPositionOnLane());
            myOutputDevice.openTag("vehicle") << " id=\"" << veh->getID()
                                              << "\" lane=\"" << veh->getLane()->getID()
                                              << "\" pos=\"" << veh->getPositionOnLane()
                                              << "\" x=\"" << pos.x()
                                              << "\" y=\"" << pos.y();
            if (GeoConvHelper::getFinal().usingGeoProjection()) {
                GeoConvHelper::getFinal().cartesian2geo(pos);
                myOutputDevice.setPrecision(GEO_OUTPUT_ACCURACY);
                myOutputDevice << "\" lat=\"" << pos.y() << "\" lon=\"" << pos.x();
                myOutputDevice.setPrecision();
            }
            myOutputDevice << "\" speed=\"" << veh->getSpeed() << "\"";
            myOutputDevice.closeTag();
        }

    }
    myOutputDevice.closeTag();
    return myFrequency;
}


/****************************************************************************/
