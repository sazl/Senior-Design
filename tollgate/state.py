state = None

class State:
    individual  = None
    generation  = None
    initialized = False
    step        = 0
    edges       = {}
    edges_list  = []
    tollgates   = []


if state is None:
    state = State()
