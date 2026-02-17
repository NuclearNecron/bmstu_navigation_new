from sqlalchemy import Column, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from backend_op.app.database.database import db


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
    number = Column(Integer, unique=True, nullable=False)
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
