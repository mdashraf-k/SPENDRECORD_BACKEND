from fastapi import APIRouter, status, HTTPException
from dependencies import DB, current_user
from crud.group_members import get_all_member, add_member, remove_from_group


router = APIRouter(
    prefix="/members",
    tags=["Members"]
)


# def is_group_member(db, current_user, group)
@router.get("/{group_id}", status_code=status.HTTP_200_OK)
async def get_all_members(db:DB, group_id:int, current_user: current_user):
    # 1️⃣ check user is member of this group
    all_member = get_all_member(db=db, group_id=group_id, user_id=current_user.id)

    if (all_member == None):
        raise HTTPException(status_code=403, detail="Not a group member")
    return all_member
    

@router.put("/{group_id}/{user_id}/remove", status_code=status.HTTP_200_OK)
async def exit_from_group(db:DB, group_id:int, user_id:int):
    remove_status = remove_from_group(db=db, group_id=group_id, user_id=user_id)

    if remove_status == None:
        raise HTTPException(status_code=403, detail="Not a group member")
    
    return remove_status


@router.post("/{group_id}/{user_id}/add_member", status_code=status.HTTP_200_OK)
async def add_member_to_group(db:DB, group_id:int, user_id:int, current_user: current_user):
    if (add_member == None):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not allowed")
    
    return add_member(db=db, group_id=group_id, user_id=user_id, admin_id=current_user.id)

