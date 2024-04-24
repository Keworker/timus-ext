from sqlalchemy import Column, Integer
from sqlalchemy_serializer import SerializerMixin

from api.database.db_session import SqlAlchemyBase


class User(SqlAlchemyBase, SerializerMixin):  # {
    __tablename__ = "users"

    id_: Column = Column(
        Integer, primary_key=True, autoincrement=True, nullable=False
    )
    timus_id: Column = Column(
        Integer, unique=True, nullable=False
    )
# }
