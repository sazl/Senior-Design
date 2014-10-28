function sendDoubleCmd(cmdID, varID, objID, value)
%sendDoubleCmd An internal function to build a message which sends a double.

%   Copyright 2013 Universidad Nacional de Colombia,
%   Politecnico Jaime Isaza Cadavid.
%   Authors: Andres Acosta, Jairo Espinosa, Jorge Espinosa.
%   $Id: sendDoubleCmd.m 17 2014-05-30 14:32:09Z afacostag $

import traci.constants
global message
traci.beginMessage(cmdID, varID, objID, 1+8);
message.string = [message.string uint8(sscanf(constants.TYPE_DOUBLE,'%x')) ...
    traci.packInt64(value)];
traci.sendExact();