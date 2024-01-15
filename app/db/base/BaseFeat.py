import json
import uuid
from datetime import datetime
from typing import TypeVar, Generic, Type, Optional

from sqlalchemy import select, Select, func, String, delete, update, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.db.dbManager import db_session


class ModelExt(object):
    """
    Model extension, implementing `__repr__` method which returns all the class attributes
    """

    def __repr__(self):
        fields = self.__dict__
        if "_sa_instance_state" in fields:
            del fields["_sa_instance_state"]

        return json.dumps(fields, ensure_ascii=False)



class DbBase(DeclarativeBase):
    id: Mapped[int] = mapped_column(String, primary_key=True)
    create_time: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    update_time: Mapped[datetime] = mapped_column(DateTime, onupdate=func.now(),server_default=func.now())
    create_user: Mapped[str] = mapped_column(String,nullable=True)
    update_user: Mapped[str] = mapped_column(String,nullable=True)

    def __repr__(self):
        fields = self.__dict__
        if "_sa_instance_state" in fields:
            del fields["_sa_instance_state"]

        return json.dumps(fields, ensure_ascii=False)


ModelType = TypeVar("ModelType", bound=DbBase)


class CRUDBase(Generic[ModelType]):

    def __init__(self, model: Type[ModelType]):

        self.model = model

    async def list(self, stm: Select[ModelType]) -> [ModelType]:
        async with db_session.begin() as session:
            # return db_session.query(ChatPromptTemplateConfig).all()
            return (await session.scalars(stm)).all()

    async def get_one(self, stm: Select[ModelType]) -> ModelType:
        # return db_session.query(ChatPromptTemplateConfig).all()
        async with db_session.begin() as session:
            return (await session.scalars(stm)).first()

    async def count(self, stm: Select[ModelType]) -> int:
        async with db_session.begin() as session:
            # return db_session.query(ChatPromptTemplateConfig).all()
            return await session.scalar(stm)

    async def page(self, stm: Select[ModelType], current: int, size: int) -> [ModelType]:
        async with db_session.begin() as session:
            return (await session.scalars(stm.limit(size).offset((current - 1) * size))).all()

    async def get_by_id(self, id: str) -> ModelType:
        return await self.get_one(self.select().filter(self.model.id == id))

    def select(self):
        return select(self.model)

    def update_stm(self):
        return update(self.model)



    def select_count(self):
        return select(func.count()).select_from(self.model)

    async def add(self, model: ModelType):
        if model.id is None or model.id == "":
            model.id = uuid.uuid4().hex
        async with db_session.begin() as session:
            session.add(model)

    async def update(self, model: ModelType):
        async with db_session.begin() as session:
            origin = (await session.scalars(self.select().filter(self.model.id == model.id))).first()
            self.copy_attr(model, origin)


    def copy_attr(self, model, to_model):
        for attr in model.__dict__.keys():
            if not attr.startswith("_"):
                setattr(to_model, attr, getattr(model, attr))

