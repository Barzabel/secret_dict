from fastapi import HTTPException
from sqlalchemy import select, insert, delete
from passlib.context import CryptContext
import cryptocode
import random 
import string 


from app.models import Secrets
from app.database import async_session_maker


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def encode_massege(massage, key):
    return cryptocode.encrypt(massage, key)

def decode_massege(encoded_massage, key):
    return cryptocode.decrypt(encoded_massage, key)

def random_str():
    return ''.join((random.choice(string.ascii_lowercase) for x in range(10)))


class SecretsDAO:
    model = Secrets


    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()


    @classmethod
    async def add(cls, password: str, body: str):
        password_hash = get_password_hash(password)
        encode_body = encode_massege(body, password)

        new_url = random_str()

        while await cls.find_one_or_none(url=new_url):
            new_url = random_str()



        query = insert(cls.model).values(password=password_hash, body=encode_body, url=new_url).returning(cls.model.url)
        async with async_session_maker() as session:
            result = await session.execute(query)
            await session.commit()
            return result.mappings().first()

    @classmethod
    async def delete(cls, url:str):
        massege = await cls.find_one_or_none(url=url)
        if massege is None:
            raise HTTPException(status_code=402, detail="Неверный url")       
        query = delete(cls.model).where(cls.model.url == url)

        async with async_session_maker() as session:
            await session.execute(query)
            await session.commit()
            return True

    @classmethod
    async def get_and_delete(cls, password, url):
        massege = await cls.find_one_or_none(url=url)
        if massege is None:
            raise HTTPException(status_code=402, detail="Неверный url")

        if not verify_password(password, massege.password):
            raise HTTPException(status_code=401, detail="Неверный пароль")
        text = decode_massege(massege.body, password)
        await cls.delete(url)
        return text
        