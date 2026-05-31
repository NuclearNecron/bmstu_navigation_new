import typing
import gc
import math
import heapq
from app.map.components import NodeType, Node, Connection, RouteNode
from app.schemas import NodeTypeSchema, NodeSchema, ConnectionSchema, NodeTypesSchema, NodesSchema, ConnectionsSchema, ChangeNodeSchema,ChangeConnectionSchema,ChangeNodeTypeSchema

class Map:

    def __init__(self):
        self.types = dict()
        self.nodes = dict()
        self.all_conns = dict()
        self.exits = dict(int)
        self.exits_list = set(int)
        self.street_connections = dict()
        self.working = False
    
    async def __get_node_types(self) -> NodeTypesSchema:
        pass

    async def __get_all_nodes(self) -> NodesSchema:
        pass

    async def __get_all_nodes_with_connections(self) -> ConnectionsSchema:
        pass





    async def start(self):
        nodetypes = await self.__get_node_types()
        for nodetype_id, nodetype in nodetypes.node_types.items():
            self.types[nodetype_id] = NodeType(
                uni=nodetype.uni,
                campus=nodetype.campus,
                complex=nodetype.complex,
                corpus=nodetype.corpus,
                building=nodetype.building,
                floor=  nodetype.floor,
                transit=nodetype.transit,
                room=nodetype.room,
                exit_point= nodetype.exit_point,
            )
        del nodetypes
        gc.collect()
        nodes = await self.__get_all_nodes()
        if nodes:
            for node_id, node in nodes.nodes.items():
                self.nodes[node_id] = Node(
                    id=node.id,
                    type=self.types[node.type_id],
                    x=node.x,
                    y=node.y,
                    z=node.z,
                    name=node.name,
                    latitude=node.latitude,
                    longitude=node.longitude,
                )
                self.types[node.type_id].realizations.append(node_id)
                if self.nodes[node_id].latitude is not None:
                    if self.nodes[node_id].type.complex is not None:
                        self.exits_list.add(node_id)
                        complex = self.nodes[node_id].type.complex
                        if complex in self.exits:
                            self.exits[complex].append(node_id)
                        else:
                            self.exits[complex] = [node_id]
                        self.street_connections[node_id] = dict()

        del nodes
        gc.collect()
        nodes_with_connections = await self.__get_all_nodes_with_connections(node_id)
        for node1_id, connected_nodes in nodes_with_connections.nodes.items():
            for node2_id, connection in connected_nodes.items():
                self.all_conns[connection.id] = Connection(
                    id=connection.id,
                    distance=connection.distance,
                    node1_id=connection.node1_id,
                    node2_id=connection.node2_id,
                )
                if self.all_conns(node1_id).latitude is not None and  self.all_conns(node2_id).latitude is not None:
                    self.street_connections[node1_id][node2_id] = self.all_conns[connection.id]
                    self.street_connections[node2_id][node1_id] = self.all_conns[connection.id]
                else:
                    self.nodes[node1_id].conns[node2_id] = self.all_conns[connection.id]
                    self.nodes[node2_id].conns[node1_id] = self.all_conns[connection.id]
        del nodes_with_connections
        gc.collect()
        self.working = True

    async def add_type(self, id:int, nodetype: NodeTypeSchema) -> None:
        self.types[id] = NodeType(
                uni=nodetype.uni,
                campus=nodetype.campus,
                complex=nodetype.complex,
                corpus=nodetype.corpus,
                building=nodetype.building,
                floor=  nodetype.floor,
                transit=nodetype.transit,
                room=nodetype.room,
                exit_point= nodetype.exit_point,
            )
        return None

    async def add_node(self, node: NodeSchema) -> None:
        node_id = node.id
        self.nodes[node_id] = Node(
            id=node.id,
            type=self.types[node.type_id],
            x=node.x,
            y=node.y,
            z=node.z,
            name=node.name,
            latitude=node.latitude,
            longitude=node.longitude,
        )
        self.types[node.type_id].realizations.append(node_id)
        if self.nodes[node_id].latitude is not None:
            if self.nodes[node_id].type.complex is not None:
                self.exits_list.add(node_id)
                complex = self.nodes[node_id].type.complex
                if complex in self.exits:
                    self.exits[complex].append(node_id)
                else:
                    self.exits[complex] = [node_id]
                self.street_connections[node_id] = dict()
        return None

    async def add_conn(self, connection: ConnectionSchema) -> None:
        self.all_conns[connection.id] = Connection(
            id=connection.id,
            distance=connection.distance,
        )
        node1_id = connection.node1_id
        node2_id = connection.node2_id
        if self.all_conns(node1_id).latitude is not None and  self.all_conns(node2_id).latitude is not None:
            self.street_connections[node1_id][node2_id] = self.all_conns[connection.id]
            self.street_connections[node2_id][node1_id] = self.all_conns[connection.id]
        else:
            self.nodes[node1_id].conns[node2_id] = self.all_conns[connection.id]
            self.nodes[node2_id].conns[node1_id] = self.all_conns[connection.id]
        return None

    async def change_type(self, nodetype: ChangeNodeTypeSchema):
        target_value = nodetype.id
        
        if nodetype.uni == target_value:
            target_param = 'uni'
        elif nodetype.campus == target_value:
            target_param = 'campus'
        elif nodetype.complex == target_value:
            target_param = 'complex'
        elif nodetype.corpus == target_value:
            target_param = 'corpus'
        elif nodetype.building == target_value:
            target_param = 'building'
        elif nodetype.floor == target_value:
            target_param = 'floor'
        elif nodetype.transit == target_value:
            target_param = 'transit'
        elif nodetype.room == target_value:
            target_param = 'room'
        elif nodetype.exit_point == target_value:
            target_param = 'exit_point'
        else:
            return None
        
        for type_id, type_obj in self.types.items():
            current_value = getattr(type_obj, target_param)
            
            if current_value == target_value:
                if nodetype.uni is not None:
                    type_obj.uni = nodetype.uni
                if nodetype.campus is not None:
                    type_obj.campus = nodetype.campus
                if nodetype.complex is not None:
                    type_obj.complex = nodetype.complex
                if nodetype.corpus is not None:
                    type_obj.corpus = nodetype.corpus
                if nodetype.building is not None:
                    type_obj.building = nodetype.building
                if nodetype.floor is not None:
                    type_obj.floor = nodetype.floor
                if nodetype.transit is not None:
                    type_obj.transit = nodetype.transit
                if nodetype.room is not None:
                    type_obj.room = nodetype.room
                if nodetype.exit_point is not None:
                    type_obj.exit_point = nodetype.exit_point
        
        return None

    async def change_node(self, node: ChangeNodeSchema):
        node_obj = self.nodes[node.id]
        
        if node.x is not None:
            node_obj.x = node.x
        if node.y is not None:
            node_obj.y = node.y
        if node.z is not None:
            node_obj.z = node.z
        if node.latitude is not None:
            node_obj.latitude = node.latitude
        if node.longitude is not None:
            node_obj.longitude = node.longitude
        if node.name is not None:
            node_obj.name = node.name
            
        return None

    async def change_conn(self, conn: ChangeConnectionSchema):
        conn_obj = self.all_conns[conn.id]
        if conn.distance is not None:
            conn_obj.distance = conn.distance
        return None

    async def delete_conn(self, id: int):
        node1_id = self.all_conns[id].node1_id
        node2_id = self.all_conns[id].node2_id
        del self.nodes[node1_id].conns[node2_id]
        del self.nodes[node2_id].conns[node1_id]
        del self.all_conns[id]
        gc.collect()
        return None

    async def delete_node(self, node_id: int):
        for _, connection in self.nodes[node_id].conns.items():
            await self.delete_conn(connection.id)
        del self.nodes[node_id]
        gc.collect()
        return None
    async def __simple_delete_type(self, type_id: int):
        for node in self.types[type_id].realizations:
            await self.delete_node(node.id)
        del self.types[type_id]
        return None

    async def delete_type(self, type_id: int):
        for node in self.types[type_id].realizations:
            await self.delete_node(node.id)
        
        nodetype = self.types[type_id]
        
        if nodetype.uni == type_id:
            target_param = 'uni'
        elif nodetype.campus == type_id:
            target_param = 'campus'
        elif nodetype.complex == type_id:
            target_param = 'complex'
        elif nodetype.corpus == type_id:
            target_param = 'corpus'
        elif nodetype.building == type_id:
            target_param = 'building'
        elif nodetype.floor == type_id:
            target_param = 'floor'
        elif nodetype.transit == type_id:
            target_param = 'transit'
        elif nodetype.room == type_id:
            target_param = 'room'
        elif nodetype.exit_point == type_id:
            target_param = 'exit_point'
        
        for new_type_id, type_obj in self.types.items():
            current_value = getattr(type_obj, target_param)
            
            if current_value == type_id:
                await self.__simple_delete_type(new_type_id)

        del self.types[type_id]
        gc.collect()
        return None

    @staticmethod
    def __calculate_distance(current: Node, target: Node) -> float:
        return math.sqrt(
            (target.x - current.x)**2
            + (target.y - current.y)**2
            + (target.z - current.z)**2
        )

    async def __navigate_building(self, start_node: int, target_node: int):
        start = self.nodes[f"{start_node}"]
        target = self.nodes[f"{target_node}"]

        to_visit = []
        visited = set()

        heapq.heappush(
            to_visit,
            RouteNode(
                target_distance=self.__calculate_distance(start, target),
                start_distance=0,
                node=start,
                previous=-1,
            ),
        )

        while to_visit:
            current_node = heapq.heappop(to_visit)

            if current_node.current.id == target.id:
                result = list()
                length = current_node.start_distance
                while current_node.previous != -1:
                    result.append(current_node.current)
                    current_node = current_node.previous
                else:
                    result.append(current_node.current)
                return {"result": result[::-1], "length": length}

            visited.add(current_node.current.id)

            for key_node_id, conn_value in current_node.current.conns.items():
                if int(key_node_id) in visited:
                    continue
                if self.nodes[f"{key_node_id}"].type.name == KEY_TYPES.STREET:
                    continue
                if self.nodes[f"{key_node_id}"].type.name == KEY_TYPES.ELEVATOR:
                    continue

                if elem := next(
                    (
                        element
                        for element in to_visit
                        if element.current.id == int(key_node_id)
                    ),
                    None,
                ):
                    if (
                        current_node.start_distance + conn_value.distance
                        < elem.start_distance
                    ):
                        elem.start_distance = (
                            current_node.start_distance + conn_value.distance
                        )
                        elem.previous = current_node
                else:
                    heapq.heappush(
                        to_visit,
                        RouteNode(
                            self.__calculate_distance(
                                self.nodes[f"{key_node_id}"], target
                            ),
                            current_node.start_distance + conn_value.distance,
                            self.nodes[f"{key_node_id}"],
                            current_node,
                        ),
                    )

    async def __navigate_street(self, start_node: int, target_node: int):
        pass

    async def navigate_main(self, start_node: int, target_node: int):
        start = self.nodes[f"{start_node}"]
        target = self.nodes[f"{target_node}"]

        kor_s = await self.__go_up(KEY_TYPES.KORPUS, start)
        kor_t = await self.__go_up(KEY_TYPES.KORPUS, target)

        if kor_s == kor_t:
            result = await self.__navigate_building(start_node, target_node)
            return result["result"]
        elif kor_s is None:
            if kor_t is None:
                result = await self.__navigate_street(start_node, target_node)
                return result["result"]
            else:
                entrances = self.exits[f"{kor_t.id}"]
                best_street_route = None
                route_length = -1
                optimal_entrance = -1
                for key in entrances:
                    temp_result = await self.__navigate_street(start_node, int(key))
                    if optimal_entrance == -1 or temp_result < route_length:
                        best_street_route = temp_result["result"]
                        route_length = temp_result.length
                        optimal_entrance = int(key)
                building_route = await self.__navigate_building(
                    optimal_entrance, target_node
                )
                return best_street_route[:-1] + building_route["result"]
        elif kor_t is None:
            exits = self.exits[f"{kor_s.id}"]
            best_street_route = None
            route_length = -1
            optimal_exit = -1
            for key in exits:
                temp_result = await self.__navigate_street(int(key), target_node)
                if optimal_exit == -1 or temp_result < route_length:
                    best_street_route = temp_result["result"]
                    route_length = temp_result.length
                    optimal_exit = int(key)
            building_route = await self.__navigate_building(start_node, optimal_exit)
            return building_route["result"][:-1] + best_street_route
        else:
            exits_s = self.exits[f"{kor_s.id}"]
            exits_t = self.exits[f"{kor_t.id}"]
            best_street_route = None
            route_length = -1
            optimal_exit_s = -1
            optimal_exit_t = -1
            for key_s in exits_s:
                for key_t in exits_t:
                    temp_result = await self.__navigate_street(int(key_s), int(key_t))
                if optimal_exit_s == -1 or temp_result < route_length:
                    best_street_route = temp_result["result"]
                    route_length = temp_result.length
                    optimal_exit_s = int(key_s)
                    optimal_exit_t = int(key_t)
            building_route_s = await self.__navigate_building(start_node, optimal_exit_s)
            building_route_t = await self.__navigate_building(optimal_exit_t, target_node)
            return building_route_s["result"][:-1] + best_street_route["result"][:-1] + building_route_t