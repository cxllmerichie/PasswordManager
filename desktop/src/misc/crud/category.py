from apidevtools.utils import INF
from typing import Any

from .. import schemas
from ..const import db


async def create_category(category: dict) -> dict[str, Any]:
    db_category = await db.insert(schemas.CategoryCreate(**category), schemas.Category)
    return db_category.dict()


async def get_category(category_id: int = None, title: str = None, schema: type = schemas.Category)\
        -> dict[str, Any] | None:
    field, value = ('id', category_id) if category_id else ('title', title)
    query, args = f'SELECT * FROM "category" WHERE "{field}" = $1;', (value, )
    db_category = await (await db.select(query, args, schema)).first()
    return db_category.dict()


async def get_categories(limit: int = INF, offset: int = 0, schema: type = schemas.Category) -> list[dict[str, Any]]:
    query, args = f'SELECT * FROM "category" ORDER BY "is_favourite" DESC, "title", "description" LIMIT $2 OFFSET $3;', (limit, offset)
    db_categories = await (await db.select(query, args, schema)).all()
    return [c.dict() for c in db_categories]


async def update_category(category_id: int, category: dict) -> dict[str, Any]:
    db_category = await (await db.update(schemas.CategoryCreate(**category), dict(id=category_id), schemas.Category)).first()
    return db_category.dict()


async def delete_category(category_id: int) -> dict[str, Any]:
    db_category = await (await db.delete(dict(id=category_id), schemas.Category, 'category')).first()
    return db_category.dict()
