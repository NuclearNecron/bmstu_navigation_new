from sqlalchemy import Column, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database.database import db


class NodeType(db):
    __tablename__ = "node_type"

    id = Column(Integer, primary_key=True, autoincrement=True)
    short_name = Column(String(50), unique=True, nullable=False)
    full_name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    colour = Column(String(50), nullable=False)
    size = Column(Float, nullable=False)

    nodes_of_type = relationship(
        "Node", back_populates="type_of_node", foreign_keys="Node.type_id"
    )


class Node(db):
    __tablename__ = "node"

    id = Column(Integer, primary_key=True, autoincrement=True)
    object_id = Column(
        Integer, ForeignKey("object.id", ondelete="cascade"), nullable=False
    )
    type_id = Column(
        Integer, ForeignKey("node_type.id", ondelete="cascade"), nullable=False
    )
    short_name = Column(String(50), unique=True, nullable=False)
    full_name = Column(String(100), unique=True, nullable=False)
    SVG = Column(Text, nullable=True)
    x = Column(Float, nullable=True)
    y = Column(Float, nullable=True)
    z = Column(Float, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    object_of_node = relationship(
        "Object", back_populates="nodes_of_object", foreign_keys="Node.object_id"
    )
    type_of_node = relationship(
        "NodeType", back_populates="nodes_of_type", foreign_keys="Node.type_id"
    )


class ConnectionNode(db):
    __tablename__ = "connection_node"

    id = Column(Integer, primary_key=True, autoincrement=True)
    node_id1 = Column(
        Integer, ForeignKey("node.id", ondelete="cascade"), nullable=False
    )
    node_id2 = Column(
        Integer, ForeignKey("node.id", ondelete="cascade"), nullable=False
    )
    connection_type_id = Column(
        Integer, ForeignKey("connection_type.id"), nullable=True
    )
    distance = Column(Float, nullable=False)

    type_of_connections = relationship(
        "ConnectionType",
        back_populates="node_connection_of_types",
        foreign_keys="ConnectionNode.connection_type_id",
    )

