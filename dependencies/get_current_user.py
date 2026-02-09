from fastapi import Depends, HTTPException, status
from typing import Annotated
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from core.config import settings



oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

# Decode current User and used them every where
def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")

        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user.")
        return {"username": username, "id": user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user.")
