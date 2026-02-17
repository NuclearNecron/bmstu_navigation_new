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

class ObjectState(db):
    __tablename__ = "object_state"

    id = Column(Integer, primary_key=True, autoincrement=True)
    number = Column(Integer, unique=True, nullable=False)
    short_name = Column(String(50), unique=True, nullable=False)
    full_name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    colour = Column(String(50), nullable=False)


class ConnectionType(db):
    __tabletame__ = "connection_type"

    id = Column(Integer, primary_key=True, autoincrement=True)
    number = Column(Integer, unique=True, nullable=False)
    short_name = Column(String(50), unique=True, nullable=False)
    full_name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    colour = Column(String(50), nullable=False)
    style = Column(Text, nullable=True)