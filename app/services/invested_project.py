from datetime import datetime
from typing import Union, List

from app.models import CharityProject, Donation


def invested_project(
    target: Union[CharityProject, Donation],
    sources: List[Union[CharityProject, Donation]]
) -> List[Union[CharityProject, Donation]]:
    target.invested_amount = target.invested_amount or 0
    count = 0
    for obj in sources:
        money = min(
            obj.full_amount - obj.invested_amount,
            target.full_amount - target.invested_amount
        )
        for item in [obj, target]:
            item.invested_amount += money
            if item.full_amount == item.invested_amount:
                item.close_date = datetime.now()
                item.fully_invested = True
        count += 1
        if target.fully_invested:
            break
    return sources[:count]
