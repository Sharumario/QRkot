from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt


class CharityProjectBase(BaseModel):
    name: str = Field(..., max_length=100)
    description: str = Field(...,)
    full_amount: PositiveInt

    class Config:
        min_anystr_length = 1


class CharityProjectCreate(CharityProjectBase):

    class Config:
        extra = Extra.forbid
        schema_extra = {
            'example': {
                'name': 'Save the cats',
                'description': 'For food',
                'full_amount': 1024
            }
        }


class CharityProjectUpdate(CharityProjectCreate):
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None)
    full_amount: Optional[PositiveInt]


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
