function setType(polygonID, polygonType)
%setType
%   setType(POLYGONID,POLYGONTTYPE) Sets the (abstract) type of the polygon.

%   Copyright 2013 Universidad Nacional de Colombia,
%   Politecnico Jaime Isaza Cadavid.
%   Authors: Andres Acosta, Jairo Espinosa, Jorge Espinosa.
%   $Id: setType.m 17 2014-05-30 14:32:09Z afacostag $

import traci.constants
global message
traci.beginMessage(constants.CMD_SET_POLYGON_VARIABLE, constants.VAR_TYPE, polygonID, 1+4+length(polygonType));
message.string = [message.string uint8(sscanf(constants.TYPE_STRING,'%x')) ...
    traci.packInt32(length(polygonType)) uint8(polygonType)]; 
traci.sendExact();