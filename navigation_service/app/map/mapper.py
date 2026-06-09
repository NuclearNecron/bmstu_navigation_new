import typing
import gc
import math
import heapq
import httpx
from app.map.components import NodeType, Node, Connection, RouteNode
from app.schemas import (
    NodeTypeSchema,
    NodeSchema,
    ConnectionSchema,
    NodeTypesSchema,
    NodesSchema,
    ConnectionsSchema,
    ChangeNodeSchema,
    ChangeConnectionSchema,
    ChangeNodeTypeSchema,
)

import os
from dotenv import load_dotenv

load_dotenv()

class Map:

    def __init__(self):
        self.object_service_url = os.getenv("OBJECT_SERVICE_URL")  # URL сервиса объектов
        self.types = dict()
        self.nodes = dict()
        self.all_conns = dict()
        self.exits = dict()
        self.exits_list = set()
        self.street_connections = dict()
        self.working = False

    async def __get_node_types(self) -> NodeTypesSchema:
        """
        Получить все типы объектов из backend_op и построить иерархию.
        Типы определяются автоматически по глубине в дереве:
        корень (parent_id=null) -> university,
        его ребёнок -> campus,
        следующий -> complex, и т.д.
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(f"http://{self.object_service_url}/objects/mapped")
            if response.status_code != 200:
                raise Exception(f"Failed to fetch mapped objects: {response.status_code}")
            objects_data = response.json()

        # --- Строим дерево ---
        tree = {}
        root_nodes = []

        for obj in objects_data:
            obj_id = obj["id"]
            parent_id = obj.get("parent_id")

            tree.setdefault(obj_id, {"obj": None, "children": []})
            tree[obj_id]["obj"] = obj

            if parent_id:
                tree.setdefault(parent_id, {"obj": None, "children": []})
                tree[parent_id]["children"].append(tree[obj_id])
            else:
                root_nodes.append(tree[obj_id])

        # --- Порядок типов: от университета к выходу ---
        hierarchy_order = [
            "university",  # 0
            "campus",      # 1
            "complex",     # 2
            "corpus",      # 3
            "building",    # 4
            "floor",       # 5
            "transit",     # 6
            "room",        # 7
            "exit_point"   # 8
        ]

        node_types = {}

        def build_hierarchy(node, depth=0, current_path=None):
            if current_path is None:
                current_path = {}

            obj = node["obj"]
            if obj is None:
                return

            # Определяем тип по глубине (с проверкой выхода за границы)
            obj_type = hierarchy_order[depth] if depth < len(hierarchy_order) else "room"

            path = current_path.copy()

            # Отображение типа в поле NodeTypeSchema
            hierarchy_map = {
                "university": "uni",
                "campus": "campus",
                "complex": "complex",
                "corpus": "corpus",
                "building": "building",
                "floor": "floor",
                "transit": "transit",
                "room": "room",
                "exit_point": "exit_point",
            }

            if obj_type in hierarchy_map:
                path[hierarchy_map[obj_type]] = obj["id"]

            # Сохраняем NodeType для этого объекта
            node_type = NodeTypeSchema(id=obj["id"], **path)
            node_types[obj["id"]] = node_type

            # Рекурсивно обрабатываем детей
            for child_node in node["children"]:
                build_hierarchy(child_node, depth + 1, path)

        # Обрабатываем все корни (глубина 0 = university)
        for root in root_nodes:
            build_hierarchy(root, depth=0)

        return NodeTypesSchema(node_types=node_types)

    async def __get_all_nodes(self) -> NodesSchema:
        async with httpx.AsyncClient() as client:
            # Получаем список нод
            response = await client.get(f"http://{self.object_service_url}/nodes/mapped")
            if response.status_code != 200:
                raise Exception(f"Failed to fetch mapped nodes: {response.status_code}")

            nodes_data = response.json()

        # Собираем словарь нод в формате {node_id: NodeSchema}
        nodes_dict = {}
        for node_data in nodes_data:
            node_id = node_data["id"]
            nodes_dict[node_id] = NodeSchema(
                id=node_data["id"],
                type_id=node_data["object_id"],
                x=node_data["x"] if node_data["x"] is not None else 0.0,
                y=node_data["y"] if node_data["y"] is not None else 0.0,
                z=node_data["z"] if node_data["z"] is not None else 0.0,
                latitude=node_data["latitude"],
                longitude=node_data["longitude"],
                name=node_data["short_name"],
            )

        return NodesSchema(nodes=nodes_dict)

    async def __get_all_nodes_with_connections(self) -> ConnectionsSchema:
        async with httpx.AsyncClient() as client:
            # Получаем все соединения узлов с помощью нового эндпоинта
            response = await client.get(f"http://{self.object_service_url}/connection-nodes/mapper")
            if response.status_code != 200:
                raise Exception(f"Failed to fetch connections: {response.status_code}")

            connections_data = response.json()

        connections_dict = {}
        for node1_id, connected_nodes in connections_data.items():
            node1_id_int = int(node1_id)
            connections_dict[node1_id_int] = {}
            for node2_id, conn_data in connected_nodes.items():
                node2_id_int = int(node2_id)
                connections_dict[node1_id_int][node2_id_int] = ConnectionSchema(
                    id=conn_data["id"],
                    node1_id=conn_data["node1_id"],
                    node2_id=conn_data["node2_id"],
                    distance=conn_data["distance"],
                )

        return ConnectionsSchema(nodes=connections_dict)

    async def start(self):
        nodetypes = await self.__get_node_types()
        for nodetype_id, nodetype in nodetypes.node_types.items():
            self.types[nodetype_id] = NodeType(
                uni=nodetype.uni,
                campus=nodetype.campus,
                complex=nodetype.complex,
                corpus=nodetype.corpus,
                building=nodetype.building,
                floor=nodetype.floor,
                transit=nodetype.transit,
                room=nodetype.room,
                exit_point=nodetype.exit_point,
            )
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
        nodes_with_connections = await self.__get_all_nodes_with_connections()
        for node1_id, connected_nodes in nodes_with_connections.nodes.items():
            for node2_id, connection in connected_nodes.items():
                self.all_conns[connection.id] = Connection(
                    id=connection.id,
                    distance=connection.distance,
                    node1_id=connection.node1_id,
                    node2_id=connection.node2_id,
                )
                if (
                    self.nodes[node1_id].latitude is not None
                    and self.nodes[node2_id].latitude is not None
                ):
                    self.street_connections[node1_id][node2_id] = self.all_conns[
                        connection.id
                    ]
                    self.street_connections[node2_id][node1_id] = self.all_conns[
                        connection.id
                    ]
                else:
                    self.nodes[node1_id].conns[node2_id] = self.all_conns[connection.id]
                    self.nodes[node2_id].conns[node1_id] = self.all_conns[connection.id]
        self.working = True

    async def add_type(self, id: int, nodetype: NodeTypeSchema) -> None:
        self.types[id] = NodeType(
            uni=nodetype.uni,
            campus=nodetype.campus,
            complex=nodetype.complex,
            corpus=nodetype.corpus,
            building=nodetype.building,
            floor=nodetype.floor,
            transit=nodetype.transit,
            room=nodetype.room,
            exit_point=nodetype.exit_point,
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
        if (
            self.nodes[node1_id].latitude is not None
            and self.nodes[node2_id].latitude is not None
        ):
            self.street_connections[node1_id][node2_id] = self.all_conns[connection.id]
            self.street_connections[node2_id][node1_id] = self.all_conns[connection.id]
        else:
            self.nodes[node1_id].conns[node2_id] = self.all_conns[connection.id]
            self.nodes[node2_id].conns[node1_id] = self.all_conns[connection.id]
        return None

    async def change_type(self, nodetype: ChangeNodeTypeSchema):
        target_value = nodetype.id

        if nodetype.uni == target_value:
            target_param = "uni"
        elif nodetype.campus == target_value:
            target_param = "campus"
        elif nodetype.complex == target_value:
            target_param = "complex"
        elif nodetype.corpus == target_value:
            target_param = "corpus"
        elif nodetype.building == target_value:
            target_param = "building"
        elif nodetype.floor == target_value:
            target_param = "floor"
        elif nodetype.transit == target_value:
            target_param = "transit"
        elif nodetype.room == target_value:
            target_param = "room"
        elif nodetype.exit_point == target_value:
            target_param = "exit_point"
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
        conn = self.all_conns[id]
        node1_id = conn.node1_id
        node2_id = conn.node2_id

        if node1_id in self.nodes and node2_id in self.nodes[node1_id].conns:
            del self.nodes[node1_id].conns[node2_id]
        if node2_id in self.nodes and node1_id in self.nodes[node2_id].conns:
            del self.nodes[node2_id].conns[node1_id]

        if (
            node1_id in self.street_connections
            and node2_id in self.street_connections[node1_id]
        ):
            del self.street_connections[node1_id][node2_id]
        if (
            node2_id in self.street_connections
            and node1_id in self.street_connections[node2_id]
        ):
            del self.street_connections[node2_id][node1_id]

        del self.all_conns[id]
        gc.collect()
        return None

    async def delete_node(self, node_id: int):
        for _, connection in list(self.nodes[node_id].conns.items()):
            await self.delete_conn(connection.id)

        if node_id in self.exits_list:
            self.exits_list.remove(node_id)

        node = self.nodes[node_id]
        if node.type.complex is not None and node.type.complex in self.exits:
            if node_id in self.exits[node.type.complex]:
                self.exits[node.type.complex].remove(node_id)
                if len(self.exits[node.type.complex]) == 0:
                    del self.exits[node.type.complex]

        if node_id in self.street_connections:
            del self.street_connections[node_id]

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
            target_param = "uni"
        elif nodetype.campus == type_id:
            target_param = "campus"
        elif nodetype.complex == type_id:
            target_param = "complex"
        elif nodetype.corpus == type_id:
            target_param = "corpus"
        elif nodetype.building == type_id:
            target_param = "building"
        elif nodetype.floor == type_id:
            target_param = "floor"
        elif nodetype.transit == type_id:
            target_param = "transit"
        elif nodetype.room == type_id:
            target_param = "room"
        elif nodetype.exit_point == type_id:
            target_param = "exit_point"

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
            (target.x - current.x) ** 2
            + (target.y - current.y) ** 2
            + (target.z - current.z) ** 2
        )

    def __group_route_by_floor(self, route: list) -> list:
        grouped_route = []
        current_floor = None
        current_floor_nodes = []

        for node in route:
            floor = node.type.floor

            if floor != current_floor:
                if current_floor is not None:
                    grouped_route.append({current_floor: current_floor_nodes})
                current_floor = floor
                current_floor_nodes = []

            current_floor_nodes.append((node.id,node.name))

        if current_floor is not None:
            grouped_route.append({current_floor: current_floor_nodes})

        return grouped_route

    async def __navigate_building(self, start_node: int, target_node: int):
        start = self.nodes[start_node]
        target = self.nodes[target_node]

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

                grouped_result = self.__group_route_by_floor(result[::-1])

                return {"result": grouped_result, "length": length}

            visited.add(current_node.current.id)

            for key_node_id, conn_value in current_node.current.conns.items():
                if int(key_node_id) in visited:
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
                            self.__calculate_distance(self.nodes[key_node_id], target),
                            current_node.start_distance + conn_value.distance,
                            self.nodes[key_node_id],
                            current_node,
                        ),
                    )

            visited.add(current_node.current.id)

            for key_node_id, conn_value in current_node.current.conns.items():
                if int(key_node_id) in visited:
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
                            self.__calculate_distance(self.nodes[key_node_id], target),
                            current_node.start_distance + conn_value.distance,
                            self.nodes[key_node_id],
                            current_node,
                        ),
                    )

    async def __navigate_street(self, start_complex: int, target_complex: int):
        start_exits = self.exits[start_complex]
        target_exits = self.exits[target_complex]

        min_distance = float("inf")
        best_start_exit = None
        best_target_exit = None

        for start_exit_id in start_exits:
            for target_exit_id in target_exits:
                if (
                    start_exit_id in self.street_connections
                    and target_exit_id in self.street_connections[start_exit_id]
                ):

                    distance = self.street_connections[start_exit_id][
                        target_exit_id
                    ].distance

                    if distance < min_distance:
                        min_distance = distance
                        best_start_exit = start_exit_id
                        best_target_exit = target_exit_id

        return {
            "distance": min_distance,
            "start_exit": best_start_exit,
            "target_exit": best_target_exit,
        }

    async def navigate_main(self, start_node: int, target_node: int):
        start = self.nodes[start_node]
        target = self.nodes[target_node]

        start_complex = start.type.complex
        target_complex = target.type.complex
        print(start_complex)
        print(target_complex)

        if start_complex is None or target_complex is None:
            return None

        if start_complex == target_complex:
            result = await self.__navigate_building(start_node, target_node)
            return result
        else:
            street_nav = await self.__navigate_street(start_complex, target_complex)
            if street_nav is None:
                return None
            start_nav = await self.__navigate_building(
                start_node=start_node, target_node=street_nav["start_exit"]
            )
            target_nav = await self.__navigate_building(
                start_node=street_nav["target_exit"], target_node=target_node
            )
            return {
                "1": start_nav,
                "street": {
                    "start_node": {
                        "id": street_nav["start_exit"],
                        "latitude": self.nodes[street_nav["start_exit"]].latitude,
                        "longtitude": self.nodes[street_nav["start_exit"]].longtitude,
                    },
                    "target_node": {
                        "id": street_nav["target_exit"],
                        "latitude": self.nodes[street_nav["target_exit"]].latitude,
                        "longtitude": self.nodes[street_nav["target_exit"]].longtitude,
                    },
                },
                "2": target_nav,
            }
