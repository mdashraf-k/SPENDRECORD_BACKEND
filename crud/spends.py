from sqlalchemy.orm import Session
from models.spends import Spend


def add_spend(db:Session, description:str, amount: int, user_id: int, group_id: int):
    spend = Spend(
        user_id = user_id,
        description = description,
        amount = amount,
        group_id = group_id
    )
    db.add(spend)
    db.commit()
    db.refresh(spend)
    return spend
