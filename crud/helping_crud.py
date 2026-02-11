from sqlalchemy.orm import Session;
from models.group_members import GroupMembers


# checking is the person is group member or not!
def is_group_member(db:Session, group_id:int, user_id:int) -> bool:
    return (
        db.query(GroupMembers).filter(GroupMembers.group_id == group_id,
                                      GroupMembers.user_id == user_id,
                                      GroupMembers.is_active == True
                                      ).first() is not None
    )