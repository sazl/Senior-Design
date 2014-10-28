/****************************************************************************/
/// @file    MSEventControlTest.cpp
/// @author  Matthias Heppner
/// @author  Michael Behrisch
/// @author  Jakob Erdmann
/// @date    2009-11-23
/// @version $Id: MSEventControlTest.cpp 15959 2014-03-17 16:58:35Z cschmidt87 $
///
// Tests the class MSEventControl  
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

#include <gtest/gtest.h>
#include <microsim/MSEventControl.h>
#include "../utils/common/CommandMock.h"


/* Test the method 'execute'. Tests if the execute method from the Command Class is called.*/

TEST(MSEventControl, test_method_execute) {	
	
	MSEventControl *edge = new MSEventControl();
	CommandMock *mock = new CommandMock(); 
	edge->setCurrentTimeStep(4);
	edge->addEvent(mock,1,MSEventControl::ADAPT_AFTER_EXECUTION);
	
	EXPECT_FALSE(mock->isExecuteCalled());
	edge->execute(5);
	EXPECT_TRUE(mock->isExecuteCalled());
}



