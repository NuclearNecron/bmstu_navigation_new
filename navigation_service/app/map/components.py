class NodeType:

    def __init__(
        self,
        uni: int | None = None,
        campus: int | None = None,
        complex: int | None = None,
        corpus: int | None = None,
        building: int | None = None,
        floor: int | None = None,
        transit: int | None = None,
        room: int | None = None,
        exit_point: int | None = None,
    ):
        self.uni = uni
        self.campus = campus
        self.complex = complex
        self.corpus = corpus
        self.building = building
        self.floor = floor
        self.transit = transit
        self.room = room
        self.exit_point = exit_point
        self.realizations = list()


class Node:

    def __init__(
        self,
        id: int,
        type: NodeType,
        x: float,
        y: float,
        z: float,
        latitude: float | None,
        longitude: float | None,
        name: str,
    ):
        self.id = id
        self.type = type
        self.x = x
        self.y = y
        self.z = z
        self.conns = dict()
        self.latitude = latitude
        self.longitude = longitude
        self.name = name

    def __lt__(self, other):
        return self.id < other.id


class Connection:

    def __init__(self, id: int, distance: float, node1_id: int, node2_id: int):
        self.id = id
        self.distance = distance
        self.node1_id = node1_id
        self.node2_id = node2_id


class RouteNode:

    def __init__(
        self, target_distance: float, start_distance: float, node: Node, previous
    ):
        self.target_distance = target_distance
        self.start_distance = start_distance
        self.current = node
        self.previous = previous

    def __lt__(self, other):
        if (
            self.target_distance + self.start_distance
            != other.target_distance + self.start_distance
        ):
            return (
                self.target_distance + self.start_distance
                < other.target_distance + self.start_distance
            )
        return self.current < other.current
