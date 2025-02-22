from fastapi.security import OAuth2PasswordBearer as OAuth2Bearer
from fastapi import Depends, HTTPException
from apidevtools.security import hasher
import jwt

from .. import schemas, const
from .user import get_user


async def authenticate_user(email: str, password: str):
    db_user = await get_user(email=email, schema=schemas.UserCreate)
    if not db_user:
        raise HTTPException(status_code=404, detail=f'Email <{email}> not registered')
    if not hasher.cmp(pw_hash=db_user.password, password=password):
        raise HTTPException(status_code=401, detail=f'Invalid password for user <{db_user.email}>')
    return db_user


async def create_token(user: schemas.User) -> schemas.Token:
    db_user = await get_user(email=user.email, schema=schemas.UserCreate)
    token = jwt.encode(payload=dict(schemas.UserPayload(**dict(db_user))), key=const.JWT_SECRET_KEY, algorithm=const.JWT_ALGORITHM)
    return schemas.Token(access_token=token, token_type='Bearer')


async def get_current_user(token: str = Depends(OAuth2Bearer(tokenUrl='/auth/token'))) -> schemas.User:
    try:
        payload = jwt.decode(jwt=token, key=const.JWT_SECRET_KEY, algorithms=[const.JWT_ALGORITHM])
    except Exception:
        raise HTTPException(status_code=401, detail='Authorization error')
    db_user = await get_user(email=payload['email'], schema=schemas.User)
    if not db_user:
        raise HTTPException(status_code=401, detail=f'Unauthorized')
    return db_user
