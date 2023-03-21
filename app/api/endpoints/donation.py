from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user, current_superuser
from app.crud.donation import donation_crud
from app.models import CharityProject, User
from app.schemas.donation import DonationCreate, DonationDB, DonationListDB
from app.services.invested_project import invested_project


router = APIRouter()


@router.get(
    '/',
    response_model_exclude_none=True,
    response_model=List[DonationListDB],
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    return await donation_crud.get_multi(session)


@router.post(
    '/',
    response_model_exclude_none=True,
    response_model=DonationDB,
)
async def create_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    donation = await donation_crud.create(
        donation, session, user, commit=False
    )
    model_objects = await donation_crud.get_investment_active(
        session, CharityProject
    )
    if model_objects:
        session.add_all(invested_project(donation, model_objects))
    await session.commit()
    await session.refresh(donation)
    return donation


@router.get(
    '/my',
    response_model_exclude_none=True,
    response_model=List[DonationDB],
)
async def get_all_user_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    return await donation_crud.get_user_donations(session, user)
