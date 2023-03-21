from typing import List, Optional, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User


SchemasModel = TypeVar('AnySchemasModel')
Model = TypeVar('AnyClassModel')


class CRUDBase:

    def __init__(self, model):
        self.model = model

    async def create(
        self,
        obj_in: SchemasModel,
        session: AsyncSession,
        user: Optional[User] = None,
        commit: bool = True,
    ) -> Model:
        obj_in_data = obj_in.dict()
        if user is not None:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        if commit:
            await session.commit()
            await session.refresh(db_obj)
        return db_obj

    async def get(self, obj_id: int, session: AsyncSession,) -> Model:
        db_obj = await session.execute(
            select(self.model).where(
                self.model.id == obj_id
            )
        )
        return db_obj.scalars().first()

    async def get_multi(self, session: AsyncSession) -> List[Model]:
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def get_investment_active(
            self,
            session: AsyncSession,
            model: Model
    ) -> Model:
        db_obj = await session.execute(
            select(model).where(
                model.fully_invested == 0
            )
        )
        return db_obj.scalars().all()
