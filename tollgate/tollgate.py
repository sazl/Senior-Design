import traci
import traci.constants as tc

from state import state

class Tollgate(object):
    global_id = 0

    def __init__(self, price, edge_id, edge_offset):
        self.price = price
        self.edge_id = state.edges_list[int(edge_id) % len(state.edges)]
        self.edge_offset = edge_offset
        self.operating = True
        self.lane_ids = []
        self.detector_ids = []
        self.total = 0
        self.revenue = 0
        self.occupancy = []
        self.average_occupancy = 0

    def update_statistics(self):
        for d in self.detector_ids:
            n = traci.inductionloop.getLastStepVehicleNumber(d)
            if n > 0:
                self.total += n
                if self.operating:
                    self.revenue += self.price * n
            oc = traci.inductionloop.getLastStepOccupancy(d)
            if oc > 0:
                self.occupancy.append(oc)

    def finalize(self):
        self.average_occupancy = sum(self.occupancy) / len(self.occupancy)

    def __str__(self):
        return 'price = {} edge_id = {} edge_offset = {}\n'.format(self.price, self.edge_id, self.edge_offset)
