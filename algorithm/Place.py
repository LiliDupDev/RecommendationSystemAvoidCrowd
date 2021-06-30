import enum

class Congestion_Level(enum.Enum):
    CONGESTIONED = -5
    UNCONGESTIONED = 5


class Place:
    def __init__(self, store, distance, coordinates, payoff, estimated_congestion, cluster):
        self.store = store
        self.distance = distance
        self.X = coordinates[1]
        self.Y = coordinates[0]
        self.utility = 0.0
        self.model_probability = 0.0
        self.payoff = payoff
        self.cluster = cluster
        if estimated_congestion >= 0.25:  # Value that indicates when to start to
            self.congestion_level = Congestion_Level.CONGESTIONED
        else:
            self.congestion_level = Congestion_Level.UNCONGESTIONED

    def __str__(self):
        return ("Store: {0} \n    Distance: {1} " +
                "\n    Coordinates: {2},{3} " +
                "\n    Payoff:{4}" +
                "\n    Congestion:{5}").format(self.store, self.distance, self.Y, self.X, self.payoff,
                                               self.congestion_level.name)

    def __eq__(self, other):
        if self.store == other.store and self.X == other.X and self.Y == other.Y:
            return True
        else:
            return False