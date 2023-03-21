from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_empty_invested_amount, check_charity_project_exists,
    check_charity_project_inactive, check_charity_project_full_amount,
    check_name_duplicate,
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charityproject import charity_project_crud
from app.models import Donation
from app.services.invested_project import invested_project
from app.schemas.charityproject import (
    CharityProjectDB, CharityProjectCreate, CharityProjectUpdate
)

router = APIRouter()


@router.get(
    '/',
    response_model_exclude_none=True,
    response_model=List[CharityProjectDB],
)
async def get_all_charity_project(
        session: AsyncSession = Depends(get_async_session),
):
    return await charity_project_crud.get_multi(session)


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    await check_name_duplicate(charity_project.name, session)
    charity_project = await charity_project_crud.create(
        charity_project,
        session,
        commit=False
    )
    model_objects = await charity_project_crud.get_investment_active(
        session, Donation
    )
    if model_objects:
        session.add_all(invested_project(charity_project, model_objects))
    await session.commit()
    await session.refresh(charity_project)
    return charity_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    return await charity_project_crud.remove(
        await check_empty_invested_amount(
            await check_charity_project_exists(project_id, session),
            session
        ),
        session
    )


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charity_project(
    project_id: int,
    charity_project_obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    charity_project_obj = await check_charity_project_exists(
        project_id, session
    )
    check_charity_project_inactive(charity_project_obj)
    if charity_project_obj_in.name:
        await check_name_duplicate(
            charity_project_obj_in.name,
            session
        )
    if not charity_project_obj_in.full_amount:
        return await charity_project_crud.update(
            charity_project_obj, charity_project_obj_in, session
        )
    check_charity_project_full_amount(
        charity_project_obj.invested_amount,
        charity_project_obj_in.full_amount
    )
    charity_project_obj = await charity_project_crud.update(
        charity_project_obj, charity_project_obj_in, session, commit=False
    )
    model_objects = await charity_project_crud.get_investment_active(
        session, Donation
    )
    if model_objects:
        session.add_all(invested_project(charity_project_obj, model_objects))
    await session.commit()
    await session.refresh(charity_project_obj)
    return charity_project_obj
