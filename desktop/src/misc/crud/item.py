from apidevtools.utils import INF, now_tz_naive
from typing import Any

from .. import schemas
from ..const import db


async def create_item(category_id: int, item: dict) -> dict[str, Any]:
    item = schemas.ItemCreateCrud(**item, category_id=category_id)
    db_item = await db.insert(item, schemas.Item)
    return db_item.dict()


async def get_item(item_id: int, schema: type = schemas.Item) -> dict[str, Any] | None:
    query, args = f'SELECT * FROM "item" WHERE "id" = $1;', (item_id, )
    db_item = await (await db.select(query, args, schema)).first()
    return db_item.dict()


async def get_items(category_id: int, limit: int = INF, offset: int = 0, schema: type = schemas.Item) -> list[dict[str, Any]]:
    query, args = f'SELECT * FROM "item" WHERE "category_id" = $1 ORDER BY "is_favourite" DESC, "title", "description" LIMIT $2 OFFSET $3;', (category_id, limit, offset)
    db_items = await (await db.select(query, args, schema)).all()
    return [i.dict() for i in db_items]


async def update_item(item_id: int, item: dict) -> dict[str, Any]:
    item['modified_at'] = now_tz_naive()
    db_item = await (await db.update(schemas.ItemCreate(**item), dict(id=item_id), schemas.Item)).first()
    return db_item.dict()


async def delete_item(item_id: int) -> dict[str, Any]:
    db_item = await (await db.delete(dict(id=item_id), schemas.Item, 'item')).first()
    return db_item.dict()
