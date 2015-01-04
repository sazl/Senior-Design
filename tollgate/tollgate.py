import traci
import traci.constants as tc

class Tollgate(object):
    global_id = 0

    def __init__(self, price, edge_id, edge_offset, operating_hours):
        self.price = price
        self.edge_id = edge_id
        self.edge_offset = edge_offset
        self.operating = True
        self.operation_hours = operating_hours
        self.detector_ids = []
        self.total = 0
        self.revenue = 0
        self.occupancy = []
        self.average_occupancy = 0

    def update_tollgate(self):
        pass
    
    def update_statistics(self):
        for d in detector_ids:
            n = traci.inductionloop.getLastStepVehicleNumber(d)
            if n > 0:
                self.total += n
                if self.operating:
                    self.revenue += price * n
            oc = traci.inductionloop.getLastStepOccupancy(d)
            if oc > 0:
                self.occupancy.append(oc)

    def finalize(self):
        self.average_occupancy = sum(self.occupancy) / len(self.occupancy)
