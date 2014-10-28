/****************************************************************************/
/// @file    MSDevice_Tripinfo.cpp
/// @author  Daniel Krajzewicz
/// @author  Laura Bieker
/// @author  Michael Behrisch
/// @author  Jakob Erdmann
/// @date    Fri, 30.01.2009
/// @version $Id: MSDevice_Tripinfo.cpp 16005 2014-03-24 12:46:02Z cschmidt87 $
///
// A device which collects info on the vehicle trip
/****************************************************************************/
// SUMO, Simulation of Urban MObility; see http://sumo-sim.org/
// Copyright (C) 2009-2014 DLR (http://www.dlr.de/) and contributors
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

#include <microsim/MSNet.h>
#include <microsim/MSLane.h>
#include <microsim/MSVehicle.h>
#include <utils/options/OptionsCont.h>
#include <utils/iodevices/OutputDevice.h>
#include "MSDevice_Tripinfo.h"

#ifdef CHECK_MEMORY_LEAKS
#include <foreign/nvwa/debug_new.h>
#endif // CHECK_MEMORY_LEAKS


// ===========================================================================
// method definitions
// ===========================================================================
// ---------------------------------------------------------------------------
// static initialisation methods
// ---------------------------------------------------------------------------
void
MSDevice_Tripinfo::buildVehicleDevices(SUMOVehicle& v, std::vector<MSDevice*>& into) {
    if (OptionsCont::getOptions().isSet("tripinfo-output")) {
        MSDevice_Tripinfo* device = new MSDevice_Tripinfo(v, "tripinfo_" + v.getID());
        into.push_back(device);
    }
}


// ---------------------------------------------------------------------------
// MSDevice_Tripinfo-methods
// ---------------------------------------------------------------------------
MSDevice_Tripinfo::MSDevice_Tripinfo(SUMOVehicle& holder, const std::string& id)
    : MSDevice(holder, id), myDepartLane(""), myDepartPos(-1), myDepartSpeed(-1),
      myWaitingSteps(0), myArrivalTime(-1), myArrivalLane(""), myArrivalPos(-1), myArrivalSpeed(-1) {
}


MSDevice_Tripinfo::~MSDevice_Tripinfo() {
}


bool
MSDevice_Tripinfo::notifyMove(SUMOVehicle& /*veh*/, SUMOReal /*oldPos*/,
                              SUMOReal /*newPos*/, SUMOReal newSpeed) {
    if (newSpeed <= SUMO_const_haltingSpeed) {
        myWaitingSteps++;
    }
    return true;
}


bool
MSDevice_Tripinfo::notifyEnter(SUMOVehicle& veh, MSMoveReminder::Notification reason) {
    if (reason == MSMoveReminder::NOTIFICATION_DEPARTED) {
        if (!MSGlobals::gUseMesoSim) {
            myDepartLane = static_cast<MSVehicle&>(veh).getLane()->getID();
        }
        myDepartPos = veh.getPositionOnLane();
        myDepartSpeed = veh.getSpeed();
    }
    return true;
}


bool
MSDevice_Tripinfo::notifyLeave(SUMOVehicle& veh, SUMOReal /*lastPos*/,
                               MSMoveReminder::Notification reason) {
    if (reason >= MSMoveReminder::NOTIFICATION_ARRIVED) {
        myArrivalTime = MSNet::getInstance()->getCurrentTimeStep();
        if (!MSGlobals::gUseMesoSim) {
            myArrivalLane = static_cast<MSVehicle&>(veh).getLane()->getID();
        }
        // @note vehicle may have moved past its arrivalPos during the last step
        // due to non-zero arrivalspeed but we consider it as arrived at the desired position
        myArrivalPos = myHolder.getArrivalPos();
        myArrivalSpeed = veh.getSpeed();
    }
    return true;
}


void
MSDevice_Tripinfo::generateOutput() const {
    SUMOReal routeLength = myHolder.getRoute().getLength();
    // write
    OutputDevice& os = OutputDevice::getDeviceByOption("tripinfo-output");
    os.openTag("tripinfo").writeAttr("id", myHolder.getID());
    routeLength -= myDepartPos;
    os.writeAttr("depart", time2string(myHolder.getDeparture())).writeAttr("departLane", myDepartLane)
    .writeAttr("departPos", myDepartPos).writeAttr("departSpeed", myDepartSpeed)
    .writeAttr("departDelay", time2string(myHolder.getDeparture() - myHolder.getParameter().depart));
    if (myArrivalLane != "") {
        routeLength -= MSLane::dictionary(myArrivalLane)->getLength() - myArrivalPos;
    }
    os.writeAttr("arrival", time2string(myArrivalTime)).writeAttr("arrivalLane", myArrivalLane)
    .writeAttr("arrivalPos", myArrivalPos).writeAttr("arrivalSpeed", myArrivalSpeed)
    .writeAttr("duration", time2string(myArrivalTime - myHolder.getDeparture()))
    .writeAttr("routeLength", routeLength).writeAttr("waitSteps", myWaitingSteps)
    .writeAttr("rerouteNo", myHolder.getNumberReroutes());
    const std::vector<MSDevice*>& devices = myHolder.getDevices();
    std::ostringstream str;
    for (std::vector<MSDevice*>::const_iterator i = devices.begin(); i != devices.end(); ++i) {
        if (i != devices.begin()) {
            str << ' ';
        }
        str << (*i)->getID();
    }
    os.writeAttr("devices", str.str()).writeAttr("vType", myHolder.getVehicleType().getID())
    .writeAttr("vaporized", (myHolder.getEdge() == *(myHolder.getRoute().end() - 1) ? "" : "0"));
}


/****************************************************************************/

