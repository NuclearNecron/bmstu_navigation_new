from sqlalchemy import Column, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database.database import db


class Object(db):
    __tablename__ = "object"

    id = Column(Integer, primary_key=True, autoincrement=True)
    parent_id = Column(
        Integer, ForeignKey("object.id", ondelete="cascade"), nullable=True
    )
    kind_id = Column(
        Integer, ForeignKey("object_kind.id", ondelete="cascade"), nullable=False
    )
    state_id = Column(
        Integer, ForeignKey("object_state.id", ondelete="cascade"), nullable=False
    )
    short_name = Column(String(50), unique=True, nullable=False)
    full_name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    address = Column(Text, nullable=True)
    plan_link = Column(Text, nullable=True)
    blueprint_link = Column(Text, nullable=True)
    scale = Column(Text, nullable=True)
    height = Column(Float, nullable=True)
    SVG = Column(Text, nullable=True)

    children = relationship("Object")
    kind_of_object = relationship(
        "ObjectKind", back_populates="objects_of_kind", foreign_keys="Object.kind_id"
    )
    state_of_object = relationship(
        "ObjectState", back_populates="objects_of_state", foreign_keys="Object.state_id"
    )

    nodes_of_object = relationship(
        "Node", back_populates="object_of_node", foreign_keys="Node.object_id"
    )


class ConnectionObject(db):
    __tablename__ = "connection_object"

    id = Column(Integer, primary_key=True, autoincrement=True)
    object_id1 = Column(
        Integer, ForeignKey("object.id", ondelete="cascade"), nullable=False
    )
    object_id2 = Column(
        Integer, ForeignKey("object.id", ondelete="cascade"), nullable=False
    )
    connection_type_id = Column(
        Integer, ForeignKey("connection_type.id"), nullable=True
    )
    distance = Column(Float, nullable=False)


    type_of_connections = relationship(
        "ConnectionType",
        back_populates="obj_connection_of_types",
        foreign_keys="ConnectionObject.connection_type_id",
    )
