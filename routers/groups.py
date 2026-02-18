from fastapi import APIRouter, status, HTTPException
from dependencies import DB, current_user
from crud.groups import create_groups, get_users_groups
from crud.groups import add_admin_as_members, edit_group_info, is_group_admin
from schemas.groups import GroupsCreate


router = APIRouter(
    prefix="/groups",
    tags=["Groups"]
)

@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_groups(user: current_user, db: DB):

    #Permission check
    if user is None:
        return HTTPException(status_code=402, detail="Authentication Failed")
    
    return get_users_groups(
        db=db,
        user=user
    )





@router.put("/{group_id}/edit", status_code=status.HTTP_200_OK)
async def edit_group(db: DB, user: current_user, group_id: int, group_edit_request: GroupsCreate):
    if user is None:
        return HTTPException(status_code=402, detail="Authentication Failed")
    
    if not is_group_admin(db=db, group_id=group_id, user_id=user.id):
        raise HTTPException(status_code=402, detail="Authentication Failed")
    
    return edit_group_info(db=db, group_id=group_id, name=group_edit_request.name, description=group_edit_request.description)






@router.post("/create_group")
async def create_group(user: current_user, db: DB, group_create_request: GroupsCreate):
    if user is None:
        return HTTPException(status_code=402, detail="Authentication Failed")
    
    # Calling crud function
    group = create_groups(
        db= db,
        name = group_create_request.name,
        created_by = user.id,
        description = group_create_request.description
    )

    # add creator as admin member
    add_admin_as_members(
        db=db,
        group_id=group.id,
        user_id=user.id,
        role="admin"
    )