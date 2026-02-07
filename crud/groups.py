from sqlalchemy.orm import Session
from models.groups import Group


def add_groups(db: Session, name:str, created_by: str):
    groups = Group(
        name = name,
        created_by = created_by
    )

    db.add(groups)
    db.commit()
    db.refresh(groups)
    return groups