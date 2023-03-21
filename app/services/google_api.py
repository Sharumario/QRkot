from datetime import datetime

from fastapi import HTTPException
from aiogoogle import Aiogoogle

from app.core.config import settings


FORMAT = "%Y/%m/%d %H:%M:%S"

SHEET_ID = 0
TABLE_COLUMN_COUNT = 11
TABLE_ROW_COUNT = 100

ERROR_COUNT_ROWS_OR_COLUMN = (
    'Ошибка! Слишком мало строк или колонок создано в таблице! '
    'Создано строк: {rows_create}, необходимо {rows_need}. '
    'Создано столбцов {columns_create}, необходимо {columns_need}.'
)

PERMISSION_BODY = {
    'type': 'user',
    'role': 'writer',
    'emailAddress': settings.email
}
SPREADSHEET_BODY = dict(
    properties=dict(
        title='Отчет на ',
        locale='ru_RU',
    ),
    sheets=[dict(properties=dict(
        sheetType='GRID',
        sheetId=SHEET_ID,
        title='Лист1',
        gridProperties=dict(
            rowCount=TABLE_ROW_COUNT,
            columnCount=TABLE_COLUMN_COUNT,
        )
    ))]
)
TABLE_HEAD = [
    ['Отчет от', ],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание']
]


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body = SPREADSHEET_BODY.copy()
    spreadsheet_body['properties']['title'] += datetime.now().strftime(FORMAT)
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    return response['spreadsheetId']


async def set_user_permissions(
        spreadsheet_id: str,
        wrapper_services: Aiogoogle
) -> None:
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=PERMISSION_BODY,
            fields="id"
        ))


async def spreadsheets_update_value(
        spreadsheet_id: str,
        charity_projects: list,
        wrapper_services: Aiogoogle
) -> None:
    service = await wrapper_services.discover('sheets', 'v4')
    table_values = TABLE_HEAD.copy()
    table_values[0].append(f'{datetime.now().strftime(FORMAT)}')
    table_values = (
        table_values +
        sorted([
            list(map(str, [
                project.name,
                project.close_date - project.create_date,
                project.description
            ])) for project in charity_projects
        ], key=lambda array: array[1])
    )
    rows = len(table_values)
    columns = max(len(columns) for columns in table_values)
    if rows > TABLE_ROW_COUNT or columns > TABLE_COLUMN_COUNT:
        raise HTTPException(
            status_code=404, detail=ERROR_COUNT_ROWS_OR_COLUMN.format(
                rows_create=TABLE_ROW_COUNT,
                rows_need=rows,
                columns_create=TABLE_COLUMN_COUNT,
                columns_need=columns
            ))
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=f'R1C1:R{rows}C{columns}',
            valueInputOption='USER_ENTERED',
            json={
                'majorDimension': 'ROWS',
                'values': table_values
            }
        )
    )
