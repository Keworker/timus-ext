from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy_serializer import SerializerMixin

from api.database.db_session import SqlAlchemyBase


class Friendship(SqlAlchemyBase, SerializerMixin):  # {
    __tablename__ = "friendships"

    sender_id: Column = Column(
        Integer, ForeignKey("users.id_"), primary_key=True, nullable=False
    )
    recipient_id: Column = Column(
        Integer, ForeignKey("users.id_"), primary_key=True, nullable=False
    )
# }
