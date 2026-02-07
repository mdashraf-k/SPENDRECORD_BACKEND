from sqlalchemy.orm import Session
from models.group_members import GroupMembers


def add_group_members(db: Session, group_id: int, user_id: int, role: str, is_active: bool):
    group_members = GroupMembers(
        group_id = group_id,
        user_id = user_id,
        role = role,
        is_active = is_active
    )
    db.add(group_members)
    db.commit()
    db.refresh(group_members)
    return group_members

