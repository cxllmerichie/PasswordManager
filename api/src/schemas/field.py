from apidevtools.security import encryptor
from apidevtools.simpleorm import Schema
from uuid import uuid4, UUID
import pydantic

from ..const import keys


class FieldBase(Schema):
    __tablename__ = 'field'

    id: UUID = pydantic.Field(default_factory=uuid4)
    name: str | bytes = pydantic.Field(default=..., min_length=1)
    value: str | bytes = pydantic.Field(default=..., min_length=1)

    async def into_db(self) -> Schema:
        self.name, key = encryptor.encrypt(self.name)
        self.value, _ = encryptor.encrypt(self.value, key)
        await keys.set(self.id, key)
        return self

    async def from_db(self) -> Schema:
        if key := await keys.get(self.id, convert=True):
            self.name = encryptor.decrypt(self.name, key, evaluate=True)
            self.value = encryptor.decrypt(self.value, key, evaluate=True)
        return self


class FieldCreate(FieldBase):
    ...


class FieldCreateCrud(FieldBase):
    item_id: int = pydantic.Field(default=...)


class Field(FieldCreateCrud):
    ...
