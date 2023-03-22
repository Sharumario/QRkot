from typing import Dict

from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud.charityproject import charity_project_crud
from app.models import CharityProject
from app.services.google_api import (
    set_user_permissions, spreadsheets_create, spreadsheets_update_value
)


router = APIRouter()
GOOGLE_SPREADSHEETS_URL = 'https://docs.google.com/spreadsheets/d/{sheet_id}'


@router.post(
    '/',
    response_model=Dict[str, str],
    dependencies=[Depends(current_superuser)],
)
async def get_report(
        session: AsyncSession = Depends(get_async_session),
        wrapper_services: Aiogoogle = Depends(get_service)

):
    spreadsheet_id = await spreadsheets_create(wrapper_services)
    await set_user_permissions(spreadsheet_id, wrapper_services)
    try:
        await spreadsheets_update_value(
            spreadsheet_id,
            await charity_project_crud.get_investment_active_or_no_active(
                session, CharityProject, no_active=True
            ),
            wrapper_services
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
    return {'url': GOOGLE_SPREADSHEETS_URL.format(
        sheet_id=spreadsheet_id
    )}
