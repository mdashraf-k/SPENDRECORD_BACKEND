from sqlalchemy.orm import Session
from models.groups import Group
from models.group_members import GroupMembers

def is_group_admin(db:Session, group_id: int, user_id:int) -> bool:
    return (
        db.query(GroupMembers).filter(GroupMembers.group_id == group_id,
                                      GroupMembers.user_id == user_id,
                                      GroupMembers.is_active == True,
                                      GroupMembers.role == "admin"

                                      ).first() is not None
    )



def get_users_groups(db:Session, user):
    
    return (
        db.query(Group).join(GroupMembers, Group.id == GroupMembers.group_id).filter(GroupMembers.user_id == user.id, GroupMembers.is_active == True).all()
    )


def create_groups(db: Session, name:str, created_by: str, description: str):
    groups = Group(
        name = name,
        created_by = created_by,
        description = description
    )

    db.add(groups)
    db.commit()
    db.refresh(groups)
    return groups


def edit_group_info(db:Session, group_id:int, name: str, description: str):
    group = db.query(Group).filter(Group.id == group_id).first()

    if group is None:
        return None
    
    if name is not None:
        group.name = name

    if description is not None:
        group.description = description

    db.commit()
    db.refresh(group)

    return group


# This crud operation for add owner as member without checking is admin adding or not
def add_admin_as_members(db: Session, group_id: int, user_id: int, role: str):
    group_members = GroupMembers(
        group_id = group_id,
        user_id = user_id,
        role = role,
    )
    db.add(group_members)
    db.commit()
    db.refresh(group_members)
    return group_members

# this function delete the group if user is admin
def group_delete(db: Session, group_id:int):
    group_for_delete = db.query(Group).filter(Group.id == group_id).first()

    if not group_for_delete:
        return None
    
    db.delete(group_for_delete)
    db.commit()
    return True
