from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.crud.item import create_item, delete_item, get_item, list_items, update_item
from app.schemas.item import ItemCreate, ItemRead, ItemUpdate

router = APIRouter()


@router.get("/", response_model=list[ItemRead])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> list[ItemRead]:
    return list_items(db, skip=skip, limit=limit)


@router.post("/", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
def create_new_item(item_in: ItemCreate, db: Session = Depends(get_db)) -> ItemRead:
    return create_item(db, item_in)


@router.get("/{item_id}", response_model=ItemRead)
def read_item(item_id: int, db: Session = Depends(get_db)) -> ItemRead:
    item = get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@router.patch("/{item_id}", response_model=ItemRead)
def patch_item(item_id: int, item_in: ItemUpdate, db: Session = Depends(get_db)) -> ItemRead:
    item = get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return update_item(db, item=item, item_in=item_in)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_item(item_id: int, db: Session = Depends(get_db)) -> None:
    item = get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    delete_item(db, item=item)
    return None

