function sendIntCmd(cmdID, varID, objID, value)
%sendIntCmd An internal function to build a message which sends an int.

%   Copyright 2013 Universidad Nacional de Colombia,
%   Politecnico Jaime Isaza Cadavid.
%   Authors: Andres Acosta, Jairo Espinosa, Jorge Espinosa.
%   $Id: sendIntCmd.m 17 2014-05-30 14:32:09Z afacostag $

import traci.constants
global message
traci.beginMessage(cmdID, varID, objID, 1+4);
message.string = [message.string uint8(sscanf(constants.TYPE_INTEGER,'%x')) ...
    traci.packInt32(value)];
traci.sendExact();