from sqlalchemy import Column, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from backend_op.app.database.database import db


class ObjectType(db):
    __tablename__ = "object_type"

    id = Column(Integer, primary_key=True, autoincrement=True)
    parent_id = Column(
        Integer, ForeignKey("object_type.id", ondelete="cascade"), nullable=True
    )
    number = Column(Integer, unique=True, nullable=False)
    short_name = Column(String(50), unique=True, nullable=False)
    full_name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    colour = Column(String(50), nullable=False)

    children = relationship("ObjectType")
    kinds_of_type = relationship(
        "ObjectKind", back_populates="type_of_kind", foreign_keys="ObjectKind.type_id"
    )


class ObjectKind(db):
    __tablename__ = "object_kind"

    id = Column(Integer, primary_key=True, autoincrement=True)
    parent_id = Column(
        Integer, ForeignKey("object_kind.id", ondelete="cascade"), nullable=True
    )
    type_id = Column(
        Integer, ForeignKey("object_type.id", ondelete="cascade"), nullable=False
    )
    number = Column(Integer, unique=True, nullable=False)
    short_name = Column(String(50), unique=True, nullable=False)
    full_name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    colour = Column(String(50), nullable=False)

    children = relationship("ObjectKind")
    type_of_kind = relationship(
        "ObjectType", back_populates="kinds_of_type", foreign_keys="ObjectKind.type_id"
    )
    objects_of_kind = relationship(
        "Object", back_populates="kind_of_object", foreign_keys="Object.kind_id"
    )


class ObjectState(db):
    __tablename__ = "object_state"

    id = Column(Integer, primary_key=True, autoincrement=True)
    number = Column(Integer, unique=True, nullable=False)
    short_name = Column(String(50), unique=True, nullable=False)
    full_name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    colour = Column(String(50), nullable=False)
    objects_of_state = relationship(
        "Object", back_populates="state_of_object", foreign_keys="Object.state_id"
    )


class ConnectionType(db):
    __tabletame__ = "connection_type"

    id = Column(Integer, primary_key=True, autoincrement=True)
    number = Column(Integer, unique=True, nullable=False)
    short_name = Column(String(50), unique=True, nullable=False)
    full_name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    colour = Column(String(50), nullable=False)
    style = Column(Text, nullable=True)

    obj_connection_of_types = relationship(
        "ConnectionObject",
        back_populates="type_of_connections",
        foreign_keys="ConnectionObject.connection_type_id",
    )
    node_connection_of_types = relationship(
        "ConnectionNode",
        back_populates="type_of_connections",
        foreign_keys="ConnectionNode.connection_type_id",
    )
