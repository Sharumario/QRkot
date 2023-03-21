from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, PositiveInt


class DonationDB(BaseModel):
    full_amount: int
    comment: Optional[str]
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationListDB(DonationDB):
    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]


class DonationCreate(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str]

    class Config:
        extra = Extra.forbid
        schema_extra = {
            'example': {
                'full_amount': 2048,
                'comment': 'For food'
            }
        }