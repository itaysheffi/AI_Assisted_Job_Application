from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate


def create_item(db: Session, item_in: ItemCreate) -> Item:
    item = Item(name=item_in.name, description=item_in.description)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def get_item(db: Session, item_id: int) -> Item | None:
    return db.get(Item, item_id)


def list_items(db: Session, *, skip: int = 0, limit: int = 100) -> list[Item]:
    stmt = select(Item).offset(skip).limit(limit)
    return list(db.scalars(stmt).all())


def update_item(db: Session, *, item: Item, item_in: ItemUpdate) -> Item:
    data = item_in.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(item, k, v)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def delete_item(db: Session, *, item: Item) -> None:
    db.delete(item)
    db.commit()

