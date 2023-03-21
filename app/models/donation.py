from sqlalchemy import Column, ForeignKey, Integer, Text

from .abstract_model import AbstractModel


class Donation(AbstractModel):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)

    def __repr__(self) -> str:
        return (
            f'user_id: {self.user_id}, '
            f'comment: {self.comment[:8]} , '
            f'{super().__repr__()}'
        )