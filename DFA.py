class State:
    def __init__(self, last_successor, goal_type=None):
        self.successors = dict()
        self.last_successor = last_successor
        self.goal_type = goal_type

    def get_next_state(self, value):
        if value in self.successors:
            return self.successors[value]
        else:
            return self.last_successor

    def add_successor(self, other_state, edge_values):
        for value in edge_values:
            if not (value in self.successors):
                self.successors[value] = other_state