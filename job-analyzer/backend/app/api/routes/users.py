from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, status

from app.schemas.users import UserCreate, UserOut

router = APIRouter(prefix="/users", tags=["users"])

# Temporary in-memory store (good enough for Day 2 API structure).
_USERS: dict[int, UserOut] = {}
_NEXT_ID = 1


@router.get("", response_model=list[UserOut])
def list_users() -> list[UserOut]:
    return list(_USERS.values())


@router.post("", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate) -> UserOut:
    global _NEXT_ID
    # NOTE: This endpoint is still using an in-memory store for now.
    # It intentionally never returns or stores the raw password.
    user = UserOut(id=_NEXT_ID, email=payload.email, created_at=datetime.now(timezone.utc))
    _USERS[_NEXT_ID] = user
    _NEXT_ID += 1
    return user


@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int) -> UserOut:
    user = _USERS.get(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

