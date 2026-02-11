from sqlalchemy.orm import Session
from models.group_members import GroupMembers



def get_all_member(db: Session, group_id:int, user_id:int):
    # print(group_id, user_id)
    is_member = db.query(GroupMembers).filter(GroupMembers.group_id == group_id, GroupMembers.user_id == user_id, GroupMembers.is_active == True)

    if not is_member:
        return None

    return db.query(GroupMembers).filter(GroupMembers.group_id == group_id, GroupMembers.is_active == True).all()


# this function cheching adder is a group admin or not
def is_group_admin(db:Session, group_id:int, user_id:int, admin_id:int) -> bool:
    return db.query(GroupMembers).filter(
        GroupMembers.group_id == group_id,
        GroupMembers.user_id == admin_id,
        GroupMembers.role == "admin",
        GroupMembers.is_active == True
    ).first() is not None

def add_member(db: Session, group_id: int, user_id: int, admin_id:int):
    if (is_group_admin(db=db, group_id=group_id, user_id=user_id, admin_id=admin_id) == False):
        return None

    group_members = GroupMembers(
        group_id = group_id,
        user_id = user_id,
    )
    db.add(group_members)
    db.commit()
    db.refresh(group_members)
    return group_members

def remove_from_group(db: Session, group_id:int, user_id:int):
    is_member = db.query(GroupMembers).filter(GroupMembers.group_id == group_id, GroupMembers.user_id == user_id, GroupMembers.is_active == True)

    if not is_member:
        return None
    
    member = db.query(GroupMembers).filter(GroupMembers.group_id == group_id, GroupMembers.user_id == user_id).first()

    member.is_active = False
    db.commit()
    db.refresh(member)
    return member