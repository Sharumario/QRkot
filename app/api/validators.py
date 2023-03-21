from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charityproject import charity_project_crud
from app.models import CharityProject


EMPTY_INVESTED_ERROR = 'В проект были внесены средства, не подлежит удалению!'
FULL_AMOUNT_ERROR = 'Нельзя установить сумму меньше уже вложенной!'
NAME_DUPLICATE_ERROR = 'Проект с таким именем уже существует!'
PROJECT_INACTIVE_ERROR = 'Закрытый проект нельзя редактировать!'
PROJECT_NOT_EXSISTS_ERROR = 'Проект не найден!'


def check_charity_project_full_amount(
        invested_amount: int,
        full_amount: int
) -> None:
    if invested_amount > full_amount:
        raise HTTPException(status_code=422, detail=FULL_AMOUNT_ERROR)


def check_charity_project_inactive(
    charity_project: CharityProject
) -> None:
    if charity_project.fully_invested:
        raise HTTPException(status_code=400, detail=PROJECT_INACTIVE_ERROR)


async def check_charity_project_exists(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    charity_project = await charity_project_crud.get(
        obj_id=project_id, session=session
    )
    if not charity_project:
        raise HTTPException(status_code=404, detail=PROJECT_NOT_EXSISTS_ERROR)
    return charity_project


async def check_empty_invested_amount(
    charity_project_obj: CharityProject,
    session: AsyncSession,
) -> CharityProject:
    if charity_project_obj.invested_amount != 0:
        raise HTTPException(status_code=400, detail=EMPTY_INVESTED_ERROR)
    return charity_project_obj


async def check_name_duplicate(
        project_name: str,
        session: AsyncSession
) -> None:
    room_id = await charity_project_crud.get_charity_project_id_by_name(
        project_name=project_name,
        session=session
    )
    if room_id is not None:
        raise HTTPException(status_code=400, detail=NAME_DUPLICATE_ERROR)
