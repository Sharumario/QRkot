from typing import Optional, List

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject
from app.schemas.charityproject import CharityProjectUpdate


class CharityProjectCrud(CRUDBase):
    async def get_charity_project_id_by_name(
            self,
            project_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        charity_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        charity_project_id = charity_project_id.scalars().first()
        return charity_project_id

    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession,
    ) -> List[CharityProject]:
        charity_projects = await session.execute(
            select(CharityProject).where(CharityProject.fully_invested)
        )
        charity_projects = charity_projects.scalars().all()
        return charity_projects

    async def update(
        self,
        charity_project_obj: CharityProject,
        charity_project_obj_in: CharityProjectUpdate,
        session: AsyncSession,
        commit: bool = True
    ) -> CharityProject:
        charity_project_obj_data = jsonable_encoder(charity_project_obj)
        update_data = charity_project_obj_in.dict(exclude_unset=True)
        for field in charity_project_obj_data:
            if field in update_data:
                setattr(charity_project_obj, field, update_data[field])
        session.add(charity_project_obj)
        if commit:
            await session.commit()
            await session.refresh(charity_project_obj)
        return charity_project_obj

    async def remove(
        self,
        charity_project_obj: CharityProject,
        session: AsyncSession,
    ) -> CharityProject:
        await session.delete(charity_project_obj)
        await session.commit()
        return charity_project_obj


charity_project_crud = CharityProjectCrud(CharityProject)
